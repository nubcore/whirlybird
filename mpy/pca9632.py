# PCA9632 I2C 4-Bit LED Driver by DEFAULT
from micropython import const

# I2C Address for LED Driver for D8-D16
_ADDR    = const(0x62)
# Register Addresses
_MODE1   = const(0x00) # 0x10=on,0x00=sleep
_MODE2   = const(0x01) # 0x00=dim,0x20=blink(group)
# 8-bit individual brightness
_PWM0    = const(0x02) # D11,D8,D14
_PWM1    = const(0x03) # D9,D10,D12
_PWM2    = const(0x04) # D16,D15,D13
_PWM3    = const(0x05) # not connected
# Group control
_GRPPWM  = const(0x06) # 7-bit
_GRPFREQ = const(0x07) # 7-bit
# 0[1:0],1[3:2],2[5:4],3[7:6]
# 00=Off,01=On,10=PWMx,11=GRPPWM/GRPFREQ
_LEDOUT = const(0x08)

class PCA9632:
 def __init__(self, i2c, address=0x62):
  self.i2c = i2c
  self.addr = address
  self.buf = bytearray(1)
  self._sleeping = True
  self.blinking = False
  #self._write(_MODE1, 0x10)  # power up

 def _write(self, register, value):
  self.buf[0] = value
  self.i2c.writeto_mem(self.addr, register, self.buf)

 def _read(self, register):
  self.i2c.readfrom_mem_into(self.addr, register, self.buf)
  return self.buf[0]

 def sleep(self, enable=True):
  if enable:
   self._write(_MODE1, 0x00)  # power down
   self._sleeping = True
  else:
   self._write(_MODE1, 0x10)  # power up
   self._sleeping = False

 def dim(self):
  self._write(_PWM0, 0x05)   # D8 & D11
  self._write(_PWM1, 0x03)   # D12
  self._write(_LEDOUT, 0x0A) # Enable PWM0 & PWM1
  self._write(_MODE2, 0x00)
  self.blinking = False

 def blink(self):
  self._write(_GRPPWM,0x0F)  # Group brightness
  self._write(_GRPFREQ,0x0F) # Group blink rate
  self._write(_LEDOUT, 0x0F) # Enable DMBLNK
  self._write(_MODE2, 0x20)
  self.blinking = True

 def toggleMode(self):
  if self.blinking:
   self.dim()
  else:
   self.blink()
