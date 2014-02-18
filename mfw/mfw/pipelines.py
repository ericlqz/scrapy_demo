# -*- coding: utf-8 -*-
import sqlite3
from os import path
 
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
 
class MfwPipeline(object):
    filename = 'data.sqlite'
 
    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)
 
    def process_item(self, item, spider):
        print 'MfwPipeline store item: %s' % item['tid']
        cursor = self.conn.cursor()
        cursor.execute('select * from post where tid=?', (item['tid'],))
        data = cursor.fetchone()
        if None != data:
            item['content'] = data[4] + ' + ' + item['content']
            cursor.execute('update post set content=? where tid=?', (item['content'], item['tid']))
            print 'update item: %s' % item['tid']
        else:
            cursor.execute('insert into post values(?,?,?,?,?)', (item['tid'], item['uid'], item['title'], item['author'], item['content']))
            print 'insert item: %s' % item['tid']

        return item
 
    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)
 
    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None
 
    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""create table post (tid text primary key, uid text, title text, author text, content text)""")
        conn.commit()
        return conn
