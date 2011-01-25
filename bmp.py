#!/usr/bin/env python

import struct
import StringIO
from math import ceil
from random import randint

INVFILE = 1

class BMP:
    def __init__(self, filename):

        f = open(filename)
        self.raw_data = f.read()

        self.width = struct.unpack_from("<i", self.raw_data, 0x12)[0]
        self.height = struct.unpack_from("<i", self.raw_data, 0x16)[0]
        self.data_offset = ord(self.raw_data[int(0xa)])
        self.bpp = ord(self.raw_data[int(0x1C)]) # Bits Per Pixel
        self.bitmap = []

        self.create_bitmap()

    def create_bitmap(self):
        off = self.data_offset

        width_bytes = self.width*(self.bpp/8)
        rowstride = ceil(width_bytes/4.0)*4
        padding = int(rowstride - width_bytes)

        for h in xrange(self.height):
            self.bitmap.append([])
            
            for w in xrange(self.width):
                b = ord(self.raw_data[off])
                g = ord(self.raw_data[off+1])
                r = ord(self.raw_data[off+2])

                off = off+3

                self.bitmap[h].append((r,g,b))

            off += padding

        self.bitmap = self.bitmap[::-1]

    def save_to(self, filename):
        raw_copy = StringIO.StringIO()
        bitmap = self.bitmap[::-1]
        
        width_bytes = self.width*(self.bpp/8)
        rowstride = ceil(width_bytes/4.0)*4
        padding = int(rowstride - width_bytes)

        raw_copy.write(self.raw_data[:self.data_offset])

        for h in xrange(self.height):
            for w in xrange(self.width):
                r, g, b = bitmap[h][w]

                # Out of range control
                if r > 255: r = 255
                if g > 255: g = 255
                if b > 255: b = 255
                if r < 0: r = 0
                if g < 0: g = 0
                if b < 0: b = 0

                #Char transformation
                r = chr(r)
                g = chr(g)
                b = chr(b)


                raw_copy.write(b+g+r)

            raw_copy.write(chr(0)*padding)

        self.raw_data = raw_copy.getvalue()

        f = open(filename, "w")
        f.write(self.raw_data)
        f.close()

    def draw_rect(self, color, start_x, start_y, end_x, end_y):
        '''Draws a rectangle at given position.
        color must be a tuple with (r,g,b)'''

        start_x = max(start_x, 0)
        start_x = min(start_x, self.width)
        start_y = max(start_y, 0)
        start_y = min(start_y, self.height)
        end_x = max(end_x, 0)
        end_x = min(end_x, self.width)
        end_y = max(end_y, 0)
        end_y = min(end_y, self.height)

        for y in xrange(start_y, end_y):
            for x in xrange(start_x, end_x):
                self.bitmap[y][x] = color

    def draw_line(self, color, x1, y1, x2, y2):
        if x2-x1 != 0:
            slope = (y2-y1)/float(x2-x1)
        else:
            slope = 0
        yintercept = y1 - slope*x1

        for x in xrange(x1, x2-x1):
            ry = int(slope*x + yintercept)
            self.bitmap[ry][x] = color

    def mosaic(self, mosaic_size):
        mid = mosaic_size/2

        for y in xrange(0, self.height, mosaic_size):
            for x in xrange(0, self.width, mosaic_size):
                ex = min(x+mosaic_size, bmp.width)
                ey = min(y+mosaic_size, bmp.height)

                ypos = min(y+mid, self.height-1)
                xpos = min(x+mid, self.width-1)
                color = self.bitmap[ypos][xpos]
                self.draw_rect(color,x, y, ex, ey)

    def invert(self):
        for y in xrange(0, self.height):
            for x in xrange(0, self.width):
                r,g,b = bmp.bitmap[y][x]
                bmp.bitmap[y][x] = (255-r, 255-g, 255-b) 

    def flip_horizontal(self):
        map(list.reverse, self.bitmap)

    def flip_vertical(self):
        self.bitmap.reverse()

    def blur_normal(self):
        copy = self.bitmap[::]

        for y in xrange(0, self.height):
            for x in xrange(0, self.width):
                total = copy[y][x]
                cont = 1

                if y != 0:
                    r, g, b = copy[y-1][x]
                    total = total[0]+r, total[1]+g, total[2]+b
                    cont += 1

                if y != self.height-1:
                    r, g, b = copy[y+1][x]
                    total = total[0]+r, total[1]+g, total[2]+b
                    cont += 1

                if x != 0:
                    r, g, b = copy[y][x-1]
                    total = total[0]+r, total[1]+g, total[2]+b
                    cont += 1

                if x != self.width-1:
                    r, g, b = copy[y][x+1]
                    total = total[0]+r, total[1]+g, total[2]+b
                    cont += 1

                if x != 0 and y != 0:
                    r, g, b = copy[y-1][x-1]
                    total = total[0]+r, total[1]+g, total[2]+b
                    cont += 1
               
                if x != self.width-1 and y != self.height-1:
                    r, g, b = copy[y+1][x+1]
                    total = total[0]+r, total[1]+g, total[2]+b
                    cont += 1

                if x != 0 and y != self.height-1:
                    r, g, b = copy[y+1][x-1]
                    total = total[0]+r, total[1]+g, total[2]+b
                    cont += 1

                if x != self.width-1 and y != 0:
                    r, g, b = copy[y-1][x+1]
                    total = total[0]+r, total[1]+g, total[2]+b
                    cont += 1

                self.bitmap[y][x] = total[0]/cont, total[1]/cont, total[2]/cont

    def blur_box(self, box_width, box_height):
        copy = self.bitmap[::]

        for y in xrange(0, self.height):
            for x in xrange(0, self.width):
                average = self._blur_box_average(x, y, box_width, box_height, copy)
                self.bitmap[y][x] = average

    def _blur_box_average(self, x, y, bw, bh, copy):
        blimit1 = (max(0, x-bw), max(0, y-bh))
        blimit2 = (min(self.width-1, x+bw), min(self.height-1, y+bh))

        total = (0, 0, 0)
        for y in xrange(blimit1[1], blimit2[1]+1):
            for x in xrange(blimit1[0], blimit2[0]+1):
                r, g, b = copy[y][x]
                total = total[0]+r, total[1]+g, total[2]+b

        area = (blimit2[0]-blimit1[0]+1)*(blimit2[1]-blimit1[1]+1)
        total = total[0]/area, total[1]/area, total[2]/area

        return total

if __name__ == "__main__":
    bmp = BMP("test.bmp")

    pot = 205.1
    light = 0.8

    """
    for y in xrange(0, bmp.height):
        for x in xrange(0, bmp.width):
            r, g, b = bmp.bitmap[y][x]

            f = ((255-r)/pot)+light
            t = ((255-g)/pot)+light
            p = ((255-b)/pot)+light

            bmp.bitmap[y][x] = int(r*f), int(g*t), int(b*p)
    """

    bmp.blur_box(4, 4)
    bmp.save_to("test.bmp")
