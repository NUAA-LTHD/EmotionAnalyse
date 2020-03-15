from django.db import models
from DjangoUeditor.models import UEditorField
import datetime
# Create your models here.

class Article(models.Model):
    class Meta:
        db_table ='Article'
        verbose_name ='文章'
        verbose_name_plural = verbose_name
    title = models.CharField(max_length=100,verbose_name='题目')
    content = UEditorField(width=600, height=300, toolbars="full", imagePath = 'images/{}/'.format(datetime.datetime.now().strftime("%Y-%m")),\
        filePath = 'files/{}/'.format(datetime.datetime.now().strftime("%Y-%m")),
                              upload_settings={"imageMaxSize":10240000},
                              settings={}, verbose_name='内容')
    create_date_time = models.DateTimeField(auto_now_add=True, verbose_name='发表时间')
    create_date=models.DateField(auto_now_add=True)
    create_time=models.TimeField(auto_now_add=True)
    emotion=models.CharField(max_length=10,verbose_name='情绪' ,default='')
    depressed=models.IntegerField(default=0)
    extreme=models.IntegerField(default=0)
    top=models.BooleanField(default=False,verbose_name='置顶')
    auth=models.ForeignKey('login.Users',on_delete=models.CASCADE,verbose_name='作者',related_name='articles',null=True)
    def __str__(self):
        return u"{}".format(self.title)


