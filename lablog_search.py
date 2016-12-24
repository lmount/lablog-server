#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Searches the list of markdown files for entries.


"""
import json
from glob import glob
from renderers import *

ENTRIES = []


def read_config():
    with open('config-sample.json') as f:
        config = json.load(f)
    return config


def compile_mds_in_lablog():
    global ENTRIES
    ENTRIES = []
    config = read_config()
    for repo in config['repositories']:
        if repo['active']:
            renderer = type_to_renderer[repo['type']]
            path = repo['path']
            ENTRIES += compile_paths_to_entries(path, renderer)
    return ENTRIES


def search_for_keyword(keys):
    keywords = keys.split()

    def has_key(entry):
        """For example: key='tag:python title:string' """
        k = key.split(':')
        if len(k) != 2:
            isInTitle = (key.lower() in entry['title'].lower())
            isInTags = (key.lower() in entry['tags'].lower())
        elif k[0].lower() == 'title':
            isInTitle = (k[1].lower() in entry['title'].lower())
            isInTags = False
        elif k[0].lower() == 'tag':
            isInTitle = False
            isInTags = (k[1].lower() in entry['tags'].lower())
        else:
            isInTitle = (key.lower() in entry['title'].lower())
            isInTags = (key.lower() in entry['tags'].lower())
        return isInTitle or isInTags
    entries = ENTRIES
    for key in keywords:
        entries = filter(has_key, entries)
    return entries


if __name__ == '__main__':
    compile_mds_in_lablog()
