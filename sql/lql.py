#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zhuzhengwei'

from parser import Parse
from semantic import Semantic
from errors import LQLError
from visitor import NodeVisitor
from ast import IdentifierNode
from . import get_possible_fields

from token import TokenType, Token

class LQL(NodeVisitor):

    def __init__(self, parser):
        self.parser = parser


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

    def run(self):
        node = self.parser.parse()
        semantic = Semantic()
        err, msg = semantic.analysis(node)
        if err:
            raise LQLError(msg)

        self.visit(node)

