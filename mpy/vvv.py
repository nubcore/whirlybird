from machine import Pin
from time import sleep_us, sleep_ms, ticks_us, ticks_diff, localtime

print("instatoast vvv")

# "Message" starts with LHL then 10 PRE "Bits" then 44 or 43 Dx "Bits"
# Each "Bit" ends Low, each "Message" ends holding High

LHL = (4450,9140,4450) # Low High Low start
NIB = 800
BIT = 1600

# 0 Bit = BIT Low
# 1 Bit = NIB High, NIB Low

PRE = (1,1,1,1,0,1,1,1,1,0) # Preamble


D0 = (1,1,1,1,1,1,1,1,1,1, 0,1,0,1,1,0,1,0,1,1, 1,1,1,0,1,0,1,1,1,0, 1,0,1,0,1,1,0,1,0,1, 1,1,1)
D1 = (1,1,1,1,1,1,1,1,1,0, 1,0,1,0,1,1,0,1,0,1, 1,1,1,1,0,1,0,1,1,1, 0,1,0,1,1,1,0,1,0,1, 1,1,1)
D2 = (1,0,1,1,1,1,1,1,1,1, 0,1,1,0,1,1,0,1,0,1, 1,1,1,1,0,1,0,1,1,1, 0,1,0,1,1,0,1,0,1,0, 1,1,1,1)
D3 = (1,0,1,1,1,1,1,1,1,1, 1,1,0,1,1,0,1,0,1,1, 1,1,1,0,1,0,1,1,1,0, 1,0,1,0,1,0,1,0,1,0, 1,1,1,1)


# Cleaner 'V'
#TX_OFF_0 = (1,1,1,1,1,1,1,1, 1,1,0,1,1,1,1,0, 1,1,1,1,1,0,1,0, 1,1,1,0,1,0,1,0, 1,1,1,1,0,1,1,1) # power on "OFF" display idle ping, long initial beep
#TX_OFF_A = (1,1,1,1,1,1,1,1, 1,0,1,1,0,1,1,0, 1,0,1,1,1,1,1,0, 1,0,1,1,1,0,1,0, 1,0,1,0,1,0,1,0, 1,1,1,1) # light timed 'off', short beep
#TX_OFF_B = (1,1,1,1,1,1,1,1, 1,0,1,0,1,0,1,1, 0,1,0,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,1,1,0,1,0,1, 1,1,1)   #     ''    timed 'off'
#TX_OFF_C = (1,1,1,1,1,1,1,1, 1,1,1,0,1,1,0,1, 0,1,1,1,1,1,0,1, 0,1,1,1,0,1,0,1, 1,0,1,0,1,0,1,1, 1,1)     #     ''    timed 'off'
#send(TX_OFF_A); sleep_ms(100); send(TX_OFF_B); sleep_ms(100); send(TX_OFF_C); sleep_ms(100); send(TX_OFF_0)

rxPin = Pin(46, Pin.IN)
txPin = Pin(43, Pin.OUT, value=1)

sleep_ms(100)


def read(endTicks):
 edges = []
 bit = False
 last = now = ticks_us()
 while now < endTicks:
  if rxPin.value():
   if not bit:
    now = ticks_us()
    bit = True
    edges.append((False,ticks_diff(now,last),int(now/1000)))
    last = now
  else:
   if bit:
    now = ticks_us()
    bit = False
    edges.append((True,ticks_diff(now,last),int(now/1000)))
    last = now
 return edges

def pCount(edges):
 c = 0
 for i in edges:
  if i[1] > 2000:
   print(c,i)
   c+=1

pCount(read(ticks_us() + 100000))

def send(bits):
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



def vvv():
 while True:
  send(PRE+D2)
  sleep_ms(60)
  send(PRE+D3)
  sleep_ms(60)
  send(PRE+D2)
  sleep_ms(60)
  send(PRE+D3)
  sleep_ms(18)
  send(PRE+D2)
  sleep_ms(18)
  send(PRE+D3)
  sleep_ms(500)

  send(PRE+D0)
  sleep_ms(60)
  send(PRE+D1)
  sleep_ms(60)
  send(PRE+D0)
  sleep_ms(60)
  send(PRE+D1)
  sleep_ms(18)
  send(PRE+D0)
  sleep_ms(18)
  send(PRE+D1)
  sleep_ms(500)
vvv()
