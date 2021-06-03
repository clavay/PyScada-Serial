# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .. import PROTOCOL_ID
from pyscada.models import DeviceProtocol

try: 
    import serial
    driver_ok = True
except ImportError:
    serial = None
    driver_ok = False

from time import time

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

        if self._device.protocol.id != PROTOCOL_ID:
            logger.error("Wrong handler selected : it's for %s device while device protocol is %s" %
                         (str(DeviceProtocol.objects.get(id=PROTOCOL_ID)).upper(),
                          str(self._device.protocol).upper()))
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

    def before_read(self):
        """
        will be called before the first read_data
        """
        return None

    def after_read(self):
        """
        will be called after the last read_data
        """
        return None

    def read_data(self, variable_instance):
        """
        read values from the device
        """

        return None

    def read_data_and_time(self, variable_instance):
        """
        read values and timestamps from the device
        """

        return self.read_data(variable_instance), self.time()

    def write_data(self, variable_id, value, task):
        """
        write values to the device
        """
        return False

    def time(self):
        return time()
