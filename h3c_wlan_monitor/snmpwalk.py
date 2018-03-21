#coding:utf-8
#Date：2017-09-06
#python Vsersion ：2.7.5
#Desc:
#	- 借用snmp服务，获取AC上各门店掉线AP情况。
#	- 以短信的方式，通知相关人员。

import netsnmp,time,os,requests
from datetime import datetime

def display(nums,names):
    #实时展示函数
    print '''
            ###############     智慧银座WLAN实时状态监控系统     ###############

            1. AP在线数统计

                和谐广场槐荫店    Online:%-10d    Offline:%-10d

                银座家居中心店    Online:%-10d    Offline:%-10d

                银座家居北园店    Online:%-10d    Offline:%-10d

            2. 离线AP清单

                和谐广场槐荫店\n\t\t     %s

                银座家居中心店\n\t\t     %s

                银座家居北园店\n\t\t     %s

             ###################     %-20s    ###################

    '''%(nums[0][0],nums[0][1],nums[1][0],nums[1][1],nums[2][0],nums[2][1],names[0],names[1],names[2],datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S"))

def getData():
    oid_dic = {
        'apName':'.1.3.6.1.4.1.2011.10.2.75.4.3.10.1.4',
        'apAssociateStatus': '.1.3.6.1.4.1.2011.10.2.75.2.1.10.1.7'
    }
    session = netsnmp.Session(Version=2, DestHost='172.31.1.2', Community='xxoo')
    res = []
    for key in oid_dic:
        Varlist = netsnmp.VarList()
        Varlist.append(netsnmp.Varbind(oid_dic[key]))  # 把oid转换成varlist，snmp session支持的类型
        res.append(session.walk(Varlist)) # 执行walk，得到结果元组
    apName,apAssociateStatus = res[0],res[1]
    apName_hx = [apname for apname in apName if str(apname).startswith("jn_hx")]
    apName_yzjj_zx = [apname for apname in apName if str(apname).startswith("jn_yzjj-zx")]
    apName_yzjj_by = [apname for apname in apName if str(apname).startswith("jn_yzjj-by")]

    apName_offline = [apInfo[0] for apInfo in zip(apName,apAssociateStatus) if apInfo[1] == '2']
    apName_hx_offline = [apname for apname in apName_offline if str(apname).startswith("jn_hx")]
    apName_yzjj_zx_offline = [apname for apname in apName_offline if str(apname).startswith("jn_yzjj-zx")]
    apName_yzjj_by_offline = [apname for apname in apName_offline if str(apname).startswith("jn_yzjj-by")]

    ap_status_num = [((len(apName_hx) - len(apName_hx_offline)),len(apName_hx_offline)),\
                 ((len(apName_yzjj_zx) - len(apName_yzjj_zx_offline)),len(apName_yzjj_zx_offline)),\
                 ((len(apName_yzjj_by) - len(apName_yzjj_by_offline)),len(apName_yzjj_by_offline))]
    ap_status_name = [apName_hx_offline,apName_yzjj_zx_offline,apName_yzjj_by_offline]
    return ap_status_num,ap_status_name

def sendMessage(message_hexie,message_all):
    phones_hexie = ['13853184270', '13969088896', '18615238050']
    for phone in phones_hexie:
        payload = {
            'send': 'send',
            'phone': phone,
            'content': message_hexie
        }
        url = "http://192.168.103.132/yinzuosmszhuan/sendsms.php"
        response = requests.get(url, params=payload)
    phones_yzysh = ['18668920289', '18668925892']
    for phone in phones_yzysh:
        payload = {
            'send': 'send',
            'phone': phone,
            'content': message_all
        }
        url = "http://192.168.103.132/yinzuosmszhuan/sendsms.php"
        response = requests.get(url, params=payload)

if __name__ == "__main__":
    try:
        # while True:
        #     ap_status_num,ap_status_name = getData()
        #     os.system('clear')
        #     display(ap_status_num,ap_status_name)
        #     # 增加发送短信给和谐广场
        #     message = "Time:%s .\n offline:%s"%(datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S"),ap_status_name[0])
        #     print message
        #     sendMessage(message)
        #     time.sleep(600)
        ap_status_num, ap_status_name = getData()
        # os.system('clear')
        # display(ap_status_num,ap_status_name)
        # 增加发送短信给和谐广场
        message_hexie = '''
       Time:%s
       门店:和谐广场
       Online:%d, Offline:%d
       离线AP清单:%s
            '''%(datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S"),\
                 ap_status_num[0][0],ap_status_num[0][1],str(','.join(ap_status_name[0])).replace("jn_hx_",""))
        message_yzjj_zx = '''
       门店:银座家居中心店
       Online:%d, Offline:%d
       离线AP清单:%s
                   ''' % (ap_status_num[1][0], ap_status_num[1][1], str(','.join(ap_status_name[1])).replace("jn_yzjj-zx_",""))
        message_yzjj_by = '''
      门店:银座家居北园店
      Online:%d, Offline:%d
      离线AP清单:%s
                          ''' % (ap_status_num[2][0], ap_status_num[2][1], str(','.join(ap_status_name[2])).replace("jn_yzjj-by_",""))
        sendMessage(message_hexie,(message_hexie + message_yzjj_zx + message_yzjj_by))
    except KeyboardInterrupt :
        print("正在停止服务器!!!!")
