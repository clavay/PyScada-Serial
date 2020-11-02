# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try: 
    import serial
    driver_ok = True
except ImportError:
    serial = None
    driver_ok = False

import logging

logger = logging.getLogger(__name__)


class GenericDevice:
    def __init__(self, pyscada_device, variables):
        self._device = pyscada_device
        self._variables = variables
        self.inst = None
        self.rm = None

    def connect(self):
        """
        establish a connection to the Instrument
        """
        if not driver_ok:
            logger.error("Cannot import serial")
            return False

        try:
            self.inst = serial.Serial(port=self._device.serialdevice.port,
                                      baudrate=self._device.serialdevice.baudrate,
                                      bytesize=self._device.serialdevice.bytesize,
                                      parity=self._device.serialdevice.parity,
                                      stopbits=self._device.serialdevice.stopbits,
                                      timeout=self._device.serialdevice.timeout,
                                      write_timeout=self._device.serialdevice.timeout)
        except serial.serialutil.SerialException as e:
            logger.debug(e)
            return False

        logger.debug('Connected to serial device : %s' % self.__str__())
        return True

    def disconnect(self):
        if self.inst is not None:
            self.inst.close()
            self.inst = None
            return True
        return False

    def read_data(self, variable_instance):
        """
        read values from the device
        """

        return None

    def write_data(self, variable_id, value, task):
        """
        write values to the device
        """
        return False
