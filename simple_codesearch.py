#!/usr/bin/env python
from flask import Flask, render_template, request, \
    redirect, url_for, abort, session

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
        ['/usr/local/bin/ag', request.form['message']], stdout=PIPE
    ).communicate()[0]  # request.form['message']
    session['message'] = session['message'].replace('\n','<br/>')
    return redirect(url_for('message'))


@app.route('/message')
def message():
    if 'username' not in session:
        return abort(403)
    return render_template('message.html', username=session['username'],
                           message=session['message'])

if __name__ == '__main__':
    app.run(debug=True)
