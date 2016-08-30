#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description


"""
import mistune as mt
from glob import glob
from bs4 import BeautifulSoup, Comment


def make_entry_header(entry):
    return """<div class="panel panel-default">"""\
        """<div class="panel-heading"><h3>{headr}</h3>"""\
        """<code>{tags}</code></div>"""\
        """<div class="panel-body scrollable">"""\
        """{text}</div></div>""".format(**entry)


def split_entries_h1(soup, **kwargs):
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
                    h1entry['tags'] = h1entry.get('comment', "") + ns
        h1entry['text'] = text
        h1entries += [h1entry]
    # Create entries, ready to be displayed
    for h1entry in h1entries:
        h1entry.update(kwargs)
        h1entry['text'] = make_entry_header(h1entry)
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
            code = '<code class="sourceCode">{}</code>'.format(
                mt.escape(code))
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
        with open(mdFile) as f:
            contents = f.read()
            htmlContents = mdCompiler(contents)
            soup = BeautifulSoup(htmlContents, 'html.parser')
            entries += split_entries_h1(soup, file=mdFile, **kwargs)
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
        with open(mdFile) as f:
            contents = f.read()
            htmlContents = mdCompiler(contents)
            soup = BeautifulSoup(htmlContents, 'html.parser')
            try:
                entries += split_entries_h1(soup, file=mdFile, **kwargs)
            except:
                print(mdFile)
    entries = entries[::-1]
    return entries


"""
* Renderer
* Create Entry
"""

# TLDR
