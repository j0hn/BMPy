#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Sepia filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''

class Sepia:
    def sepia(self):
        '''Transform the image colors to a sepia scale'''

        for y in xrange(self.height):
            for x in xrange(self.width):
                r, g, b = self.bitmap[y][x]

                nr = r*0.393 + g*0.769 + b*0.189
                ng = r*0.349 + g*0.686 + b*0.168
                nb = r*0.272 + g*0.534 + b*0.131

                self.bitmap[y][x] = int(nr), int(ng), int(nb)
