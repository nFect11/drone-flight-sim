import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

while True:
    lol = adc.read_adc(0, gain=1)
    print (lol)
    time.sleep(0.2)
