from django.db import models


class users(models.Model):
    class Meta:
        db_table = "users"
    status=models.IntegerField(default=0)
    nickname = models.CharField(max_length=20,null=True)
    username = models.CharField(max_length=15,null=True)
    password = models.CharField(max_length=32,null=True)
    email=models.CharField(max_length=25,null=True)
    register_date = models.DateTimeField(auto_now_add=True)


