#!/bin/python

import csv
import board
import busio
import adafruit_bno055
import sys
import time
import datetime

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

sys.stdout = open('output-imu.csv', 'w')

#date = datetime.datetime.now()
print('datetime, temperature, accelerometer, magnetometer, gyroscope, euler_angle, quaternion, linear_acceleration, gravity')
while(1):
    date = datetime.datetime.now()
    print (date.strftime("%Y-%m-%d %H:%M:%S")+", ("+str(sensor.temperature)+"), "+str(sensor.acceleration)+", "+str(sensor.magnetic)+", "+str(sensor.gyro)+", "+str(sensor.euler)+", "+str(sensor.quaternion)+", "+str(sensor.linear_acceleration)+", "+str(sensor.gravity))

    time.sleep(1)

sys.stdout.close()
