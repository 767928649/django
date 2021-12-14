#!/usr/bin python3
# -*- encoding: utf-8 -*-
# @Author : Ly
# @File : urls.py
# @Time : 2020/10/28 4:52 下午
from django.urls import path
from .views import *


urlpatterns = [
    # path('', indexView, name='index'),
    path('', IndexClassView.as_view(), name='index'),
]