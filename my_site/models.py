from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(verbose_name="姓名", max_length=32, null=True)
    password = models.CharField(verbose_name="密码", max_length=64, null=True)
    GENDER_CHOICES = (('male', '男'), ('female', '女'))
    birthday = models.DateField(verbose_name="出生年月", max_length=64, null=True, blank=True)
    gender = models.CharField(verbose_name="性别",choices=GENDER_CHOICES, default="female", max_length=64)
    phone = models.CharField(verbose_name="手机号", max_length=11, null=True)
    email = models.EmailField(verbose_name="邮箱", max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username

class UserToken(models.Model):
    user = models.OneToOneField(to="UserInfo")
    token = models.CharField(max_length=64)


class FreeCourse(models.Model):
    name = models.CharField(max_length=32)
    img = models.CharField(max_length=32)
    price = models.CharField(max_length=32)


class SeniorCourse(models.Model):
    name = models.CharField(max_length=32)
    img = models.CharField(max_length=32)
    price = models.CharField(max_length=32)


class GoodsCategory(models.Model):
    name = models.CharField(verbose_name="商品类名",max_length=32)
    Category_Type = ((1, "一级类"), (2, "二级类"),(3, "三级类"))
    category = models.IntegerField(verbose_name="商品类录级别",choices=Category_Type,null=True )
    parent_category = models.ForeignKey(to="self",on_delete=models.CASCADE, null=True, verbose_name="父类目",related_name="sub_cat")

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Goods(models.Model):
    catagory = models.ForeignKey(to="GoodsCategory", on_delete=models.CASCADE, verbose_name="商品类别",max_length=32)
    name = models.CharField(verbose_name="商品名称",max_length=32)
    class Meta:
        verbose_name = "商品信息"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class Comments(models.Model):
    name = models.CharField(verbose_name="昵称",max_length=32,null=False)
    content = models.CharField(verbose_name="内容",max_length=100,null=False)
    time = models.CharField(max_length=32,null=True)
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name