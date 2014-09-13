#!/usr/bin/env python2.7
import os
import sys

# Set up django environment
project_directory = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = 'urlshortener.settings'
from django.conf import settings

# Load words
from urlshortener.models import DictionaryWord

with open('cleaned_words.txt') as cleaned_words:
    for word in cleaned_words:
        DictionaryWord.objects.create(word=word.rstrip())
