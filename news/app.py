#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['TEMPLATES_AUTO_RELOAD'] =True
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/news',
    SQLALCHEMY_TRACK_MODIFICATIONS=False ))
db = SQLAlchemy(app)



class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    create_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category')
    def __init__(self, title, create_time, content, category):
        self.title = title
        self.content = content
        self.create_time = create_time
        self.category = category
"""  
    def __repr__(self):
        return 'file: %r' % self.title, self.create_time, self.content
"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    files = db.relationship('File', backref = 'categories')

    def __init__(self, name):
        self.name = name
''' 
    def __repr__(self):
        return 'Category:%r' % self.name

'''


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html', files=File.query.all())
 

@app.route('/files/<int:file_id>')
def file(file_id):
    file_item = File.query.get_or_404(file_id)
    return render_template('file.html', file_item=file_item)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    java = Category(id=1, name='Java')
    python = Category(id=2, name='Python')
    file1 = File(id=1, title='Hello Java', create_time=datetime.utcnow(), category_id=1, content= 'File Content _Java is cool!')
    file2 = File(id=2, title='Hello Python', create_time=datetime.utcnow(),category_id=2,  content='File Content _Python is also cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    app.run(debug=True)
