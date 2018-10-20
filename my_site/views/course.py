from rest_framework.views import APIView
from django.shortcuts import HttpResponse, redirect
from rest_framework.response import Response
from my_site import models
from my_site.serializers.course_serializer import FreeCourseSerializer, SeniorCourseSerializer
from utils.auth import Auth
from django_redis import get_redis_connection
import datetime
from my_site.serializers.comment_serializer import CommentsSerializer

class GetFreeCourseList(APIView):

    def get(self,request,*args,**kwargs):
        ret = {"code":1000}
        queryset = models.FreeCourse.objects.all()
        ser = FreeCourseSerializer(instance=queryset,many=True)
        ret["data"] = ser.data
        # print(ret)
        return Response(ret)


class GetSeniorCourseList(APIView):
    authentication_classes = [Auth, ]

    def get(self,request,*args,**kwargs):

        ret = {"code":1000}
        queryset = models.SeniorCourse.objects.all()
        ser = SeniorCourseSerializer(instance=queryset,many=True)
        ret["data"] = ser.data
        # print(ret)
        return Response(ret)


class Comments(APIView):
    authentication_classes = [Auth, ]
    def get(self,request,*args,**kwargs):
        ret = {"code":1000}
        queryset = models.Comments.objects.all()
        ser = CommentsSerializer(queryset,many=True)
        ret["data"] = ser.data
        return Response(ret)

    def post(self,request,*args,**kwargs):
        ret = {"code": 1000}
        name = request.data.get("name")
        content = request.data.get("textarea")
        time = str(datetime.datetime.now()).split(".")[0]
        models.Comments.objects.create(name=name,content=content,time=time)
        queryset = models.Comments.objects.all()
        ser = CommentsSerializer(queryset,many=True)
        ret["data"] = ser.data
        return Response(ret)


# def Index(request):
#     return HttpResponse("123")

from utils.weibo_sdk import APIClient

APP_KEY = "2503730139"
APP_SECRET = "bcac17f961b0d1f5f4c12cd57a015173"
CALLBACK_URL = 'http://127.0.0.1:8000/callback/'
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

class WeiBoLogin(APIView):
    def get(self,request,*args,**kwargs):
        ret = {"code":1000}
        url = client.get_authorize_url()
        ret["data"] = url
        print(ret)
        return Response(ret)
    # return redirect(client.get_authorize_url())


def Callback(request):
    code = request.GET.get("code")
    r = client.request_access_token(code)
    print(r)
    user = r["uid"]
    token = r["access_token"]
    print(user,token)
    # models.UserToken.objects.update_or_create(user=obj, defaults={"token": token})
    # ret["token"] = token
    return redirect("http://127.0.0.1:8080/index/")


