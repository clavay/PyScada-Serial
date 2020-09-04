# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pyscada.serial.devices import GenericDevice
from pyscada.models import VariableProperty


class Handler(GenericDevice):
    """
    AirLink GX450 and other Devices with the same command set
    """

    def read_data(self, variable_instance):
        """
        read values from the device
        """
        if self.inst is None:
            return
        if variable_instance.serialvariable.device_property.upper() == 'POWERIN?':
            self.inst.write(str("AT*" + variable_instance.serialvariable.device_property.upper() + "\r\n").encode())
            return self.parse_value(str(self.inst.readall().decode()), variable_instance)
        elif variable_instance.serialvariable.device_property.upper() == 'BOARDTEMP?':
            self.inst.write(str("AT*" + variable_instance.serialvariable.device_property.upper() + "\r\n").encode())
            return self.parse_value(str(self.inst.readall().decode()), variable_instance)
        elif variable_instance.serialvariable.device_property.upper() == 'HWTEMP?':
            self.inst.write(str("AT*" + variable_instance.serialvariable.device_property.upper() + "\r\n").encode())
            return self.parse_value(str(self.inst.readall().decode()), variable_instance)
        elif variable_instance.serialvariable.device_property.upper() == 'NETRSSI?':
            self.inst.write(str("AT*" + variable_instance.serialvariable.device_property.upper() + "\r\n").encode())
            return self.parse_value(str(self.inst.readall().decode()), variable_instance)
        return None

    def write_data(self, variable_id, value, task):
        """
        write values to the device
        """
        variable = self._variables[variable_id]
        if task.property_name != '':
            # write the freq property to VariableProperty use that for later read
            vp = VariableProperty.objects.update_or_create_property(variable=variable, name=task.property_name.upper(),
                                                                    value=value, value_class='FLOAT64')
            return True
        if variable.serialvariable.variable_type == 0:  # configuration
            # only write to configuration variables
            pass
        else:
            return False

    def parse_value(self, value, variable_instance):
        """
        takes a string in the AirLink GX450 format and returns a float value or None if not parseable
        """
        try:
            value.replace(str("AT*" + variable_instance.serialvariable.device_property.upper() + "\r\n"), '')
            value.replace('\r\nOK\r\n', '')
            value.replace('\r', '')
            value.replace('\n', '')
            return float(value)
        except:
            return None
