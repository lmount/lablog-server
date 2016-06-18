#!/usr/bin/env python
from flask import Flask, render_template, request, \
    redirect, url_for, abort, session, Markup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    from subprocess import Popen, PIPE
    session['message'] = Popen(
        ['/usr/local/bin/ag', '--group', request.form['query']],
        # ['/usr/local/bin/ag', '--nogroup', request.form['query']],
        stdout=PIPE
    ).communicate()[0]
    return render_template('index.html', message=session['message'],
                           query=request.form['query'])


if __name__ == '__main__':
    app.run(debug=True)
