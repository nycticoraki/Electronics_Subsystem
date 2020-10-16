import time
import board
import busio
import adafruit_bno055
import adafruit_mpl3115a2


class Sensors():
    # declare each class privately so that we can limit it to one instance per class
    class _Altimeter():
        def __init__(self, i2c):
            self.i2c = i2c
            self.sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
        def getAllData(self):
            return {
                'Pressure': self.sensor.pressure,
                'Altitude': self.sensor.altitude,
                'Temperature': self.sensor.temperature,
            }
    class _IMUSensor():
        def __init__(self, i2c):
            self.i2c = i2c
            self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)
        def getAllData(self):
            return {
                'Temperature': self.sensor.temperature,
                'Accelerometer': self.sensor.acceleration,
                'Magnetometer': self.sensor.magnetic,
                'Gyroscope': self.sensor.gyro,
                'EulerAngle': self.sensor.euler,
                'Quaternion': self.sensor.quaternion,
                'LinearAcceleration': self.sensor.linear_acceleration,
                'Gravity': self.sensor.gravity
            }

    # instances
    _imuSensor = None
    _altSensor = None
    _i2c = None

    # ensure that we only ever create one instance of an imu and altimeter object
    # not since python does not allow private members, we use _name to denote objects that should not be altered
    def __init__(self):
        if not (Sensors._imuSensor and Sensors._altSensor):
            Sensors._i2c = busio.I2C(board.SCL, board.SDA)  # can only have one instance of busio.I2C(SCL, SDA)
            Sensors._imuSensor = Sensors._IMUSensor(Sensors._i2c)
            Sensors._altSensor = Sensors._Altimeter(Sensors._i2c)

    def getImuData(self):
        return Sensors._imuSensor.getAllData()
    
    def getAltData(self):
        return Sensors._altSensor.getAllData()

    






"""
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)

print('Pressure: {0:0.3f} pascals'.format(sensor.pressure))
print('Altitude: {0:0.3f} meters'.format(sensor.altitude))
print('Temperature: {0:0.3f} degrees Celsius'.format(sensor.temperature))



print('Temperature: {} degrees C'.format(sensor.temperature))
print('Accelerometer: (m/s^2): {}'.format(sensor.acceleration))
print('Magnetometer (microteslas): {}'.format(sensor.magnetic))
print('Gyroscope (deg/sec): {}'.format(sensor.gyro))
print('Euler angle: {}'.format(sensor.euler))
print('Quaternion: {}'.format(sensor.quaternion))
print('Linear acceleration (m/s^2): {}'.format(sensor.linear_acceleration))
print('Gravity (m/s^2): {}'.format(sensor.gravity))
"""
