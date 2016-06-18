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
    session['username'] = request.form['username']
    session['message'] = Popen(
        ['/usr/local/bin/ag', '--nogroup', request.form['query']], stdout=PIPE
    ).communicate()[0]  # request.form['message']
    # session['message'] = session['message'].replace('\n','<br/>')
    # session['message'] = session['message'].replace('\n', Markup('<br />'))
    return render_template('index.html', username=session['username'],
                           message=session['message'], query=request.form['query'])
    # return redirect(url_for('message'))


if __name__ == '__main__':
    app.run(debug=True)
