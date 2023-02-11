from django.db import models


class User(models.Model):
    uid = models.IntegerField(primary_key=True, unique=True)
    nickname = models.CharField(max_length=50)
    server = models.CharField(max_length=50)

    def __str__(self):
        return self.nickname
