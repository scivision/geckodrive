#!/usr/bin/env python
req = ['nose','pyserial','numpy']

import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception:
    pip.main(['install'] + req)
# %%
from setuptools import setup #enables develop


#%% install
setup(name='geckodrive',
      packages=['geckodrive'],
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/geckodrive',
      description='control Geckodrive motion',
      install_requires=req,
	  )

