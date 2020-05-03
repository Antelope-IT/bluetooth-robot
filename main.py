#!/usr/bin/env python3
"""A module having the Main entry point for the robot

Usage:
    python3 main.py <device path = /dev/input/eventX>
"""
import sys
import time
from core.robot_control import RobotControl
from core.events import EventSource
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
    path = args[1]
    robot = Robot(left=(9, 10), right=(7, 8))
    rc = RobotControl(path)
    robot.source = rc()
    pause()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} /dev/input/eventX".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv)
