# Vaisala RS41 Serial Communication by DEFAULT

# Testing with "W2334448", renamed "TEST"

# Vaisala RS41 Radiosonde SW V2.05.06
# Copyright (c) Vaisala Oyj 2022. All rights reserved.
# Serial number: TEST
# Transmitter frequency: 401.00 MHz
# Transmitter power: 0/7
# Number of SW resets is 8
#
#
# (S)ensors        Fre(q)uencies  (P)arameters    (A)lfa        TX p(o)wer
# TX (f)requency   T(X) state     (T)X registers  TX ran(d)om   TX (c)arrier
# (B)aud rate      Ser(i)al no    (R)ed LED info  (N)o menu     (K)eep test mode
# S(W) version     (M)easurements (L)aunch/Drop   (E)xit
# >

# (S)ensors:
#   RH: 521.99 RHtu:  25.29 Trh:  51.78 T:   0.91 Tref:  31.45 Tmcu:   8.01 C:  47.36 Rt: 1116.52 Rts: 1218.48 Tp:  0.1765 Cp:  0.2910

# (G)PS Calculated:
#   wk 2335 tow 179368999 x -268384791 y -428401417 z 387613697 vx -17 vy -14 vz -2 nsv 10 acc 2 pdop 16



from machine import Pin, UART, RTC, Timer
from micropython import const
from time import sleep_ms, gmtime, localtime

_DAYS_DELTA = const(7300)  # Days between 1980.01.06 & 2000.01.01
_DAYS_2_SEC = const(86400) # Seconds per day
_LEAP_SEC_O = const(18)     # Leap seconds to offset

_MODE_UNKNOWN = "?"
_MODE_OFF = "Power Off"
_MODE_INIT = "Initializing"
_MODE_RESET = "Reseting"
_MODE_MENU = "Main Menu"
_MODE_MENU_MEASUREMENTS = "Measurements Menu"
_MODE_SENSORS = "Sensors Active"
_MODE_GPS_INIT = "GPS Initializing"
_MODE_GPS_AQUIRING = "GPS Aquiring"
_MODE_GPS_READY = "GPS Ready"


def _c2f(temp):
 return temp * 1.8 + 32

