# -*- coding:utf-8 -*- 
#Name:manual_author.py
#DATE：2018-01-02
#Description:
#用于手动wifi授权，基础数据来源于白名单文件wl.txt.


#encoding:utf-8
from module.Controller_li import *

def get_user_lists():
	with open('/home/unifi/data/wl.txt','r') as f:
		for line in f.readlines():
			usermac = line.split('\t')[0]
			yield usermac


if __name__=="__main__":
	c = Controller()
	c.auth(get_user_lists(),1440)