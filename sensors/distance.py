from gpiozero import DistanceSensor

pinTrigger = 17
pinEcho = 18


class ProximitySensor:
    """A wrapper class for the GPIOZero DistanceSensor class.

    Args:
        safe_distance: A minimum distance in 'cm' the sensor should consider safe to move default = 5cm
        send: The GPIO pin number the trigger signal is connected to default = pin 17
        receive: The GPIO pin number the echo return signal is connected to default = pin 18
        pin_factory: The pin factory to use for the GPIOZero device consider using the PiGPIO factory
                     when running on a PiZero for increased performance.
    """
    def __init__(self, safe_distance=5, send=pinTrigger, receive=pinEcho, pin_factory=None):
        self.sensor = DistanceSensor(echo=receive, trigger=send, pin_factory=pin_factory)
        self.limitDistance = safe_distance

    def safe(self):
        # Returns True if the sensors measured distance is greater than the configured safe distance
        return True if self.sensor.distance * 10 > self.limitDistance else False
