#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zhuzhengwei'

from token import Token, TokenType

class AST(object):
    """ abstract syntax tree"""
    pass


class NumberNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return '{!r}'.foramt(self.value)

class StringNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return '{!r}'.format(self.value)


class IdentifierNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return '{!r}'.format(self.value)


class BinaryOpNode(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


    def __repr__(self):
        return '({!r} {!r} {!r})'.format(self.left, self.op.value, self.right)


class WhereNode(AST):
    def __init__(self, cond):
        self.cond = cond

    def __repr__(self):
        return '({!r})'.format(self.cond)


class OrderNode(AST):
    def __init__(self, field, order):
        self.field = field
        self.token = self.order = order
        self.asc = self.order.token_type = TokenType.T_ASC

    def __repr__(self):
        return '{!r} {!r}'.format(self.field, self.asc)


class LimitNode(AST):

    def __init__(self,
                 limit=Token(TokenType.T_NUMBER, 10),
                 offset=Token(TokenType.T_NUMBER, 0)):
        self.limit = limit
        self.offset = offset

    def __repr__(self):
        return '{!r} {!r}'.format(self.limit.value, self.offset.value)


class SelectNode(AST):

    def __init__(self, fields, table, where, order, limit):
        self.fields = fields
        self.table = table
        self.where = where
        self.order = order
        self.limit = limit


