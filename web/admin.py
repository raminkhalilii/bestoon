from django.contrib import admin

# Register your models here.
from .models import Expenses, Tokens,Passwordresetcodes
from .models import Income

admin.site.register(Expenses)
admin.site.register(Income)
admin.site.register(Tokens)
admin.site.register(Passwordresetcodes)

