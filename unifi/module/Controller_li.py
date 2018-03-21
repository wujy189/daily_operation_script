#encoding:utf-8
import requests
from datetime import datetime

class Controller:
    username = 'admin'
    password = '123654789'
    def auth(self,usermac_all,minutes=1440):
        LOGIN_PARAM = {'username': self.username,
                         'password': self.password
                         }
        with requests.Session() as session:
            session.verify = False
            Response_Login = session.post('https://192.168.103.201:8443/api/login',json = LOGIN_PARAM,timeout = 3)
            if Response_Login.status_code ==200:
                try:
                    for usermac in usermac_all:
                        AUTH_PARAM = {"cmd": "authorize-guest", "mac": usermac, "minutes": minutes}
                        Response_Auth = session.post('https://192.168.103.201:8443/api/s/default/cmd/stamgr',json=AUTH_PARAM)
                        HTTP_CODE = Response_Auth.status_code
                        if HTTP_CODE == 200:
                            print("%s   [%s] 授权成功,时长:%d"%(datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S"),usermac,minutes))
                        else:
                            print("%s   [%s] 授权失败" % (datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S"), usermac))
                except:
                    pass
                finally:
                    session.post('https://192.168.103.201:8443/api/logout')
