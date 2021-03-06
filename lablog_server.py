#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Description


"""
import sys
from flask import Flask, render_template, request, \
    redirect, url_for, abort, session, Markup, jsonify
import keyword_search as kwsearch
import urllib


app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34PF$($e34D'


def search_source_code(key):
    results = {}
    entries = kwsearch.search_for_keyword(key)
    results['query'] = key
    # results['message'] = unicode("<br\><br\>".join(messages), "utf8")
    results['entries'] = entries
    numberOfEntries = len(entries)
    if numberOfEntries == 0:
        results['numberOfEntries'] = "No entries found"
    elif numberOfEntries == 1:
        results['numberOfEntries'] = "1 entry found"
    else:
        results['numberOfEntries'] = "{} entries found".format(numberOfEntries)
    return results


@app.route('/')
def home():
    query = request.args.get('query')
    if query is None:
        query = request.args.get('q')
    if query is None:
        return render_template('index.html')
    else:
        results = search_source_code(query)
        results['query'] = query
        session.update(results)
        return render_template('index.html', **results)


@app.route('/', methods=['POST'])
def signup():
    rqf = {}
    for k, v in request.form.iteritems():
        rqf[k] = v.encode("utf-8")
    return redirect('/?' + urllib.urlencode(rqf))


@app.route('/<query>/')
def fwd_query(query):
    return redirect('/?query=' + query)


@app.route('/rebuild', methods=['POST'])
def rebuild():
    kwsearch.compile_mds_in_lablog()
    query = session.get('query')
    if query is None:
        query = session.get('q')
    if query != "":
        formData = {"query": query.encode("utf-8")}
        redirect_url = ('/?' + urllib.urlencode(formData))
    else:
        redirect_url = ('/')
    return redirect(redirect_url)


if __name__ == '__main__':
    kwsearch.compile_mds_in_lablog()
    app.run(debug=True, port=5001)
