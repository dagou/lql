#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zhuzhengwei'

from . import red
from token import TokenType,Token
from errors import LQLError
import string


class Lexer(object):

    REVERSED_KEYWORDS = {
        'select': TokenType.T_SELECT,
        'from': TokenType.T_FROM,
        'where': TokenType.T_WHERE,
        'order': TokenType.T_ORDER,
        'by': TokenType.T_BY,
        'limit': TokenType.T_LIMIT,
        'offset': TokenType.T_OFFSET,
        'in': TokenType.T_IN,
        'desc': TokenType.T_DESC,
        'asc': TokenType.T_ASC,
        'and': TokenType.T_AND,
        'or': TokenType.T_OR,
        'not': TokenType.T_NOT
    }

    SINGLE_CHAR_TYPES = {
        '*': TokenType.T_ASTERISK,
        ',': TokenType.T_COMMA,
        ';': TokenType.T_SEMICOLON,
        '(': TokenType.T_LPARAN,
        ')': TokenType.T_RPARAN,
        '=': TokenType.T_EQ,
    }

    TWO_CHAR_TYPES = {
        '>': ('=', TokenType.T_GT, TokenType.T_GTE),
        '<': ('=', TokenType.T_LT, TokenType.T_LTE),
    }

    def __init__(self, s = ''):
        self.source = s  #源文件字符流
        self.source_len = len(s)
        self.pos = 0  #当前指针
        self.current_char = self.source[self.pos] if self.source_len > 0 else None

    # 判断文件是否结束
    def eof(self, pos=None):
        if pos is None:
            pos = self.pos
        return pos > self.source_len - 1


    #指针往前移动
    def forward(self):
        self.pos += 1
        if self.eof():
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]

    def peek(self):
        pos = self.pos + 1
        if self.eof(pos):
            return None
        else:
            return self.source[pos]

    #跳过空格
    def skip_whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.forward()

    def error(self):
        print('\t{}'.format(red(self.source)))
        print('\t{}^'.format(' ' * self.pos))
        raise LQLError('invalid character')


    #读取数字
    def integer(self):
        s = ''
        if self.current_char == '-':
            s += '-'
            self.forward()
            if not self.current_char.isdigit():
                self.error()

        while self.current_char is not None and self.current_char.isdigit():
            s += self.current_char
            self.forward()

        return Token(TokenType.T_NUMBER, int(s))

    #获取字符串
    def string(self):
        s = ''
        delimeter = self.current_char #左边引号
        self.forward()

        while self.current_char is not None and self.current_char != delimeter:
            if self.current_char == '\\':
                self.forward()
            s += self.current_char
            self.forward()

        if self.current_char != delimeter:
            self.error()

        self.forward()
        return Token(TokenType.T_STRING,s)


    def identifier(self):
        s = ''
        valid_chars = string.ascii_letters + '_'
        while self.current_char is not None and self.current_char in valid_chars:
            s += self.current_char
            self.forward()

        token_type = self.REVERSED_KEYWORDS.get(s.lower(),TokenType.T_IDENTIFIER)
        return Token(token_type,s)



    #获取next token
    def next_token(self):
        while self.current_char is not None:
            #空格
            if self.current_char.isspace():
                self.skip_whitespaces()
                continue
            elif self.current_char == '-' or self.current_char.isdigit():
                return self.integer()

            elif self.current_char == '\'' or self.current_char == '"':
                return self.string()
            elif self.current_char.isalpha():
                return self.identifier()
            elif self.current_char in self.SINGLE_CHAR_TYPES:
                c = self.current_char
                self.forward()
                return Token(self.SINGLE_CHAR_TYPES[c],c)

            elif self.current_char in self.TWO_CHAR_TYPES:
                c = self.current_char
                second_c, single_dt, double_dt = self.TWO_CHAR_TYPES[c]
                if self.peek() == second_c:
                    self.forward()
                    self.forward()
                    return Token(double_dt, c+second_c)
                else:
                    self.forward()
                    return Token(single_dt, c)
            elif self.current_char == '!':
                c = self.current_char
                if self.peek() == '=':
                    self.forward()
                    self.forward()
                    return Token(TokenType.T_NEQ)
                else:
                    return self.error()
            else:
                return self.error()

        return Token(TokenType.T_EOF, None)