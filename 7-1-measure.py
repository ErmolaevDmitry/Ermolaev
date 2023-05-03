import RPi.GPIO
import sys
import time
import matplotlib.pyplot as plt

RPi.GPIO.setmode(RPi.GPIO.BCM)
dac=[26,19,13,6,5,11,9,10]
leds = [24, 25, 8, 7, 12, 16, 20, 21]
comp=4
troyka=17

RPi.GPIO.setup(dac,RPi.GPIO.OUT)
RPi.GPIO.setup(troyka,RPi.GPIO.OUT,initial=RPi.GPIO.LOW)
RPi.GPIO.setup(leds, RPi.GPIO.OUT, initial=RPi.GPIO.LOW)
RPi.GPIO.setup(comp,RPi.GPIO.IN)

def perev(a):
    return[int(elem) for elem in bin(a)[2:].zfill(8)]

def adc():
    k=0
    for i in range(7, -1, -1):
        k+=2**i
        RPi.GPIO.output(dac, perev(k))
        time.sleep(0.002)
        if RPi.GPIO.input(comp)==0:
            k-=2**i
    return k        


try:
    data = []
    data.append(adc())
    start = time.time()
    N = 0
    RPi.GPIO.output(troyka, 1)
    while True:
        N += 1
        k = adc()
        data.append(float(k))
        RPi.GPIO.output(leds, perev(k))
        if k >= 0.97 * 255:
            break
    RPi.GPIO.output(troyka, 0)
    while True:
        N += 1
        k = adc()
        data.append(k)
        RPi.GPIO.output(leds, perev(k))
        if k <= 0.02 * 255:
            break
    end = time.time()
    period = end - start
    
    dataFile = open('data.txt', 'w')
    for i in data:
        dataFile.write(str(i) + "\n")
    dataFile.close()
    
    settingsFile = open('settings.txt', 'w')
    settingsFile.write(str(N / period) + " " + str(3.3 / (2**8 - 1)))
    settingsFile.close()
    
    plt.plot(data)
    plt.show()
    
    print(period, period / N, N / period, 3.3 / (2**8 - 1))
    
finally:
    RPi.GPIO.output(dac, 0)
    RPi.GPIO.output(leds, 0)
    RPi.GPIO.output(troyka, 0)
    RPi.GPIO.cleanup() 
