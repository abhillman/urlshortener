#!/usr/bin/env python2.7
import os
import sys

# Set up django environment
project_directory = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = 'urlshortener.settings'
from django.conf import settings
from django.db import IntegrityError

# Load words
from urlshortener.models import DictionaryWord

with open('cleaned_words.txt') as cleaned_words:
    for word in cleaned_words:
        try:
            DictionaryWord.objects.create(word=word.rstrip())
        except IntegrityError:
            print "Skipping word %s -- already loaded" % word
