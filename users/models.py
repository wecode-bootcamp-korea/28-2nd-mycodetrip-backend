from django.db import models

class User(models.Model):
    email        = models.CharField(max_length=100, unique=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    name         = models.CharField(max_length=20, null=True)
    nickname     = models.CharField(max_length=50)
    kakao_id     = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'users'