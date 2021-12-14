from django.shortcuts import render
from commodity.models import *
from django.views.generic.base import TemplateView
# Create your views here.


def indexView(request):
    # 设置网页标签内容
    title = '首页'
    # 控制网页导航栏的样式
    classContent = ''
    # 查询模型Commodity销量最好的八条数据
    commodityInfos = CommodityInfos.objects.order_by('-sold').all()[:8]
    # 查询模型Type的所有数据
    types = Type.objects.all()
    # 宝宝服饰
    cl = [x.seconds for x in types if x.first == '儿童服饰']  # 作为clothes查询条件
    clothes = CommodityInfos.objects.filter(types__in=cl).order_by('-sold')[:5]
    # 奶粉辅食
    fl = [x.seconds for x in types if x.first == '奶粉辅食']
    food = CommodityInfos.objects.filter(types__in=fl).order_by('-sold')[:5]
    # 宝宝用品
    gl = [x.seconds for x in types if x.first == '儿童用品']
    goods = CommodityInfos.objects.filter(types__in=gl).order_by('-sold')[:5]
    return render(request, 'index.html', locals())


class IndexClassView(TemplateView):
    # 设置模板文件名
    template_name = 'index.html'
    template_engine = None
    content_type = None
    extra_context = {'title': '首页', 'classContent': ''}

    # 重新定义模板上下文的获取方式
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commodityInfos'] = CommodityInfos.objects.order_by('-sold').all()[:8]
        types = Type.objects.all()
        # 宝宝服饰
        cl = [x.seconds for x in types if x.firsts == '儿童服饰']
        context['clothes'] = CommodityInfos.objects.filter(types__in=cl).order_by('-sold')[:5]
        # 奶粉辅食
        fl = [x.seconds for x in types if x.firsts == '奶粉辅食']
        context['food'] = CommodityInfos.objects.filter(types__in=fl).order_by('-sold')[:5]
        # 宝宝用品
        gl = [x.seconds for x in types if x.firsts == '儿童用品']
        context['goods'] = CommodityInfos.objects.filter(types__in=gl).order_by('-sold')[:5]
        return context

    # 定义HTTP的GET请求处理方法
    # 参数request代表HTTP请求信息
    # 若路由设有路由变量，则可从参数kwargs里获取
    def get(self, request, *args, **kwargs):
        pass
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    # 定义HTTP的POST请求处理方法
	# 参数request代表HTTP请求信息
	# 若路由设有路由变量，则可从参数kwargs里获取
    def post(self, request, *args, **kwargs):
        pass
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


def page_not_found(request):
    return render(request, '404.html', status=404)


def page_error(request):
    return render(request, '404.html', status=500)