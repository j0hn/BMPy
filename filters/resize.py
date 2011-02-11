#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Resize filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''


class Resize:
    def resize(self, new_width, new_height, method="simple"):

        if new_width > self.width or new_height > self.height:
            raise NotImplementedError, "Only resizing to make the image smaller"

        try:
            getattr(self, "resize_" + method)(new_width, new_height)
        except AttributeError:
            print "Skiping resize " + method
            print "Reason: No method called " + method

    def resize_simple(self, new_width, new_height):
        fh = self.height/float(new_height)
        fw = self.width/float(new_width)

        new_grid = []

        ch = 0
        for i in range(new_height):
            new_grid.append([])

            y = int(round(ch))

            cw = 0
            for j in range(new_width):
                x = int(round(cw))

                new_grid[i].append(self.bitmap[y][x])

                cw += fw

            ch += fh

        self.bitmap = new_grid
        self.height = new_height
        self.width = new_width
