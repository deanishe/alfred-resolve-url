#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2014 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2014-09-04
#

"""
"""

from __future__ import print_function, unicode_literals

import sys
# import subprocess
import re

from workflow import Workflow, ICON_WARNING, web, ICON_INFO

log = None


def resolve(url):
    try:
        r = web.get(url)
        r.raise_for_status()
    except Exception as err:
        log.error('URL : {}, ERROR : {}'.format(url, err))
        return None
    url2 = r.url
    if url == url2:
        log.info('No redirect : {}'.format(url))
    else:
        log.info('{}  ->  {}'.format(url, url2))
    return url2


def url_valid(url):
    """Return True/False if URL is valid"""
    return re.match(r'https?://.+', url, re.IGNORECASE)


# def url_from_clipboard():
#     cmd = ['pbpaste', '-Prefer', 'txt']
#     text = subprocess.check_output(cmd).decode('utf-8')
#     if not url_valid(text):
#         log.debug('No valid URL on clipboard')
#         return None
#     log.info('URL from clipboard : {}'.format(text))
#     return text


def main(wf):
    url = None
    if len(wf.args):
        url = wf.args[0]

    if not url:
        wf.add_item('No URL specified',
                    'Paste a URL',
                    icon=ICON_WARNING)

    elif not url_valid(url):
        wf.add_item('Invalid URL', url, icon=ICON_WARNING)

    else:
        url2 = resolve(url)
        if not url2:
            wf.add_item("Couldn't open URL", url, icon=ICON_WARNING)

        elif url == url2:
            wf.add_item('No redirects', url, icon=ICON_INFO)

        else:
            wf.add_item(url2, 'Copy to Clipboard',
                        arg=url2,
                        valid=True,
                        uid=url2,
                        icon='redirect.png')

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
