#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Searches the list of markdown files for entries.


"""
from __future__ import print_function  # In python 2.7
import sys
from glob import glob
from bs4 import BeautifulSoup, Comment
import mistune as mt
from entry_types import TLDREntries, SimpleMarkdownEntries

HOME = "/Users/lmount/Dropbox/Projects/"
LABLOG_DIRECTORY = HOME + "/LaBlog/*.md"
TLDR_DIRECTORY = HOME + "/services/LaBlog_search/tldr/pages/*/*.md"

MARKDOWN_DB = [
    (LABLOG_DIRECTORY, SimpleMarkdownEntries),
    (TLDR_DIRECTORY, TLDREntries),
]

ENTRIES = []


def compile_mds_in_lablog():
    global ENTRIES
    ENTRIES = []
    for (markdownMask, reader) in MARKDOWN_DB:
        ENTRIES += reader(markdownMask)
    return ENTRIES


def search_for_keyword(keys):
    keywords = keys.split()

    def has_key(entry):
        isInTitle = (key.lower() in entry['title'].lower())
        isInTags = (key.lower() in entry['tags'].lower())
        return isInTitle or isInTags
    entries = ENTRIES
    for key in keywords:
        entries = filter(has_key, entries)
    return entries


if __name__ == '__main__':
    compile_mds_in_lablog()
