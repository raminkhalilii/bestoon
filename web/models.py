from django.db import models

from django.contrib.auth.models import User


class Expenses(models.Model):
    Name = models.CharField(max_length=200)
    amount = models.IntegerField
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
