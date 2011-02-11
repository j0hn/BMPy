#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Detect edges filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''

class DetectEdges:
    def detect_edges(self):
        '''Highlights image edges'''

        conv_matrix = [[-1,  -1,  -1],
                       [-1,   8,  -1],
                       [-1,  -1,  -1]]

        conv_matrix_height = 3
        conv_matrix_width = 3

        new_bitmap = self.bitmap[:]
        for y in range(len(self.bitmap)):
            new_bitmap[y] = self.bitmap[y][:]

        for y in xrange(1, self.height-1):
            for x in xrange(1, self.width-1):
                r, g, b = 0, 0, 0

                for y2 in xrange(conv_matrix_height):
                    for x2 in xrange(conv_matrix_width):
                        r += self.bitmap[y-(y2-1)][x-(x2-1)][0]*conv_matrix[y2][x2]
                        g += self.bitmap[y-(y2-1)][x-(x2-1)][1]*conv_matrix[y2][x2]
                        b += self.bitmap[y-(y2-1)][x-(x2-1)][2]*conv_matrix[y2][x2]

                new_bitmap[y][x] = (r, g, b)

        self.bitmap = new_bitmap
