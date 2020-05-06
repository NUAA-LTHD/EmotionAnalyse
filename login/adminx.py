import xadmin
from .models import Users
from xadmin import views

class UsersAdmin(object):
    list_display=['username','nickname','available']
    search_fields = ['username', 'nickname']
    list_display_links=['username','nickname']#指定哪些可进入编辑
    list_editable=['available']
    readonly_fields=['username','nickname','email','register_date']
    exclude=['password']#隐藏字段
    ordering=['username']#排序
    list_filter = ['available']#过滤器
xadmin.site.register(Users,UsersAdmin)



class GlobalSetting(object):
    site_title = "心灵日记"  # 设置标题
    site_footer = "lthd"  # 设置底部文字



xadmin.site.register(views.CommAdminView, GlobalSetting)