from django.db import models

from django.contrib.auth.models import User


class Expenses(models.Model):
    name = models.TextField(null=True)
    amount = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Income(models.Model):
    name = models.TextField(null=True)
    amount = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Tokens(models.Model):
    token = models.TextField(max_length=48, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
