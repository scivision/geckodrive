#!/usr/bin/env python3
"""
use this program at your own risk. no emergency stop.
Python >=3.5
"""
from geckodrive.basic import connectdrive, configdrive, movedrive

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='GeckoDrive GM215 Motion control code')
    p.add_argument('--steps',help='(default 1cm) number of steps to move on each cmd',type=int,
                   default=int(10000/2.54))
    p.add_argument('-d','--dir',help='+ fwd, - rev',default='+')
    p.add_argument('-y','--y',help='move in y (2nd axis of slaved GM215 pair)',action='store_true')
    p.add_argument('-p','--port',help='port RS485 USB adapter is on',default='/dev/ttyUSB0')
    p.add_argument('-a','--accel',help='acceleration of movements (dont jerk the load)',type=int,default=10)
    p.add_argument('-v','--vel',help='velocity of movements',type=int,default=100)
    p = p.parse_args()

    try:
        S = connectdrive(p.port)

        configdrive(S,p.accel,p.vel)

        movedrive(S,p.steps,p.dir,p.y)
    except KeyboardInterrupt:
        pass
    finally:
        print('Disconnect')
        S.close()