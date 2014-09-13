#!/usr/bin/env python2.7
"""
Takes a text file with one line per word and prints out
the inputted text file (not in order) with all the words
lowercase -- with duplicate words removed and only with
words that have alphanumeric or underscore characters.
"""
import re
import sys

if len(sys.argv) != 2:
    print "Usage: %s words_list" % sys.argv[0]

seen_words = set()
with open(sys.argv[1]) as words_file:
    for word in words_file:
        # Check to make sure word is only alphanumeric characters
        if re.findall(r'^[a-zA-Z0-9]+$', word):
            seen_words.add(word.rstrip().lower())

for word in seen_words:
    print word
