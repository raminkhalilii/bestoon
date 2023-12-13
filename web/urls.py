from . import views
from django.urls import re_path as url

urlpatterns = [
    url(r'^submit/expense/$', views.submit_expense, name='submit expense'),
    url(r'^submit/income/$', views.submit_income, name='submit income')
]
