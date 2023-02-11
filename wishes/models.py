from django.db import models


class Wish(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    banner_type = models.IntegerField()
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    rarity = models.IntegerField()
    time = models.DateTimeField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
