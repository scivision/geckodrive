=============================================================
GeckoDrive GeckoMotion Python alternative servo motor control
=============================================================

`GeckoDrive's <http://www.geckodrive.com/>`_ `GeckoMotion <http://www.geckodrive.com/support/geckomotion.html>`_ software seems very buggy on Windows 10.
As a result the bytes sent by GeckoMotion to the GeckoDrive for various commands were inspected and this workaround program originated.

For your safety, do not use this code in any way where living things or property or anything is at risk. 
There is no Emergency Stop facility in this code.

.. contents::

Prereq
======
This program is designed for Python >= 3.5, which can be obtained via::

  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
  bash Miniconda3*.sh


Install
=======
::

  git clone https://github.com/scivision/geckodrive/
  python3 setup.py develop
  
Usage Examples
==============
::

  ./gogecko.py x 10
  
  ./gogecko.py y -8 
  
where the first argument is direction [x,y] and second number is distance in centimeters (positive or negative)

Other parameters
----------------
-s    steps per inch (verify for your drive! damage can result!)
-a    acceleration for all axes
-v    velocity for all axes

Using from Matlab
=================
Like usual, you can use the ``system()`` function to make movements from Matlab. 

Matlab usage example
--------------------
From within Matlab::

  system('python3 gogecko.py x 10')
  
  system('python3 gogecko.py y -8')
