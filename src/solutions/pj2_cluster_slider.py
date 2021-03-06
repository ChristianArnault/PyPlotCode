#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import lib_args, lib_fits, lib_background, lib_cluster
sys.path.append('../skeletons')


class UpdateSlider():

    def __init__(self, pixels, background, dispersion, imgplot, fig):

        self.pixels = pixels
        self.background = background
        self.dispersion = dispersion
        self.imgplot = imgplot
        self.fig = fig

    def __call__(self, val):

        clustering = lib_cluster.Clustering()
        clusters = clustering(self.pixels, self.background, self.dispersion, val)
        print('{} clusters'.format(len(clusters)))
        crosses = lib_cluster.add_crosses(self.pixels, clusters)
        self.imgplot.set_data(crosses)
        self.fig.canvas.draw_idle()


def main():

    file_name, interactive = lib_args.get_args()
    header, pixels = lib_fits.read_first_image(file_name)
    background, dispersion, max_x = lib_background.compute_background(pixels)
    clustering = lib_cluster.Clustering()
    clusters = clustering(pixels, background, dispersion)

    # console output
    if not interactive:

        print('{} clusters'.format(len(clusters)))

    else:
        # graphic output

        fig, axis = plt.subplots()
        imgplot = axis.imshow(pixels)

        axcolor = 'lightgoldenrodyellow'
        ax_thresh = plt.axes([0.25, 0.92, 0.65, 0.03], axisbg=axcolor)

        threshold = 6.0
        slider = widgets.Slider(ax_thresh, 'Threshold', 0.0, 5*threshold, valinit=threshold)

        update_slider = UpdateSlider(pixels, background, dispersion, imgplot, fig)
        slider.on_changed(update_slider)
        update_slider(threshold)

        plt.show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
