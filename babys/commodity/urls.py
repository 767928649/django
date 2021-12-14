#!/usr/bin python3
# -*- encoding: utf-8 -*-
# @Author : Ly
# @File : urls.py
# @Time : 2020/10/28 4:52 下午
from django.urls import path
from .views import *


urlpatterns = [
    path('.html', commodityView, name='commodity'),  # 响应commodity视图函数
    path('/.detail.<int:id>.html', detailView, name='detail'),
    path('/collect.html', collectView, name='collect'),
]

