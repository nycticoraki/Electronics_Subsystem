from flask import Flask, request
from sensorIO import RangeSensor

app = Flask(__name__)

sensor = RangeSensor(23, 24)


@app.route('/')
def test():
    return '<h1>Test</h1>'

@app.route('/getDistance', methods=['GET'])
def getDistance():
    return str(sensor.getDistance())


