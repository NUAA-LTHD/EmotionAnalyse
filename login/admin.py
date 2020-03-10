from django.contrib import admin
from login.models import users
# Register your models here.
class UnderwriterAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id', 'nickname', 'username',)

    # 设置哪些字段可以点击进入编辑界面，默认是第一个字段
    list_display_links = ('id','nickname')

# 注册时，在第二个参数写上 admin model
admin.site.register(users,UnderwriterAdmin)