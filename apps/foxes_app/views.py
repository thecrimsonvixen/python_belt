# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.registration_validation(request.POST)
    password = request.POST['password']
    hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        new_user = User.objects.create(firstname=request.POST["firstname"], lastname=request.POST["lastname"], email=request.POST["email"], password=hash1, birthdate=request.POST["birthdate"])
        request.session['user'] = new_user.id
        return redirect ("/home")

def login(request):
    email = request.POST['emaillogin']
    password = request.POST['passwordlogin']
    user_database = User.objects.filter(email=email)
    errors = User.objects.login_validation(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        request.session['user'] = user_database[0].id
        return redirect ("/home")

def home(request):
    
    user_id=request.session['user']
    id_info=User.objects.get(id=user_id)
    all_users = User.objects.all()
    current_user_friends = User.objects.filter(friended=request.session['user']) #add friended by instead of created by
    context={
        "current_user":id_info,
        "all_users":all_users,
        "current_user_friends":current_user_friends,
    }

    return render(request, "home.html", context)

def logout(request):
    del request.session["user"]
    return redirect("/")

def view(request, id):
    
    user_id=request.session['user']
    id_info=User.objects.get(id=user_id)
    all_users = User.objects.all()
    current_user_friends = User.objects.filter(friended=request.session['user']) #add friended_by instead of created_by
    other_user = User.objects.get(id=id) #other_user instead of current_fox
    context={
        "current_user":id_info,
        "all_users":all_users,
        "current_user_friends":current_user_friends,
        "other_user":other_user, #other_user instead of current_fox
    }
    return render(request, "view.html", context)

def friend(request, id):

    user_id=request.session['user']
    id_info=User.objects.get(id=user_id)
    other_user = User.objects.get(id=id)
    other_user.friended.add(user_id) #change liked to friended
    other_user.save()

    return redirect ("/home")

def unfriend(request,id):

    user_id=request.session['user']
    id_info=User.objects.get(id=user_id)
    other_user = User.objects.get(id=id)
    other_user.friended.remove(user_id) #change liked to friended
    other_user.save()

    return redirect ("/home")
