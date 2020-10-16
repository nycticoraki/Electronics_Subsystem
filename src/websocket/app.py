from flask import Flask, request, jsonify, render_template, url_for
from flask_socketio import SocketIO, send, emit
from sensorIO import Sensors
import time

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static')
app.config['SECRET_KEY'] = 'tmp'
socketio = SocketIO(app, async_mode="threading")

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

""" Considering having a separate thread for each sensor but that could cause problems
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
"""

# while a user is using a service, send data in the background
#       --  Consider having a user specify what sensor data it wants
def background_feed_data():
    #print('here')
    while not all(len(subscription_list[key]) == 0 for key in subscription_list):
        #print(' in here ')
        data = {"time": time.time() - start_time, "data": None}
        if len(subscription_list['altsensor']) != 0:
            data["data"] = sensors.getAltData()
            send(data, namespace='/altsensor', broadcast=True)

        if len(subscription_list['imusensor']) != 0:
            data["data"] = sensors.getImuData()     # I have a feeling this is gonna worsen the issues with timing issues
            send(data, namespace='/imusensor', broadcast=True)
        
        # please use a reasonable delay
        socketio.sleep(delay)
        

def subscribe(sensor_name, sid):
    if not request.sid in subscription_list[sensor_name]:
        print(sid, " subscribed to " + sensor_name)
        if all(len(subscription_list[key]) == 0 for key in subscription_list):
            subscription_list[sensor_name].append(sid)
            background_feed_data()
        else:
            subscription_list[sensor_name].append(sid)
        

def unsubscribe(sensor_name, sid):
    if sid in subscription_list[sensor_name]:
        print(sid, " unsubscribed to " + sensor_name)
        subscription_list[sensor_name].remove(sid)


# deal with standard http requests
@app.route('/')
def test():
    return render_template('index.html')

# Deal with socket connections
@socketio.on('connect', namespace="/")
def handleConnect():
    print('New Connection!')


@socketio.on('message', namespace='/altsensor')
def handleUnsubscribe(msg):
    if msg == 'subscribe':
        subscribe('altsensor', request.sid)
    elif msg == 'unsubscribe':
        unsubscribe('altsensor', request.sid)

@socketio.on('message', namespace='/imusensor')
def handleUnsubscribe(msg):
    if msg == 'subscribe':
        subscribe('imusensor', request.sid)
    elif msg == 'unsubscribe':
        unsubscribe('imusensor', request.sid)

""" Client Disconnects
    -   handle client disconnecting without sending an unsubscribe message i.e. closing browser
"""
@socketio.on('disconnect', namespace='/imusensor')
def disconnect():
    unsubscribe('imusensor', request.sid)

@socketio.on('disconnect', namespace='/imusensor')
def disconnect():
    unsubscribe('imusensor', request.sid)







if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)