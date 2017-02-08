#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zhuzhengwei'

from . import red

class LQLError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return '{}: {}'.format(red('LQLError'), self.message)
