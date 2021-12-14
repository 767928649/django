#!/usr/bin python3
# -*- encoding: utf-8 -*-
# @Author : Ly
# @File : urls.py
# @Time : 2020/10/28 4:52 下午
from django.urls import path
from .views import *


urlpatterns = [
    path('.html', shopperView, name='shopper'),
    path('/login.html', loginView, name='login'),
    path('/registere.html', registereView, name='registere'),
    path('/logout.html', logoutView, name='logout'),
    path('/shopcart.html', shopcartView, name='shopcart'),
    path('/pays.html', paysView, name='pays'),
    path('/delete.html', deleteAPI, name='delete'),
]