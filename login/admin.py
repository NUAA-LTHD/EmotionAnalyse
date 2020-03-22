# from django.contrib import admin
# from login.models import users
# # Register your models here.
# class Admin(admin.ModelAdmin):
#     list_display = ('id', 'nickname', 'username',)# 需要显示的字段信息
#     list_display_links = ('id','nickname')# 设置哪些字段可以点击进入编辑界面，默认是第一个字段
#     list_max_show_all = 10
#     list_per_page = 10  # 分页
#     search_fields = ('nickname', 'username',)  # 搜索字段
#     #list_filter = ('name', 'account', 'depart', 'publish_date')  # 过滤器
#     list_editable = ()  # 可编辑哪几个字段
#     #date_hierarchy = ''  # 头部添加  详细时间分层筛选　
#     ordering = ('id',)  # 排序
#
#
# # 注册时，在第二个参数写上 admin model
# admin.site.register(users,Admin)