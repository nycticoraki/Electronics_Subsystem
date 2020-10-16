from flask import Flask, request, jsonify, render_template, url_for
from flask_socketio import SocketIO, send, emit
from sensorIO import Sensors
import time

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static')
app.config['SECRET_KEY'] = 'tmp'
socketio = SocketIO(app)

# singleton instance of one sensor
sensors = Sensors()

# time from the start of the sensors runtime
start_time = time.time()

# figure out who is connected to what
subscription_list = {'imusensor': [], 'altsensor': [], 'none': []}

# delay between messages
delay = 1.0/10.0    

with app.test_request_context():
    url_for('static', filename='main.css')
    url_for('static', filename='source.js')
    url_for('static', filename='plotly-latest.min.js')


def feed_data_imu():
    while len(subscription_list['imusensor']) != 0:
        data = {"time": time.time() - start_time, "data": sensors.getImuData()}
        send(data, broadcast=True)
        socketio.sleep(delay)
        #time.sleep(delay)

def feed_data_alt():
    while len(subscription_list['altsensor']) != 0:
        data = {"time": time.time() - start_time, "data": sensors.getAltData()}
        send(data, broadcast=True)
        socketio.sleep(delay)
        #time.sleep(delay)

# deal with standard http requests
@app.route('/')
def test():
    return render_template('index.html')

# Deal with socket connections
@socketio.on('connect')
def handleConnect():
    print('New Connection!')

@socketio.on('message', namespace='/imusensor')
def handleMessage(msg):
    if msg == 'subscribe':       # whenever a new user joins, broadcast data to them :: replace with namespaces later
        print('adding to imusensor')
        if len(subscription_list['imusensor']) == 0:
            subscription_list['imusensor'].append(request.sid)
            feed_data_imu()
        else:
            subscription_list['imusensor'].append(request.sid)
        
    elif msg == 'unsubscribe':
        subscription_list['imusensor'].remove(request.sid)

@socketio.on('message', namespace='/altsensor')
def handleMessage(msg):
    if msg == 'subscribe':       # whenever a new user joins, broadcast data to them :: replace with namespaces later
        if len(subscription_list['altsensor']) == 0:
            subscription_list['altsensor'].append(request.sid)
            feed_data_alt()
        else:
            subscription_list['altsensor'].append(request.sid)
        
    elif msg == 'unsubscribe':
        subscription_list['altsensor'].remove(request.sid)







if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)