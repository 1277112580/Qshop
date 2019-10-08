from django.urls import path ,re_path,include
from Buyer.views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/',index),
    path('logout/',logout),
    path('goods_list/',goods_list),
    re_path('detail/(?P<id>\d+)',detail),
    path('user_center_info/',user_center_info),
    path('place_order/',place_order),
    re_path('alipayviews', AlipayViews),
    path('cart/',cart),
    path('add_cart/',add_cart),
    path('payresult/',payresult),
    path('user_center_order/',user_center_order),
    path('place_oeder_more/',place_oeder_more),
]