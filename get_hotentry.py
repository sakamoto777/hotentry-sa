#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch

import re
import datetime

import datastores

def get_hotentry():
    hotentry_url = 'http://b.hatena.ne.jp/hotentry'
    fetch_result = urlfetch.fetch(hotentry_url,deadline=60)

    if fetch_result.status_code == 200:
#        pattern = re.compile(r'''<h3 class="hb-entry-link-container" 
#          ><a href="(.*?)" class="entry-link" 
#            title="(.*?)"
#            data-entryrank="(.*?)"
#            data-track-click-target="direct">(.*?)</a></h3>''',re.S)

        pattern = re.compile(r'''<h3 class="entrylist-contents-title">
        <a href="(.*?)"
           title="(.*?)"
           target="_blank" rel="noopener"
           class="js-keyboard-openable"
           data-gtm-click-label="entry-info-title">(.*?)</a>
      </h3>''',re.S)

        parse_result = pattern.findall(fetch_result.content)

        return [row[0] for row in parse_result]


def put_entry(entry_url,checktime):
    query = datastores.Entries.gql('WHERE entry_url = :url',url=entry_url)
    entry = query.get()

    if entry:
        entry.hotentry_check_time = checktime
        entry.put()
    else:
        entry = datastores.Entries()
        entry.entry_url = entry_url
        entry.hotentry_check_time = checktime
        entry.score_check_time = datetime.datetime(2018,1,1)
        entry.put()


if __name__ == "__main__":
    checktime = datetime.datetime.today()
    for entry_url in get_hotentry():
        put_entry(entry_url,checktime)