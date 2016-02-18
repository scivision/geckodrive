#!/usr/bin/env python3
"""
use this program at your own risk. no emergency stop.
Python >=3.5
"""
import serial
from time import sleep
#
bh = b'\x04\x00' #comes before all(?) commands

def connectdrive(port='/dev/ttyUSB0'):
    S = serial.Serial(
    port=port,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    xonxoff=serial.XOFF,
    rtscts=False,
    dsrdtr=False
    )

    S.writeTimeout = 0.5

    if S.open:
        S.close()

    S.open()
    assert S.isOpen(),'could not open connection to drive on {}'.format(port)

    return S

def configdrive(S,accel=10,vel=100):
    baccel = int2bytes(accel)
    bvel = int2bytes(vel)
#%% params
    clist = [b'\x19\x0e\x0a\x32', # x configure: 2.5 amps, idle at 50% after 1 seconds
             b'\x19\x4e\x0a\x32', # y configure: 2.5 amps, idle at 50% after 1 seconds
             b'\x01\x0f\xa0\x86', # x limit cw 100000
             b'\x01\x4f\xa0\x86', # y limit cw 100000
             b'\x00\x13\xe8\x03', # x offset 1000
             b'\x00\x53\xe8\x03', # y offset 1000
             b'\x00\x0a\x00\x00', # analog inputs to {0} ; NO AXIS USING ANALOG
             b'\x00\x0b\x00\x00', # vector axis are {0} ; NO AXIS USING VECTOR
             b'\x00\x0c'+baccel, # x acceleration
             b'\x00\x4c'+baccel, # y acceleration
             b'\x00\x07'+bvel, # x velocity
             b'\x00\x47'+bvel, # y velocity
            ]

    for c in clist:
        S.write(bh+c)
        sleep(0.05) #without this pause, the drive won't always work. Minimum pause unknown.

def movedrive(S,step,direc,ymov):
    """
    10000 steps/inch
    direc: positive: forward or up
           negative: backward or down
    """
#%% which direction
    if direc=='-':
        bdir = b'\x80'
    elif direc=='+':
        bdir = b'\x00'
#%% which axis
    if ymov:
        bxy = b'\x41'
    else:
        bxy = b'\x01'
#%% how many steps
    bstep = int2bytes(step)
#%% MOVE (no abort)
    S.write(bh+bdir+bxy+bstep)

def int2bytes(n,byteorder='little'):
    return n.to_bytes((n.bit_length() // 8) + 1, byteorder=byteorder)
