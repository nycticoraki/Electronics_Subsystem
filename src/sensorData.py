#!/usr/bin/python3

IMU_TEMPERATURE = 'Temperature'
IMU_ACCELEROMETER = 'Accelerometer'
IMU_MAGNETOMETER = 'Magnetometer'
IMU_GYROSCOPE = 'Gyroscope'
IMU_EULERANGLE = 'EulerAngle'
IMU_QUATERNION = 'Quaternion'
IMU_LINEARACCELERATION = 'LinearAcceleration'
IMU_GRAVITY = 'Gravity'

ALT_PRESSURE = 'Pressure'
ALT_ALTITUDE = 'Altitude'
ALT_TEMPERATURE = 'Temperature'

class ImuSensorData(object):
    def __init__(self, data=None):
        if data is not None and type(data) != dict:
            raise ValueError("data MUST be a dictionary!")
        self.imu_data = {
         IMU_TEMPERATURE: 0,
         IMU_ACCELEROMETER: 0,
         IMU_MAGNETOMETER: 0,
         IMU_GYROSCOPE: 0,
         IMU_EULERANGLE: 0,
         IMU_QUATERNION: 0,
         IMU_LINEARACCELERATION: 0,
         IMU_GRAVITY: 0,
        }
        if data is not None:
            for key in data.keys():
                if key not in self.imu_data.keys():
                    raise ValueError("Attempting to assign bad key \"{}\" to ImuSensorData!".format(key))
                self.imu_data[key] = data[key]

    def __getitem__(self, key):
        if key in self.imu_data.keys():
            return self.imu_data[key]
        else:
            raise ValueError("Key \"{}\" not valid for imu or alt data".format(key))
    def __setitem__(self, key, value):
        if key in self.imu_data.keys():
            self.imu_data[key] = value
        else:
            raise ValueError("Key \"{}\" not valid for imu or alt data".format(key))
    def __str__(self):
        return str(self.imu_data)

class AltSensorData(object):
    def __init__(self, data=None):
        if data is not None and type(data) != dict:
            raise ValueError("data MUST be a dictionary!")
        self.alt_data = {
         ALT_PRESSURE: 0,
         ALT_ALTITUDE: 0,
         ALT_TEMPERATURE: 0,
        }
        if data is not None:
            for key in data.keys():
                if key not in self.alt_data.keys():
                    raise ValueError("Attempting to assign bad key \"{}\" to AltSensorData!".format(key))
                self.alt_data[key] = data[key]

    def __getitem__(self, key):
        if key in self.alt_data.keys():
            return self.alt_data[key]
        else:
            raise ValueError("Key \"{}\" not valid for imu or alt data".format(key))
    def __setitem__(self, key, value):
        if key in self.alt_data.keys():
            self.alt_data[key] = value
        else:
            raise ValueError("Key \"{}\" not valid for imu or alt data".format(key))
    def __str__(self):
        return str(self.alt_data)
