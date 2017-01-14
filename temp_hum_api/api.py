from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from flaskext.mysql import MySQL
from config import configure_app

print(__name__)
app = Flask(__name__)
configure_app(app)
api = Api(app)

mysql = MySQL()
mysql.init_app(app)

temperature = {}
humidity = {}


def abort_if_record_doesnt_exist(record_id):
    if record_id not in temperature:
        abort(404, message="Temperature record {} doesn't exist".format(record_id))
    if record_id not in humidity:
        abort(404, message="Temperature record {} doesn't exist".format(record_id))

parser = reqparse.RequestParser()
parser.add_argument('temp', type=float, help='Temperature measured by sensor')
parser.add_argument('hum', type=float, help='Humidity measured by sensor')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/', '/hello')


class TemperatureHumidity(Resource):
    def get(self, record_id):
        abort_if_record_doesnt_exist(record_id)
        return {record_id: [temperature[record_id], humidity[record_id]]}

    def put(self, record_id):
        args = parser.parse_args()
        temp = args['temp']
        hum = args['hum']
        abort_if_record_doesnt_exist(record_id)
        temperature[record_id] = temp
        humidity[record_id] = hum
        return {record_id: [temperature[record_id], humidity[record_id]]},201


class TemperatureHumidityList(Resource):
    def get(self):
        records = {}
        for key,temp in temperature.iteritems():
            records.update({key: [temp, humidity[key]]})
        return records

    def post(self):
        args = parser.parse_args()
        record_id = int(max(temperature.keys())) + 1
        temperature[record_id] = args['temp']
        humidity[record_id] = args['hum']
        return {record_id: [temperature[record_id], humidity[record_id]]}, 201

api.add_resource(TemperatureHumidity, '/temp-hum/<int:record_id>', endpoint='temp_hum')
api.add_resource(TemperatureHumidityList, '/temp-hum-list/')

if __name__=='__main__':
    app.run(
        host=app.config['host'],
        port=app.config['port']
    )