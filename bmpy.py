#!/usr/bin/env python

'''
Small library to open and edit bmp files

Author: j0hn  <j0hn.com.ar@gmail.com>
'''

import sys
import struct
import StringIO
from math import ceil
import random

from absImage import Image
from filters import *

WIDTH_OFFSET = int(0x12)
HEIGHT_OFFSET = int(0x16)
DATA_OFFSET = int(0x0a)
BPP_OFFSET = int(0x1C)


class BMPy(Image, blur.Blur, box_blur.BoxBlur, mosaic.Mosaic,
           sepia.Sepia, invert.Invert, flip.Flip, desaturate.Desaturate,
           magic_wand.MagicWand, resize.Resize, crop.Crop,
           convolution.ConvolutionMatrix, detect_edges.DetectEdges,
           conv_random.ConvRandom):
    '''
    Open, edit, and save a bmp file
    '''

    def load_from_file(self, filename):
        '''Main class to open and edit a 24 bits bmp image'''

        bmpfile = open(filename)
        self.raw_data = bmpfile.read()
        bmpfile.close()

        self.width = struct.unpack_from("<i", self.raw_data, WIDTH_OFFSET)[0]
        self.height = struct.unpack_from("<i", self.raw_data, HEIGHT_OFFSET)[0]
        self.data_offset = ord(self.raw_data[DATA_OFFSET])
        self.bpp = ord(self.raw_data[BPP_OFFSET])  # Bits Per Pixel
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

                self.bitmap[y].append((r, g, b))

            off += padding

        self.bitmap = self.bitmap[::-1]

    def save_to(self, filename):
        '''Export the bmp saving the changes done to the bitmap'''

        raw_copy = StringIO.StringIO()
        bitmap = self.bitmap[::-1]

        width_bytes = self.width*(self.bpp/8)
        rowstride = ceil(width_bytes/4.0)*4
        padding = int(rowstride - width_bytes)

        # Same header as before until the width
        raw_copy.write(self.raw_data[:WIDTH_OFFSET])

        s = struct.Struct("<i")
        _w = s.pack(self.width)   # Transform width, height to
        _h = s.pack(self.height)  # little indian format
        raw_copy.write(_w)
        raw_copy.write(_h)

        # After the new width and height the header it's the same
        raw_copy.write(self.raw_data[HEIGHT_OFFSET+4:self.data_offset])

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
                r = chr(int(r))
                g = chr(int(g))
                b = chr(int(b))

                raw_copy.write(b + g + r)

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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_name = sys.argv[1]
    else:
        print "Usage: " + sys.argv[0] + " FILE"
        print
        print "Note: it must be a 24-bit bmp file"
        sys.exit(1)

    #try:
    bmp = BMPy()
    bmp.load_from_file(image_name)
    #bmp.detect_edges()
    bmp.conv_random()
    bmp.save_to("test.bmp")
    #except Exception, e:
        #print "Error:", e
        #sys.exit(1)
