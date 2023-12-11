from django.contrib import admin

# Register your models here.
from .models import Expenses

admin.site.register(Expenses)
