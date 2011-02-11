#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Flip filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''

class Flip:
    def flip_horizontal(self):
        '''Flip the image horizontaly'''

        map(list.reverse, self.bitmap)

    def flip_vertical(self):
        '''Flip the image verticaly'''

        self.bitmap.reverse()
