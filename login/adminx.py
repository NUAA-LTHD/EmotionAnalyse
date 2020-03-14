import xadmin
from .models import users
class UsersAdmin(object):
    list_display=['username','nickname','status']
    search_fields = ['username', 'nickname']
    list_display_links=['username','nickname']#指定哪些可进入编辑
    list_editable=['status']
    readonly_fields=['username','nickname','email']
    exclude=['password']#隐藏字段
    ordering=['username']#排序
xadmin.site.register(users,UsersAdmin)