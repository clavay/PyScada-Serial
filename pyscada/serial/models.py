# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyscada.models import Device
from pyscada.models import Variable

import serial

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import logging

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class SerialDevice(models.Model):
    serial_device = models.OneToOneField(Device, null=True, blank=True, on_delete=models.CASCADE)
    protocol_choices = ((0, 'serial AT'),)
    protocol = models.PositiveSmallIntegerField(default=0, choices=protocol_choices)
    port = models.CharField(default='/dev/ttyAMA0',
                            max_length=400,
                            help_text="enter serial port (/dev/pts/13))")
    timeout = models.PositiveSmallIntegerField(default=0, help_text="0 use default, else value in seconds")
    stopbits_choices = ((serial.STOPBITS_ONE, 'one stopbit'),
                        (serial.STOPBITS_ONE_POINT_FIVE, 'one point five stopbit'),
                        (serial.STOPBITS_TWO, '2 stopbits'),)
    stopbits = models.CharField(default=serial.STOPBITS_ONE, max_length=254, choices=stopbits_choices)
    bytesize_choices = ((serial.FIVEBITS, 'FIVEBITS'), (serial.SIXBITS, 'SIXBITS'),
                        (serial.SEVENBITS, 'SEVENBITS'), (serial.EIGHTBITS, 'EIGHTBITS'),)
    bytesize = models.CharField(default=serial.EIGHTBITS, max_length=254, choices=bytesize_choices)
    parity_choices = ((serial.PARITY_NONE, 'NONE'), (serial.PARITY_EVEN, 'EVEN'), (serial.PARITY_ODD, 'ODD'),
                      (serial.PARITY_MARK, 'MARK'), (serial.PARITY_SPACE, 'SPACE'),)
    parity = models.CharField(default=serial.PARITY_NONE, max_length=254, choices=parity_choices)
    baudrate = models.PositiveIntegerField(default=9600, help_text="0 use default")
    instrument = models.ForeignKey('SerialDeviceHandler', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.serial_device.short_name


@python_2_unicode_compatible
class SerialVariable(models.Model):
    serial_variable = models.OneToOneField(Variable, null=True, blank=True, on_delete=models.CASCADE)
    device_property = models.CharField(default='present_value', max_length=255,
                                       help_text='name of the Property the variable be assigned to')

    def __str__(self):
        return self.id.__str__() + "-" + self.serial_variable.short_name


@python_2_unicode_compatible
class SerialDeviceHandler(models.Model):
    name = models.CharField(default='', max_length=255)
    handler_class = models.CharField(default='pyscada.serial.devices.AirLinkGX450', max_length=255,
                                     help_text='a Base class to extend can be found at '
                                               'pyscada.serial.devices.GenericDevice')
    handler_path = models.CharField(default=None, max_length=255, null=True, blank=True, help_text='')  # todo help

    def __str__(self):
        return self.name


class ExtendedSerialDevice(Device):
    class Meta:
        proxy = True
        verbose_name = 'Serial Device'
        verbose_name_plural = 'Serial Devices'


class ExtendedSerialVariable(Variable):
    class Meta:
        proxy = True
        verbose_name = 'Serial Variable'
        verbose_name_plural = 'Serial Variables'
