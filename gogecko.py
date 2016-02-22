#!/usr/bin/env python3
"""
use this program at your own risk. no emergency stop.
Python 3
"""
#
from geckodrive.basic import connectdrive, configdrive, movedrive

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='GeckoDrive GM215 Motion control code')
    p.add_argument('axis',help='x or y')
    p.add_argument('dist_inch',help=' +/-distance in inches to move',type=float)
    p.add_argument('-s','--stepsperinch',help='steps per inch for your system',type=int,default=10000)
    #p.add_argument('-a','--accel',help='acceleration of movements (dont jerk the load)',type=int,default=5)
    #p.add_argument('-v','--vel',help='velocity of movements',type=int,default=100)
    p.add_argument('-p','--port',help='RS485 adapter port',default='/dev/ttyUSB0')
    p.add_argument('-v','--verbose',help='debug',action='store_true')
    p = p.parse_args()

    try:
        S = connectdrive(p.port)

        configdrive(S,p.port)

        movedrive(S,p.axis,p.dist_inch,p.stepsperinch,p.port,p.verbose)
    except KeyboardInterrupt:
        pass
#    finally:
#        stopdrive(S,p.port)
#        print('Disconnect')
#       S.close()
