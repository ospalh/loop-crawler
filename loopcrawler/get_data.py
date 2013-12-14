# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–2013 Roland Sieker, ospalh@gmail.com
#
# License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html


'''
Download stuff.
'''

import urllib
import urllib2
import urlparse
from lxml import html

user_agent = '''Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) \
Gecko/20100101 Firefox/15.0.1'''


def get_data_from_url(url_in):
    """
    Return raw data loaded from an URL.

    Helper function. Put in an URL and it sets the agent, sends
    the requests, checks that we got error code 200 and returns
    the raw data only when everything is OK.
    """
    try:
        # There have been reports that the request was send in a
        # 32-bit encoding (UTF-32?). Avoid that. (The whole things
        # is a bit curious, but there shouldn't really be any harm
        # in this.)
        request = urllib2.Request(url_in.encode('ascii'))
    except UnicodeDecodeError:
        request = urllib2.Request(url_in)
    try:
        # dto. But i guess this is even less necessary.
        request.add_header('User-agent', user_agent.encode('ascii'))
    except UnicodeDecodeError:
        request.add_header('User-agent', user_agent)
    response = urllib2.urlopen(request)
    if 200 != response.code:
        raise ValueError(str(response.code) + ': ' + response.msg)
    return response.read()

def get_html_from_url(url_in):
    """
    Return data loaded from an URL, as BeautifulSoup(3) object.

    Wrapper helper function aronud get_data_from_url()
    """
    return html.fromstring(get_data_from_url(url_in))
