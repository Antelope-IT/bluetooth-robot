import math

import libevdev

from collections import namedtuple
from core.events import EventSource
from utils.utilities import print_event

Command = namedtuple('Command', ['forward', 'reverse', 'left_turn', 'right_turn'])


def clamped(value, limit=1):
    return max(-1 * limit, min(limit, value))


def calculate_drive(speed, heading, fwd_safe, fwd_proximity):
    if speed > 0:
        slow = fwd_proximity if fwd_safe else 0
        left = slow * (speed if heading < 0 else math.sqrt(heading ** 2 + speed ** 2))
        right = slow * (speed if heading > 0 else math.sqrt(heading ** 2 + speed ** 2))
    elif speed == 0:
        if fwd_safe:
            left = 0 if heading < 0 else heading
            right = 0 if heading > 0 else heading
        else:
            right = 0 if heading < 0 else -1 * heading
            left = 0 if heading > 0 else -1 * heading
    else:
        right = speed if heading < 0 else -1 * math.sqrt(heading ** 2 + speed ** 2)
        left = speed if heading > 0 else -1 * math.sqrt(heading ** 2 + speed ** 2)
    return clamped(left), clamped(right)


def adjust_bias(left, right, bias):
    if bias > 0:
        right = right * (1 - bias)
    elif bias < 0:
        left = left * (1 + bias)
    return left, right


class RobotControl:

    def __init__(self, path, bias=0, max_speed=1, fwd_sensor=None):
        self.eventSource = EventSource(path)
        self.max_speed = max_speed
        self.fwd_sensor = fwd_sensor
        self.speed = 0
        self.heading = 0
        self.bias = bias
        self.bias_adjust = 1 / 32
        self.sensitivity = 1 / 16
        self.slow = 1 / 8
        self.left = False
        self.right = False
        self.forward = False
        self.reverse = False

    def __call__(self, *args, **kwargs):
        while True:
            if self.fwd_sensor is not None:
                fwd_safe, fwd_proximity = self.fwd_sensor.proximity()
            else:
                fwd_safe = True
                fwd_proximity = 1

            if self.eventSource.is_connected:
                try:
                    ev = next(self.eventSource.events())
                    if ev is not None:
                        command = self._decode_event(ev)
                    else:
                        command = Command(self.forward, self.reverse, self.left, self.right)
                    self._update_state(command)

                    if self.speed > 0 and not fwd_safe:
                        self.reset()
                except KeyboardInterrupt:
                    pass
                except Exception as ex:
                    print(f"{type(ex)}: {ex}")
                    self.reset()
            else:
                self.reset()
            left, right = adjust_bias(*calculate_drive(self.speed, self.heading, fwd_safe, fwd_proximity), self.bias)
            print(f'left: {left}, right: {right}')
            yield left, right

    def reset(self):
        self.forward = False
        self.reverse = False
        self.left = False
        self.right = False
        self.speed = 0
        self.heading = 0

    def _update_state(self, command):

        if command is None:
            self.reset()
        else:
            speed_increment = abs(self.speed) * self.sensitivity if abs(
                self.speed) > self.sensitivity else self.sensitivity
            heading_increment = abs(self.heading) * self.sensitivity if abs(
                self.heading) > self.sensitivity else self.sensitivity
            if command.forward or command.reverse:
                self.speed += speed_increment if command.forward and self.speed < 1 else 0
                self.speed -= speed_increment if command.reverse and self.speed > -1 else 0
            else:
                self.speed -= self.speed * self.slow
                if abs(self.speed) < self.sensitivity:
                    self.speed = 0

            if command.left_turn or command.right_turn:
                self.heading += heading_increment if command.right_turn and self.heading < 1 else 0
                self.heading -= heading_increment if command.left_turn and self.heading > -1 else 0
            else:
                self.heading -= self.heading * self.slow
                if abs(self.heading) < self.sensitivity:
                    self.heading = 0

    def _decode_event(self, event):
        if event is None:
            return

        if event.matches(libevdev.EV_ABS.ABS_HAT0X):
            # Left and Right
            # e.value 1 => Right
            # e.value 0 => TurnReleased
            # e.value -1 => Left
            self.left = False
            self.right = False
            if event.value > 0:
                self.right = True
            elif event.value < 0:
                self.left = True
        elif event.matches(libevdev.EV_ABS.ABS_HAT0Y):
            # Forward and Reverse
            # e.value 1 => Backward
            # e.value 0 => DriveReleased
            # e.value -1 => Forward
            self.forward = False
            self.reverse = False
            if event.value > 0:
                self.reverse = True
            elif event.value < 0:
                self.forward = True
        elif event.matches(libevdev.EV_KEY.BTN_Z):
            # RT
            # e.value 1 => Pressed
            # e.value 0 => Release
            if event.value == 1:
                self.bias -= self.bias_adjust
        elif event.matches(libevdev.EV_KEY.BTN_WEST):
            # LT
            # e.value 1 => Pressed
            # e.value 0 => Release
            if event.value == 1:
                self.bias += self.bias_adjust
        elif event.matches(libevdev.EV_KEY.BTN_SOUTH):
            # B
            # All Stop
            if event.value == 1:
                self.reset()
        else:
            print_event(event)

        return Command(self.forward, self.reverse, self.left, self.right)
