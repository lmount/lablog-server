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

LABLOG_DIRECTORY = "/Users/lmount/Dropbox/Projects/LaBlog/*.md"
TLDR_DIRECTORY = """/Users/lmount/Dropbox/Projects/services/"""\
    """LaBlog_search/tldr/pages/*/*.md"""
EAL_DIRECTORY = "/Users/lmount/EAL_S02/mier/md_notes/*.md"

MARKDOWN_DB = [
    (LABLOG_DIRECTORY, SimpleMarkdownEntries),
    (TLDR_DIRECTORY, TLDREntries),
    (EAL_DIRECTORY, SimpleMarkdownEntries),
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
        isInHeadr = (key.lower() in entry['headr'].lower())
        isInTags = (key.lower() in entry['tags'].lower())
        return isInHeadr or isInTags
    entries = ENTRIES
    for key in keywords:
        entries = filter(has_key, entries)
    return entries


if __name__ == '__main__':
    compile_mds_in_lablog()
