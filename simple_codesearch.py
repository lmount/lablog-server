#!/usr/bin/env python
from __future__ import print_function  # In python 2.7
import sys
from flask import Flask, render_template, request, \
    redirect, url_for, abort, session, Markup, jsonify
from subprocess import Popen, PIPE
import lablog_search as labs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D'


def search_source_code(key):
    results = "<br\><br\>".join(labs.search_for_keyword(key))
    return unicode(results)


@app.route('/')
def home():
    return render_template('index.html')


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
    if request.method == 'POST':
        session['message'] = search_source_code(request.form['query'])
        return render_template('index.html', message=session['message'],
                               query=request.form['query'])
    else:
        return render_template('index.html')


@app.route('/rebuild', methods=['POST'])
def rebuild():
    labs.compile_mds_in_lablog()
    return render_template('index.html', message="Database rebuild.")


if __name__ == '__main__':
    app.run(debug=True)
