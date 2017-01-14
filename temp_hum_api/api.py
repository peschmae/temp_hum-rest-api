from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from flaskext.mysql import MySQL
from config import configure_app

app = Flask(__name__)
configure_app(app)
api = Api(app)

mysql = MySQL()
mysql.init_app(app)

def abort_if_record_doesnt_exist(record_id):
    db = mysql.connect()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM temperature WHERE id = {0}'.format(record_id))
    temperature = cursor.fetchall()
    cursor.execute('SELECT * FROM humidity WHERE id = {0}'.format(record_id))
    humidity = cursor.fetchall()
    db.close()
    if len(temperature) != 1:
        abort(404, message="Temperature record {} doesn't exist".format(record_id))
    if len(humidity) != 1:
        abort(404, message="Temperature record {} doesn't exist".format(record_id))

parser = reqparse.RequestParser()
#parser.add_argument('record_id', type=int, help='Record ID to fetch or update')
parser.add_argument('temp', type=float, help='Temperature measured by sensor')
parser.add_argument('hum', type=float, help='Humidity measured by sensor')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/', '/hello')


class TemperatureHumidity(Resource):
    def get(self, record_id):
        abort_if_record_doesnt_exist(record_id)
        db = mysql.connect()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM temperature')
        temperatures = dict(cursor.fetchall())
        cursor.execute('SELECT * FROM humidity')
        humidities = dict(cursor.fetchall())
        db.close()
        return {record_id: [temperatures[record_id], humidities[record_id]]}

    def put(self, record_id):
        args = parser.parse_args()
        temp = args['temp']
        hum = args['hum']
        abort_if_record_doesnt_exist(record_id)
        db = mysql.connect()
        cursor = db.cursor()
        cursor.execute('UPDATE temperature SET temp={0} WHERE id={1}'.format(temp, record_id))
        cursor.execute('UPDATE humidity SET hum={0} WHERE id={1}'.format(hum, record_id))
        db.commit()
        db.close()
        return {record_id: [temp, hum]},201


class TemperatureHumidityList(Resource):
    def get(self):
        db = mysql.connect()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM temperature')
        temperatures = dict(cursor.fetchall())
        cursor.execute('SELECT * FROM humidity')
        humidities = dict(cursor.fetchall())
        db.close()
        records = {}
        for key,temp in temperatures.iteritems():
            records.update({key: [temp, humidities[key]]})
        return records

    def post(self):
        args = parser.parse_args()
        db = mysql.connect()
        cursor = db.cursor()
        cursor.execute('INSERT INTO temperature(temp) VALUES ({0})'.format(args['temp']))
        cursor.execute('INSERT INTO humidity(hum) VALUES ({0})'.format(args['hum']))
        record_id = db.insert_id()
        db.commit()
        db.close()
        return {record_id: [args['temp'], args['hum']]}, 201

api.add_resource(TemperatureHumidity, '/temp-hum/<int:record_id>', endpoint='temp_hum')
api.add_resource(TemperatureHumidityList, '/temp-hum-list/')

if __name__=='__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT']
    )