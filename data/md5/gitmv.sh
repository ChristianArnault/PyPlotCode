#!/bin/bash

#for ex in ex1_read_image ex2_background ex3_clusters ex4_coordinates ex5_find_stars
#for ex in ex1_read_image ex2_background ex3_clusters ex4_coordinates ex5_find_stars
#do
    for txt in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22
    do
        git mv ex4_coordinates.NPAC$txt.ref ex4_stars.NPAC$txt.ref
        git mv ex5_find_stars.NPAC$txt.ref ex5_show_stars.NPAC$txt.ref
        #git mv $ex.NPAC$txt.ref.tmp $ex.NPAC02.ref
        #git mv $ex.NPAC$txt.md5.tmp $ex.NPAC02.md5
    done
#done
