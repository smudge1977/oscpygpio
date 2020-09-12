#! /usr/bin/env python3
'''
Title:         check_ics_zones.py
Description:   Checks /dva/config/CurrentConfig.cfg to the ICS pcdva_config.xml
Author:        Keith Marston
Version:       1.3
Last Update:   26-07-20
Usage:         python3 ./check_ics_zones.py
                -q will only output errors

Look for # ** to find things to enhance!


dependancy 
sudo apt install python3-gpiozero
sudo pip3 install gpiozero
pip install rpi.gpio pigpio

pip install python-osc

'''


import argparse
import math
import logging
import time
import random

import RPi.GPIO as gpio

from pythonosc import udp_client
#from gpiozero import LED
from pythonosc import dispatcher
from pythonosc import osc_server
# from pythonosc import udp_client

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass


def gpio_set(*args):
    print('----')
    # logging.info('Setting pin', args[0], 'to ',args[1])
    # if not args[1]:
    #   # This all doesn't work at the moment!
    #   print('gpio set: "{}" value: "{}"'.format(args[0],'TOGGLE'))
    #   value = 'TOGGLE'
    #   # need a GPIO read to work out what to be!
    # else:
    #   value = args[1]
    value = args[1]
    pin = int(args[0].split('/')[-1])
    print('gpio set: "{}" value: "{}"'.format(pin,value))
    gpio.setup(pin, gpio.OUT)
    value = str(value).upper()
    if value in ('1','HIGH'):
      print('Setting HIGH')
      gpio.output(pin, gpio.HIGH)
      client.send_message('/style/text/0/20', ['HIGH'])
      client.send_message('/press/bank/1/6', 1) # sets the button - works
      #client.send_message('/style/bgcolor/bank/1/6', (255,255,255))
      client.send_message('/style/bgcolor/bank/1/6', [255,255,255])
      #client.send_message('/style/bgcolor/bank/1/6', "255 255 255")
      
      #client.send_message('/style/color/bank/1/6', (255,255,0))
      client.send_message('/style/color/bank/1/6', [99, 99, 99])
      client.send_message('/style/color/bank/1/6', [99., 99., 99.])
      client.send_message('/style/color/bank/1/6', ["99", "99", "99"])
      client.send_message('/press/bank/1/5', None) # taps the button - works
      client.send_message('/press/bank/1/6', 1) # sets the button - works
      client.send_message('/press/bank/1/6', 0) # sets the button - works

      client.send_message('/style/text/bank/1/6', "BUTTON TEXT")
      #client.send_message('/style/text/bank/1/6', "YO YO")
      #client.send_message('/style/text/bank/1/6', "YO YO")
    else:
      print('setting LOW')
      gpio.output(pin,gpio.LOW)
      client.send_message('/style/text/1/20', ['LOW'])
      client.send_message('/press/bank/1/6', 0) # sets the button - works
      client.send_message('/style/bgcolor/bank/1/6', (0,0,0))
    
    print('Pin: {} is set {}'.format(pin,gpio.input(pin)))
    client.send_message('/press/bank/1/5', None) # taps the button - works

    print('----')
          

if __name__ == "__main__":


  gpio.setmode(gpio.BCM) # Broadcom pin-numbering scheme
  
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="192.168.0.255", help="The ip to listen on (must be link local broadcast)")

  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  
  parser.add_argument("--replyport", type=int, default=12321,
      help="Companion control port - assumes on same network and that our IP is the link local broadcast")
  
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient("192.168.0.255", args.replyport)

  client.send_message('/style/color/bank/1/6', [99, 99, 99])
  client.send_message('/style/color/bank/1/6', [99., 99., 99.])
  client.send_message('/style/color/bank/1/6', ["99", "99", "99"])
  client.send_message('/press/bank/1/5', None) # taps the button - works
  client.send_message('/press/bank/1/6', 1) # sets the button - works
  client.send_message('/press/bank/1/6', 0) # sets the button - works

  dispatcher = dispatcher.Dispatcher()
  
  dispatcher.map("/gpio", print)
  dispatcher.map("/gpio/set", print)
  for i in range(0,20):
    dispatcher.map('/gpio/set/' + str(i), gpio_set)
    #PIN.set(i,'default')
    

  dispatcher.map("/filter", print)
  dispatcher.map("/volume", print_volume_handler, "Volume")
  dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  
  print('Server on {} bind {}'.format(server.server_address,server.server_bind))
  logging.info(str('Serving on {}'.format(server.server_address)))
  server.serve_forever()

