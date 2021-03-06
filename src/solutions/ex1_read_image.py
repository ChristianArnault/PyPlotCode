#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('../skeletons')
import lib_args, lib_fits

def main():

    file_name, interactive = lib_args.get_args()
    header, pixels = lib_fits.read_first_image(file_name)

    # console output
    print('RESULT: cd1_1 = {CD1_1:.10f}'.format(**header))
    print('RESULT: cd1_2 = {CD1_2:.10f}'.format(**header))
    print('RESULT: cd2_1 = {CD2_1:.10f}'.format(**header))
    print('RESULT: cd2_2 = {CD2_2:.10f}'.format(**header))

    # graphic output
    if interactive:
        import matplotlib.pyplot as plt

        _, axis = plt.subplots()
        plt.text(0, -10, file_name, fontsize=14, color='white')
        axis.imshow(pixels)
        plt.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())

