print("Whirlybird by DEFAULT [EXPERIMENTAL]")

from machine import Pin, SoftI2C, Timer, UART
from micropython import const
from time import sleep_ms
from neopixel import NeoPixel
from pi4ioe5v6416 import PI4IOE5V6416
from pca9632 import PCA9632
from rs41 import RS41

_NEO_A_COUNT = const(24)
_NEO_B_COUNT = const(8)
_NEO_A_PIN = const(42)
_NEO_B_PIN = const(41)

count = 0

npA = NeoPixel(Pin(_NEO_A_PIN), _NEO_A_COUNT, bpp=4)
npB = NeoPixel(Pin(_NEO_B_PIN), _NEO_B_COUNT, bpp=4)

npA.fill((1,0,0,0))
npB.fill((0,0,0,0))
npA.write()
npB.write()

I2C1_SDA = Pin(5)
I2C1_SCL = Pin(4)

# Whirlybird I2C (4+ devices connected)
i2c = SoftI2C(scl=4, sda=5, freq=100_000)

sleep_ms(100)

xio = PI4IOE5V6416(i2c)
leds = PCA9632(i2c)

# Enable RS41 RESET
xio.outputEnable(0, 3)

def rs41Reset(reset=True):
 if reset:
  xio.output(0,3,1)
  npB.fill((0,0,0,0))
  npB.write()
 else:
  xio.output(0,3,0)
  npB.fill((0,0,1,0))
  npB.write()

sonde = RS41(rs41Reset)

npA.fill((0,1,0,0))
npA.write()

def rgbw(p):
 npA[p] = (0, 0, 0, 1)
 npA.write()
 sleep_ms(NEO_DELAY)

def ring():
 for i in range(24,32):
  rgbw(i)
  npA.fill((0,0,0,0))
  npA.write()
 for i in range(23,-1, -1):
  rgbw(i)
 npA.fill((0,0,0,0))
 npA.write()

def updateRing():
 npA.fill((0,0,0,0))
 if sonde.temperature > 0:
  f = int(sonde.temperature * 1.8 + 32)
  j = f - 74
  print(f, j)
  for i in range(j):
   npA[i] = (2,0,0,0)
 npA.write()

#sleep_ms(100)
#leds.blink()

#ring()

def loop(t):
 global count
 count += 1
 if count > 1000: # 1 minute interval
  count = 0
  updateRing()

timer0 = Timer(0)
timer0.init(period=20, mode=Timer.PERIODIC, callback=loop)

#sleep_ms(100)
#sonde.enable()
#sleep_ms(5000)
#sonde.measurementsSensors('10')
#sleep_ms(1000)
#updateRing()

#sondeConnected = False
#xio.output(0,3,0)

#while not sondeConnected:
# pass

#print("\nRS41 Talking")
#sleep_ms(100)
#print("Requesting Menu")
#uart.write('\r')
#sleep_ms(100)
#uart.write('STwsv\r')

#xio.output(0,3,1)
