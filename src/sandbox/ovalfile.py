
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

    { "name" : "patho" , "command" : "python check_pathologic_clusters.py -b ../../data/fits/common.fits"  },

]

# filters

run_filters_out = [ {"name": "wcs", "re": "^(WARNING:|warning:|Defunct|this form of).*$", "apply": "find%"}, ]

diff_filters_in = [
    {"name": "pylint1", "re": "%rated at%", "apply": "(analyze%)|(oval%)"},
    {"name": "pylint2", "re": "[CEWIDR]:%", "apply": "(analyze%)|(oval%)"},
    {"name": "patho", "re": "^(.+) pathologic clusters$", "apply": "patho%"},
]
