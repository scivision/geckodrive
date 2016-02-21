#!/usr/bin/env python3
"""
use this program at your own risk. no emergency stop.
"""
from typing import Union,Optional
import serial
from time import sleep
#
bESTOP=b'\x00\00' #unverified
bSTOP= b'\x01\00'
bRUN = b'\x04\x00'
PORT='/dev/ttyUSB0' #only if user didn't specify


def connectdrive(port:Optional[str]=None):
    if port == '/dev/null': #simulation mode
        print('simulation open')
        S = Simport()
        return S
    elif port is None:
        port = PORT

    S = serial.Serial(
    port=port,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    xonxoff=serial.XOFF,
    rtscts=False,
    dsrdtr=False,
    timeout = 0.2) #this 0.02 timeout was in original SDK

    if S.isOpen():
        S.close()

    S.open()
    assert S.isOpen(),'could not open connection to drive on {}'.format(port)

    return S

def estopdrive(S=None,port:Optional[str]=None):
    """
    This function may not work. Whenever using a motor drive, be within reach
    of hardware emergency off switch!
    """
    if not S or not S.isOpen():
        S=connectdrive(port)

    S.write(bESTOP)
    print('attempted EMERGENCY stop drive')

def stopdrive(S=None, port:Optional[str]=None):
    """
    This function may not work. Whenever using a motor drive, be within reach
    of hardware emergency off switch!
    """
    if not S or not S.isOpen():
        S=connectdrive(port)

    S.write(bSTOP)
    print('attempted to stop drive')

def configdrive(S, #accel:Union[int,float]=10, vel:Union[int,float]=100,
                                   port:Optional[str]=None,verbose:bool=False):
    if not S or not S.isOpen():
        S=connectdrive(port)

#FIXME accept user param
    #baccel = int2bytes(accel)
    #bvel = int2bytes(vel)
#%% params
    clist = [b'\x19\x0e\x0a\x32', # x configure: 2.5 amps, idle at 50% after 1 seconds
             b'\x19\x4e\x0a\x32', # y configure: 2.5 amps, idle at 50% after 1 seconds
             b'\x01\x0f\xa0\x86', # x limit cw 100000
             b'\x01\x4f\xa0\x86', # y limit cw 100000
             b'\x00\x13\xe8\x03', # x offset 1000
             b'\x00\x53\xe8\x03', # y offset 1000
             b'\x00\x0a\x00\x00', # analog inputs to {0} ; NO AXIS USING ANALOG
             b'\x00\x0b\x00\x00', # vector axis are {0} ; NO AXIS USING VECTOR
             b'\x00\x0c\x05\x00',#+baccel, # x acceleration
             b'\x00\x4c\x05\x00',#+baccel, # y acceleration
             b'\x00\x07\xe8\x03',#+bvel, # x velocity
             b'\x00\x47\xe8\x03',#+bvel, # y velocity
            ]

    for c in clist:
        ccmd = bRUN+c
        if verbose:
            print(ccmd)
        S.write(ccmd)
        sleep(0.02) #without this pause, the drive won't always work. Minimum pause unknown.

def movedrive(S, axis:str, dist_cm:Union[int,float], steps_per_inch:int,
                                                port:Optional[str]=None,verbose:bool=False):
    if not S or not S.isOpen():
        S=connectdrive(port)
        configdrive(S,port)
#%% which direction
    if dist_cm<0:
        bdir = b'\x80'
    elif dist_cm>=0:
        bdir = b'\x00'
    else:
        raise ValueError('unknown distance {} cm'.format(dist_cm))
#%% which axis
    if axis.lower()=='x':
        bxy = b'\x41'
    elif axis.lower()=='y':
        bxy = b'\x01'
    else:
        raise ValueError('unknown direction {}'.format(axis))
#%% how many steps
    bstep = int2bytes(distcm2step(dist_cm,steps_per_inch,verbose))
#%% MOVE (no abort)
    movecmd=bRUN+bdir+bxy+bstep
    if verbose:
        print('sending {}'.format(movecmd))
    S.write(movecmd)

    S.close()

def int2bytes(n: int, byteorder: str='little') -> bytes:
    assert 0 <= n < 65536,'need a better method to convert >65535, <I struct vs. <H struct'
    return n.to_bytes((n.bit_length() // 8) + 1, byteorder=byteorder)

def distcm2step(dist_cm: Union[int,float], steps_per_inch:int=10000, verbose:bool=False) -> int:
    """
    verify steps per inch with your drive!!
    returns integer number of steps corresponding to centimeters requests.
    sign is handled in move function.
    """
    steps = round(abs(dist_cm)/2.54 * steps_per_inch)
    if verbose:
        print('{} steps'.format(steps))
    return steps

from tempfile import mkstemp
class Simport():
    """
    this class is used for selftest, when you don't have or want to use the RS485 convertor
    or the real motor drive
    """
    def __init__(self):
        import pipes
        self.f = pipes.Template()
        self.pipefn = mkstemp()[1]

    def isOpen(self):
        return True

    def write(self, cmd: bytes):
        with self.f.open(self.pipefn,'w') as f:
            f.write(str(cmd))

    def close(self):
        self.f.reset()
        print('simulation disconnect')
