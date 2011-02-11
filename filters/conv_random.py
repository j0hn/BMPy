#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Random filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''

from random import randint

class ConvRandom:
    def conv_random(self):
        '''WHO KNOWS?!?!!11one'''

        conv_matrix = []

        for y in range(3):
            conv_matrix.append([])
            for x in range(3):
                conv_matrix[y].append(randint(-2, 2))

        print conv_matrix

        self.apply_convolution_matrix(conv_matrix)
