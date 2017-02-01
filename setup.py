#!/usr/bin/env python3
from setuptools import setup #enables develop
try:
    import conda.cli
    conda.cli.main('install','--file','requirements.txt')
except Exception as e:
    print(e)


#%% install
setup(name='geckodrive',
      packages=['geckodrive'],
	  )

