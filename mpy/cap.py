from machine import Pin
from time import sleep_us, sleep_ms, ticks_us, ticks_diff, localtime
print("rxPin 46 capture")
# "Message" starts with LHL then 10 PRE "Bits" then 44 or 43 Dx "Bits"
# Each "Bit" ends Low, each "Message" ends holding High
rxPin = Pin(46, Pin.IN)


# 21:25-23:55 working out LHL (<30min) and short/long bit captures, seeing 2 bits swap when "off"
# 23:55-00:55 tracking down Display & Relay board MCU's to BYD BF7515BM44-LJTX & BF7515BM44-LJTX
#  not manchester encoding (per-say), not UART as specified by MCU's, high pulses of n, only 1 low


def idle():
 aLow=bHigh=cLow=start=now=ticks_us()
 bit = False
 while True:
  if rxPin.value():
   if not bit:
    start = ticks_us()
    bit = True
   elif ticks_diff(ticks_us(), start) > 10_000:
    break  # high idle for more than 10ms, no active data
  elif bit:
   bit = False
 while rxPin.value():
  pass     # low after being idle, start of message
 start = ticks_us()
 while not rxPin.value():
  pass     # first 'half' long low
 now = ticks_us()
 aLow = ticks_diff(now, start)
 start = now
 while rxPin.value():
  pass     # long high
 now = ticks_us()
 bHigh = ticks_diff(now, start)
 start = now
 while not rxPin.value():
  pass     # second 'half' long low
 now = ticks_us()
 cLow = ticks_diff(now, start)
 print("low/high\low",aLow,bHigh,cLow)
 if (aLow > 4100 and aLow < 5100) and (bHigh > 9000 and bHigh < 10000) and (cLow > 4100 and cLow < 5100):
  return True    # valid low/high\low idle to start of message
 else:
  print("low/high\low",aLow,bHigh,cLow)
  return False

def read():
 edges = []
 bit = True  # starts low (False) after idle
 diff = start = ticks_us()
 while True:
  while rxPin.value():
   diff = ticks_diff(ticks_us(), start)
   if diff > 10_000:
    return edges    # high idle, message ended
  #print("HIGH", diff)
  #start = ticks_us()
  while not rxPin.value():
   pass      # data bits low
  diff = ticks_diff(ticks_us(), start)
  #print("LOW ", diff)
  if diff < 2_000:
   edges.append((1, diff))
  else:
   edges.append((0, diff))
  start = ticks_us()

def dumpCap(edges):
 c = 0
 for i in edges:
  print(c,i)
  c+=1

def dumpBinary(edges):
 b = ""
 c = 1
 for i in edges:
  if i[0] == 1:
   b += "1"
  else:
   b += "0"
  if c % 10 == 0:
   b += " "
  c += 1
 print(b)

def loop():
 while True:
  if idle():
   dumpCap(read())
   dumpBinary(read())
  else:
   print("ERROR waiting for low/high\low")

loop()
