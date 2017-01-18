#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import matplotlib.pyplot as plt
import numpy as np
import lib_args, lib_fits, lib_background, lib_cluster
import lib_wcs, lib_stars

CONE = 0.001


class ShowCelestialObjects():

    def __init__(self, the_region, the_wcs, the_fig):

        self.region = the_region
        self.wcs = the_wcs
        self.fig = the_fig
        self.text = None

    def __call__(self, event):

        if event.xdata is None or event.ydata is None: return

        if self.text is not None:
            self.text.remove()
            self.text = None

        x, y = int(event.xdata), int(event.ydata)
        results = self.region.find_clusters(x, y, 5)

        if len(results) > 0:

            tokens = []

            for cluster in results:

                x, y = cluster['c'], cluster['r']
                ra, dec = lib_wcs.convert_to_radec(self.wcs, x, y)

                cobjects, _, _ = lib_stars.get_celestial_objects(ra, dec, CONE)
                tokens.extend(cobjects)

            self.text = plt.text(x, y, ' '.join(tokens), fontsize=14, color='white')

        self.fig.canvas.draw()


def main():

    file_name, batch = lib_args.get_args()
    header, pixels = lib_fits.read_first_image(file_name)
    background, dispersion, _ = lib_background.compute_background(pixels)

    # search for clusters in a sub-region of the image
    threshold = 6.0
    region = lib_cluster.Region(pixels, background + threshold*dispersion)
    pattern, cp_image, peaks = region.run_convolution()

    # coordinates ra dec
    max_cluster = region.clusters[0]
    wcs = lib_wcs.get_wcs(header)
    ra, dec = lib_wcs.convert_to_radec(wcs, max_cluster['c'], max_cluster['r'])

    # celestial objects
    cobjects, _, _ = lib_stars.get_celestial_objects(ra, dec, CONE)

    # console output
    for cobj in cobjects.keys():
        print('celestial object: {}'.format(cobj))

    # graphic output
    if not batch:
        fig, main_ax = plt.subplots()
        main_ax.imshow(peaks, interpolation='none')
        fig.canvas.mpl_connect('motion_notify_event',
          ShowCelestialObjects(the_region=region,the_wcs=wcs,the_fig=fig))
        plt.show()

    return 0

if __name__ == '__main__':
    sys.exit(main())