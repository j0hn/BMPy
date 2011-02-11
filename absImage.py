#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Module to abstract a class representating an
image and it's operations
'''

from abc import ABCMeta, abstractmethod

class Image:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.width = 0
        self.height = 0
        self.bitmap = None

    @abstractmethod
    def create_bitmap(self):
        pass

    @abstractmethod
    def load_from_file(self, filename):
        pass

    @abstractmethod
    def save_to(self, filename):
        pass
