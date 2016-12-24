#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Searches the list of markdown files for entries.


"""
import json
from glob import glob
from renderers import *

ENTRIES = []


def compile_mds_in_lablog():
    global ENTRIES
    ENTRIES = []
    with open('config-sample.json') as f:
        config = json.load(f)
    for repo in config['repositories']:
        if repo['active']:
            renderer = type_to_renderer[repo['type']]
            path = repo['path']
            ENTRIES += compile_paths_to_entries(path, renderer)
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
