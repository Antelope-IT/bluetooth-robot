#!/usr/bin/env python3
"""A module having the Main entry point for the robot

Usage:
    python3 main.py <device path = /dev/input/eventX> [-z|--zero]
"""
import argparse
import time
from signal import pause

from gpiozero import Robot
from gpiozero.pins.pigpio import PiGPIOFactory

from core.events import EventSource
from core.robot_control import RobotControl
from sensors.distance import ProximitySensor
from utils.utilities import print_event


def event_printer(config):
    path = config.device
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


def main(config):
    try:
        pin_factory = PiGPIOFactory() if config.zero else None
        proximity = ProximitySensor(safe_distance=10, pin_factory=pin_factory)
        robot = Robot(left=(10, 9), right=(8, 7), pin_factory=pin_factory)
        rc = RobotControl(config.device, fwd_sensor=proximity)
        robot.source = rc()
        pause()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print(f"{type(ex)}: {ex}")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A remote controlled robot rover')
    parser.add_argument('device', help='device is the path to a file like device of the form /dev/input/eventX where '
                                       'X is an integer. See the readme for help finding this value.')
    parser.add_argument('-z', '--zero', action='store_true', default=False,
                        help='The code is running on a piZero use the PiGPIO pin factory for improved performance.')
    args = parser.parse_args()
    if args.zero:
        import pigpio
        pi = pigpio.pi()
        if not pi.connected:
            print('Requested PiGPIO pin factory but PiGPIO daemon not started exiting...')
            exit(1)
    main(args)
