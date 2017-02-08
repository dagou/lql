#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhuzhengwei'

class Semantic(object):

    def check_table(self, node):
        return

    def check_fields(self, node):
        return

    def check_where(self, node):
        return

    def check_order(self, node):
        return

    def check_limit(self, node):
        return


    def analysis(self,node):
        checkers = (self.check_table,self.check_fields, self.check_where,
                    self.check_order,self.check_limit)

        for check in checkers:
            err_msg = check(node)
            if err_msg:
                return True, err_msg

        return False, None