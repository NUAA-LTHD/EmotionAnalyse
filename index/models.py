from django.db import models


class emotion(models.Model):
    class Meta:
        db_table = "users"
    nickname = models.CharField(max_length=20)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=32)
    gender = models.CharField(max_length=6)
    register_date = models.DateTimeField()
