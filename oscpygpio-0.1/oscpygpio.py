#! /usr/bin/env python3
'''
Title:         oscpygpio.py
Description:   OSC Implementation of GPIO control on the PI - design to work with companion as the OSC source
Author:        Keith Marston
Version:       1.0
Last Update:   13-09-20

Look for #* to find things to enhance!

Dependancies:
  sudo apt install python3-gpiozero
  sudo pip3 install gpiozero 
  pip install rpi.gpio pigpio # these should be on a PI anyway i beleive as standard packages
  pip install python-osc # the OSC package definatly will need installing

Need to: read response actions from config file

Good to: Listen on both broadcast and unicast - send response to jsut unicast 
  - event driven status updates will fix other companion instances been aware

Be nice to: makefile to install as a service etc. and then make into a deb package

Be nice to: dispatch gpio_read(pin) seperatly so after inital init compaion will follow actual pin states

'''


import argparse
#import math
import logging
#import time

import RPi.GPIO as gpio

from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

def gpio_read(pin,*args):
  ''' 
  Get value of requested pin and send back to ip of companion
  #* Would be nice to send back to the broadcast if sent to the broadcast and unicast if sent to the unicast address
  #* A) Don't know source address
  #* b) I am yet to get OSC client working with broadcast addressess
  '''
  logging.info('Get status of pin %i' % pin)
  client = udp_client.SimpleUDPClient("192.168.0.255", args_dict.get('replyport'), allow_broadcast=True)
  #* needs to be wrapped in a try!
  gpio.setup(pin, gpio.IN)
  pin_state = gpio.input(pin)
  #* needs to get the commands to send back from the config file.
  if pin_state == 1:
    value = '%i HIGH' % pin
    # client.send_message('/style/text/1/6', '%i HIGH' % pin)
    # client.send_message('/press/bank/1/6', 0) # sets the button - works
    # client.send_message('/style/bgcolor/1/6', [20,20,20])
    # client.send_message('/style/color/1/6', [180,180,180])
  elif pin_state == 0:
    value = '%i LOW' % pin
    # client.send_message('/style/text/1/6', '%i LOW' % pin)
  else:
    logging.critical(str('pin: "{}", pin_state: "{}", message: "UNKOWN STATE!! "'.format(pin, pin_state)))
  destination = '/style/text/1/6'
  client.send_message(destination, value)
  logging.info(str('response sent to: "{}", value: "{}"'.format(destination, value)))

def gpio_set(*args):
  # who did we get dispatcher by?
  # this will become a question if we haev a listener on the broadcast and the unicast address
  logging.debug(str('{} was recipient of {}'.format(server.server_address, args)))
  #* Whole bunch a error catching potentially here?
  value = args[1]
  pin = int(args[0].split('/')[-1])
  gpio.setup(pin, gpio.OUT)
  value = str(value).upper()
  if value in ('1','HIGH'):
    gpio.output(pin, gpio.HIGH)
    logging.info(str('pin: "{}", set: "HIGH", by: "{}", with: "{}"'.format(pin, server.server_address, args)))
  else:
    gpio.output(pin,gpio.LOW)
    logging.info(str('pin: "{}", set: "LOW", by: "{}", with: "{}"'.format(pin, server.server_address, args)))
  #* the read maybe eventually on another thread triggered by PIN state changes
  #* the then means companion STATE gets updated to reflect real world
  gpio_read(pin)       

if __name__ == "__main__":
  # What things have we been told on the command line?
  parser = argparse.ArgumentParser()
  parser.add_argument('--ip', default='192.168.0.255', 
    help='OSC Listen IP - #* Improve to look at local link broadcast address and listen on both broadcast and unicast')
  parser.add_argument('--port', type=int, default=5005, 
    help="The port to listen on")
  parser.add_argument('--replyport', type=int, default=12321,
    help='Companion control port - not really any point to this switch as companion has a fixed listen port')
  parser.add_argument('--companion', default='192.168.0.81',
    help='Companion IP - this is for sending back the OSC to give feed back #* would be nice to know the source of the OSC and just send back to that rather than specify')
  parser.add_argument('--config', default='oscpygpio.conf', 
    help='config from a file - #* too be implemented')
  parser.add_argument('--log', default='DEBUG',
    help='Set log level i.e. DEBUG or INFO - INFO would seem sencible for normal systemctl running')
  args = parser.parse_args()
  args_dict = dict((k,v) for k,v in vars(args).items())

  # First setup logger
  numeric_level = getattr(logging, args.log.upper(), None)
  if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
  logging.basicConfig(level=numeric_level)

  logging.debug('Set GPIO to BCM mode')
  gpio.setmode(gpio.BCM) # Broadcom pin-numbering scheme

  dispatcher = dispatcher.Dispatcher()
  #* This is crude - create a dispatcher for configured pins from the config file
  # This also potentially prevents clashes with other things using the GPIO on your PI
  for i in range(0,20):
    gpio_read(i) # get actual state to bring companion in line with current state on startup.
    dispatcher.map('/gpio/set/' + str(i), gpio_set)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  logging.warning('Config is:%s' % str(args_dict))
  logging.info('Server listening on:%s' % str(server.server_address))
  server.serve_forever()

