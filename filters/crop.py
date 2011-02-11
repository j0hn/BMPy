#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Crop filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''


class Crop:
    def crop(self, start_x, start_y, end_x, end_y):
        '''Crops the image to the rectangle formed by
        the points (start_x, start_y) and (end_x, end_y)'''

        self.width = end_x - start_x
        self.height = end_y - start_y

        self.bitmap = self.bitmap[start_y:end_y]
        for y in range(len(self.bitmap)):
            self.bitmap[y] = self.bitmap[y][start_x:end_x]
