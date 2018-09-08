#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template
import os, json, os.path

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] =True


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    for files in os.walk('/home/shiyanlou/files'):
        filelist = files[2]

    return render_template('index.html', filelist = filelist)
 


@app.route('/files/<filename>')
def file(filename):
    filepath =''.join(['/home/shiyanlou/files/', str(filename),'.json'])
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
        return render_template('file.html', data=data)
    
    else:
        abort(404)

if __name__ == '__main__':
    app.run()

