from hashlib import md5
import base64
import datetime
import urllib.request
import json
from utils.xmltojson import xmltojson

class REST:
    AccountSid = ''
    AccountToken = ''
    AppId = ''
    SubAccountSid = ''
    SubAccountToken = ''
    ServerIP = ''
    ServerPort = ''
    SoftVersion = ''
    Iflog = True  # 是否打印日志
    Batch = ''  # 时间戳
    BodyType = 'xml'  # 包体格式，可填值：json 、xml

    # 初始化
    # @param serverIP       必选参数    服务器地址
    # @param serverPort     必选参数    服务器端口
    # @param softVersion    必选参数    REST版本号
    def __init__(self, ServerIP, ServerPort, SoftVersion):
        self.ServerIP = ServerIP
        self.ServerPort = ServerPort
        self.SoftVersion = SoftVersion

    def setAccount(self, AccountSid, AccountToken):
        self.AccountSid = AccountSid
        self.AccountToken = AccountToken

    def sendTemplateSMS(self, to, datas, tempId):

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")
        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = md5(signature.encode('utf-8')).hexdigest().upper()
        # 拼接URL
        url = "https://" + self.ServerIP + ":" + self.ServerPort + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/SMS/TemplateSMS?sig=" + sig
        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode()).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)
        # 创建包体
        b = ''
        for a in datas:
            b += '<data>%s</data>' % (a)

        body = '<?xml version="1.0" encoding="utf-8"?><TemplateSMS><datas>' + b + '</datas><to>%s</to><templateId>%s</templateId><appId>%s</appId>\
            </TemplateSMS>\
            ' % (to, tempId, self.AppId)
        if self.BodyType == 'json':
            # if this model is Json ..then do next code
            b = '['
            for a in datas:
                b += '"%s",' % (a)
            b += ']'
            body = '''{"to": "%s", "datas": %s, "templateId": "%s", "appId": "%s"}''' % (to, b, tempId, self.AppId)
        req.data = body.encode('utf-8')
        data = ''
        try:
            res = urllib.request.urlopen(req)
            data = res.read()
            res.close()

            if self.BodyType == 'json':
                # json格式
                locations = json.loads(data)
            else:
                # xml格式
                xtj = xmltojson()
                locations = xtj.main(data)
            if self.Iflog:
                self.log(url, body, data)
            return locations
        except Exception as error:
            if self.Iflog:
                self.log(url, body, data)
            return {'172001': '网络错误'}


    def setAppId(self, AppId):
        self.AppId = AppId

    def log(self, url, body, data):
        print('这是请求的URL：')
        print(url)
        print('这是请求包体:')
        print(body)
        print('这是响应包体:')
        print(data)
        print('********************************')


    def accAuth(self):
        if (self.ServerIP == ""):
            print('172004')
            print('IP为空')

        # if (self.ServerPort <= 0):
        #     print('172005')
        #     print('端口错误（小于等于0）')

        if (self.SoftVersion == ""):
            print('172013')
            print('版本号为空')

        if (self.AccountSid == ""):
            print('172006')
            print('主帐号为空')

        if (self.AccountToken == ""):
            print('172007')
            print('主帐号令牌为空')

        if (self.AppId == ""):
            print('172012')
            print('应用ID为空')

    def setHttpHeader(self, req):
            if self.BodyType == 'json':
                req.add_header("Accept", "application/json")
                req.add_header("Content-Type", "application/json;charset=utf-8")

            else:
                req.add_header("Accept", "application/xml")
                req.add_header("Content-Type", "application/xml;charset=utf-8")