#!/usr/bin/env python3
"""A module for connecting to input devices.

Usage:
    python3 device_connector.py <device path = /dev/input/eventX>
"""
import sys
import time
import libevdev
import fcntl
import os

from libevdev import InputEvent
from utils.utilities import print_event


def device_connector(path, blocking=True):
    """A generator function yielding an infinite set of Input device objects.
    A new device object is returned each time the device connects or reconnects
    
    Args:
        path: A path for file like object of the form /dev/input/eventX
        blocking: An optional boolean when set causes the script to wait (block)
                  until the next event is emitted. The default value is True (blocking).

    Yields:
        An InputDevice specified by the path argument. 
    """
    connected = False
    allowedToConnect = True
    connect_retry_delay = 5

    while allowedToConnect:
        try:
            with open(path, "rb") as fd:
                connected = True
                print(f"Connected to device {path}.")
                if not blocking:
                    fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)

                dev = libevdev.Device(fd)
                yield dev
                print(f"Finished with device {path}.")
        except KeyboardInterrupt:
            allowedToConnect = False
        except IOError as e:
            import errno
            if e.errno == errno.EACCES:
                print(f"Insufficient permissions to access {path}.")
            elif e.errno == errno.ENOENT:
                if connected:
                    print(f"Device {path} disconnected.")
                    connected = False
                else:
                    print(f"Waiting to connect to {path}.")
            else:
                raise e
        # Delay before trying to connect again
        if not blocking:
            break

        if allowedToConnect:
            time.sleep(connect_retry_delay)

    return


def device_events(path, blocking=True):
    """A generator function yielding an infinite set of
    InputDevice events

    Args:
        path: A path for file like object of the form /dev/input/eventX
        blocking: An optional boolean when set causes the script to wait (block)
                  until the next event is emitted. The default value is True (blocking).
                  
    Yields:
        InputEvents from the InputDevice specified by the path argument. 
    """
    try:
        for dev in device_connector(path, blocking):
            haveDevice = True
            while haveDevice:
                haveEvent = False
                try:
                    e: InputEvent
                    for e in dev.events():
                        haveEvent = True
                        yield e
                    if haveEvent is False:
                        print('Connected No Events')
                        time.sleep(0.1)
                except libevdev.EventsDroppedException:
                    for e in dev.sync():
                        yield e
                except KeyboardInterrupt:
                    return
                except:
                    haveDevice = False

    except:
        return


def main(args):
    path = args[1]
    for e in device_events(path):
        print_event(e)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} /dev/input/eventX".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv)
