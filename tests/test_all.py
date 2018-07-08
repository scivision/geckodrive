#!/usr/bin/env python
import pytest
import geckodrive as gecko

bESTOP = b'\x00\00'  # unverified
bSTOP = b'\x01\00'
bRUN = b'\x04\x00'
PORT = '/dev/null'  # always using simulated port for selftest


def test_stopdrive():
    S = gecko.Simport()

    gecko.stopdrive(S, PORT)

    with S.f.open(S.pipefn, 'r') as f:
        assert f.read() == str(bSTOP)


def test_estopdrive():  # not physically tested
    S = gecko.Simport()

    gecko.estopdrive(S, PORT)

    with S.f.open(S.pipefn, 'r') as f:
        assert f.read() == str(bESTOP)


def test_distcm2step():
    assert gecko.distcm2step(1, 10000) == 3937


def test_int2bytes():
    assert gecko.int2bytes(n=4, byteorder='little') == bRUN


def test_movedrive():
    S = gecko.Simport()

    gecko.movedrive(S, axis='x', dist_inch=1, steps_per_inch=10000)

    with S.f.open(S.pipefn, 'r') as f:
        assert f.read() == str(b"\x04\x00\x00A\x10'")


if __name__ == '__main__':
    pytest.main()
