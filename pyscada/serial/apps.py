# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PyScadaSerialConfig(AppConfig):
    name = 'pyscada.serial'
    verbose_name = _("PyScada Serial")
    path = os.path.dirname(os.path.realpath(__file__))

    def ready(self):
        import pyscada.serial.signals
