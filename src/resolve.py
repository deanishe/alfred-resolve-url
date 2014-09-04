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
import re
from urlparse import urlparse
from socket import gethostbyname_ex
from multiprocessing.dummy import Pool
from time import time

from workflow import Workflow, ICON_WARNING, web, ICON_ERROR

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

DOMAIN_WITH_PORT = re.compile(r'(.+):\d+')

log = None


def resolve(url):
    s = time()
    try:
        r = web.get(url)
        r.raise_for_status()
    except Exception as err:
        log.error('Error opening URL {} : {}'.format(url, err))
        return None
    url2 = r.url
    if url == url2:
        log.info('No redirect : {}'.format(url))
    else:
        log.info('{}  ->  {}'.format(url, url2))
    log.info('Resolved canonical URL in {:0.3f} seconds'.format(time() - s))
    return url2


def url_valid(url):
    """Return True/False if URL is valid"""
    return URL_REGEX.match(url)


def hostname_for_url(url):
    """Return hostname for URL"""
    host = urlparse(url).netloc
    m = DOMAIN_WITH_PORT.match(host)
    if m:
        host = m.group(1)
    log.debug('{} <- {}'.format(host, url))
    return host


def dns_info(url):
    """Return DNS info for host of URL"""
    s = time()
    domain = hostname_for_url(url)
    try:
        hostname, aliases, ipaddrs = gethostbyname_ex(domain)
    except Exception as err:
        log.error('Error fetching DNS for {} : {}'.format(domain, err))
        return None
    log.info('Retrieved DNS info in {:0.3f} seconds'.format(time() - s))
    return {
        'hostname': hostname,
        'aliases': aliases,
        'ipaddrs': ipaddrs}


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
        url = None

    if not url:
        wf.send_feedback()
        return

    pool = Pool(2)

    resolver = pool.apply_async(resolve, (url,))
    dns = pool.apply_async(dns_info, (url,))

    url2 = resolver.get()
    dnsinfo = dns.get()

    if not url2:
        wf.add_item("Couldn't open URL", url, icon=ICON_ERROR)
        wf.send_feedback()
        return

    elif url == url2:
        wf.add_item('URL is canonical', url, icon='canonical.png')

    else:
        # Update DNS info if this is a different host
        if hostname_for_url(url) != hostname_for_url(url2):
            dnsinfo = dns_info(url2)

        wf.add_item(url2, 'Copy to Clipboard',
                    arg=url2,
                    valid=True,
                    largetext=url2,
                    icon='redirect.png')

    if dnsinfo:

        wf.add_item(dnsinfo['hostname'],
                    'Primary host',
                    copytext=dnsinfo['hostname'],
                    largetext=dnsinfo['hostname'],
                    icon='host.png')

        for ipaddr in reversed(dnsinfo['ipaddrs']):
            wf.add_item(ipaddr, 'IP address',
                        copytext=ipaddr,
                        largetext=ipaddr,
                        icon='ipaddr.png')

        for alias in sorted(dnsinfo['aliases']):
            wf.add_item(alias, 'Host alias',
                        copytext=alias,
                        largetext=alias,
                        icon='alias.png')

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
