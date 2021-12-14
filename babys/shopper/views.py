from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import reverse
from .form import *
from django.contrib.auth.decorators import login_required
from .models import CarInfos
from .models import OrderInfos
# from commodity.models import CommodityInfos
from django.http import JsonResponse
from .views_if import login_api
# Create your views here.
from commodity.models import CommodityInfos


def loginView(request):
    # 用户登录
    title = '用户登录'
    classContent = 'logins'
    # data = login_api(request)
    # print(data)
    if request.method == 'POST':
        infos = LoginModelForm(data=request.POST)
        data = infos.data
        username = data['username']
        password = data['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # return redirect(reverse('shopper:shopper'))
            return redirect(reverse('index:index'))
            # return HttpResponse('login success', {'username': username, 'password':password})

        else:
            state = '账号密码错误'
            return render(request, 'login.html', locals())
    else:
        infos = LoginModelForm()
    return render(request, 'login.html', locals())


def logoutView(request):
    # 抹掉session
    request.session.flush()
    # 重定向到首页
    return redirect(reverse('index:index'))


def registereView(request):
    title = '用户注册'
    classContent = 'logins'
    if request.method == 'POST':
        infos = LoginModelForm(data=request.POST)
        data = infos.data
        username = data['username']
        password = data['password']
        # print(username, password)
        if User.objects.filter(username=username):
            state = '该用户已存在！！！'
            return render(request, 'registere.html', locals())
        # if User.objects.filter(username=username):
        #     user = authenticate(username=username, password=password)
        #     if user:
        #         login(request, user)
        #         return redirect(reverse('shopper:shopper'))
        else:
            state = '注册成功'
            d = dict(username=username, password=password, is_staff=1, is_active=1)
            user = User.objects.create_user(**d)
            user.save()
    else:
        infos = LoginModelForm()
    return render(request, 'registere.html', locals())


@login_required(login_url='shopper/login.html')
def shopperView(request):
    title = '个人中心'
    classContent = 'informations'
    p = request.GET.get('p', 1)
    # 处理已支付的订单
    t = request.GET.get('t', '')
    payTime = request.session.get('payTime', '')
    if t and payTime and t == payTime:
        payInfo = request.session.get('payInfo', '')
        OrderInfos.objects.create(**payInfo)
        del request.session['payTime']
        del request.session['payInfo']
    # 根据当前用户查询用户订单信息
    orderInfos = OrderInfos.objects.filter(user_id=request.user.id).order_by('-created')
    # 分页功能
    paginator = Paginator(orderInfos, 7)
    try:
        pages = paginator.page(p)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return render(request, 'shopper.html', locals())


@login_required(login_url='/shopper/login.html')
def shopcartView(request):
    title = '我的购物车'
    classContent = 'shopcarts'
    id = request.GET.get('id', '')
    quantity = request.GET.get('quantity', 1)
    userID = request.user.id
    if id:
        CarInfos.objects.update_or_create(commodityInfos_id=id, user_id=userID, quantity=quantity)
        return redirect('shopper:shopcart')
    getUserId = CarInfos.objects.filter(user_id=userID)
    commodityDcit = {x.commodityInfos_id: x.quantity for x in getUserId}
    commodityInfos = CommodityInfos.objects.filter(id__in=commodityDcit.keys())
    return render(request, 'shopcart.html', locals())


def paysView():
    pass


def deleteAPI(request):
    result = {'state': 'success'}
    userId = request.GET.get('userId', '')
    commodityId = request.GET.get('commodityId', '')
    if userId:
        CarInfos.objects.filter(user_id=userId).delete()
    elif commodityId:
        CarInfos.objects.filter(commodityInfos_id=commodityId).delete()
    else:
        result = {'state': 'fail'}
    return JsonResponse(result)
