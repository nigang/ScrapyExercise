# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from tutorial.items import AQIItem


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


#class AQIRecord(object):
#    def __init__(self):
#        self.conn = None
#        self.cur = None
#
#    def open_spider(self, spider):
#        self.conn = sqlite3.connect("AQIRecode.sqlite")
#        self.cur = self.conn.cursor()
#        self.cur.execute('create table if not exists aqi(updated_time date primary KEY, value text)')
#
#    def close_spider(self, spider):
#        self.conn.commit()
#        self.conn.close()
#
#    def process_item(self, item, spider):
#
#        col = ','.join(item.keys())
#        placeholder = ','.join(len(item)*'?')
#        search_aql = 'select * from lottery_rec where updated_time = ?'
#
#        if self.cur.execute(search_aql, (item.get('updated_time'),)) and self.cur.rowcount != -1:
#            update_sql = "update lottery_rec set value = '%s' where updated_time = '%s'"\
#                         % (item.get("value"), item.get("updated_time"))
#            self.cur.execute(update_sql)
#        else:
#            insert_sql = 'insert into lottery_rec({}) values({})'
#            self.cur.execute(insert_sql.format(col, placeholder), tuple(item.values()))
#        return item


class LotteryRecord(object):
    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.conn = sqlite3.connect("LotteryRecode.sqlite")
        self.cur = self.conn.cursor()
        self.cur.execute('create table if not exists lottery(date date primary KEY, '
                         'hundred varchar(1), decade varchar(1), unit varchar(1), sales text)')

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        if self.cur.execute("select * from lottery where date = '%s' " % item.get('date')).fetchall():
            return item
        col = ','.join(item.keys())
        placeholder = ','.join(len(item)*'?')
        insert_sql = 'insert into lottery({}) values({})'
        self.cur.execute(insert_sql.format(col, placeholder), tuple(item.values()))

        return item