class RS41:
 def __init__(self, reset, enabled=True, rx=44, tx=43, baud=9600):
  self.reset = reset
  self.rx = rx
  self.tx = tx
  self.baud = baud
  self.mode = _MODE_UNKNOWN
  self.uart = UART(1, baudrate=baud, tx=tx, rx=rx, timeout=100, timeout_char=10)
  self.count = 0  # Number of UART reads with more than 0 bytes
  self.radioActive = -1
  self.buf = bytearray(1)
  self.temperature = -99.99
  self.humidity = -1

  self.showCount = True
  self.showBytes = False

  self.autoTxDisable = True

  self.uart.irq(self._read, UART.IRQ_RX) #UART.IRQ_RXIDLE + UART.IRQ_BREAK)

  if enabled:
   self.enable()
  #self._write()

  self.timer2 = Timer(2)
  print("   AUTO DISABLE TX IN 3 SECONDS")
  self.timer2.init(period=3000, mode=Timer.ONE_SHOT, callback=self._auto_tx_disable)


  #sleep_ms(500)
  #self.enable(False)  # Turn it "Off"
  # TODO: Refactor to async, changed to event based
  #self.timer2 = Timer(2)
  #self.timer2.init(period=10, mode=Timer.PERIODIC, callback=self._loop)
  #self.enable()       # Turn it "On"


 def _loop(self, t):
  pass
  #self._read()

 def _read(self, irq):
  if self.uart.any() > 0:
   self.count += 1
   self.buf += self.uart.read()
   self.decode()

 def _write(self, msg=''):
  if msg == '':
   msg = '\r'
  print(msg)
  self.uart.write(msg)

 def _mode(self, mode):
  if self.mode == mode:
   return
   print("   MODE: " + mode)
  else:
   print("   MODE - FROM: " + self.mode + " TO: " + mode)
  self.mode = mode

 def enable(self, on=True):
  if on:
   print("< RS41 RESET: LOW 'Releasing Reset, initializing for few seconds!'")
   self.reset(False) # xio.output(0,3,0)
   self._mode(_MODE_INIT)
   #sleep_ms(5000)
  else:
   print("< RS41 RESET: HIGH 'Entering Reset, will generate software reset on release.'")
   self.reset(True) #xio.output(0,3,1)
   self._mode(_MODE_RESET)
   sleep_ms(500)

 def _auto_tx_disable(self, t):
  self.txState()

 def _auto_measurements(self, t):
  print("   SENSORS INTERVAL STARTING IN 2 SECONDS")
  self.timer2.init(period=2000, mode=Timer.ONE_SHOT, callback=self._auto_sensors)
  self.measurements()
  self.mode = _MODE_MENU_MEASUREMENTS

 def _auto_sensors(self, t):
  self.sensors(10)

 def decode(self):
  #try:
  if True:
   if self.showCount:
    print("> RS41 UART: {} ({})".format(self.count, len(self.buf)))
   if self.showBytes:
    print(self.buf)

   msg = str(self.buf, 'utf-8').split('\r')
   for i in msg:
    if True or not _MODE_GPS_READY:
     print(i)

    if i.find("Vaisala RS41 Radiosonde") >= 0:
     # Powered on or Reset
     self._mode(_MODE_INIT)
     self.menu()

    if i.find("(L)aunch/Drop   (E)xit") >= 0:
     # Get Name, SW Version, Serial, Frequency, Power, SW Resets
     self._mode(_MODE_MENU)

    if i.find("D(I)rect GPS mode (E)xit") >= 0:
     if not self.mode == _MODE_GPS_AQUIRING:
      self._mode(_MODE_MENU_MEASUREMENTS)

    if i.find("Enabled TX") >= 0:    # Enabled automatically
     self.radioActive = True
     if self.autoTxDisable:
      self.txState()
    elif i.find("TX enabled") >= 0:  # Enabled by command
     self.radioActive = True
    elif i.find("TX disabled") >= 0: # Disabled by command
     self.radioActive = False
     self.timer2.init(period=2000, mode=Timer.ONE_SHOT, callback=self._auto_measurements)
     print("   MEASUREMENTS MENU IN 2 SECONDS")

    if i.find("Tref:") >= 0:
     self._mode(_MODE_SENSORS)
     j = i.index("Tref:") + 7
     t = float(i[j:j+5])
     self.temperature = t
     j = i.index("RHtu:") + 7
     h = float(i[j:j+5])
     self.humidity = h
     print('Temperature: {}C/{}F  Humidity: {}%'.format(t, t * 1.8 + 32, h))

    if self.mode == _MODE_GPS_INIT:
     #if len(i) < 56:
     # return
     self._mode(_MODE_GPS_AQUIRING)
    elif self.mode == _MODE_GPS_AQUIRING:
     #if len(i) < 88:
     # return
     if i.startswith('wk '):
      self._mode(_MODE_GPS_READY)

    if _MODE_GPS_READY and i.find('wk ') >= 0:
     #if i.find('pdop ') < 0:
     # return
     j = i.index('wk ') + 3
     wk = int(i[j:j+4])
     j += 9
     tow = int(i[j:j+9])
     if wk > 0 and tow >= 0:
      self.gpsTime(wk, tow)
     else:
      print("> RS41 UART: GPS TIME ERROR")

    self.buf = bytearray()

  #except:
  # print("> RS41 UART: DECODE ERROR")
  # print(self.buf)

 def txState(self):
  print("< RS41: T(X) state")
  self._write('X')

 def menu(self):
  self._write('STwsv\r')

 def noMenu(self):
  self._write('N')

 def exit(self, quit=False):
  if self.mode == _MODE_MENU:
   if quit:
    print("   Leaving Service Menu, you may need to re-initialize to use any features!")
    self._write('E')
   else:
    print("   You are at the top level Menu, 'QUIT' parameter required to execute command.")
  elif self.mode == _MODE_MENU_MEASUREMENTS:
   self.measurements(True)
  else:
   print("   Do not know how to exit from here, giving up.")

 def measurements(self, exit=False):
  if not exit:
   print("< RS41: (M)easurements")
   self._write('M')
   sleep_ms(1000)
  else:
   print("< RS41: (E)xit")
   sleep_ms(500)
   self._write('E')

 def sensors(self, interval=''):
  if interval == '':   # One Time read
   if self.mode == _MODE_MENU:
    print("< RS41: (S)ensor")
    self._write('S')
   else:
    print("   Not in main menu, can't start one time read!")
  elif interval > 0:   # Interval read
   if self.mode == _MODE_MENU:
    self.measurements()
    return
   if self.mode == _MODE_MENU_MEASUREMENTS:
    print("< RS41: (S)ensors")
    self._write('S')
    sleep_ms(1000)
    print("< RS41: Period [" + str(interval) + "] \r")
    self._write(str(interval) + '\r')
   else:
    print("   Failed to enter " + _MODE_MENU_MEASUREMENTS)
  else:                # Stop Interval read
   if self.mode == _MODE_SENSORS:
    self._mode(_MODE_MENU_MEASUREMENTS)
    print("< RS41: [\r] 'Pressing any key'")
    self._write()
   else:
    print("   Not in expected mode or menu, trying menu refresh")
    self._write()
  if interval == '':
   interval = 0
  if interval < 0 and self.mode == _MODE_MENU_MEASUREMENTS:
   self.measurements(True)

 def gps(self):
  if self.mode == _MODE_MENU:
   self.measurements()
   return
  if self.mode == _MODE_MENU_MEASUREMENTS:
   print("< RS41: (G)PS (2)=Calculated")
   self._write('G2\r')
   self._mode(_MODE_GPS_INIT)
  elif self.mode == _MODE_GPS_READY or self.mode == _MODE_GPS_AQUIRING or self.mode == _MODE_GPS_INIT:
   print("< RS41: (G)PS (0)=None")
   self._write('G0\r')
   self._mode(_MODE_MENU_MEASUREMENTS)

 def round(self, f):
  return int('{:.0f}'.format(f))

 def gpsTime(self, wk, tow):
  try:
   t = (wk * 7 - _DAYS_DELTA) * _DAYS_2_SEC + self.round(tow / 1000) - _LEAP_SEC_O
   print('wk: {} tow: {} - Time: {}'.format(wk, tow, gmtime(t)))
   return gmtime(t)
  except:
   print("> RS41: ERROR Converting GPS time")
   return 0

#637813700

 def test(self, disable=True, initialDelay=1000, stateDelay=1000, disableDelay=1000):
  print("Power on Radiosonde")
  self.enable(True)
  while not self.connected:
   pass
  sleep_ms(initialDelay)
  print("Send menu command")
  _write('\r')
  _write('STwsv\r')
  sleep_ms(stateDelay)
  print("Send TX Disable")
  _write('X')
  if disable:
   sleep_ms(disableDelay)
   print("Disabling")
   self.enable(False)

#test(True, 500, 1000, 3000)
