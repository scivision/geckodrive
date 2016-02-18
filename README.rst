=============================================================
GeckoDrive GeckoMotion Python alternative servo motor control
=============================================================

`GeckoDrive's <http://www.geckodrive.com/>`_ `GeckoMotion <http://www.geckodrive.com/support/geckomotion.html>`_ software seems very buggy on Windows 10.
As a result the bytes sent by GeckoMotion to the GeckoDrive for various commands were inspected and this workaround program originated.

For your safety, do not use this code in any way where living things or property or anything is at risk. 
There is no Emergency Stop facility in this code.

Prereq
======
This program is designed for Python >= 3.5, which can be obtained via::

  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
  bash Miniconda3*.sh


Install
=======
::

  python setup.py develop
  
Usage
=====
::

  ./geckorun.py 
  
-d    \+ or - direction along your axis to move
-y    move the second drive (for systems with two GM215 tied together)
