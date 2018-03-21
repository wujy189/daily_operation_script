#-*- coding:utf-8 -*-

from pymongo import MongoClient
from datetime import datetime

#连接Mongodb
class Mongodb:
    def __init__(self,ip,dbName,collectionName):
        try:
            client = MongoClient("mongodb://%s:27017/"%(ip))
            db = client[dbName]
            self.collection = db[collectionName]
        except:
            print ("数据库连接异常")
    def insert_one(self,document):
        self.collection.insert_one(document)
    def insert_many(self,documents):
        self.collection.insert_many(documents,ordered=False)
    #清除数据
    def delete_many(self,filter={}):
        self.collection.delete_many(filter)
    def aggregate_group(self):
        #按开卡门店编码统计笔数
        # group = {'$group': {'_id': "$info:cdmkkmktid", 'count': {'$sum': 1}}}
        # 按日期统计日消费笔数、交易金额
        group = {'$group': {'_id': { 'year': { '$year': "$info:cdmselldate"},'month': { '$month': "$info:cdmselldate" },'day': { '$dayOfMonth':"$info:cdmselldate"},},
                            'jybs': {'$sum': 1},'jyje':{'$sum':'$info:cdmxfje'}}}
        pipeline = [group]
        res = self.collection.aggregate(pipeline)
        return res

    def aggregate_count(self):
        # 按日期统计线上交易笔数、金额
        group = {'$group': {'_id': {'year': {'$year': "$info:cdmselldate"}, 'month': {'$month': "$info:cdmselldate"},
                                    'day': {'$dayOfMonth': "$info:cdmselldate"},'cdmkkmktid':'$info:cdmkkmktid' },
                            'md_jybs': {'$sum': 1},'md_jyje':{'$sum':'$info:cdmxfje'}}}
        pipeline = [group]
        res = self.collection.aggregate(pipeline)
        return res

if __name__ == '__main__':
    mongo_inst = Mongodb('127.0.0.1', 'renly', 'custsellday')
    # res = mongo_inst.aggregate_group()
    # documents = []
    # for doc in res:
    #     dic = {
    #         'date': datetime(doc['_id']['year'], doc['_id']['month'], doc['_id']['day']),
    #         'jybs':doc['jybs'],
    #         'jyje':doc['jyje']
    #     }
    #     documents.append(dic)
    # #数据入库
    # mongo_store = Mongodb('127.0.0.1', 'renly', 'daily_Stat')
    # mongo_store.delete_many()
    # mongo_store.insert_many(documents)

    #线上交易笔数、金额
    res = mongo_inst.aggregate_count()
    for doc in res:
        if doc['_id']['cdmkkmktid'] == '9998':
            print(doc)