#!/usr/bin/env python
from __future__ import print_function  # In python 2.7
import sys
from flask import Flask, render_template, request, \
    redirect, url_for, abort, session, Markup, jsonify
from subprocess import Popen, PIPE

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D'


def search_source_code(query):
    results = Popen(
        ['/usr/local/bin/ag', '--group', '--stats',
            '--ignore-dir', 'static', request.form['query']],
        # ['/usr/local/bin/ag', '--nogroup', request.form['query']],
        stdout=PIPE
    ).communicate()[0]
    return results


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


if __name__ == '__main__':
    app.run(debug=True)
