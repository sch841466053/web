from django.views.generic import View
from my_site.models import Goods, GoodsCategory
from django.shortcuts import HttpResponse
import json
from django.forms.models import model_to_dict
from django.core import serializers
from django.http import JsonResponse
from my_site.serializers.goods_serializer import GoodsSerializer,CategorySerializer1, CategorySerializer2,CategorySerializer3
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import mixins
from rest_framework import generics
#1.原生django的方式取得数据
# class GetGoods(View):
#     def get(self, request):
#         list = []
#         goods = Goods.objects.all()
#         for good in goods:
#             dict = {}
#             dict["name"] = good.name
#             dict["category"] = good.catagory.name
#             list.append(dict)
#             # print(list)
#         json_list = json.dumps(list, ensure_ascii=False)
#             # print(json_list)
#         return HttpResponse(json_list, content_type='application/json')
#         # return HttpResponse(json.dumps(list))

#2.利用django的model_to_dict 获取数据
# class GetGoods(View):
#     def get(self, request):
#         list = []
#         goods = Goods.objects.all()
#         for good in goods:
#             dict = model_to_dict(good)
#             list.append(dict)
#             # print(list)
#         json_list = json.dumps(list, ensure_ascii=False)
#             # print(json_list)
#         return HttpResponse(json_list, content_type='application/json')

#3.利用django的serializers
# class GetGoods(View):
#     def get(self, request):
#         goods = Goods.objects.all()
#         ser = serializers.serialize('json',goods)
#         print(ser)
#         dict_list = json.loads(ser)
#         print(dict_list)
#         json_list = JsonResponse(dict_list,json_dumps_params={'ensure_ascii':False},safe=False)
#         print(json_list)
#         return json_list

#4.django rest framework(Modelserializer与APIView)获取数据
# class GetGoods(APIView):
#     def get(self, request,*args,**kwargs):
#         goods = Goods.objects.all()
#         ser = GoodsSerializer(goods, many=True)
#         print(ser)
#         print(ser.data)
#
#         return Response(ser.data)
#         # return HttpResponse("111")
#         # return JsonResponse(ser.data,json_dumps_params={'ensure_ascii':False},safe=False)


#5.django rest framework(GenericView)获取数据
# class GetGoods(mixins.ListModelMixin,generics.GenericAPIView):
#             queryset = Goods.objects.all()
#             serializer_class = GoodsSerializer
#
#             def get(self, request,*args,**kwargs):
#                 return self.list(request,*args,**kwargs)

#6.优化方案5
# class GetGoods(generics.ListAPIView):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer

#7.viewsets和router完成商品列表页
from rest_framework import viewsets


class GetGoods(mixins.ListModelMixin,viewsets.GenericViewSet):

    #这里必须要定义一个默认的排序,否则会报错
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer


#获取商品一级目录分类信息
class GetGoodsCategory1(mixins.ListModelMixin,viewsets.GenericViewSet):

    queryset = GoodsCategory.objects.filter(category=1)
    serializer_class = CategorySerializer1


#获取商品二级目录分类信息
class GetGoodsCategory2(mixins.ListModelMixin,viewsets.GenericViewSet):

    queryset = GoodsCategory.objects.filter(category=2)
    serializer_class = CategorySerializer2


#获取商品三级目录分类信息
class GetGoodsCategory3(mixins.ListModelMixin,viewsets.GenericViewSet):

    queryset = GoodsCategory.objects.filter(category=3)
    serializer_class = CategorySerializer3



