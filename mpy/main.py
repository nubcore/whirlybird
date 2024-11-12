print('hellorld!, RGBW test on GPIO42')

from machine import Pin, ADC
from time import sleep_ms
import neopixel

# 2.998 ADC @ 8.07v

blink = True
brightness = 10
c = 32
d = 50
np = neopixel.NeoPixel(Pin(42), c, bpp=4)

a10 = ADC(Pin(10), atten=ADC.ATTN_11DB)

b0 = Pin(0, Pin.IN)
b3 = Pin(3, Pin.IN)
b46 = Pin(46, Pin.IN)

def fill():
 np.fill([brightness,brightness,brightness,brightness])
 np.write()
 sleep_ms(d*4)

def rgbw(p):
 np[p] = (brightness, 0, 0, 0)
 np.write()
 sleep_ms(d)
 np[p] = (0, brightness, 0, 0)
 np.write()
 sleep_ms(d)
 np[p] = (0,0,brightness,0)
 np.write()
 sleep_ms(d)
 np[p] = (0,0,0,brightness)
 np.write()
 sleep_ms(d)
 np[p] = (0,0,0,0)

def check():
 global brightness, blink
 if b0.value() == 0:
  #print("Button 0")
  brightness += 10
  print(brightness)
 if b3.value() == 0:
  #print("Button 3")
  brightness -= 10
  print(brightness)
 if b46.value() == 0:
  #print("Button 46")
  print("Battery: {:0.2f} volts".format(a10.read_uv()/1_000_000*2.7))
  blink = not blink

def loop():
 for i in range(c):
  check()
  if blink:
   rgbw(i)
  else:
   fill()

while True:
 loop()
