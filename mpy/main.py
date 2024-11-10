print('hellorld!, RGBW test on GPIO42')

from machine import Pin
from time import sleep_ms
import neopixel

c = 32
d = 50
np = neopixel.NeoPixel(Pin(42), c, bpp=4)

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
