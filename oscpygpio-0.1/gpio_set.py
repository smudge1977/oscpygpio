#!/bin/python
import argparse
import math
import logging
import RPi.GPIO as gpio
import time





        

if __name__ == "__main__":


  gpio.setmode(gpio.BCM)
  gpio.setup(18, gpio.OUT)
  gpio.output(18, gpio.LOW)
  gpio.output(18, gpio.HIGH)
