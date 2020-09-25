from flask import Flask, request, jsonify, render_template, url_for
from sensorIO import RangeSensor, ActuallyWhat

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static')

sensor = RangeSensor(23, 24)
myId = ActuallyWhat(0)


@app.route('/')
def test():
    return render_template('index.html')

@app.route('/getDistance', methods=['GET'])
def getDistance():
    data = {"distance": sensor.getDistance(), "time": sensor.getTime()}
    return jsonify(data)

@app.route('/getID', methods=['GET'])
def getID():
    myId.val = myId.val + 1
    data = {"ID": myId.val, "START_TIME": sensor.getTime()}
    return jsonify(data)

with app.test_request_context():
    url_for('static', filename='main.css')
    url_for('static', filename='source.js')
    url_for('static', filename='plotly-latest.min.js')
