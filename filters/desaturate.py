#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Desaturate filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''

class Desaturate:
    def desaturate(self):
        '''In other words, convert the image to gray scale'''

        for y in xrange(self.height):
            for x in xrange(self.width):
                r, g, b = self.bitmap[y][x]

                average = (r + g + b)/3

                self.bitmap[y][x] = average, average, average
