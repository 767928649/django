from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from .models import *
from django.http import JsonResponse
from django.db.models import F
# Create your views here.


def detailView(request, id):
    title = '商品介绍'
    classContent = 'datails'
    commoditys = CommodityInfos.objects.filter(id=id).first()
    items = CommodityInfos.objects.exclude(id=id).order_by('-sold')[:5]
    likesList = request.session.get('likes', [])
    likes = True if id in likesList else False
    return render(request, 'details.html', locals())


def commodityView(request):
    title = '商品列表'
    classContent = 'commoditys'
    # 根据模型Types生成商品分类列表
    firsts = Type.objects.values('firsts').distinct()
    # 查询模型type的所有数据
    typesList = Type.objects.all()
    # 获取请求参数
    t = request.GET.get('t', '')  # 查询二级类型的商品信息
    s = request.GET.get('s', 'sold')  # 商品显示排序方式 若为空。则为默认值sold
    p = request.GET.get('p', 1)
    n = request.GET.get('n', '')  # 查询功能的关键词

    # 根据请求参数查询商品信息
    commodityInfos = CommodityInfos.objects.all()
    if t:
        types = Type.objects.filter(id=t).first()
        commodityInfos = commodityInfos.filter(types=types.seconds)
    if s:
        commodityInfos = commodityInfos.order_by('-' + s)
    if n:
        commodityInfos = commodityInfos.filter(name__contains=n)
    # 分页功能
    paginator = Paginator(commodityInfos, 6)
    try:
        pages = paginator.page(p)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'commodity.html', locals())


def collectView(request):
    id = request.GET.get('id', '')
    result = {"result": "已收藏"}
    likes = request.session.get('likes', [])
    print(likes)
    if id and not int(id) in likes:
        # 对商品的收藏数量执行自增加1
        CommodityInfos.objects.filter(id=id).update(likes=F('likes')+1)
        result['result'] = "收藏成功"
        request.session['likes'] = likes + [int(id)]
    else:
        CommodityInfos.objects.filter(id=id).update(likes=F('likes')-1)
        result['result'] = '取消收藏成功'
    return JsonResponse(result)

