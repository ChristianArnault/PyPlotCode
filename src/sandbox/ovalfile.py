
'''
Configuration file for the tool oval.
'''

# simple targets

targets = [

#    {"name": "analyze", "command": "pylint find_stars.py"},
#
#    {"name": "analyze_lib_background", "command": "pylint lib_background.py"},
#    {"name": "analyze_lib_cluster", "command": "pylint lib_cluster.py"},
#    {"name": "analyze_lib_logging", "command": "pylint lib_logging.py"},
#    {"name": "analyze_lib_model", "command": "pylint lib_model.py"},
#    {"name": "analyze_lib_fits", "command": "pylint lib_fits.py"},
#    {"name": "analyze_lib_wcs", "command": "pylint lib_wcs.py"},
#
#    {"name": "oval", "command": "pylint oval"},
#    {"name": "ovalfile", "command": "pylint ovalfile"},
#
#    {"name": "lib_logging", "command": "python lib_logging.py"},

    { "name" : "find_stars" , "command" : "python find_stars.py -b ../../data/fits/NPAC.fits"  },

    { "name" : "pj1_background_suppress" , "command" : "python pj1_background_suppress.py -b ../../data/fits/NPAC.fits"  },
    { "name" : "pj2_cluster_slider" , "command" : "python pj2_cluster_slider.py -b ../../data/fits/NPAC.fits"  },
    { "name" : "pj3_file_selector" , "command" : "python pj3_file_selector.py -b ../../data/fits/NPAC.fits"  },
    { "name" : "pj4_threaded_clusters" , "command" : "python pj4_threaded_clusters.py -b ../../data/fits/NPAC.fits"  },
    { "name" : "pj5_animate_clusters" , "command" : "python pj5_animate_clusters.py -b ../../data/fits/NPAC.fits"  },
]

# filters

run_filters_out = [ {"name": "wcs", "re": "^(WARNING:|warning:|Defunct|this form of).*$", "apply": "find%"}, ]

diff_filters_in = [
    {"name": "pylint1", "re": "%rated at%", "apply": "(analyze%)|(oval%)"},
    {"name": "pylint2", "re": "[CEWIDR]:%", "apply": "(analyze%)|(oval%)"},
    {"name": "info", "re": "^(.+)$", "apply": "%"},
]