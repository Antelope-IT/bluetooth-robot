#!/usr/bin/env python3
"""A module for connecting to input devices.

Usage:
    python3 device-connector.py <device path = /dev/input/eventX>
"""
import sys
import time
import libevdev
import fcntl
import os

def print_event(e):
    """A utility function for printing event details.

    Args:
        e: The event to print out.
    """
    print("Event: time {}.{:06d}, ".format(e.sec, e.usec), end='')
    if e.matches(libevdev.EV_SYN):
        if e.matches(libevdev.EV_SYN.SYN_MT_REPORT):
            print("++++++++++++++ {} ++++++++++++".format(e.code.name))
        elif e.matches(libevdev.EV_SYN.SYN_DROPPED):
            print(">>>>>>>>>>>>>> {} >>>>>>>>>>>>".format(e.code.name))
        else:
            print("-------------- {} ------------".format(e.code.name))
    else:
        print("type {:02x} {} code {:03x} {:20s} value {:4d}".format(e.type.value, e.type.name, e.code.value, e.code.name, e.value))


def device_connector(path, blocking = False):
    """A generator function yielding an infinite set of Input device objects.
    A new device object is returned each time the device connects or reconnects
    
    Args:
        path: A path for file like object of the form /dev/input/eventX
        blocking: 

    Yields:
        An Input Device for path specified as the argument. 
    """

    connected = False
    allowedToConnect = True
    connect_retry_delay = 5
    
    while allowedToConnect:
        try:
            with open(path, "rb") as fd:
                connected = True
                print(f"Connected to device {path}.")
                dev = libevdev.Device(fd)
                if blocking:
                    fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
                yield dev
                print(f"Finished with device {path}.")
        except KeyboardInterrupt:
            allowedToConnect = False
        except IOError as e:
            import errno
            if e.errno == errno.EACCES:
                print(f"Insufficient permissions to access {path}.")
                allowedToConnect = False
            elif e.errno == errno.ENOENT:
                if connected:
                    print(f"Device {path} disconected.")
                    connected = False
                else:
                    print(f"Waiting to connect to {path}.")
            else:
                raise e
        # Delay before trying to connect again
        if allowedToConnect:
            time.sleep(connect_retry_delay)
               
    return

            
def device_events(path, blocking = False):
    try:
        for dev in device_connector(path, blocking):          
            haveDevice = True
            
            while haveDevice:
                try:
                    for e in dev.events():
                        yield e
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

        
