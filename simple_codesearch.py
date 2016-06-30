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
    results = "<br\><br\>".join(labs.search_for_keyword(key))
    return unicode(results, "utf8")


@app.route('/')
def home():
    query = request.args.get('query')
    if query is None:
        query = request.args.get('q')
    if query is None:
        return render_template('index.html')
    else:
        message = search_source_code(query)
        session['message'] = message
        session['query'] = query
        return render_template('index.html', message=message,
                               query=query)


@app.route('/_stuff', methods=['GET', 'POST'])
def stuff():
    # print(request.form['query'], file=sys.stderr)
    if len(request.form['query']) > 3:
        session['message'] = search_source_code(request.form['query'])
    else:
        session['message'] = ""
    return jsonify(message=session['message'], query=request.form['query'])


@app.route('/signup', methods=['POST'])
def signup():
    return redirect('/?' + urllib.urlencode(request.form))


@app.route('/rebuild', methods=['POST'])
def rebuild():
    labs.compile_mds_in_lablog()
    if 'message' in session and 'query' in session:
        return render_template('index.html', message="Database rebuild." +
                               session['message'], query=session['query'])
    else:
        return redirect('/')


if __name__ == '__main__':
    labs.compile_mds_in_lablog()
    app.run(debug=True, port=5001)
