#!/usr/bin/env python
install_reuqires = ['pyserial','numpy']
tests_require = ['nose','coveralls']
# %%
from setuptools import setup,find_packages

setup(name='geckodrive',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      url='https://github.com/scivision/geckodrive',
      description='control Geckodrive motion',
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require},
      python_requires='>=3.6',
	  )

