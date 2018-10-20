from django.conf.urls import url,include
from my_site.views import account
from my_site.views import course
from my_site.views import goods
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'getgoods', goods.GetGoods)
router.register(r'getgoodscategory1', goods.GetGoodsCategory1)
router.register(r'getgoodscategory2', goods.GetGoodsCategory2)
router.register(r'getgoodscategory3', goods.GetGoodsCategory3)


urlpatterns = [

    url(r'^auth/$', account.LoginAuth.as_view()),
    url(r'^register/$', account.Register.as_view()),
    url(r'^freecourse/$', course.GetFreeCourseList.as_view()),
    url(r'^seniorcourse/$', course.GetSeniorCourseList.as_view()),
    url(r'^shoppingcar/$', account.Shopping_Car.as_view()),
    url(r'^payment/$', account.Payment.as_view()),
    url(r'^alipay/$', account.Alipay.as_view()),
    url(r'^getcode/$', account.GetCode.as_view()),
    # url(r'^getgoods/$', goods.GetGoods.as_view()),
    url('^', include(router.urls)),
    url(r'^getcomments/$', course.Comments.as_view()),
    url(r'^postcomments/$', course.Comments.as_view()),
    url(r'^test/$', account.test),
]
