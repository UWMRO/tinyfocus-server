#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: arduino_connection.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import serial


DEV = "/dev/serial/by-id/usb-Arduino_Srl_Arduino_Uno_8543931313035131F0F0-if00"


class FocusArduinoConnection:
    """A connection to the focuser arduino. It connects and calls the real arduino."""

    def __init__(self):
        self.serial = serial.Serial(DEV, baudrate=9600, timeout=1)

    async def status(self):
        if not self.serial.is_open:
            self.serial.open()

        self.serial.write(b"status\n")

        return self.serial.readline().decode()

    async def move_steps(self, num_steps: int):
        if not self.serial.is_open:
            self.serial.open()

        self.serial.write(f"move?steps={num_steps}\n".encode("utf-8"))

        for _ in range(30):
            response = self.serial.readline()
            if response.decode() == "":
                continue
            return response.decode()

        return "ERROR"
