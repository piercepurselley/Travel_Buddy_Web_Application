from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from models import *
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, "assignment/index.html")

def process(request, action):
    if action == "reg":
        validate_res = User.objects.validate_reg(request.POST)
        if validate_res['status'] == "bad":
            for error in validate_res['data']:
                messages.error(request, error)
            return redirect('/')
        else:
            print validate_res
            request.session['user_id'] = validate_res['data'].id
            return redirect('/dashboard')

    elif action == "log":
        login_res = User.objects.validate_log(request.POST)
        if login_res['status'] == "bad":
            messages.error(request, login_res['data'])
            print "FUCK ME AND THE QUEEN"
            return redirect('/')
        else:
            request.session['user_id'] = login_res['data'].id
            return redirect('/dashboard')

def dashboard(request):
    if not 'user_id' in request.session:
        messages.error(request, "You are not logged in")
        print "you are not logged in"
        return redirect('/')
    else: 
        context = {
            "user" : User.objects.get(id = request.session["user_id"]),
            "products" : Product.objects.all(),
        }
        print "hey person"
        print request.session['user_id']
        return render(request, 'assignment/dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def create(request):
    if not 'user_id' in request.session:
        messages.error(request, "You are not logged in")
        print "you are not logged in"
        return redirect('/')
    else: 
        context = {
            "user" : User.objects.get(id = request.session["user_id"])
        }
    print request.session['user_id']
    return render(request, 'assignment/create.html', context)

def delete(request, product_id):
    the_product =  Product.objects.get(id = product_id)
    the_product.delete()
    return redirect('/dashboard')

def add_item(request):
    if request.method == 'POST':
        Product.objects.create(item = request.POST["item"], uploader = User.objects.get(id = request.session["user_id"]))
        return redirect('/dashboard')
    else:
        return redirect('/')
    return redirect('/dashboard') 

def item(request, product_id):
    the_product = Product.objects.get(id = product_id)
    context = {
        "product" : the_product
    }
    return render(request, 'assignment/item.html', context)
