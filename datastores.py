#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Entries(db.Model):
  entry_url = db.StringProperty()
  entry_title = db.StringProperty()
  bukuma_count = db.IntegerProperty()
  bukuma_url = db.StringProperty()
  score = db.IntegerProperty()
  magnitude = db.IntegerProperty()
  hotentry_check_time = db.DateTimeProperty()
  score_check_time = db.DateTimeProperty()