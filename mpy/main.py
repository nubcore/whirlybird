print('hellorld!, RGBW test on GPIO44/Rx')

from machine import I2C, Pin
from machine import Pin, I2C
from time import sleep_ms
import neopixel

c = 32
d = 50
np = neopixel.NeoPixel(Pin(44), c, bpp=4)

I2C1_SDA = Pin(5)
I2C1_SCL = Pin(4)

i2c1 = I2C(1, scl=I2C1_SCL, sda=I2C1_SDA, freq=100000, timeout=200000 )
print("I2C Device found at address : ",i2c1.scan(),"\n")

def rgbw(p):
 np[p] = (8, 0, 0, 0)
 np.write()
 sleep_ms(d)
 np[p] = (0, 8, 0, 0)
 np.write()
 sleep_ms(d)
 np[p] = (0,0,8,0)
 np.write()
 sleep_ms(d)
 np[p] = (0,0,0,8)
 np.write()
 sleep_ms(d)
 np[p] = (0,0,0,0)

def loop():
 for i in range(c):
  rgbw(i)

while True:
 loop()
