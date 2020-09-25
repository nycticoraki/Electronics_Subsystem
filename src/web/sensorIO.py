import RPi.GPIO as GPIO
import time

class ActuallyWhat():
    def __init__(self, val):
        self.val = val
        


class RangeSensor():
    def __init__(self, TRIG, ECHO):
        GPIO.setmode(GPIO.BCM)
        self.TRIG = TRIG
        self.ECHO = ECHO
        self.init_time = time.time()
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, False)
        time.sleep(2)

    def getDistance(self):
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001) # delay needed from sending signal to TRIG
        GPIO.output(self.TRIG, False)
        pulse_start = 0
        pulse_end = 0

        # wait for echo to start
        while GPIO.input(self.ECHO) == False:
            pulse_start = time.time()

        # wait for echo to end
        while GPIO.input(self.ECHO) == True:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        pulse_duration = pulse_duration * 17150
        pulse_duration = round(pulse_duration, 2)
        if pulse_duration > 200:
            pulse_duration = 0
        return pulse_duration

    def getTime(self):
        return time.time() - self.init_time

