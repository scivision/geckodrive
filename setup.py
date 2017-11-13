#!/usr/bin/env python
req = ['nose','pyserial','numpy']
# %%
from setuptools import setup #enables develop

setup(name='geckodrive',
      packages=['geckodrive'],
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/geckodrive',
      description='control Geckodrive motion',
      install_requires=req,
      python_requires='>=3.6',
	  )

