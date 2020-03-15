import xadmin
from .models import Users
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