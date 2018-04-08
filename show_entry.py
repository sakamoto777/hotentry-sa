#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import os

import datastores

class top(webapp.RequestHandler):
    def get(self):

        query1 = datastores.Entries.gql('ORDER BY hotentry_check_time DESC')
        entry1 = query1.get()

        query2 = datastores.Entries.gql('WHERE hotentry_check_time = :time ORDER BY score ASC',time=entry1.hotentry_check_time)
        entry2 = query2.fetch(50)

        yami_entries =[]
        counter = 0
        for row in entry2:
            if (row.score != None and row.score < 0):
                yami_entries.append(row)
                counter += 1
                if counter == 5:
                    break

        query3 = datastores.Entries.gql('WHERE hotentry_check_time = :time ORDER BY score DESC',time=entry1.hotentry_check_time)
        entry3 = query3.fetch(5)

        kirei_entries =[]
        for row in entry3:
            if (row.score != None and row.score >= 0):
                kirei_entries.append(row)

        query4 = datastores.Entries.gql('WHERE hotentry_check_time = :time ORDER BY magnitude DESC',time=entry1.hotentry_check_time)
        entry4 = query4.fetch(5)

        yure_entries =[]
        for row in entry4:
            if row.score != None:
                yure_entries.append(row)

        template_values = { 'yami_entries' : yami_entries,
                                         'kirei_entries' : kirei_entries,
                                         'yure_entries' : yure_entries}

        path = os.path.join(os.path.dirname(__file__), 'top.html')
        self.response.out.write(template.render(path, template_values))

class yami(webapp.RequestHandler):
    def get(self):
        query1 = datastores.Entries.gql('ORDER BY hotentry_check_time DESC')
        entry1 = query1.get()

        query2 = datastores.Entries.gql('WHERE hotentry_check_time = :time ORDER BY score ASC',time=entry1.hotentry_check_time)
        entry2 = query2.fetch(50)

        yami_entries =[]
        for row in entry2:
            if (row.score != None and row.score < 0):
                yami_entries.append(row)

        template_values = { 'yami_entries' : yami_entries}

        path = os.path.join(os.path.dirname(__file__), 'yami.html')
        self.response.out.write(template.render(path, template_values))


class kirei(webapp.RequestHandler):
    def get(self):
        query1 = datastores.Entries.gql('ORDER BY hotentry_check_time DESC')
        entry1 = query1.get()

        query2 = datastores.Entries.gql('WHERE hotentry_check_time = :time ORDER BY score DESC',time=entry1.hotentry_check_time)
        entry2 = query2.fetch(50)

        kirei_entries =[]
        for row in entry2:
            if (row.score != None and row.score >= 0):
                kirei_entries.append(row)

        template_values = { 'kirei_entries' : kirei_entries}

        path = os.path.join(os.path.dirname(__file__), 'kirei.html')
        self.response.out.write(template.render(path, template_values))


class yure(webapp.RequestHandler):
    def get(self):
        query1 = datastores.Entries.gql('ORDER BY hotentry_check_time DESC')
        entry1 = query1.get()

        query2 = datastores.Entries.gql('WHERE hotentry_check_time = :time ORDER BY magnitude DESC',time=entry1.hotentry_check_time)
        entry2 = query2.fetch(50)

        yure_entries =[]
        for row in entry2:
            if row.score != None:
                yure_entries.append(row)

        template_values = { 'yure_entries' : yure_entries}

        path = os.path.join(os.path.dirname(__file__), 'yure.html')
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication([('/', top),
                                                                    ('/yami', yami),
                                                                    ('/kirei', kirei),
                                                                    ('/yure', yure)],
                                                                    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()