from django.contrib import admin

# Register your models here.
from .models import Expenses
from .models import Income

admin.site.register(Expenses)
admin.site.register(Income)

