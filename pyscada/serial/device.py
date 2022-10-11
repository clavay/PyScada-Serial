# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import time, sleep

import sys

import logging

try:
    import serial
    driver_serial_ok = True
except ImportError:
    logger.error('Cannot import serial')
    driver_serial_ok = False

logger = logging.getLogger(__name__)
_debug = 1


class Device:
    """
    Serial device
    """

    def __init__(self, device):
        self.variables = {}
        self.device = device
        if self.device.serialdevice.instrument_handler is not None \
                and self.device.serialdevice.instrument_handler.handler_path is not None:
            sys.path.append(self.device.serialdevice.instrument_handler.handler_path)
        try:
            mod = __import__(self.device.serialdevice.instrument_handler.handler_class, fromlist=['Handler'])
            device_handler = getattr(mod, 'Handler')
            self._h = device_handler(self.device, self.variables)
            self.driver_handler_ok = True
        except ImportError:
            self.driver_handler_ok = False
            logger.error("Handler import error : %s" % self.device.short_name)

        for var in self.device.variable_set.filter(active=1):
            if not hasattr(var, 'serialvariable'):
                continue
            self.variables[var.pk] = var

        if driver_serial_ok and self.driver_handler_ok:
            # logger.error("serial connect")
            if not self._h.connect():
                sleep(60)
                self._h.connect()

    def request_data(self):

        output = []

        if not driver_serial_ok or not self.driver_handler_ok:
            return output

        for item in self.variables.values():
            value = self._h.read_data(item)

            if value is not None and item.update_value(value, time()):
                output.append(item.create_recorded_data_element())

        return output

    def write_data(self, variable_id, value, task):
        """
        write value to a Serial Device
        """

        output = []
        if not driver_serial_ok:
            logger.info("Cannot import serial")
            return output

        for item in self.variables:
            if item.id == variable_id:
                if not item.writeable:
                    return False
                read_value = self._h.write_data(variable_id, value, task)
                if read_value is not None and item.update_value(read_value, time()):
                    output.append(item.create_recorded_data_element())

        return output
