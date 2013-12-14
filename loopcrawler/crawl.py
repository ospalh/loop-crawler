#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–2013 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

u"""Download all images from a blog."""

from lxml import html
import argparse
import os
import urllib2
import urlparse

from .get_data import get_html_from_url
from .get_images import get_highest_resolution_image
from .utils import mkdir_p


def crawl(argv):
    u"""Wrapper to parse the arguments."""
    parser = argparse.ArgumentParser(
        description=u"""Retrieve all images from a blog.
This programme retrieves all images from a blog that follows the
standard of a typical tumblr.com blog.
""")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-f', '--forwards', type=int, help='Increase the page numbers')
    group.add_argument(
        '-b', '--backwards', type=int,
        help='Decrease the page numbers, starting at the given value')
    parser.add_argument(
        '--basedir', type=str,
        help='''The directory where the files are stored''', default='.')
    parser.add_argument('url', type=str, help='The URL to crawl')
    parser.add_argument(
        '-o', '--offset', type=int, help='first images number')
    args = parser.parse_args(argv[1:])

    url = args.url
    page_count = 1
    step = 1
    if args.forwards:
        page_count = args.forwards
    if args.backwards:
        page_count = args.backwards
        step = -1
    url = url.rstrip(u'/')
    if not u'//' in url:
        url = 'http://' + url

    split_url = urlparse.urlsplit(url)
    blog_name, base_name, dummy_name = split_url.netloc.split('.')
    base_dir = os.path.join(args.basedir, base_name)
    blog_name_dir = os.path.join(base_dir, blog_name)
    print('blog name dir: {}, url: {}'.format(
            blog_name_dir, url))
    img_count = 1
    if args.offset:
        img_count = args.offset
    mkdir_p(blog_name_dir)
    while page_count > 0:
        # EAFP. Working out a way to cleanly exit comes later.
        print('effective url: {}/page/{}'.format(url, page_count))
        for i in range(5):
            try:
                page = get_html_from_url('{}/page/{}'.format(url, page_count))
            except urllib2.URLError:
                if i == 4:
                    raise
            else:
                break
        if step > 1:
            imgs = page.iter('img')
        else:
            imgs = list(page.iter('img'))
        for image in imgs:
            try:
                fname = get_highest_resolution_image(
                    image.get('src'), base_dir)
            except (KeyError, IndexError, ValueError, AttributeError) as e:
                continue
            if not fname:
                continue
            base_name = os.path.basename(fname)
            os.symlink(os.path.relpath(fname, blog_name_dir),
                       os.path.join(blog_name_dir, u'{:05}_{}'.format(
                        img_count, base_name)))
            print(u'saved {:05}_{}'.format(
                        img_count, os.path.basename(fname)))
            img_count += 1
        page_count = page_count + step



if __name__ == '__main__':
    import sys
    crawl(sys.argv)
