from machine import Pin, Timer
from time import sleep_us, sleep_ms, ticks_us, ticks_diff, localtime

print("insta proof & dehydrate")

# 20240930
# 13:00-19:30 translate commands from oscilliscope to bit sequences, note function and power, test playback

# TODO: Convect LO/HI variations sampling. Temperature set changes?

# "Message" starts with LHL then 10 PRE "Bits" then 44 or 43 Dx "Bits"
# Each "Bit" ends Low, each "Message" ends holding High

# Original 4450/9140\4450
LHL = [4500,9000,4500] # Low High Low start
LHL_DEFAULT = [4500,9000,4500] # Low High Low start
NIB = NIB_DEFAULT = 800
BIT = BIT_DEFAULT = 1600

def vp(v,p,h=False):
 if h: # apply half of change
  return v + int(v*p)
 else:
  return v + 2 * int(v*p)

def speed(p=0):
 global LHL, NIB, BIT
 #LHL[0] = vp(LHL_DEFAULT[0],p,True)
 #LHL[1] = vp(LHL_DEFAULT[1],p)
 #LHL[2] = vp(LHL_DEFAULT[2],p,True)
 NIB = vp(NIB_DEFAULT,p,True)
 BIT = vp(BIT_DEFAULT,p)


# 0 Bit = BIT Low
# 1 Bit = NIB High, NIB Low

PRE = (1,1,1,1,0,1,1,1,1,0) # Preamble

# Note: empty line following sequence represents power cycle reset to known starting state

DOOR_O   = (1,0,1,1,1,1,1,1, 1,1,0,1,1,0,1,1, 0,1,0,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,0,1,1,0,1,0, 1,0,1,1,1,1) # door opened, light on
DOOR_U   = (1,1,1,1,1,1,1,1, 1,0,1,1,0,1,1,0, 1,0,1,1,1,1,1,0, 1,0,1,1,1,0,1,0, 1,0,1,0,1,0,1,0, 1,1,1,1) # door open, light timed off
DOOR_T   = (1,1,1,1,1,1,1,1, 1,0,1,0,1,0,1,1, 0,1,0,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,1,1,0,1,0,1, 1,1,1) # door closed, light already off
DOOR_C   = (1,0,1,1,1,1,1,1, 1,1,0,1,0,1,0,1, 1,0,1,0,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,0,1,1,0,1, 0,1,1,1,1) # door closed, light on
DOOR_I   = (1,1,1,1,1,1,1,1, 1,0,1,0,1,0,1,1, 0,1,0,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,1,1,0,1,0,1, 1,1,1) # door close, light timed off

# "Light" press 'on', timed 'off', press 'on', timed 'off', press 'on', press 'off', press 'on', timed 'off'
TX_OFF_0 = (1,1,1,1,1,1,1,1, 1,1,0,1,1,1,1,0, 1,1,1,1,1,0,1,0, 1,1,1,0,1,0,1,0, 1,1,1,1,0,1,1,1) # power on "OFF" display idle ping, long initial beep
TX_ON_A  = (1,0,1,1,1,1,1,1, 1,1,0,1,1,0,1,1, 0,1,0,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,1,0,1,0,1,0, 1,1,1,1) # "Light" press 'on' 25W
TX_OFF_A = (1,1,1,1,1,1,1,1, 1,0,1,1,0,1,1,0, 1,0,1,1,1,1,1,0, 1,0,1,1,1,0,1,0, 1,0,1,0,1,0,1,0, 1,1,1,1) # light timed 'off', short beep
TX_ON_B  = (1,0,1,1,1,1,1,1, 1,1,0,1,0,1,0,1, 1,0,1,0,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,0,1,1,0,1, 0,1,1,1,1) # "Light" press 'on' short beep
TX_OFF_B = (1,1,1,1,1,1,1,1, 1,0,1,0,1,0,1,1, 0,1,0,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,1,1,0,1,0,1, 1,1,1)   #     ''    timed 'off'
TX_ON_C  = (1,1,1,1,1,1,1,1, 1,1,0,1,1,0,1,0, 1,1,1,1,1,0,1,0, 1,1,1,0,1,0,1,0, 1,0,1,0,1,0,1,1, 1,1)     #     ''    press 'on' short beep
TX_OFF_C = (1,1,1,1,1,1,1,1, 1,1,1,0,1,1,0,1, 0,1,1,1,1,1,0,1, 0,1,1,1,0,1,0,1, 1,0,1,0,1,0,1,1, 1,1)     # ??? ''    timed 'off'
TX_ON_D  = (1,0,1,1,1,1,1,1, 1,1,1,0,1,0,1,1, 0,1,0,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,1,1,0,1,0,1, 1,1,1,1) #     ''    press 'on' no beep
TX_OFF_D = (1,1,1,1,1,1,1,1, 1,1,0,1,0,1,1,0, 1,0,1,1,1,1,1,0, 1,0,1,1,1,0,1,0, 1,0,1,1,0,1,0,1, 1,1,1)   #     ''    press 'off' no beep
TX_PROOF = (1,1,1,1,1,1,1,1, 1,0,1,1,0,1,0,1, 1,1,1,1,0,1,0,1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,1,1, 1) # "Proof" press, times out TX_OFF_B

