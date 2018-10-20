from my_site import models
from rest_framework import serializers

class CategorySerializer3(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display')
    parent_category = serializers.CharField(source="parent_category.name")
    class Meta:
        model = models.GoodsCategory
        fields = "__all__"



class CategorySerializer2(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display')
    parent_category = serializers.CharField(source="parent_category.name")
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = models.GoodsCategory
        fields = "__all__"


class CategorySerializer1(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display')
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = models.GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    catagory = serializers.CharField(source="catagory.name")
    class Meta:
        model = models.Goods
        fields = '__all__'
