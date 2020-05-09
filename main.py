#!/usr/bin/env python3
"""A module having the Main entry point for the robot

Usage:
    python3 main.py <device path = /dev/input/eventX>
"""
import sys
import time
import argparse

from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.pins.native import NativeFactory

from core.robot_control import RobotControl
from core.events import EventSource
from sensors.distance import ProximitySensor
from utils.utilities import print_event
from gpiozero import Robot
from signal import pause


def event_printer(args):
    path = args[1]
    es = EventSource(path)
    while True:
        try:
            if es.is_connected:
                e = next(es.events())
                if e:
                    print_event(e)
            else:
                print('Not Connected')
                time.sleep(2)
        except KeyboardInterrupt:
            return
        except Exception as ex:
            print(f"{type(ex)}: {ex}")


def main(args):
    path = args.device
    onZero = args.zero
    pin_factory = PiGPIOFactory if onZero else NativeFactory()
    proximity = ProximitySensor(pin_factory=pin_factory)
    robot = Robot(left=(10, 9), right=(8, 7), pin_factory=pin_factory)
    rc = RobotControl(path, fwd_sensor=proximity)
    robot.source = rc()
    pause()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A remote controlled robot rover')
    parser.add_argument('device', help='device is the path to a file like device of the form /dev/input/eventX where '
                                       'X is an integer. See the readme for help finding this value.')
    parser.add_argument('-z', '--zero', action='store_true', default=False,
                        help='The code is running on a piZero use the PiGPIO pin factory for improved performance.')
    main(parser.parse_args())
