# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–2013 Roland Sieker, ospalh@gmail.com
#
# License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html


'''
Get img links.
'''

from lxml import html
import errno
import os
import urllib
import urllib2
import urlparse


from .get_data import get_data_from_url, get_html_from_url
from .utils import mkdir_p

resolution_list = [1280, 700, 500, 400]


def split_url(url):
    split_url = urlparse.urlsplit(url)
    first = split_url.netloc.split('.')[0]
    filename = os.path.basename(url)
    split_name = filename.split(u'_')
    base_filename = u'_'.join(split_name[:-1])
    base_url = u'_'.join(url.split(u'_')[:-1])
    resolution = split_name[-1].split('.')[0]
    ftype = split_name[-1].split('.')[1]
    # This calles for a named tuple.
    # The int() are mostly to detect links we don’t like
    return int(first), filename, base_filename, base_url, int(resolution), \
        ftype

def get_highest_resolution_image(url, base_dir):
    surl = split_url(url)
    target_dir = os.path.join(base_dir, str(surl[0]))
    mkdir_p(target_dir)
    for res in resolution_list:
        fname = u'{b}_{r}.{e}'.format(b=surl[2], r=res, e=surl[5])
        fpath = os.path.join(target_dir, fname)
        if os.path.exists(fpath):
            print('have that')
            return fpath
        try:
            img_data = get_data_from_url('{b}_{r}.{e}'.format(
                    b=surl[3], r=res, e=surl[5]))
        except:
            continue
        with open(fpath, 'wb') as img_file:
            img_file.write(img_data)
        return fpath


def get_base_name(post):
    """
    Determine a base file name

    Determine a file name from the data in the post. Idealy this
    includes the post date and title.
    """
    # TODO
    pass


def get_date_title_from_tag(tag):
    # idea: call tag = tag.getparent() until the new tag has class
    # post, then look down again to find class date, and a link with
    # /post/, which should contain a title.
    pass
