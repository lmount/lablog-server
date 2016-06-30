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


LABLOG_DIRECTORY = "/Users/lmount/Dropbox/Projects/LaBlog/*.md"
TLDR_DIRECTORY = """/Users/lmount/Dropbox/Projects/services/"""\
    """LaBlog_search/tldr/pages/*/*.md"""
MARKDOWN_DIRECTORIES = [LABLOG_DIRECTORY, TLDR_DIRECTORY]
ENTRIES = []


class HighlightRenderer(mt.Renderer):

    def block_code(self, code, lang):
        preCode = '\n<div class="sourceCode"><pre class="sourceCode">'
        postCode = '</pre></div>\n'
        if not lang:
            code = '<code class="sourceCode">{}</code>'.format(
                mt.escape(code))
            return preCode + code + postCode
        else:
            preCode = '\n<div class="sourceCode"><pre class="sourceCode">'
            postCode = '</pre></div>\n'
            code = '<code class="sourceCode {}">{}</code>'.format(
                lang, mt.escape(code))
            return preCode + code + postCode


def make_entry_header(headr, tags, entryString):
    return """<div class="panel panel-default">"""\
        """<div class="panel-heading"><h3>{}</h3><code>{}</code></div>"""\
        """<div class="panel-body">"""\
        """{}</div></div>""".format(
            headr, tags, entryString)


def create_entries(soup):
    # Split all entries by "h1" headers
    h1tags = soup.find_all('h1')
    h1entries = []
    for h1 in h1tags:
        h1entry = dict(headr=h1.text, tags="")
        text = ""
        for ns in h1.nextSiblingGenerator():
            if str(ns.name) == 'h1':
                break
            else:
                if not isinstance(ns, Comment):
                    text = text + str(ns)
                else:
                    h1entry['tags'] = h1entry.get('comment', "") + str(ns)
        h1entry['text'] = text
        h1entries += [h1entry]
    # Create entries, ready to be displayed
    for h1entry in h1entries:
        h1entry['text'] = make_entry_header(
            h1entry['headr'], h1entry['tags'], h1entry['text'])
    return h1entries


def compile_mds_in_lablog():
    renderer = HighlightRenderer()
    mdCompiler = mt.Markdown(renderer=renderer)

    markdownFiles = []
    for markdownDir in MARKDOWN_DIRECTORIES:
        markdownFiles += glob(markdownDir)

    contents = ""
    for mdFile in markdownFiles:
        with open(mdFile) as f:
            contents = contents + '\n' + f.read()
    htmlContents = mdCompiler(contents)
    soup = BeautifulSoup(htmlContents, 'html.parser')
    global ENTRIES
    ENTRIES = create_entries(soup)
    return


def search_for_keyword(keys):
    keywords = keys.split()

    def has_key(entry):
        isInHeadr = (key.lower() in entry['headr'].lower())
        isInTags = (key.lower() in entry['tags'].lower())
        return isInHeadr or isInTags
    entries = ENTRIES
    for key in keywords:
        entries = filter(has_key, entries)
    entries = map(lambda x: x['text'], entries)
    return entries


if __name__ == '__main__':
    compile_mds_in_lablog()
