#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import subprocess

import matplotlib.pyplot as plt

import lib_read_file
import lib_wcs as lwcs
import numpy as np
import time
import re
import random

import threading

DATAPATH = 'data/'

def get_fits_file(number=0):
    if number == 0:
        return DATAPATH + 'misc/M81' + '.fits'
    else:
        return DATAPATH + 'student/NPAC%02d' % number + '.fits'

class Display(object):

    def __init__(self):

        self.image = get_fits_file(1)
        self.header_image = lib_read_file.read_header(self.image)
        self.pixels_image = lib_read_file.read_pixels(self.image)

        self.fig, self.main_ax = plt.subplots()

        self.y1_max, self.x1_max = self.pixels_image.shape
        self.border = 5
        self.font_size = 14

        self.pixels_image = np.zeros_like(self.pixels_image)

        self.imgplot = self.main_ax.imshow(self.pixels_image)
        self.update = None

    def doit(self):

        update_text = 'Last update: ' + time.asctime(time.localtime(time.time())).split()[3]
        print(update_text)

        i = int(random.random()*self.x1_max)
        j = int(random.random()*self.y1_max)
        print((i, j))
        self.pixels_image[i, j] = int(random.random()*32000)

        if self.update is not None:
            self.update.remove()
            self.update = None

        self.update = plt.text(self.border, self.y1_max-self.border, update_text, fontsize=self.font_size, color='white')

        self.imgplot.set_data(self.pixels_image)
        self.fig.canvas.draw_idle()


class MtDisplay(threading.Thread, Display):

    def __init__(self):
        threading.Thread.__init__(self)
        Display.__init__(self)
        self.plt_lock = threading.Lock()

    def run(self):
        while True:
            self.plt_lock.acquire()
            self.doit()
            self.plt_lock.release()
            time.sleep(1.0)

if __name__ == '__main__':

    # process command-line options
    parser = argparse.ArgumentParser(description='Display progress of all teams')
    args = parser.parse_args()

    # real stuff
    disp = MtDisplay()
    disp.start()
    plt.show()

    # end
    sys.exit(0)