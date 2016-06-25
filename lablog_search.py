#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Searches the list of markdown files for entries.

TODO: Move away from global parser

"""
from __future__ import print_function  # In python 2.7
import sys
from subprocess import Popen, PIPE
from glob import glob
from bs4 import BeautifulSoup, Comment

LABLOG_DIRECTORY = "/Users/lmount/Dropbox/Projects/LaBlog/"
PANDOC_PATH = "/usr/local/bin/pandoc"
HTML_FILE = LABLOG_DIRECTORY + '/lablog.html'


def html_contents():
    try:
        with open(HTML_FILE) as x:
            ret = x.read()
    except IOError:
        ret = ""
    return ret

SOUP_CONTENTS = BeautifulSoup(html_contents(), 'html.parser')


def compile_mds_in_lablog():
    markdownFiles = glob(LABLOG_DIRECTORY+"/*.md")

    results = Popen(
        [PANDOC_PATH, '--from', 'markdown_github',
         "-o", HTML_FILE] + markdownFiles,
        stdout=PIPE).communicate()[0]
    global SOUP_CONTENTS
    SOUP_CONTENTS = BeautifulSoup(html_contents(), 'html.parser')
    return results


def makeEntryHeader(headr, tags, entryString):
    return """<div class="panel panel-default">"""\
        """<div class="panel-heading"><h3>{}</h3><code>{}</code></div>"""\
        """<div class="panel-body">"""\
        """{}</div></div>""".format(
            headr, tags, entryString)


def search_for_keyword(keys):
    comments = SOUP_CONTENTS.findAll(text=lambda t: isinstance(t, Comment))
    keywords = keys.split()
    for key in keywords:
        comments = filter(lambda c: key.lower() in str(c).lower(), comments)
    entries = []
    for c in comments:
        entries += ["<p/>"]
        headr = c.parent.text
        for p in c.parents:
            if p.name in ['li']:
                entries += [str(p)]
                break
            elif p.name in ['h1', 'h2', 'h3']:
                # Find next header
                headr = p.text
                ret = ""
                for ns in p.nextSiblingGenerator():
                    if str(ns.name)[0] == 'h' and \
                       str(ns.name)[1] <= str(p.name)[1]:
                        break
                    else:
                        ret = ret + str(ns)
                entries += [str(ret)]
                break
            else:
                print("search_for_keyword:: Could not find parent",
                      file=sys.stderr)
        entries[-1] = makeEntryHeader(headr, c, entries[-1])
    return entries


if __name__ == '__main__':
    compile_mds_in_lablog()
