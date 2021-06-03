# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pyscada

__version__ = '0.7.0rc18'
__author__ = 'Camille Lavayssière'

default_app_config = 'pyscada.serial.apps.PyScadaSerialConfig'

PROTOCOL_ID = 93

parent_process_list = [{'pk': PROTOCOL_ID,
                        'label': 'pyscada.serial',
                        'process_class': 'pyscada.serial.worker.Process',
                        'process_class_kwargs': '{"dt_set":30}',
                        'enabled': True}]
