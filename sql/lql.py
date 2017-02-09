#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zhuzhengwei'

from parser import Parser
from semantic import Semantic
from errors import LQLError
from visitor import NodeVisitor
from ast import IdentifierNode
from . import get_possible_fields

from token import TokenType, Token

from operator import itemgetter

class LQL(NodeVisitor):

    def __init__(self, parser, logCollector):
        self.logCollector = logCollector
        self.parser = parser
        self.row_data = None


    def update_row_data(self,obj):
        data = {
            'time': obj.time.strftime('%Y-%m-%d %H:%M:%S'),
            'level': obj.level,
            'thread': obj.thread,
            'class': obj.clazz,
            'method': obj.method,
            'line': int(obj.line),
            'message': obj.message
        }

        self.row_data = data

    def walk(self, node, objects):
        limit = node.limit.limit.value
        offset = node.limit.offset.value
        n = 0
        rows = []

        header = [field.value for field in node.fields]
        header_lower = [field.lower() for field in header]

        for obj in objects:
            if limit != -1 and n >= limit:
                break

            self.update_row_data(obj)

            if node.where and not self.visit(node.where.cond):
                continue

            if offset:
                offset -= 1
                continue

            n += 1
            row = [self.row_data[field] for field in header_lower]
            rows.append(row)

        if node.order:
            i = header_lower.index(node.order.field.value.lower())
            rows.sort(key=itemgetter(i), reverse=not node.order.asc)

        return header, rows


    def visit_num(self, node):
        return node.value

    def visit_string(self, node):
        return node.value

    def visit_identifier(self, node):
        return self.row_data[node.value.lower()]

    def visit_unaryop(self, node):
        token_type = node.op.token_type
        if token_type == TokenType.T_NOT:
            return not self.visit(node.expr)
        else:
            # What's wrong...
            pass

    def visit_binop(self, node):
        op_funcs = {
            TokenType.T_AND: lambda x, y: x and y,
            TokenType.T_OR: lambda x, y: x or y,
            TokenType.T_EQ: lambda x, y: x == y,
            TokenType.T_NEQ: lambda x, y: x != y,
            TokenType.T_LT: lambda x, y: x < y,
            TokenType.T_LTE: lambda x, y: x <= y,
            TokenType.T_GT: lambda x, y: x > y,
            TokenType.T_GTE: lambda x, y: x >= y,
            TokenType.T_IN: lambda x, y: x in y
        }

        return op_funcs[node.op.token_type](self.visit(node.left),
                                            self.visit(node.right))

    def expandAsterisk(self,node):
        table = node.table.value
        possible_field_nodes  = [
            IdentifierNode(Token(TokenType.T_IDENTIFIER, f)) for f in get_possible_fields(table)
        ]

        for i, field in enumerate(node.fields):
            if field.token.token_type == TokenType.T_ASTERISK:
                node.fields[i:i+1] = possible_field_nodes
                return


    def visit_select(self, node):
        self.expandAsterisk(node)

        return self.walk(node, self.logCollector.loadData())

    def run(self):
        node = self.parser.parse()
        semantic = Semantic()
        err, msg = semantic.analysis(node)
        if err:
            raise LQLError(msg)

        return self.visit(node)

