from flask import Flask, request, jsonify, render_template, url_for
from flask_socketio import SocketIO, send
from sensorIO import RangeSensor
import time

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static')
app.config['SECRET_KEY'] = 'tmp'
socketio = SocketIO(app)

sensor = RangeSensor(23, 24)

start_time = time.time()

with app.test_request_context():
    url_for('static', filename='main.css')
    url_for('static', filename='source.js')
    url_for('static', filename='plotly-latest.min.js')


def feed_data():
    while True:
        data = {"time": time.time() - start_time, "sensor": 1}
        send(data, broadcast=True)
        socketio.sleep(1.0/50.0)

# deal with standard http requests
@app.route('/')
def test():
    return render_template('index.html')

# Deal with socket connections
@socketio.on('connect')
def handleConnect():
    print('New Connection!')
    start_time = time.time()

@socketio.on('message')
def handleMessage(msg):
    if msg == 'feed me!':
        start_time = time.time()
        feed_data()




if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)