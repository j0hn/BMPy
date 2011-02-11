#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Magic Wand filter

Author: j0hn <j0hn.com.ar@gmail.com>
'''

class MagicWand:
    def magic_wand(self, start_x, start_y, color, tolerance):
        # http://editor.pixastic.com/tools/selectwand.js

        to_explore = []
        explored = []

        org_color = self.bitmap[start_y][start_x]

        bw = bh = 1
        blimit1 = (max(0, start_x-bw), max(0, start_y-bh))
        blimit2 = (min(self.width-1, start_x + bw), \
                   min(self.height-1, start_y + bh))

        for y in xrange(blimit1[1], blimit2[1]+1):
            for x in xrange(blimit1[0], blimit2[0]+1):
                to_explore.append((x, y))

        neig = [(-1, 0),
               (1, 0),
               (0, -1),
               (0, 1),
               (-1, -1),
               (-1, 1),
               (1, -1),
               (1, 1)]

        while len(to_explore) != 0:
            x, y = to_explore.pop()

            if (x, y) not in explored:
                explored.append((x, y))

                for i in xrange(8):
                    nx = x + neig[i][0]
                    ny = y + neig[i][1]

                    if nx not in range(0, self.width) \
                          or ny not in range(0, self.height):
                        continue

                    r, g, b = self.bitmap[ny][nx]

                    dr = abs(org_color[0]-r)
                    dg = abs(org_color[1]-g)
                    db = abs(org_color[2]-b)

                    if dr <= tolerance and dg <= tolerance and db <= tolerance:
                        self.bitmap[ny][nx] = color
                        to_explore.append((nx, ny))
