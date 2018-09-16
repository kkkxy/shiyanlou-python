#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)


app.config['TEMPLATES_AUTO_RELOAD'] =True
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/news',
    SQLALCHEMY_TRACK_MODIFICATIONS=False ))
db = SQLAlchemy(app)
client = MongoClient('127.0.0.1', 27017).news



class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80), unique = True)
    create_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', uselist = False)
    content = db.Column(db.Text)

    def __init__(self, id, title, create_time, category, content):
        self.title = title
        self.create_time = create_time
        self.category = category
        self.content = content
        self.id = id

    def add_tag(self, tag_name):
        file_item = client.files.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']
            if tag_name not in tags:
                tags.append(tag_name)
                client.files.update_one({'file_id': self.id}, {'$set': {'tags': tags}})
        else:
            tags = [tag_name]
            client.files.insert_one({'file_id': self.id, 'tags': tags})
        return tags

                                                                        
    def remove_tag(self, tag_name):
        file_item = client.files.find_one({'file_id': self.id})
        if file_item:
            tags = file_item['tags']
            try:
                tags.remove(tag_name)
                new_tags = tags
            except ValueError:                 
                return tags
            client.files.update_one({'file_id': self.id}, {'$set': {'tags': new_tags}})
            return new_tags

    @property
    def tags(self):
        file_item = client.files.find_one({'file_id': self.id})
        if file_item:
            return file_item['tags']
        else:
            return []

'''
    def add_tag(self, tag_name):
        if client.files.find_one({"file_id":self.id, "tagname":tag_name}) is None:
            tags = client.files.insert_one({"file_id":self.id, "tagname":tag_name})
            return tags
        else:
            pass

    def remove_tag(self, tag_name):
        if client.files.find_one({"file_id":self.id, "tagname":tag_name}) is None:
            pass

        else:
            tags = client.files.update({"file_id":self.id},{"$unset":{"tagname":tag_name}})
        return tags
                    
    @property
    def tags(self):
        for item in client.files.find({"file_id":self.id}):
            print(item)
'''

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    files = db.relationship('File')

    def __init__(self, name):
        self.name = name


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
    app.run()

