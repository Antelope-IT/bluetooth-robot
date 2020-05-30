from gpiozero import Button
from subprocess import check_call

pinShutdown = 13


def shutdown():
    check_call(['sudo', 'poweroff'])


class ShutdownSensor:

    def __init__(self, pin_trigger=pinShutdown, trigger_time=2,  pin_factory=None):
        self.callbacks = [];
        self.sensor = Button(pin_trigger, hold_time=trigger_time, pin_factory=pin_factory)
        self.sensor.when_held = self.safe_shutdown

    def subscribe(self, shutdown_callback):
        self.callbacks.append(shutdown_callback)

    def notify_shutdown(self):
        for cb in self.callbacks:
            if callable(cb):
                cb()

    def safe_shutdown(self):
        self.notify_shutdown()
        shutdown()
