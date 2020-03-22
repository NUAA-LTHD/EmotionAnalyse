import xadmin
from .models import Article
class ArticleAdmin(object):
    style_fields = {'content': 'ueditor'}
    list_display=['title','create_date_time','auth','top']
    list_editable=['top']
    search_fields=['title']
    readonly_fields =['create_date_time','create_date','create_time','auth','title']
    ordering = ['-top','-create_date_time']
    date_hierarchy = ['create_date_time']
    list_filter = ['top','create_date_time']
xadmin.site.register(Article,ArticleAdmin)