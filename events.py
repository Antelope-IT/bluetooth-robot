""" A module containing The EventSource class

Ussage:
    None.
"""
import libevdev
from device_connector import device_connector


class EventSource:
    """A configurable event source class

    Args:
        path: A path for file like object of the form /dev/input/eventX
        blocking: An optional boolean when set causes the script to wait (block)
                  until the next event is emitted. The default value is false (non blocking).
    """
    def __init__(self, path, blocking=False):
        self._path = path
        self._connected = False
        self._blocking = blocking
        self._connector = device_connector(self._path, self._blocking)
        self._dev = None

    @property
    def is_connected(self):
        """Get the connected state of the event source. If not connect attempts to connect."""
        while not self._connected:
            try:
                self._dev = next(self._connector, None)
                if self._dev is None:
                    self._connected = False
                    self._connector = device_connector(self._path, self._blocking)
                    break

                self._connected = True
            except StopIteration:
                if not self._blocking:
                    break

        return self._connected

    def events(self):
        """A generator a function which yields an infinite sequence of InputsEvents
           from the device as long as it is connected."""
        try:
            while self.is_connected:
                try:
                    for e in self._dev.events():
                        yield e
                except libevdev.EventsDroppedException:
                    for e in self._dev.sync():
                        yield e
                except KeyboardInterrupt:
                    break
            return

        except OSError as ex:
            import errno
            if ex.errno == errno.ENODEV:
                self._connected = False

        return
