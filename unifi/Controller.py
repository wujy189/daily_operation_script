#encoding:utf-8

import requests,json

class Controller:
    username = 'admin'
    password = '123654789'
    #Login
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
    def login(self):
        LOGIN_PARAM = {'username': self.username,
                       'password': self.password
                       }
        try:
            response = self.session.post('https://192.168.103.201:8443/api/login', json=LOGIN_PARAM, timeout=3)
            return response.status_code
        except:
            return 400
    def auth(self,usermac,seconds,apmac):
            Response_Login = self.login()
            if Response_Login ==200:
                AUTH_PARAM = {"cmd": "authorize-guest", "mac": usermac, "minutes": seconds, "ap_mac": apmac}
                Response_Auth = self.session.post('https://192.168.103.201:8443/api/s/default/cmd/stamgr',json=AUTH_PARAM)
                self.session.post('https://192.168.103.201:8443/api/logout')
                return Response_Auth.status_code
            else:
                return Response_Login.status_code
    def restart_AP(self,apmac):
        Response_Login = self.login()
        if Response_Login == 200:
            RESTART_PARAM = {'mac': apmac,
                             'cmd':'restart'}
            r = self.session.post('https://192.168.103.201:8443/api/s/default/cmd/devmgr',json = RESTART_PARAM)
        else:
            print ('login error')
    def get_AP_MAC(self):
        Response_Login = self.login()
        APMAC = []
        params = ({'_depth': 2, 'test': 0})
        if Response_Login == 200:
            texts = self.session.get('https://192.168.103.201:8443/api/s/default/stat/device',data = params)
            res = json.loads(texts.text.encode('utf8')) ##unicode 转 str,str转dic
            for ap in res['data']:
                try:
                    APMAC.append(ap['vap_table'][0]['ap_mac'])
                except:
                    pass
            return APMAC
            #print res['data'][0]['vap_table'][0]['ap_mac']
            # print res['data'][1]['vap_table'][0]['ap_mac']
            # for AP in res['data']:
            #     print AP