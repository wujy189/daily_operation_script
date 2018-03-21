#-*- coding:utf-8 -*-
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *
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
#连接Hbase
def get_Data():
    transport = TSocket.TSocket('192.168.103.115', 60777)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Hbase.Client(protocol)
    transport.open()
    print client.getTableNames(),'\n'
    # print client.getColumnDescriptors('custsellday'),'\n'
    # scanner = client.scannerOpen('custsellday', '', ['info'])
    # r = client.scannerGet(scanner)
    # while r:
    #     document = dict(map(lambda (k, v): (k, v.value), r[0].columns.items()))
    #     document['info:cdmxfje'] = float(document['info:cdmxfje'])
    #     document['info:cdmselldate'] = datetime.strptime(document['info:cdmselldate'],"%Y-%m-%d %H:%M:%S.0")
    #     r = client.scannerGet(scanner)
    #     yield document
    # client.scannerClose(scanner)
    transport.close()
    # document = dict(map(lambda (k, v): (k, v.value), r[0].columns.items()))
    # return document
    # print(dic01['info:cdmxfmktname'])
    # while r:
    #     r = client.scannerGet(scanner)
    #     print r
    # while r:
    #     #printRow(r[0])
    #     r = client.scannerGet(scanner)
    # print 'scanner finished '

if __name__ == '__main__':
    # num = 500 #批量插入条数
    # documents = []
    # mongo_inst = Mongodb('127.0.0.1', 'renly', 'custsellday')
    # mongo_inst.delete_many()
    # for document in get_Data():
    #     documents.append(document)
    #     if len(documents) == num:
    #         mongo_inst.insert_many(documents)
    #         documents =[]
    #     else:
    #         pass
    # # print(get_Data().next())
    get_Data()