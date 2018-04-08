#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch

import json
import datetime

import datastores


def call_hatebuapi(url):
    hatebuapi_url = 'http://b.hatena.ne.jp/entry/jsonlite/' + url
    fetch_result = urlfetch.fetch(hatebuapi_url,deadline=60)

    if fetch_result.status_code == 200:

        json_result = json.loads(fetch_result.content)

        comments = ''
        for bookmark in json_result['bookmarks']:
            comments = comments + bookmark['comment']

        return {'title':json_result['title'],
                    'count':json_result['count'],
                    'entry_url':json_result['entry_url'],
                    'comments':comments}


def call_gnlapi(comments,apikey):
    gnlapi_url = 'https://language.googleapis.com/v1/documents:analyzeSentiment?key=' + apikey
    headers = {'Content-Type': 'application/json'}
    body = {"document": {"type": "PLAIN_TEXT","language": "JA","content": comments},
                    "encodingType": "UTF8"}

    fetch_result = urlfetch.fetch(url=gnlapi_url,
                    headers=headers,
                    payload=json.dumps(body),
                    method=urlfetch.POST,
                    deadline=60,
                    validate_certificate=False)

    if fetch_result.status_code == 200:
        json_result = json.loads(fetch_result.content)

        return {'score':json_result['documentSentiment']['score'],
                    'magnitude':json_result['documentSentiment']['magnitude']}


if __name__ == "__main__":
    apikey ='place gnl_apikey'

    query = datastores.Entries.gql('ORDER BY hotentry_check_time DESC , score_check_time ASC')
    entry = query.get()
    if entry:
        hatebuapi_result = call_hatebuapi(entry.entry_url)
        gnlapi_result = call_gnlapi(hatebuapi_result['comments'],apikey)

        entry.entry_title = hatebuapi_result['title']
        entry.bukuma_count = int(hatebuapi_result['count'])
        entry.bukuma_url = hatebuapi_result['entry_url']
        entry.score = int(float(gnlapi_result['score']) * 100)
        entry.magnitude = int(gnlapi_result['magnitude'])
        entry.score_check_time = datetime.datetime.today()
        entry.put()