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

        self.apply_convolution_matrix(conv_matrix)
