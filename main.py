#!/usr/bin/env python3
"""A module having the Main entry point for the robot

Usage:
    python3 main.py <device path = /dev/input/eventX>
"""
import sys
import time
from events import EventSource
from utilities import print_event


def main(args):
    path = args[1]
    es = EventSource(path)
    try:
        while True:
            if es.is_connected:
                for e in es.events():
                    print_event(e)
            else:
                print('Not Connected')
                time.sleep(1)
    except KeyboardInterrupt:
        return
    except Exception as ex:
        print(f"{0}: {1}", type(ex), ex)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} /dev/input/eventX".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv)
