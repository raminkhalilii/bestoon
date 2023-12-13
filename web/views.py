from django.shortcuts import render
from json import JSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web.models import Expenses, User, Income, Tokens
from datetime import datetime


@csrf_exempt
def submit_expense(request):
    date, this_user, amount, name = read_post_income_expense(request)
    Expenses.objects.create(name=name, amount=amount, user=this_user, date=date)
    return JsonResponse({
        'status': 'ok'

    }, encoder=JSONEncoder)


@csrf_exempt
def submit_income(request):
    date, this_user, amount, name = read_post_income_expense(request)
    Income.objects.create(name=name, amount=amount, user=this_user, date=date)
    return JsonResponse({
        'status': 'ok'

    }, encoder=JSONEncoder)


def read_post_income_expense(request):
    this_token = request.POST['token']
    user = User.objects.filter(tokens__token=this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()
    else:
        date = request.POST['date']
    amount = request.POST['amount']
    name = request.POST['name']
    return date, user, amount, name
