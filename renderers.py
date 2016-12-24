#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description


"""
import os
import mistune as mt
from glob import glob
from bs4 import BeautifulSoup, Comment


def split_entries_h1(soup, **kwargs):
    # Split all entries by "h1" headers
    h1tags = soup.find_all('h1')
    h1entries = []
    for h1 in h1tags:
        h1entry = dict(title=h1.text, tags="")
        text = ""
        for ns in h1.nextSiblingGenerator():
            if str(ns.name) == 'h1':
                break
            else:
                if not isinstance(ns, Comment):
                    text = text + str(ns)
                else:
                    h1entry['tags'] = h1entry.get('comment', "") + ns
        h1entry['text'] = text
        h1entry.update(kwargs)
        for key, value in h1entry.items():
            h1entry[key] = value.decode('utf-8')
        h1entries += [h1entry]
    return h1entries


"""
Simple Markdown files
-----------------
"""


class SimpleMarkdownCodeRenderer(mt.Renderer):

    def block_code(self, code, lang):
        preCode = '\n<div class="sourceCode"><pre class="sourceCode">'
        postCode = '</pre></div>\n'
        if not lang:
            try:  # ASCII might pose problems
                code = '<code class="sourceCode">{}</code>'.format(
                    mt.escape(code))
            except:
                code = '<code class="sourceCode">{}</code>'.format(
                    mt.escape(code).encode('ascii', 'ignore'))
            return preCode + code + postCode
        else:
            code = '<code class="sourceCode {}">{}</code>'.format(
                lang, mt.escape(code))
            return preCode + code + postCode


def SimpleMarkdownEntries(pathMask, **kwargs):
    renderer = SimpleMarkdownCodeRenderer()
    mdCompiler = mt.Markdown(renderer=renderer)

    entries = []
    for mdFile in glob(pathMask):
        mdFilename = os.path.basename(mdFile)
        with open(mdFile, 'r') as f:
            mdContents = unicode(f.read(), "utf8")
            htmlContents = mdCompiler(mdContents)
            soup = BeautifulSoup(htmlContents, 'html.parser')
            tmpEntries = split_entries_h1(soup,
                                          file=mdFile,
                                          filename=mdFilename,
                                          line="1",
                                          **kwargs)

            for i, entry in enumerate(tmpEntries):
                entry['line'] = str(
                    1 + mdContents.split(entry['title'])[0].count('\n'))
            entries += tmpEntries
    # Create entries, ready to be displayed
    entries = entries[::-1]
    return entries


"""
tldr Entries
-----------------
"""


class TLDRCodeRenderer(SimpleMarkdownCodeRenderer):

    def codespan(self, code):
        preCode = '\n<div class="sourceCode"><pre class="sourceCode">'
        postCode = '</pre></div>\n'
        code = '<code class="sourceCode">{}</code>'.format(
            mt.escape(code))
        return preCode + code + postCode

    def block_quote(self, text):
        comment = text.strip().replace("<p>", "").replace("</p>", "")
        ret = '<!-- tldr: ' + comment + ' -->'
        # print ret
        # return ""  # unicode(ret, 'utf-8')
        return ret  # unicode(ret, 'utf-8')


def TLDREntries(pathMask, **kwargs):
    renderer = TLDRCodeRenderer()
    mdCompiler = mt.Markdown(renderer=renderer)

    entries = []
    for mdFile in glob(pathMask):
        with open(mdFile, 'r') as f:
            mdFilename = os.path.basename(mdFile)
            mdContents = f.read()
            htmlContents = mdCompiler(mdContents)
            soup = BeautifulSoup(htmlContents, 'html.parser')
            try:
                entries += split_entries_h1(soup,
                                            file=mdFile,
                                            filename=mdFilename,
                                            line="1",
                                            **kwargs)
            except:
                print(mdFile)
    entries = entries[::-1]
    return entries
