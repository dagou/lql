#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zhuzhengwei'

from errors import LQLError

from ast import SelectNode
from token import TokenType

class Parse(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def error(self, expect):
        message = 'Got {!r} while expect {!r}.'.format(
            self.current_token.token_type.name, expect.name)
        raise LQLError(message)

    def select(self):


        return

    def parse(self):
        self.current_token = self.lexer.next_token()

        node = self.select() #构造sql syntax tree

        if self.current_token.token_type != TokenType.T_EOF:
            self.error(TokenType.T_EOF)

        return node

