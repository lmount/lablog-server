#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description


"""
import os
import mistune as mt
from glob import glob
from bs4 import BeautifulSoup, Comment


class SimpleMarkdownCodeRenderer(mt.Renderer):
    """
    Simple Markdown file to HTML renderer
    """

    def block_code(self, code, lang):
        preCode = '\n<div class="sourceCode"><pre class="sourceCode">'
        postCode = '</pre></div>\n'
        if not lang:
            try:  # ASCII might pose problems
                html_code = '<code class="sourceCode">{}</code>'.format(
                    mt.escape(code))
            except:
                html_code = '<code class="sourceCode">{}</code>'.format(
                    mt.escape(code).encode('ascii', 'ignore'))
            return preCode + html_code + postCode
        else:
            html_code = '<code class="sourceCode {}">{}</code>'.format(
                lang, mt.escape(code))
            return preCode + html_code + postCode


class TLDRCodeRenderer(SimpleMarkdownCodeRenderer):
    """
    tldr-pages to HTML renderer
    """

    preCode = '\n<div class="sourceCode"><pre class="sourceCode">'
    postCode = '</pre></div>\n'

    def correct_for_non_block_code(self, text):
        """
        Safe removal of pre-code and post-code.
        """
        pos = text.find(self.preCode)
        while pos > -1:
            text = text[:pos] + text[pos:].replace(self.postCode, "", 1)
            text = text[:pos] + text[pos:].replace(self.preCode, "", 1)
            pos = text.find(self.preCode)
        return text

    def list_item(self, text):
        html_text = self.correct_for_non_block_code(text)
        html_text = "<li>{}</li>".format(html_text)
        return html_text

    def codespan(self, code):
        html_code = '<code class="sourceCode">{}</code>'.format(
            mt.escape(code))
        return self.preCode + html_code + self.postCode

    def block_quote(self, text):
        comment = text.strip().replace("<p>", "").replace("</p>", "")
        comment = self.correct_for_non_block_code(comment)
        ret = '<!-- tldr: ' + comment + '-->'
        # print ret
        # return ""  # unicode(ret, 'utf-8')
        return ret  # unicode(ret, 'utf-8')


type_to_renderer = dict(markdown=SimpleMarkdownCodeRenderer,
                        tldr=TLDRCodeRenderer)
"""
Type to renderer
"""


def split_entries(soup, html_token='h1', **kwargs):
    # Split all entries by "h1" headers
    h1tags = soup.find_all(html_token)
    h1entries = []
    for h1 in h1tags:
        h1entry = dict(title=h1.text, tags="")
        text = ""
        for ns in h1.nextSiblingGenerator():
            if str(ns.name) == html_token:
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


def compile_paths_to_entries(path_mask, renderer, **kwargs):
    md_renderer = renderer()
    markdown_compiler = mt.Markdown(renderer=md_renderer)

    entries = []
    for mdFile in glob(path_mask):
        with open(mdFile, 'r') as f:
            mdFilename = os.path.basename(mdFile)
            # mdContents = unicode(f.read(), "utf8")
            mdContents = f.read()
            htmlContents = markdown_compiler(mdContents)
            soup = BeautifulSoup(htmlContents, 'html.parser')
            try:
                tmpEntries = split_entries(soup,
                                           file=mdFile,
                                           filename=mdFilename,
                                           line="1",
                                           **kwargs)
                for i, entry in enumerate(tmpEntries):
                    entry['line'] = str(
                        1 + mdContents.split(entry['title'])[0].count('\n'))
            except:
                print(mdFile)
            entries += tmpEntries

    # Create entries, ready to be displayed
    entries = entries[::-1]
    return entries
