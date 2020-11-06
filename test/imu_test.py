#!/bin/python

import board
import busio
import adafruit_bno055
import time

def start():
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bno055.BNO055_I2C(i2c)
    print('Temperature: {} degrees C'.format(sensor.temperature))
    print('Accelerometer: (m/s^2): {}'.format(sensor.acceleration))
    print('Magnetometer (microteslas): {}'.format(sensor.magnetic))
    print('Gyroscope (deg/sec): {}'.format(sensor.gyro))
    print('Euler angle: {}'.format(sensor.euler))
    print('Quaternion: {}'.format(sensor.quaternion))
    print('Linear acceleration (m/s^2): {}'.format(sensor.linear_acceleration))
    print('Gravity (m/s^2): {}'.format(sensor.gravity))


    average = 0
    outlier = 0
    for i  in range(0, 1000):
        outlier = sensor.temperature
        if outlier < 20:
            print(outlier)
        average += outlier
    print (average / 1000)

if name == __main__():
    start()

