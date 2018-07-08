#!/usr/bin/env python
"""
use this program at your own risk. no emergency stop.
"""
import serial
from time import sleep
from struct import pack
from numpy import sign
from tempfile import mkstemp
#
bESTOP = b'\x00\00'  # unverified
bSTOP = b'\x01\00'
bRUN = b'\x04\x00'
PORT = '/dev/ttyUSB0'  # only if user didn't specify


def connectdrive(port: str=PORT):
    if port == '/dev/null':  # simulation mode
        print('simulation open')
        S = Simport()
        return S

    S = serial.Serial(
        port=port,
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        xonxoff=serial.XOFF,
        rtscts=False,
        dsrdtr=False,
        timeout=0.2)  # this 0.02 timeout was in original SDK

    if S.isOpen():
        S.close()

    S.open()
    assert S.isOpen(), f'could not open connection to drive on {port}'

    return S


def estopdrive(S, port: str):
    """
    This function may not work. Whenever using a motor drive, be within reach
    of hardware emergency off switch!
    """
    if not S or not S.isOpen():
        S = connectdrive(port)

    S.write(bESTOP)
    print('attempted EMERGENCY stop drive')


def stopdrive(S, port: str):
    """
    This function may not work. Whenever using a motor drive, be within reach
    of hardware emergency off switch!
    """
    if not S or not S.isOpen():
        S = connectdrive(port)

    S.write(bSTOP)
    print('attempted to stop drive')


# accel=10, vel=100,
def configdrive(S, port: str, verbose: bool=False):
    if not S or not S.isOpen():
        S = connectdrive(port)

# FIXME accept user param
    # baccel = int2bytes(accel)
    # bvel = int2bytes(vel)
# %% params
    clist = [b'\x19\x0e\x0a\x32',  # x configure: 2.5 amps, idle at 50% after 1 seconds
             b'\x19\x4e\x0a\x32',  # y configure: 2.5 amps, idle at 50% after 1 seconds
             b'\x01\x0f\xa0\x86',  # x limit cw 100000
             b'\x01\x4f\xa0\x86',  # y limit cw 100000
             b'\x00\x13\xe8\x03',  # x offset 1000
             b'\x00\x53\xe8\x03',  # y offset 1000
             b'\x00\x0a\x00\x00',  # analog inputs to {0} ; NO AXIS USING ANALOG
             b'\x00\x0b\x00\x00',  # vector axis are {0} ; NO AXIS USING VECTOR
             b'\x00\x0c\x05\x00',  # +baccel, # x acceleration
             b'\x00\x4c\x05\x00',  # +baccel, # y acceleration
             b'\x00\x07\xe8\x03',  # +bvel, # x velocity
             b'\x00\x47\xe8\x03',  # +bvel, # y velocity
             ]

    for c in clist:
        ccmd = bRUN+c
        if verbose:
            print(ccmd)
        S.write(ccmd)
        sleep(0.02)  # without this pause, the drive won't always work. Minimum pause unknown.


def movedrive(S, axis: str, dist_inch: float, steps_per_inch: int,
              verbose: bool=False):

    # %% which direction
    if dist_inch < 0:
        bdir = b'\x80'
    elif dist_inch >= 0:
        bdir = b'\x00'
    else:
        raise ValueError(f'unknown distance {dist_inch}')
# %% which axis
    if axis.lower() == 'x':
        bxy = b'\x41'
    elif axis.lower() == 'y':
        bxy = b'\x01'
    else:
        raise ValueError(f'unknown direction {axis}')
# %% how many steps
    distmax = 65535/steps_per_inch
    if abs(dist_inch)*steps_per_inch > 65535:
        q, r = divmod(abs(dist_inch), distmax)
        for _ in range(int(q)):
            domove(S, sign(dist_inch)*distmax, bdir, bxy, steps_per_inch, verbose)
            sleep(25)  # TODO base on speed, dist
        domove(S, sign(dist_inch)*r, bdir, bxy, steps_per_inch, verbose)
    else:
        domove(S, dist_inch, bdir, bxy, steps_per_inch, verbose)

    S.close()


def domove(S, dist_inch: float, bdir: bytes, bxy: bytes,
           steps_per_inch: int, verbose: bool):

    bstep = int2bytes(distinch2step(dist_inch, steps_per_inch, verbose))
# %% MOVE (no abort)
    movecmd = bRUN+bdir+bxy+bstep
    if verbose:
        print(f'moving {dist_inch} inch, sending {movecmd}')
    S.write(movecmd)


def int2bytes(n: int, byteorder: str='little') -> bytes:
    # cmdbytes= n.to_bytes((n.bit_length() // 8) + 1, byteorder=byteorder)
    cmdbytes = pack('<I', n)
    if n < 65536:
        cmdbytes = cmdbytes[:-2]
    else:
        raise NotImplementedError('more than 65535 steps not yet done')
        # tail = cmdbytes[-4:]
        # cmdbytes = cmdbytes[:-4] + tail[-2:] + tail[-4:-2]
    return cmdbytes


def distinch2step(dist_inch, steps_per_inch: int=10000,
                  verbose: bool=False) -> int:
    """
    verify steps per inch with your drive!!
    returns integer number of steps corresponding to inches requests.
    sign is handled in move function.
    """
    steps = int(round(abs(dist_inch) * steps_per_inch))
    if verbose:
        print(f'{steps} steps')
    return steps


def distcm2step(dist_cm: float, steps_per_inch: int=10000,
                verbose: bool=False) -> int:
    """
    verify steps per inch with your drive!!
    returns integer number of steps corresponding to centimeters requests.
    sign is handled in move function.
    """
    assert isinstance(steps_per_inch, int)
    steps = int(round(abs(dist_cm)/2.54 * steps_per_inch))
    if verbose:
        print(f'{steps} steps')
    return steps


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

    def open(self):
        pass

    def write(self, cmd: bytes):
        with self.f.open(self.pipefn, 'w') as f:
            f.write(str(cmd))

    def close(self):
        self.f.reset()
        print('simulation disconnect')
