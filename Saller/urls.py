from django.urls import path ,re_path,include
from Saller.views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/',index),
    path('logout/',logout),
    path('goods_list/',goods_list),
    # 商品状态页面路由
    re_path('goods_list/(?P<status>[01])/(?P<page>\d+)',goods_list),
    # 商品操作路由
    re_path('goods_status/(?P<status>\w+)/(?P<id>\d+)',goods_status),
    path('personal_info/',personal_info),
    path('goods_add/',goods_add),


]