# "Proof" Convect LO 90F 01:00
PROOF_A  = (1,1,1,1,1,1,1,1, 1,0,1,1,0,1,1,0, 1,0,1,1,1,1,1,0, 1,0,1,1,1,0,1,0, 1,0,1,0,1,0,1,0, 1,1,1,1) # "Proof" press, "Cancel" OR times out to TX_OFF_B
PROOF_S  = (1,0,1,1,0,1,1,0, 1,1,1,1,0,1,0,1, 1,0,1,1,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,0,1,1,0,1, 0,1,0,1,0,1,1) # "Start" press, heats and light 'on'
PROOF_T  = (1,1,1,0,1,1,0,1, 1,1,1,0,1,0,1,1, 0,1,1,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,1,1,0,1,0,1, 0,1,0,1,1) # light timed 'off'
PROOF_L  = (1,0,1,1,0,1,1,0, 1,1,1,1,1,1,0,1, 1,0,1,0,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,1,1,1,0,1, 0,1,1,1) # "Light" press 'on'
PROOF_O  = (1,1,1,0,1,1,0,1, 1,1,1,1,0,1,0,1, 1,0,1,0,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,0,1,0,1,1, 0,1,0,1,1,1) # "Light" press 'off'
PROOF_U  = (1,1,1,0,1,1,0,1, 1,1,1,0,1,1,0,1, 1,0,1,0,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,1,1,1,0,1, 0,1,1,1) # light timed out 'off'
PROOF_C  = (1,1,1,0,1,1,1,1, 1,1,0,1,0,1,0,1, 1,0,1,0,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,1,0,1,1,0, 1,1,1,1) # "Cancel" press, cycle end, fan continues (delay off un-commanded)

PROOF_AL = (1,0,1,1,1,1,1,1, 1,1,0,1,0,1,0,1, 1,0,1,0,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,0,1,1,0,1, 0,1,1,1,1) # ALT of 'A' if light pressed first then proof
PROOF_SL = (1,0,1,1,0,1,1,0, 1,1,1,1,1,1,1,0, 1,1,1,1,1,1,1,0, 1,0,1,1,1,0,1,0, 1,0,1,0,1,0,1,0, 1,0,1,0,1,1) # "Start" pressed, light still on
PROOF_CL = (1,1,1,0,1,1,1,1, 1,1,1,0,1,0,1,1, 0,1,0,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,1,0, 1,1,1,1) # "Cancel" pressed, proofing ended
PROOF_UL = (1,1,1,1,1,1,1,1, 1,1,0,1,1,0,1,0, 1,1,1,1,1,0,1,0, 1,1,1,0,1,0,1,0, 1,0,1,0,1,0,1,1, 1,1) # light timed 'off'
PROOF_TC = (1,1,1,1,1,1,1,1, 1,1,1,0,1,1,0,1, 0,1,1,1,1,1,0,1, 0,1,1,1,0,1,0,1, 1,0,1,0,1,0,1,1, 1,1) # "Proof" times out, no "Start" or "Cancel" press

