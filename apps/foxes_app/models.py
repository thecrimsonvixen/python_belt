# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import bcrypt, re, datetime
from django import forms

# Create your models here.

class UserManager(models.Manager):
    
    def registration_validation(self, post_data):
        email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        firstname = post_data['firstname']
        lastname = post_data['lastname']
        email = post_data['email']
        password = post_data['password']
        passwordverify = post_data['passwordverify']
        birthdate = post_data['birthdate']
        user_database = User.objects.filter(email=email)
        
        errors = []
        if len(firstname) < 2:
            errors.append("Make sure your name is at least two characters long!")

        if len(lastname) < 2:
            errors.append("Make sure your alias is at least two characters long!")

        if not email_regex.match(post_data['email']):
            errors.append("Make sure you enter a valid email address!")

        if len(password) < 8:
            errors.append("Make sure your password is at least 8 characters long!")

        if passwordverify != password:
            errors.append("Make sure you enter the same password both times!")

        if birthdate == 0:
            errors.append("Make sure you select a date of birth.")
        
        if unicode(datetime.datetime.now()) <= birthdate:
            errors.append("Your birthdate must be today's date or earlier.")

        if user_database.count() > 0:
            errors.append("This email is already in use! Please use another email address to register.")

        return errors

    def login_validation(self, post_data):
        email = post_data['emaillogin']
        password = post_data['passwordlogin']
        user_database = User.objects.filter(email=email)
        errors = []
       
        if len(password) < 8:
            errors.append("Make sure your password is at least 8 characters long!")

        if user_database.count() == 0:
            errors.append("Email not found! Please check to make sure you have entered it correctly, or register a new account.")
        
        elif bcrypt.checkpw(password.encode(), User.objects.get(email=email).password.encode()) == False:
            errors.append("Wrong password! Please check to make sure you have entered it correctly.")

        return errors


class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    passwordverify = models.CharField(max_length=255)
    birthdate = models.DateTimeField(auto_now_add = False)
    friended = models.ManyToManyField("self")

    objects = UserManager()