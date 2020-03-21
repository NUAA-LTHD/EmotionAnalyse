from django.db import models

# Create your models here.
class email_record(models.Model):
    class Meta:
        db_table="email_record"
    addr=models.CharField(max_length=25)
    time=models.IntegerField()
    verify_code=models.CharField(max_length=6)

class token_record(models.Model):
    class Meta:
        db_table="token_record"
    user_id=models.CharField(max_length=20)
    token1=models.CharField(max_length=40)
    time1=models.IntegerField()
    token2 = models.CharField(max_length=40)
    time2 = models.IntegerField()