# BNO08x Micropython I2C Test programm by Dobodu
#
# This program set up an I2C connection to the BNO08x device
# Then Create a BNO08x class based object
# Then enables sensors
# And finally report sensors every 0.5 seconds.
#
# Original Code from Adafruit CircuitPython Library

# Updates to integrate with whilrlybird DF'n by DEFAULT

from machine import I2C, Pin
import time
from time import sleep_ms
import math
from bno08x_i2c import *
import neopixel

NEO_COUNT = 32
NEO_DELAY = 50

np = neopixel.NeoPixel(Pin(44), NEO_COUNT, bpp=4)

I2C1_SDA = Pin(5)
I2C1_SCL = Pin(4)

def rgbw(p):
 np[p] = (0, 0, 0, 1)
 np.write()
 sleep_ms(NEO_DELAY)

def ring():
 for i in range(24,32):
  rgbw(i)
  np.fill((0,0,0,0))
  np.write()
 for i in range(23,-1, -1):
  rgbw(i)
 np.fill((0,0,0,0))
 np.write()

ring()


i2c1 = I2C(1, scl=I2C1_SCL, sda=I2C1_SDA, freq=100000, timeout=200000 )
#print("I2C Device found at address : ",i2c1.scan(),"\n")
bno = BNO08X_I2C(i2c1, debug=False)
print("BNO08x I2C connection : Done\n")

bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
#bno.enable_feature(BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR)
#bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
#bno.enable_feature(BNO_REPORT_ACTIVITY_CLASSIFIER)
#bno.enable_feature(BNO_REPORT_STABILITY_CLASSIFIER)

print("BNO08x sensors enabling : Done\n")

def tilt():
#26/30 left/right, 28/31 down/up
 x,y,z = bno.acceleration
 np.fill((0,0,0,0))
 if x < -1:
  np[26] = (int(x*-3),0,0,0)
 elif x > 1:
  np[30] = (int(x*3),0,0,0)
 if y < -1:
  np[31] = (0,int(y*-3),0,0)
 elif y > 1:
  np[28] = (0,0,int(y*3),0)
 #print("X: %0.6f\tY: %0.6f\tZ: %0.6f" % (x,y,z))

def turn():
 x,y,z = bno.euler
 r = z + 180 - 13
 if r < 0:
  r += 360
 #print(z,r)
 np[int(r/15)] = (0,0,0,5)
 np.write()

def classifier():
 print(bno.stability_classification, bno.activity_classification["most_likely"])

def loop():
 while True:
  tilt()
  turn()
  #classifier()
  sleep_ms(50)

loop()

#cpt = 0

#while True:
#    time.sleep(0.5)
#    cpt += 1
#    geo_x, geo_y, geo_z, geo_w = bno.geomagnetic_quaternion
#    mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
#    heading = math.atan2(mag_x, mag_y) * 180 / math.pi

#    print("%0.f Geo\tX: %0.6f\tY: %0.6f\tZ: %0.6f\tW: %0.6f\tMag X: %0.6f\tY: %0.6f\tZ: %0.6f\tuT %d" % (heading, geo_x, geo_y, geo_z, geo_w, mag_x, mag_y, mag_z, cpt))
    #if cpt == 10 :
    #    bno.tare


#    print("cpt", cpt)
#    accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
#    print("Acceleration\tX: %0.6f\tY: %0.6f\tZ: %0.6f\tm/s²" % (accel_x, accel_y, accel_z))
#    gyro_x, gyro_y, gyro_z = bno.gyro  # pylint:disable=no-member
#    print("Gyroscope\tX: %0.6f\tY: %0.6f\tZ: %0.6f\trads/s" % (gyro_x, gyro_y, gyro_z))

#    quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
#    print("Rot Vect Quat\tI: %0.6f\tJ: %0.6f\tK: %0.6f\tReal: %0.6f" % (quat_i, quat_j, quat_k, quat_real))
#    R, T, P = bno.euler
#    print("Euler Angle\tX: %0.1f\tY: %0.1f\tZ: %0.1f" % (R, T, P))
#    print("")
