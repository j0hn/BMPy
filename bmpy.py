#!/usr/bin/env python
'''Small library to open and edit bmp files'''

import sys
import struct
import StringIO
from math import ceil
import random

class BMPy:
    def __init__(self, filename):
        '''Main class to open and edit a 24 bits bmp image'''

        f = open(filename)
        self.raw_data = f.read()

        self.width = struct.unpack_from("<i", self.raw_data, 0x12)[0]
        self.height = struct.unpack_from("<i", self.raw_data, 0x16)[0]
        self.data_offset = ord(self.raw_data[int(0xa)])
        self.bpp = ord(self.raw_data[int(0x1C)]) # Bits Per Pixel
        self.bitmap = []

        if self.raw_data[0] != "B" and self.raw_data[1] != "M":
            raise TypeError, "Not a BMP file!"
        if self.bpp != 24:
            raise TypeError, "Not a 24 bits BMP file"

        self.create_bitmap()

    def create_bitmap(self):
        '''Creates the bitmap from the raw_data'''

        off = self.data_offset

        width_bytes = self.width*(self.bpp/8)
        rowstride = ceil(width_bytes/4.0)*4
        padding = int(rowstride - width_bytes)

        for y in xrange(self.height):
            self.bitmap.append([])

            for x in xrange(self.width):
                b = ord(self.raw_data[off])
                g = ord(self.raw_data[off+1])
                r = ord(self.raw_data[off+2])

                off = off+3

                self.bitmap[y].append((r,g,b))

            off += padding

        self.bitmap = self.bitmap[::-1]

    def save_to(self, filename):
        '''Export the bmp saving the changes done to the bitmap'''

        raw_copy = StringIO.StringIO()
        bitmap = self.bitmap[::-1]

        width_bytes = self.width*(self.bpp/8)
        rowstride = ceil(width_bytes/4.0)*4
        padding = int(rowstride - width_bytes)

        s = struct.Struct("<i")
        raw_copy.write(self.raw_data[:int(0x12)])
        _w = s.pack(self.width)
        _h = s.pack(self.height)
        raw_copy.write(_w)
        raw_copy.write(_h)

        raw_copy.write(self.raw_data[int(0x1A):self.data_offset])

        for y in xrange(self.height):
            for x in xrange(self.width):
                r, g, b = bitmap[y][x]

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
        ''' Draw a line from (x1, y1) to (x2, y2)'''

        if x2-x1 != 0:
            slope = (y2-y1)/float(x2-x1)
        else:
            slope = 0

        yintercept = y1 - slope*x1

        for x in xrange(x1, x1+(x2-x1)+1):
            ry = int(slope*x + yintercept)
            self.bitmap[ry][x] = color

    def mosaic(self, mosaic_size):
        '''Pixelate the image with block size of mosaic_size'''

        mid = mosaic_size/2

        for y in xrange(0, self.height, mosaic_size):
            for x in xrange(0, self.width, mosaic_size):
                ex = min(x+mosaic_size, self.width)
                ey = min(y+mosaic_size, self.height)

                ypos = min(y+mid, self.height-1)
                xpos = min(x+mid, self.width-1)
                color = self.bitmap[ypos][xpos]
                self.draw_rect(color,x, y, ex, ey)

    def invert(self):
        '''Invert the colors of the image'''

        for y in xrange(0, self.height):
            for x in xrange(0, self.width):
                r,g,b = self.bitmap[y][x]
                self.bitmap[y][x] = (255-r, 255-g, 255-b)

    def flip_horizontal(self):
        '''Flip the image horizontaly'''

        map(list.reverse, self.bitmap)

    def flip_vertical(self):
        '''Flip the image verticaly'''

        self.bitmap.reverse()

    def blur(self):
        '''Simple blur'''

        copy = self.bitmap[::]

        self.box_blur(1, 1)

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
        blimit2 = (min(self.width-1, x+bw), min(self.height-1, y+bh))

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

    def desaturate(self):
        '''In other words, convert the image to gray scale'''

        for y in xrange(self.height):
            for x in xrange(self.width):
                r, g, b = self.bitmap[y][x]

                average = (r+g+b)/3

                self.bitmap[y][x] = average, average, average

    def sepia(self):
        '''Transform the image colors to a sepia scale'''

        for y in xrange(self.height):
            for x in xrange(self.width):
                r, g, b = self.bitmap[y][x]

                nr = r*0.393 + g*0.769 + b*0.189
                ng = r*0.349 + g*0.686 + b*0.168
                nb = r*0.272 + g*0.534 + b*0.131

                self.bitmap[y][x] = int(nr), int(ng), int(nb)

    def magic_wand(self, start_x, start_y, color, tolerance):
        # http://editor.pixastic.com/tools/selectwand.js

        to_explore = []
        explored = []

        org_color = self.bitmap[start_y][start_x]

        bw = bh = 1
        blimit1 = (max(0, start_x-bw), max(0, start_y-bh))
        blimit2 = (min(self.width-1, start_x+bw), min(self.height-1, start_y+bh))

        for y in xrange(blimit1[1], blimit2[1]+1):
            for x in xrange(blimit1[0], blimit2[0]+1):
                to_explore.append((x,y))

        neig = [(-1,0),
               (1,0),
               (0,-1),
               (0,1),
               (-1,-1),
               (-1,1),
               (1,-1),
               (1,1)]


        while len(to_explore) != 0:
            x, y = to_explore.pop()

            if (x,y) not in explored:
                explored.append((x,y))

                for i in xrange(8):
                    nx = x + neig[i][0]
                    ny = y + neig[i][1]

                    if nx not in range(0, self.width) or ny not in range(0, self.height):
                        continue

                    r, g, b = self.bitmap[ny][nx]

                    dr = abs(org_color[0]-r)
                    dg = abs(org_color[1]-g)
                    db = abs(org_color[2]-b)

                    if dr <= tolerance and dg <= tolerance and db <= tolerance:
                        self.bitmap[ny][nx] = color
                        to_explore.append((nx, ny))

    def crop(self, start_x, start_y, end_x, end_y):
        self.width = end_x - start_x
        self.height = end_y - start_y

        self.bitmap = self.bitmap[start_y:end_y]
        for y in range(len(self.bitmap)):
            self.bitmap[y] = self.bitmap[y][start_x:end_x]

    def resize(self, new_width, new_height, method="simple"):

        if new_width > self.width or new_height > self.height:
            raise NotImplementedError, "Only resizing to make the image smaller"

        try:
            getattr(self, "resize_"+ method )(new_width, new_height)
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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_name = sys.argv[1]
    else:
        print "Usage: " + sys.argv[0] + " FILE"
        print
        print "Note: it must be a 24-bit bmp file"
        sys.exit(1)

    try:
        bmp = BMPy(image_name)
        bmp.resize(180, 150, method="simple")
        bmp.box_blur(5, 5, fuzzy=True)
        bmp.save_to("test.bmp")
    except Exception, e:
        print "Error:", e
        sys.exit(1)

    """
    # Crazy test
    pot = 205.1
    light = 0.8

    for y in xrange(0, bmp.height):
        for x in xrange(0, bmp.width):
            r, g, b = bmp.bitmap[y][x]

            f = ((255-r)/pot)+light
            t = ((255-g)/pot)+light
            p = ((255-b)/pot)+light

            bmp.bitmap[y][x] = int(r*f), int(g*t), int(b*p)
    """

