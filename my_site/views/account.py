from rest_framework.views import APIView
from rest_framework.response import Response
from my_site import models
import uuid
from utils.auth import Auth
from django_redis import get_redis_connection
from utils.pay import AliPay
import time
import json
from django.conf import settings
from django.shortcuts import redirect, HttpResponse, render


class LoginAuth(APIView):
    def post(self,request, *args, **kwargs):
        print(request.data)
        ret = {"code":1000}
        user = request.data.get("user")
        pwd = request.data.get("pwd")
        obj = models.UserInfo.objects.filter(username=user,password=pwd).first()
        if not obj:
            ret["code"] = 1001
            ret["error"] = "用户名或者密码不存在"
        else:
            token = str(uuid.uuid4())
            models.UserToken.objects.update_or_create(user=obj,defaults={"token":token})
            ret["token"] = token
        return Response(ret)


class Register(APIView):
    def post(self,request,*args,**kwargs):
        ret = {"code":1000}
        print(request.data)
        username = request.data.get("user")
        password = request.data.get("pwd")
        phone = request.data.get('phone')
        gender = request.data.get('gender')
        obj = models.UserInfo.objects.filter(username=username)
        if obj:
            ret["code"] = 1001
            ret["error"] = "用户名已经存在"
            return Response(ret)
        models.UserInfo.objects.create(username=username,password=password,phone=phone,gender=gender)
        return Response(ret)


class Shopping_Car(APIView):
    authentication_classes = [Auth, ]
    conn = get_redis_connection("default")

    def post(self,request,*args,**kwargs):
        ret = {"code":1000}
        book_list = request.data.get("books")
        for book in book_list:
            book_obj = models.FreeCourse.objects.filter(name=book).first()
            if not book_obj:
                continue
            book_dict = {
                "name":book_obj.name,
                "img" :book_obj.img,
                "price":book_obj.price
            }
        # print(book_dict)
            car_key = "shopping_car_%s_%s" % (request.auth.user_id,book_obj.id)
            self.conn.hmset(car_key,book_dict)
            # ser = FreeCourseSerializer(instance=book_obj,many=False)
            # print(ser.data)
            # ret["data"].append(ser.data)
        # print(ret)
        return Response(ret)

    def get(self,request,*args,**kwargs):
        ret = {"code":1000,"data":[]}
        key_match = "shopping_car_%s_%s" % (request.auth.user_id, "*")
        car_key = self.conn.keys(key_match)
        # print(car_key)
        for key in car_key:
            info = {
                "name":self.conn.hget(key,"name").decode("utf-8"),
                "img":self.conn.hget(key,"img").decode("utf-8"),
                "price":self.conn.hget(key,"price").decode("utf-8")
            }
            ret["data"].append(info)
        # print(ret)
        return Response(ret)


class Payment(APIView):
    authentication_classes = [Auth, ]
    conn = get_redis_connection("default")

    def post(self,request,*args,**kwargs):
        del_match_key = "payment_key_%s_%s" % (request.auth.user_id, '*')
        del_key = self.conn.keys(del_match_key)
        print(del_key)
        if del_key:
            self.conn.delete(*del_key)
        print(self.conn.keys())
        ret = {"code":1000}
        book_list = request.data.get("books")
        print(book_list)
        for book in book_list:
            book_obj = models.FreeCourse.objects.filter(name=book).first()
            if not book_obj:
                continue
            book_dict = {
                "name":book_obj.name,
                "img" :book_obj.img,
                "price":book_obj.price
            }
            payment_key = "payment_key_%s_%s" % (request.auth.user_id, book_obj.id)
            self.conn.hmset(payment_key, book_dict)
            print(self.conn.keys())

        return Response(ret)

    def get(self, request, *args, **kwargs):
        print(11111111111)
        ret = {"code": 1000, "data": []}
        key_match = "payment_key_%s_%s" % (request.auth.user_id, "*")
        payment_key = self.conn.keys(key_match)
        print(9999999999)
        print(payment_key)
        for key in payment_key:
            info = {
                "name": self.conn.hget(key, "name").decode("utf-8"),
                "img": self.conn.hget(key, "img").decode("utf-8"),
                "price": self.conn.hget(key, "price").decode("utf-8")
            }
            ret["data"].append(info)
        # print(ret)
        return Response(ret)


class Alipay(APIView):
    authentication_classes = [Auth,]

    def post(self,request,*args,**kwargs):
        ret = {"code":1000}
        alipay = AliPay(
            appid=settings.APPID,
            app_notify_url=settings.NOTIFY_URL,  # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成）
            return_url=settings.RETURN_URL,  # 如果支付成功，重定向回到你的网站的地址。
            alipay_public_key_path=settings.PUB_KEY_PATH,  # 支付宝公钥
            app_private_key_path=settings.PRI_KEY_PATH,  # 应用私钥
            debug=True,  # 默认False,
        )
        money = list(request.POST)[0]
        money = float(json.loads(money)["price"])
        # money = float(request.POST.get('price'))
        # print(money,type(money))
        out_trade_no = "x2" + str(time.time())
        query_params = alipay.direct_pay(
            subject="小姐姐晚上好",  # 商品简单描述
            out_trade_no=out_trade_no,  # 商户订单号
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
        )
        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
        ret["data"] = pay_url
        return Response(ret)

from utils.getcode_sdk import REST
accountSid= '8aaf070866235bc501667678bbba2bd4'
accountToken= '510275b77fe1474cac9cdbf0459d70f9'
appId='8aaf070866235bc501667678bc0b2bda'
serverIP='app.cloopen.com'
serverPort='8883'
softVersion='2013-12-26'


def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    dict = {}
    for k, v in result.items():

        if k == 'templateSMS':
            for k, s in v.items():
                # print('%s:%s' % (k, s))
                dict[k] = s
        else:
            # print('%s:%s' % (k, v))
            dict[k] = v
    return dict

def test(request):
    if request.method == "GET":
        return render(request,'test.html')
    phone = request.POST.get('phone')
    # print(phone,type(phone))
    s = sendTemplateSMS(phone,'',1)
    print(s)
    return HttpResponse("1111")


class GetCode(APIView):
    def post(self,request,*args, **kwargs):
        ret = {"code":1000}
        phone = request.data.get("phone")
        dict = sendTemplateSMS(phone, '', 1)
        ret["data"] = dict
        # print(ret)
        return Response(ret)