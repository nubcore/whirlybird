from machine import Pin, Timer
from time import sleep_us, sleep_ms, ticks_us, ticks_diff, localtime
print("insta OFF")
# "Message" starts with LHL then 10 PRE "Bits" then 44 or 43 Dx "Bits"
# Each "Bit" ends Low, each "Message" ends holding High
LHL = (4450,9140,4450) # Low High Low start
NIB = 800
BIT = 1600
# 0 Bit = BIT Low / 1 Bit = NIB High, NIB Low
PRE = (1,1,1,1,0,1,1,1,1,0) # Preamble
D0 = (1,1,1,1,1,1,1,1,1,1, 0,1,0,1,1,0,1,0,1,1, 1,1,1,0,1,0,1,1,1,0, 1,0,1,0,1,1,0,1,0,1, 1,1,1)
D1 = (1,1,1,1,1,1,1,1,1,0, 1,0,1,0,1,1,0,1,0,1, 1,1,1,1,0,1,0,1,1,1, 0,1,0,1,1,1,0,1,0,1, 1,1,1)
D2 = (1,0,1,1,1,1,1,1,1,1, 0,1,1,0,1,1,0,1,0,1, 1,1,1,1,0,1,0,1,1,1, 0,1,0,1,1,0,1,0,1,0, 1,1,1,1)
D3 = (1,0,1,1,1,1,1,1,1,1, 1,1,0,1,1,0,1,0,1,1, 1,1,1,0,1,0,1,1,1,0, 1,0,1,0,1,0,1,0,1,0, 1,1,1,1)

txPin = Pin(43, Pin.OUT, value=1)

def send(bits):
 bits = PRE + bits
 txPin.off()
 sleep_us(LHL[0])
 txPin.on()
 sleep_us(LHL[1])
 txPin.off()
 sleep_us(LHL[2])
 for b in bits:
  if b == 1:
   txPin.on()
   sleep_us(NIB)
   txPin.off()
   sleep_us(NIB)
  else:
   sleep_us(BIT)
 txPin.on()

def idlePing(t):
 send(D0)

tim0 = Timer(0)
tim0.init(period=1000, mode=Timer.PERIODIC, callback=idlePing)