# "Dehydrate" Convect HI 135F 08:00
DEHYD_A  = (1,1,1,1,1,1,1,1, 1,0,1,1,0,1,1,0, 1,0,1,1,1,1,1,0, 1,0,1,1,1,0,1,0, 1,0,1,0,1,0,1,0, 1,0,1,1,1,1) # "Dehydrate" press
DEHYD_S  = (1,0,1,1,0,1,0,1, 1,0,1,1,0,1,0,1, 0,1,1,0,1,1,1,1, 1,1,1,0,1,0,1,1, 1,0,1,0,1,0,1,0, 1,1,1,0,1,1,1,0) # "Start"
DEHYD_2  = (1,0,1,1,0,1,0,1, 1,1,1,1,0,1,0,1, 1,0,1,1,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,0,1,0,1,1, 1,1,0,1,1,0) # 2nd phase? (un-commanded)
DEHYD_T  = (1,1,1,0,1,0,1,1, 1,1,1,0,1,0,1,1, 0,1,1,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,1,0,1,1,1,1, 0,1,1) # light timed 'off'
DEHYD_HI = (1,1,1,0,1,0,1,1, 0,1,1,0,1,0,1,0, 1,1,0,1,1,1,1,1, 1,1,0,1,0,1,1,1, 0,1,0,1,1,0,1,1, 1,0,1,1,1,0) # 'hi' 1380W (2 clicks, un-commanded)
DEHYD_F  = (1,1,1,0,1,0,1,1, 1,1,1,0,1,0,1,1, 0,1,1,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,1,0,1,1,1,1, 0,1,1) # convection blower 52W (un-commanded)
DEHYD_L  = (1,0,1,1,0,1,0,1, 1,1,1,1,1,1,0,1, 1,0,1,0,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,1,1,0,1,1, 1,1,1) # "Light" press & blower on 76W
DEHYD_U  = (1,1,1,0,1,0,1,1, 1,1,1,1,1,0,1,1, 0,1,0,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,0,1,1,0,1,1, 1,1,1) # light timed 'off', blower on 51W
DEHYD_HL = (1,0,1,1,0,1,0,1, 1,0,1,1,0,1,1,0, 1,0,1,1,0,1,0,1, 1,1,1,1,0,1,0,1, 1,1,0,1,0,1,1,0, 1,0,1,1,1,0,1,1, 0) # "Light" press 'on', high power 1420W
DEHYD_HU = (1,0,1,1,0,1,0,1, 1,1,1,1,1,0,1,0, 1,1,0,1,0,1,1,1, 1,1,0,1,0,1,1,1, 0,1,0,1,1,0,1,0, 1,1,1,1,1) # light timed 'off' 51W
DEHYD_UU = (1,1,1,0,1,0,1,1, 1,1,1,0,1,1,0,1, 1,0,1,0,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,1,1,0,1,1, 1,1,1) # light timed 'off' low
DEHYD_HJ = (1,1,1,0,1,0,1,1, 0,1,1,0,1,0,1,1, 0,1,1,0,1,0,1,1, 1,1,1,0,1,0,1,1, 1,0,1,0,1,1,1,0, 1,1,1,0) # high power (un-commanded)
DEHYD_C  = (1,1,1,0,1,1,1,1, 1,1,0,1,0,1,0,1, 1,0,1,0,1,1,1,1, 1,0,1,0,1,1,1,0, 1,0,1,1,0,1,1,0, 1,1,1,1) # "Cancel", fan continues 3W
DEHYD_I  = (1,1,1,1,1,1,1,1, 1,0,1,0,1,0,1,1, 0,1,0,1,1,1,1,1, 0,1,0,1,1,1,0,1, 0,1,1,1,0,1,0,1, 1,1,1) # fan off idle 1W

# "Warm" Convect LO 170F 01:00

# "Roast" Convect HI Rotate 400F 00:18

# "Broil" Convect LO 450F 00:10

# "Bake" Convect LO Rotate 350F 00:40

# "Slow Cook" Convect LO 210F 08:00

# "Reheat" Conect LO 300F 00:10

# "Toast" 2PC 05:50 Toast LEvel 4/7

# TODO: Rx LHL then 3 low, 17 high start after


rxPin = Pin(46, Pin.IN)
txPin = Pin(43, Pin.OUT, value=1)

command = TX_OFF_0

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

def sendCommand(t):
 send(command)

tim0 = Timer(0)
def repeatOn():
 tim0.init(period=250, mode=Timer.PERIODIC, callback=sendCommand)

def repeatOff():
 tim0.deinit()

#repeatOn()

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
#vvv()
