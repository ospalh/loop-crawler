# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–2013 Roland Sieker, ospalh@gmail.com
#
# License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html


'''
Get img links.
'''

import errno
import os


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
