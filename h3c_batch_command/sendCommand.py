#coding:utf-8
import pexpect

#家居店交换机
def getSN_JIAJU(device_ip):
    print("Num: %d\r\n" % (len(device_ip)))
    for ip in device_ip:
        foo = pexpect.spawn('/usr/bin/telnet %s'%(ip))
        index = foo.expect("Username:")
        foo.sendline('admin')
        foo.expect("Password:")
        foo.sendline('xxoo')
        foo.expect('>')
        foo.sendline('display device manuinfo')
        foo.expect('>')
        infomation = foo.before.decode('utf8').strip('b').split('\r\n')  #生成信息列表
        print("%s\r\n%s"%(infomation[2],infomation[3]))
        print("\r\n")

#和谐广场店交换机
def getSN_HEXIE():
    device_ip = []
    with open('hexieSwitch.txt','r') as f:
        for line in f.readlines():
            device_ip.append(line.strip('\n'))
    print("Num: %d\r\n" % (len(device_ip)))
    for ip in device_ip:
        foo = pexpect.spawn('/usr/bin/telnet %s'%(ip))
        index = foo.expect("Username:")
        foo.sendline('admin')
        foo.expect("Password:")
        foo.sendline('ysh@2015')
        foo.expect('>')
        foo.sendline('display device manuinfo')
        foo.expect('>')
        infomation = foo.before.decode('utf8').strip('b').split('\r\n')  #生成信息列表
        print("%s\r\n%s"%(infomation[2],infomation[3]))
        print("\r\n")


if __name__ == "__main__":
    DEVICE_IP_BEIYUANJIAJU = ['172.18.2.10','172.18.2.20','172.18.2.30','172.18.2.40','172.18.2.50','172.18.2.60']
    DEVICE_IP_ZHONGXINJIAJU = ['172.18.1.10', '172.18.1.11', '172.18.1.20', '172.18.1.21', '172.18.1.30', '172.18.1.31','172.18.1.40','172.18.1.41','172.18.1.50','172.18.1.51','172.18.1.60','172.18.1.61']
    # getSN_JIAJU(DEVICE_IP_BEIYUANJIAJU)
    # getSN_JIAJU(DEVICE_IP_ZHONGXINJIAJU)
    getSN_HEXIE()
