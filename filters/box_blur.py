#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Box Blur filter

Author: j0hn <j0hn.com.ar@gmail.com>
        Andruli <andresb9163@gmail.com>
'''

import random

class BoxBlur:
    def box_blur(self, box_width, box_height, fuzzy=False):
        '''More advance blur where you can specify a box
        where the blur takes information from

        fuzzy effect makes a noizy blur distort'''

        copy = self.bitmap[::]

        for y in xrange(0, self.height):
            for x in xrange(0, self.width):
                average = self._box_blur_average(x, y, box_width,
                                                 box_height, copy, fuzzy)
                self.bitmap[y][x] = average

    def _box_blur_average(self, x, y, bw, bh, copy, fuzzy=False):
        blimit1 = (max(0, x-bw), max(0, y-bh))
        blimit2 = (min(self.width-1, x + bw), min(self.height-1, y + bh))

        if fuzzy:
            total = self.bitmap[random.randint(blimit1[1],
                blimit2[1])][random.randint(blimit1[0], blimit2[0])]
        else:
            total = (0, 0, 0)
            for y in xrange(blimit1[1], blimit2[1]+1):
                for x in xrange(blimit1[0], blimit2[0]+1):
                    r, g, b = copy[y][x]
                    total = total[0]+r, total[1]+g, total[2]+b

            area = (blimit2[0]-blimit1[0]+1)*(blimit2[1]-blimit1[1]+1)
            total = total[0]/area, total[1]/area, total[2]/area

        return total
