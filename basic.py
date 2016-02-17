#!/usr/bin/env python3

import serial
from time import sleep
#
bh = b'\x04\x00'

def connectdrive():
    S = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    xonxoff=serial.XOFF,
    rtscts=False,
    dsrdtr=False
    )

    S.writeTimeout = 0.2

    if S.open:
        S.close()

    S.open()
    assert S.isOpen(),'could not open connection to drive'

    return S

def configdrive(S):
#%% params
    clist = [b'\x19\x0e\x0a\x32', # x configure: 2.5 amps, idle at 50% after 1 seconds
             b'\x19\x4e\x0a\x32', # y configure: 2.5 amps, idle at 50% after 1 seconds
             b'\x01\x0f\xa0\x86', # x limit cw 100000
             b'\x01\x4f\xa0\x86', # y limit cw 100000
             b'\x00\x13\xe8\x03', # x offset 1000
             b'\x00\x53\xe8\x03', # y offset 1000
             b'\x00\x0a\x00\x00', # analog inputs to {0} ; NO AXIS USING ANALOG
             b'\x00\x0b\x00\x00', # vector axis are {0} ; NO AXIS USING VECTOR
             b'\x00\x0c\x1e\x00', # x acceleration 30 ; RUN ACCELERATION
             b'\x00\x4c\x1e\x00', # y acceleration 30 ; RUN ACCELERATION
             b'\x00\x07\xa0\x0f', # x velocity 4000 ; RUN VELOCITY
             b'\x00\x47\xa0\x0f', # y velocity 4000 ; RUN VELOCITY
            ]

    for c in clist:
        S.write(bh+c)
        sleep(0.05)

def movedrive(S,steps,direc):
    """
    5000 steps/inch, 1000 is one rev. of motor
    direc: positive: forward or up
           negative: backward or down
    """
#%% move!
    #S.write(bh+b'\x00\x01\xe8\x03') #x-1000
    for i in range(10):
        S.write(bh+b'\x80\x01\xe8\x03') #x-1000
        sleep(0.5)

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='GeckoDrive BitBang code')
    p.add_argument('--steps',help='number of steps to move on each cmd',type=int,default=1000)
    p.add_argument('-d','--dir',help='+ fwd, - rev',default='-')
    p = p.parse_args()

    try:
        S = connectdrive()

        configdrive(S)

        movedrive(S,p.steps,p.dir)

    except KeyboardInterrupt:
        pass
    finally:
        S.close()