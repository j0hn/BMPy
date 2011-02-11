#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Mosaic filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''


class Mosaic:
    def mosaic(self, mosaic_size):
        '''Pixelate the image with block size of mosaic_size'''

        mid = mosaic_size/2

        for y in xrange(0, self.height, mosaic_size):
            for x in xrange(0, self.width, mosaic_size):
                ex = min(x + mosaic_size, self.width)
                ey = min(y + mosaic_size, self.height)

                ypos = min(y + mid, self.height-1)
                xpos = min(x + mid, self.width-1)
                color = self.bitmap[ypos][xpos]
                self.draw_rect(color, x, y, ex, ey)
