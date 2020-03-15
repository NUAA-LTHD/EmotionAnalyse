import xadmin
from .models import Article
class ArticleAdmin(object):
    style_fields = {'content': 'ueditor'}
    list_display=['title','auth','top']
    list_editable=['top']
    search_fields=['title']
    readonly_fields =['create_time']
    ordering = ['-top','title']
    date_hierarchy = ['create_time']
    list_filter = ['top']
xadmin.site.register(Article,ArticleAdmin)