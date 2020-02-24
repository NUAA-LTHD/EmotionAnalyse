from django.db import models

class emotion(models.Model):
     class Meta:
          db_table = "users"
     username = models.CharField(max_length=100)
     password = models.CharField(max_length=100)
     gender = models.CharField(max_length=15)
     register_date = models.DateTimeField()
