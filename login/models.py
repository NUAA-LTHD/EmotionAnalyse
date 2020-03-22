from django.db import models


class Users(models.Model):
    class Meta:
        db_table = "users"
        verbose_name="用户"
        verbose_name_plural=verbose_name
    available=models.BooleanField(default=1,verbose_name='可用')
    nickname = models.CharField(max_length=20,null=True,verbose_name='昵称')
    username = models.CharField(max_length=15,null=True,verbose_name='用户名')
    password = models.CharField(max_length=32,null=True)
    email=models.CharField(max_length=25,null=True,verbose_name='邮箱')
    register_date = models.DateTimeField(auto_now_add=True,verbose_name='注册时间')
    def __str__(self):
        return u"{}".format(self.nickname)


