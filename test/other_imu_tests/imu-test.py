import board
import busio
import adafruit_bno055
import string

i2c = busio.I2C(board.SCL, board.SDA)

print(i2c)
#print(board.SCL)
#print(board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
print('Temperature: {} degrees C'.format(sensor.temperature))


