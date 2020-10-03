from flask import Flask, request, jsonify, render_template, url_for
from flask_socketio import SocketIO, send, emit
from sensorIO import RangeSensor
import time

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static')
app.config['SECRET_KEY'] = 'tmp'
socketio = SocketIO(app)

sensor = RangeSensor(23, 24)

start_time = time.time()

# figure out who is connected to what
sensors = {'rangefinder': [], 'none': []}

delay = 1.0/60.0

with app.test_request_context():
    url_for('static', filename='main.css')
    url_for('static', filename='source.js')
    url_for('static', filename='plotly-latest.min.js')


def feed_data():
    while True and len(sensors['rangefinder']) != 0:
        data = {"time": time.time() - start_time, "data": sensor.getDistance()}
        send(data, broadcast=True)
        socketio.sleep(delay)
        time.sleep(delay)

# deal with standard http requests
@app.route('/')
def test():
    return render_template('index.html')

# Deal with socket connections
@socketio.on('connect')
def handleConnect():
    print('New Connection!')

@socketio.on('message', namespace='/RangeFinder')
def handleMessage(msg):
    if msg == 'subscribe':       # whenever a new user joins, broadcast data to them :: replace with namespaces later
        if len(sensors['rangefinder']) == 0:
            sensors['rangefinder'].append(request.sid)
            feed_data()
        else:
            sensors['rangefinder'].append(request.sid)
        
    elif msg == 'unsubscribe':
        sensors['rangefinder'].remove(request.sid)







if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)