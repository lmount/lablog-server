#!/usr/bin/env python
from __future__ import print_function  # In python 2.7
import sys
from flask import Flask, render_template, request, \
    redirect, url_for, abort, session, Markup, jsonify
import lablog_search as labs
import urllib


app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D'


def search_source_code(key):
    results = {}
    messages = labs.search_for_keyword(key)
    results['query'] = key
    results['message'] = unicode("<br\><br\>".join(messages), "utf8")
    numberOfEntries = len(messages)
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
        session.update(results)
        return render_template('index.html', **results)


@app.route('/_stuff', methods=['GET', 'POST'])
def stuff():
    # print(request.form['query'], file=sys.stderr)
    if len(request.form['query']) > 3:
        results = search_source_code(request.form['query'])
    else:
        results = dict(message="")
    session.update(results)
    return jsonify(**results)


@app.route('/signup', methods=['POST'])
def signup():
    return redirect('/?' + urllib.urlencode(request.form))


@app.route('/rebuild', methods=['POST'])
def rebuild():
    labs.compile_mds_in_lablog()
    formData = {"q": session.get('query', "")}
    if formData['q'] != "":
        return redirect('/?' + urllib.urlencode(formData))
    else:
        return redirect('/')


if __name__ == '__main__':
    labs.compile_mds_in_lablog()
    app.run(debug=True, port=5001)
