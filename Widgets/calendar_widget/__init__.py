#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = '1.0'

import os

from kivy.resources import resource_add_path
resource_add_path(os.path.abspath(os.path.dirname(__file__)))

from .calendar_ui import Calendar, DatePicker # noqa
