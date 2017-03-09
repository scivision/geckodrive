#!/usr/bin/env python3
from setuptools import setup #enables develop

req = ['nose','pyserial','numpy']


#%% install
setup(name='geckodrive',
      packages=['geckodrive'],
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/geckodrive',
      description='control Geckodrive motion',
      install_requires=req,
	  )

