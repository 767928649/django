from django.contrib import admin
from .models import *
# Register your models here.
# 自定义title和header
admin.site.site_title = '商城后台系统'
admin.site.site_header = '后台管理系统'
admin.site.index_title = '母婴平台管理'


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = [x for x in list(Type._meta._forward_fields_map.keys())]
    search_fields = ['firsts', 'seconds']
    list_filter = ['firsts']


@admin.register(CommodityInfos)
class CommodityInfosAdmin(admin.ModelAdmin):
    # 遍历数据库所有字段展示出来
    list_display = [x for x in list(CommodityInfos._meta._forward_fields_map.keys())]
    # 在数据新增页活数据修改页面设置可编辑的字段
    # readonly_fields = ['sold']
    # 设置排序方式，['id']为升序， 降序为['-id']
    ordering = ['id']
    # 设置数据列表的没累数据是否可排序显示
    sortable_by = ['price', 'discount']
    # 为数据列表的字段id和name设置路由地址，该路由地址可进入数据修改
    # list_display_links = ['id', 'name']
    # 设置过滤器，若有外间，则应使用双下滑线连接两个模型的字段
    list_filter = ['types']
    # 在数据列表页设置每一页显示的数据量
    list_per_page = 100
    # 在数据列表页这是每一页显示的最大上限数据量
    list_max_show_all = 200
    # 为数据列表的字段name设置编辑状态
    list_editable = ['name', 'price', 'discount']
    # 设置搜索的字段
    search_fields = ['name', 'types']
    # 在数据列表这是日期选择器
    date_hierarchy = 'created'
    # 在数据修改页添加另存为功能
    save_as = True
    # 设置动作栏的位子
    actions_on_top = False
    actions_on_bottom = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'types':
            db_field.choices = [
                (x['seconds'], x['seconds'])
                for x in Type.objects.values('seconds')
            ]
        return super().formfield_for_dbfield(db_field, **kwargs)

