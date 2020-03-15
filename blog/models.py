from django.db import models
from DjangoUeditor.models import UEditorField
# Create your models here.

class Article(models.Model):
    class Meta:
        db_table ='Article'
        verbose_name ='文章'
        verbose_name_plural = verbose_name
    title = models.CharField(max_length=100,verbose_name='题目')
    content = UEditorField(width=600, height=300, toolbars="full", imagePath="images/", filePath="files/",
                              upload_settings={"imageMaxSize":1204000},
                              settings={}, verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发表时间')
    emotion=models.CharField(max_length=10,verbose_name='情绪' ,default='')
    depressed=models.IntegerField(default=0)
    extreme=models.IntegerField(default=0)
    top=models.BooleanField(default=False,verbose_name='置顶')
    auth=models.ForeignKey('login.Users',on_delete=models.CASCADE,verbose_name='作者',related_name='articles')
    def __str__(self):
        return u"{}".format(self.title)


