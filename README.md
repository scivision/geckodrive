[![image](https://travis-ci.org/scivision/geckodrive.svg?branch=master)](https://travis-ci.org/scivision/geckodrive)
[![image](https://coveralls.io/repos/github/scivision/geckodrive/badge.svg?branch=master)](https://coveralls.io/github/scivision/geckodrive?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/8244cc31073b44f253a9/maintainability)](https://codeclimate.com/github/scivision/geckodrive/maintainability)

# GeckoDrive GeckoMotion for Python 

An alternative servo motor control.

[GeckoDrive's](http://www.geckodrive.com/)
[GeckoMotion](http://www.geckodrive.com/support/geckomotion.html)
software seems very buggy on Windows 10. 
As a result the bytes sent by GeckoMotion to the GeckoDrive for various commands were inspected and this workaround program originated.

For your safety, do not use this code in any way where living things or
property or anything is at risk. 
There is no Emergency Stop facility in this code.

## Install

    pip install -e .

## Usage

    gogecko x 10

    gogecko y -8 

where the first argument is direction [x, y] and second number is
distance in centimeters (positive or negative)

### Other parameters

* `-s` steps per inch (verify for your drive! damage can result!) 
* `-a` acceleration for all axes 
* `-v` velocity for all axes

## Using from Matlab

Like usual, you can use the `system()` function to make movements from Matlab.

### Matlab usage example

From within Matlab:
```matlab
system('gogecko x 10')

system('gogecko y -8')
```

## TODO

-   Read Feedback from drive