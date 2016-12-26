#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description


"""
import os
import codecs
import mistune as mt
from glob import glob
from bs4 import BeautifulSoup, Comment


class SimpleMarkdownCodeRenderer(mt.Renderer):
    """
    Simple Markdown file to HTML renderer
    """

    def block_code(self, code, lang):
        pre_code = '\n<div class="sourceCode"><pre class="sourceCode">'
        code = mt.escape(code)
        post_code = '</pre></div>\n'
        if not lang:
            lang = ""
        src = '<code class="sourceCode ' + lang + '">' + code + '</code>'
        return pre_code + src + post_code


class TLDRCodeRenderer(SimpleMarkdownCodeRenderer):
    """
    tldr-pages to HTML renderer
    """

    pre_code = '\n<div class="sourceCode"><pre class="sourceCode">'
    post_code = '</pre></div>\n'

    def correct_for_non_block_code(self, text):
        """
        Safe removal of pre-code and post-code.
        """
        pos = text.find(self.pre_code)
        while pos > -1:
            text = text[:pos] + text[pos:].replace(self.post_code, "", 1)
            text = text[:pos] + text[pos:].replace(self.pre_code, "", 1)
            pos = text.find(self.pre_code)
        return text

    def list_item(self, text):
        html_text = self.correct_for_non_block_code(text)
        html_text = "<li>" + html_text + "</li>"
        return html_text

    def codespan(self, code):
        html_code = '<code class="sourceCode">' + mt.escape(code) + '</code>'
        return self.pre_code + html_code + self.post_code

    def block_quote(self, text):
        comment = text.strip().replace("<p>", "").replace("</p>", "")
        comment = self.correct_for_non_block_code(comment)
        ret = '<!-- tldr: ' + comment + '-->'
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
        h1entry['text'] = unicode(text, "utf-8")
        h1entry.update(kwargs)
        for key, value in h1entry.items():
            h1entry[key] = value
        h1entries += [h1entry]
    return h1entries


def compile_paths_to_entries(path_mask, renderer, **kwargs):
    md_renderer = renderer()
    markdown_compiler = mt.Markdown(renderer=md_renderer)

    entries = []
    for md_file in glob(path_mask):
        with codecs.open(md_file, "r", encoding='utf-8', errors='ignore') as f:
            md_filename = os.path.basename(md_file)
            md_contents = f.read()
            html_contents = markdown_compiler(md_contents)
            soup = BeautifulSoup(html_contents, 'html.parser')
            try:
                tmp_entries = split_entries(soup,
                                            file=md_file,
                                            filename=md_filename,
                                            line="1",
                                            **kwargs)
                for i, entry in enumerate(tmp_entries):
                    entry['line'] = str(
                        1 + md_contents.split(entry['title'])[0].count('\n'))
            except:
                print("In " + md_file + " occured an error.")
            entries += tmp_entries
    # Create entries, ready to be displayed
    entries = entries[::-1]
    return entries
