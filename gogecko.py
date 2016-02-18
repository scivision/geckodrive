#!/usr/bin/env python3
"""
use this program at your own risk. no emergency stop.
Python >=3.5
"""
from geckodrive.basic import connectdrive, configdrive, movedrive

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='GeckoDrive GM215 Motion control code')
    p.add_argument('axis',help='x or y')
    p.add_argument('dist',help=' +/-distance in centimeters to move',type=float)
    p.add_argument('-s','--stepsperinch',help='steps per inch for your system',type=int,default=10000)
    p.add_argument('-a','--accel',help='acceleration of movements (dont jerk the load)',type=int,default=5)
    p.add_argument('-v','--vel',help='velocity of movements',type=int,default=100)
    p = p.parse_args()

    try:
        S = connectdrive(p.port)

        configdrive(S,p.accel,p.vel,p.port)

        movedrive(S,p.axis,p.dist,p.stepsperinch,p.port)
    except KeyboardInterrupt:
        pass
    finally:
        print('Disconnect')
        S.close()
