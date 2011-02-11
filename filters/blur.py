#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Blur filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''

class Blur:
    def blur(self):
        '''Simple blur'''

        self.box_blur(1, 1)
