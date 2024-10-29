from machine import Pin
from time import sleep_us, sleep_ms, ticks_us, ticks_diff, localtime
print("rxPin 46 capture")
# "Message" starts with LHL then 10 PRE "Bits" then 44 or 43 Dx "Bits"
# Each "Bit" ends Low, each "Message" ends holding High
rxPin = Pin(46, Pin.IN)

# 20240929
# 21:25-23:55 working out LHL (<30min) and short/long bit captures, seeing 2 bits swap when "off"
# 23:55-00:55 tracking down Display & Relay board MCU's to BYD BF7515BM44-LJTX & BF7515BM44-LJTX
#  not manchester encoding (per-say), not UART as specified by MCU's, high pulses of n, only 1 low

# 20240930
# 09:30-      testing reading bits at 1234us interval

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
 if (aLow > 4100 and aLow < 5100) and (bHigh > 9000 and bHigh < 10000) and (cLow > 4100 and cLow < 5100):
  return now    # valid low/high\low idle to start of message
 else:
  print("low/high\low",aLow,bHigh,cLow)
  return -1

def dumpBinary(bits):
 b = ""
 c = 1
 for i in range(len(bits)):
  if bits[i] == 1:
   b += "1"
  else:
   b += "0"
  if c % 8 == 0:
   b += " "
  c += 1
 print(b)

bits = []

def readBit(bit):
 bits.append(rxPin.value())

def loop():
 while True:
  bits = []
  start = idle()
  #print(start)
  if start > -1:
   for i in range(32):
    while ticks_diff(ticks_us(), start + int(i * 1666) + 20) < 0:
     pass
    bits.append(rxPin.value())
   dumpBinary(bits)
  else:
   print("ERROR waiting for low/high\low")

loop()

