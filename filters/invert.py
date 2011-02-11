#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Invert filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''

class Invert:
    def invert(self):
        '''Invert the colors of the image'''

        for y in xrange(0, self.height):
            for x in xrange(0, self.width):
                r, g, b = self.bitmap[y][x]
                self.bitmap[y][x] = (255-r, 255-g, 255-b)
