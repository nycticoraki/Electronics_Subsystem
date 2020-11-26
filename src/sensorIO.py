import time
import board
import busio
import adafruit_bno055
import adafruit_mpl3115a2
import sensorData as sd
from sensorData import ImuSensorData,AltSensorData

class Sensors():
    # declare each class privately so that we can limit it to one instance per class
    class _Altimeter():
        def __init__(self, i2c):
            self.i2c = i2c
            self.sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
        def getAllData(self):
            altData = AltSensorData({
                sd.ALT_PRESSURE: self.sensor.pressure,
                sd.ALT_ALTITUDE: self.sensor.altitude,
                sd.ALT_TEMPERATURE: self.sensor.temperature,
            })
            return altData
    class _IMUSensor():
        def __init__(self, i2c):
            self.i2c = i2c
            self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)
        def getAllData(self):
            imuData = ImuSensorData({
                sd.IMU_TEMPERATURE: self.sensor.temperature,
                sd.IMU_ACCELEROMETER: self.sensor.acceleration,
                sd.IMU_MAGNETOMETER: self.sensor.magnetic,
                sd.IMU_GYROSCOPE: self.sensor.gyro,
                sd.IMU_EULERANGLE: self.sensor.euler,
                sd.IMU_QUATERNION: self.sensor.quaternion,
                sd.IMU_LINEARACCELERATION: self.sensor.linear_acceleration,
                sd.IMU_GRAVITY: self.sensor.gravity
            })
            return imuData

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
