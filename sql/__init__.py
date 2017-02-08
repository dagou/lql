#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zhuzhengwei'

from termcolor import colored

__version__ = '1.0.0'


Tables = {
    'logs':[
        'time',
        'level',
        'thread',
        'class',
        'method',
        'line',
        'message'
    ]
}



def get_possible_fields(table):
    return Tables.get(table.lower(), [])


def show_all_tables():
    print('Tables: \n')
    for table, fields in Tables.items():
        print('{}'.format(table))
        print('\t{}.\n'.format(', '.join(fields)))

def red(s):
    return colored(s, 'red')


def bold(s):
    return colored(s, attrs=['bold'])