import string
from random import random

from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from json import JSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web.models import Expenses, User, Income, Tokens, Passwordresetcodes
from datetime import datetime
from random import choice


# from utils import grecaptcha_verify
@csrf_exempt
def submit_expense(request):
    date, this_user, amount, name = read_post_income_expense(request)
    Expenses.objects.create(name=name, amount=amount, user=this_user, date=date)
    return JsonResponse({
        'status': 'ok'

    }, encoder=JSONEncoder)


# def grecaptcha_verify(request):
#     #logger.debug("def grecaptcha_verify: " + format(request.POST))
#     data = request.POST
#     captcha_rs = data.get('g-recaptcha-response')
#     url = "https://www.google.com/recaptcha/api/siteverify"
#     params = {
#         'secret': settings.RECAPTCHA_SECRET_KEY,
#         'response': captcha_rs,
#         'remoteip': get_client_ip(request)
#     }
#     verify_rs = requests.get(url, params=params, verify=True)
#     verify_rs = verify_rs.json()
#     return verify_rs.get("success", False)


@csrf_exempt
def submit_income(request):
    date, this_user, amount, name = read_post_income_expense(request)
    Income.objects.create(name=name, amount=amount, user=this_user, date=date)
    return JsonResponse({
        'status': 'ok'

    }, encoder=JSONEncoder)


def read_post_income_expense(request):
    # TODO: validate input data, handle exceptions
    this_token = request.POST['token']
    user = User.objects.filter(tokens__token=this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()
    else:
        date = request.POST['date']
    amount = request.POST['amount']
    name = request.POST['name']
    return date, user, amount, name


def get_random_string(n):
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_string = ''.join(choice(characters) for _ in range(n))
    return random_string


# if "requestcode' in request.POST:
# ipdb install
# import ipdb
# ipdb.set_trace()

def register(request):
    # import pdb
    # pdb.set_trace()
    if 'requestcode' in request.POST:  # form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        #     # is this spam? check reCaptcha
        #     if not grecaptcha_verify(request):  # captcha was not correct
        #         # TODO: forgot password
        #         return render(request, 'register.html')

        if User.objects.filter(email=request.POST['email']).exists():  # duplicate email
            context = {
                'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'register.html', context)

        if not User.objects.filter(username=request.POST['username']).exists():  # if user does not exists
            code = get_random_string(64)
            now = datetime.now()
            email = request.POST['email']
            password = make_password(request.POST['password'])
            username = request.POST['username']
            # TODO: encrypt the password and then save it in password db, and you should make a password db as well
            temporarycode = Passwordresetcodes(email=email, time=now, code=code, username=username, password=password)
            temporarycode.save()
            #TODO: you should email this code
            message = "{}?code={}&email={}".format(
                request.build_absolute_uri('/accounts/register/'), code, email)
            context = {
                'message': message}
            return render(request, 'login.html', context)
        else:
            context = {
                'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که '
                           'فرم ذخیره نشده. درست می شه'}  # TODO: forgot password
            # TODO: keep the form data
            return render(request, 'register.html', context)
    elif 'code' in request.GET:  # user clicked on code
        # import pdb
        # pdb.set_trace()
        email = request.GET['email']
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(
                code=code).exists():  # if code is in temporary db, read the data and create the user
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newUser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password, email=email)
            this_token = get_random_string(64)
            token = Tokens.objects.create(token=this_token, user=newUser)
            Passwordresetcodes.objects.filter(code=code).delete()  # delete the temporary activation code from db
            context = {'message': 'اکانت شما فعال شد. لاگین کنید - البته اگر دوست داشتی'}
            return render(request, 'login.html', context)
        else:
            context = {'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'login.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)
