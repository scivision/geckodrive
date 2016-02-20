#!/usr/bin/env python3

from geckodrive import connectdrive,configdrive

S=connectdrive()
configdrive(S)

S.write(b'\x04\x00\x00\x01'
