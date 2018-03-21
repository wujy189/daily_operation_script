# -*- coding:utf-8 -*- 

#DATE：2017-11-30
#Description:
#	用于自动重启uap，解决portal授权时间结束后，再次连接AP，会提示为授权用户，接着自动下线，触发认证.


from Controller import *

if __name__=="__main__":
	#APMAC = ['04:18:d6:00:70:db']
	c = Controller()
	# for apmac in APMAC:
	# 	c.restart_AP(apmac)
	APMAC = c.get_AP_MAC()
	for apmac in APMAC:
		c.restart_AP(apmac)