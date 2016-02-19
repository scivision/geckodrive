#!/usr/bin/env python3
from numpy.testing import assert_allclose,run_module_suite
import pipes
#
from geckodrive.basic import *
#
bESTOP=b'\x00\00' #unverified
bSTOP= b'\x01\00'
bRUN = b'\x04\x00'
PORT='/dev/null' #always using simulated port for selftest

def test_stopdrive():
    S = Simport()
    stopdrive(S,PORT)
    with S.f.open('pipe','r') as f:
        assert f.read()==str(bSTOP)

def test_estopdrive(): #not physically tested
    S = Simport()
    estopdrive(S,PORT)
    with S.f.open('pipe','r') as f:
        assert f.read()==str(bESTOP)

def test_distcm2step():
    assert distcm2step(1, 10000) == 3937

def test_int2bytes():
    assert(int2bytes(n=4, byteorder='little')+
           int2bytes(n=0, byteorder='little')) == bRUN

def test_movedrive():
    S = Simport()
    movedrive(S, axis='x',dist_cm=1, steps_per_inch=10000)
    with S.f.open('pipe','r') as f:
        assert f.read()==str(b'\x04\x00\x00Aa\x0f')


if __name__ == '__main__':
    run_module_suite()
