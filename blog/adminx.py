import xadmin
from .models import Article
class ArticleAdmin(object):
    style_fields = {'content': 'ueditor'}
xadmin.site.register(Article,ArticleAdmin)