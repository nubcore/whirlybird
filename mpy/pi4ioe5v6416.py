# PI4IOE5V6416 by DEFAULT

# TODO: WTF "Port 4" == '3'? LSB/MSB?

from micropython import const

_PORT0_IN  = const(0x00)
_PORT1_IN  = const(0x01)
_PORT0_OUT = const(0x02)
_PORT1_OUT = const(0x03)
_PORT0_CFG = const(0x06) # 1=in (default)
_PORT1_CFG = const(0x07) # 0=out
_INT0_MASK = const(0x8A) # 1=enabled
_INT1_MASK = const(0x8B) # INT pin active LOW
_INT0_TRIG = const(0x8C) # 1=interrupt source
_INT1_TRIG = const(0x8D)

class PI4IOE5V6416:
 def __init__(self, i2c, address=0x20):
  self.i2c = i2c
  self.addr = address
  self.buf = bytearray(1)
  self.output0 = 0xFF
  self.output1 = 0xFF
  self.config0 = 0xFF
  self.config1 = 0xFF

 def _write(self, register, value):
  self.buf[0] = value
  self.i2c.writeto_mem(self.addr, register, self.buf)

 def _read(self, register):
  self.i2c.readfrom_mem_into(self.addr, register, self.buf)
  return self.buf[0]

 def input(self, port, bit):
  return self._read(_PORT0_IN + port) >> bit & 0x1

 def output(self, port, bit, on=True):
  output = self.output0 if port == 0 else self.output1
  if on:
   output |= 1 << bit
  else:
   output &= ~(1 << bit)
  if port == 0:
   self.output0 = output
  else:
   self.output1 = output
  self._write(_PORT0_OUT + port, output)

 def outputEnable(self, port, bit, enable=True):
  config = self.config0 if port == 0 else self.config1
  if enable:
   config &= ~(1 << bit)
  else:
   config |= 1 << bit
  if port == 0:
   config0 = config
  else:
   config1 = config
  self._write(_PORT0_CFG + port, config)
