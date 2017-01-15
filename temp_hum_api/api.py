from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse, abort
from flaskext.mysql import MySQL
from config import configure_app
import time

app = Flask(__name__)
configure_app(app)
api = Api(app)

mysql = MySQL()
mysql.init_app(app)

def abort_if_record_doesnt_exist(record_id):
    try:
        db = mysql.connect()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM temp_hum_records WHERE id = {0}'.format(record_id))
        record = cursor.fetchall()
    finally:
        db.close()
    if len(record) != 1:
        abort(404, message="Record {} doesn't exist".format(record_id))

parser = reqparse.RequestParser()
parser.add_argument('record_id', type=int, help='Record ID to fetch or update')
parser.add_argument('temp', type=float, help='Temperature measured by sensor')
parser.add_argument('hum', type=float, help='Humidity measured by sensor')


@app.route("/")
def index():
    return render_template('index.html', baseurl='http://{0}:{1}'.format(app.config['HOST'], app.config['PORT']))


class TemperatureHumidity(Resource):
    def get(self, record_id):
        abort_if_record_doesnt_exist(record_id)
        try:
            db = mysql.connect()
            cursor = db.cursor()
            cursor.execute('SELECT * FROM temp_hum_records WHERE id = {0}'.format(record_id))
            sql_record = cursor.fetchone()
            record = []
            record.insert(sql_record[0], {
                'timestamp': int(time.mktime(sql_record[1].timetuple())),
                'temp': sql_record[2],
                'hum': sql_record[3]
            })
        finally:
            db.close()
        return record

    def put(self, record_id):
        args = parser.parse_args()
        temp = args['temp']
        hum = args['hum']
        abort_if_record_doesnt_exist(record_id)
        try:
            db = mysql.connect()
            cursor = db.cursor()
            cursor.execute('UPDATE temp_hum_records SET temp={0},hum={1} WHERE id={2}'.format(temp, hum, record_id))
            db.commit()
        finally:
            db.close()
        record = []
        record.insert(record_id, {
            'temp': temp,
            'hum': hum
        })
        return record, 201


class TemperatureHumidityList(Resource):
    def get(self):
        try:
            db = mysql.connect()
            cursor = db.cursor()
            cursor.execute('SELECT * FROM temp_hum_records')
            records = []
            for sql_record in cursor:
                records.insert(
                    sql_record[0],
                    {
                        'timestamp': int(time.mktime(sql_record[1].timetuple())),
                        'temp': sql_record[2],
                        'hum': sql_record[3]
                    }
                )
        finally:
            db.close()
        return records

    def post(self):
        args = parser.parse_args()
        try:
            db = mysql.connect()
            cursor = db.cursor()
            cursor.execute('INSERT INTO temp_hum_records(temp,hum) VALUES ({0},{1})'.format(args['temp'],args['hum']))
            record_id = db.insert_id()
            db.commit()
        finally:
            db.close()
        record = []
        record.insert(record_id, {
            'temp': args['temp'],
            'hum': args['hum']
        })
        return record, 201

api.add_resource(TemperatureHumidity, '/temp-hum/<int:record_id>', endpoint='temp_hum')
api.add_resource(TemperatureHumidityList, '/temp-hum-list/')

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT']
    )
