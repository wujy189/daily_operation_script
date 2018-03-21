#description:
#	-针对h3c设备，自动备份脚本
#coding:utf-8

import pexpect
import time,datetime
import os,re

#tftp服务器
tftpServer = '192.168.103.137'
#备份主机列表,从数据库读取
successed_list,failed_list=[],[]

def log(data):
    filepath = "/home/log/"
    # filename = sys._getframe().f_back.f_code.co_name + ".log"
    filename = "autobackup.log"
    try:
        if os.path.exists(filepath) == False:
            os.mkdir(filepath)
            os.chdir(filepath)
        else:
            os.chdir(filepath)
        with open(filename, "a") as f:
            f.write(datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S") + '\n\t' + data + '\n')
    except:
        print("写入日志文件失败！！")

# 检查主机是否可达
def ipCheck(sysname,ip):
    if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",ip):
        if os.uname()[0] == "Linux":
            output = os.popen("/bin/ping -c 1 -W 2 %s" % (ip)).read().split(" ") #ping结果为列表
            if "0%" in output:
                info = "[%s]设备在线，开始备份"%(sysname)
            else:
                # info = "[%s]无法ping通设备，备份失败."%(sysname)
                failed_list.append(sysname)
                return
    else:
        failed_list.append(sysname)
        # info = "[%s]请检查IP地址格式."%(sysname)
        return
#h3c 设备函数
def h3c_telnet(sysname,ip):
    try:
        foo = pexpect.spawn('/usr/bin/telnet %s'% (ip))
        index = foo.expect(['sername:', 'assword:'])
        if index == 0:
            foo.sendline('backup')
            foo.expect("assword:")
            foo.sendline('backup@2017')
        elif index == 1:
            foo.sendline('backup@2017')
        foo.expect(">")
	if(ip in ['192.168.10.225','192.168.10.226']):
            foo.sendline("tftp %s put %s source interface Loop1" % (tftpServer,"startup.cfg"))
	else:
	    foo.sendline("tftp %s put %s" % (tftpServer,"startup.cfg"))
        time.sleep(5)
        os.chdir('/opt/tftpboot')
        os.popen('mv startup.cfg %s'%(sysname+'_'+str(time.strftime("%Y%m%d",time.localtime()))+".cfg"))
        foo.expect(">")
        foo.sendline("quit")
        successed_list.append(sysname)
    except:
        failed_list.append(sysname)
        foo.close()
#调用核心代码函数
def backup():
    with open('/home/hostinfo.txt','r') as f:
        for line in f.readlines():
            list = line.split()
            sysname,ip,flag = list[0],list[1],list[2]
            if flag =='Y':
                ipCheck(sysname,ip)
                h3c_telnet(sysname,ip)
    info = "备份成功:%s.\n\t 备份失败:%s"%(str(successed_list),str(failed_list))
    log(info)

if __name__ == "__main__":
    backup()
