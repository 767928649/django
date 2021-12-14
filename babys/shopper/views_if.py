# -*- coding: utf-8 -*-
# @Time    : 2020/12/8 5:04 下午
# @Author  : Ly
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import reverse
from .form import *
from django.contrib.auth.decorators import login_required
from .models import CarInfos
from .models import OrderInfos
from django.http import JsonResponse, HttpResponse


def login_api(request):
    if request.method == 'POST':
        infos = LoginModelForm(data=request.POST)
        data = infos.data
        username = data['username']
        password = data['password']
        # print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # return redirect(reverse('shopper:shopper'))
            return JsonResponse({'status': 200, 'message': '账号密码正确'})
            # return HttpResponse('login success', {'username': username, 'password':password})
        else:
            return JsonResponse({'status': 10001, 'message': '账号或密码错误'})
    else:
        return JsonResponse({'status': 10002, 'message': '账号输入有误！！'})