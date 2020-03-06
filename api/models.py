from django.db import models

# Create your models here.
class email_record(models.Model):
    class Meta:
        db_table="email_record"
    addr=models.CharField(max_length=25)
    time=models.IntegerField()
    verify_code=models.CharField(max_length=6)