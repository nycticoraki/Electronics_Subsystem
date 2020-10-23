#!/bin/python

import board
import busio
import adafruit_bno055
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

fo = open("imu_output.txt", "wb")

print('Temperature: {} degrees C'.format(sensor.temperature))
print('Accelerometer: (m/s^2): {}'.format(sensor.acceleration))
print('Magnetometer (microteslas): {}'.format(sensor.magnetic))
print('Gyroscope (deg/sec): {}'.format(sensor.gyro))
print('Euler angle: {}'.format(sensor.euler))
print('Quaternion: {}'.format(sensor.quaternion))
print('Linear acceleration (m/s^2): {}'.format(sensor.linear_acceleration))
print('Gravity (m/s^2): {}'.format(sensor.gravity))

fo.close()
