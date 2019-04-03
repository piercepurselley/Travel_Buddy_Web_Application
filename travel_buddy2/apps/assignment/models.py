from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_reg(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors.append("First and last name must be 2 or more characters")
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha():
            errors.append("First and last name must be only alphabetical characters")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email is invalid")
        if len(postData['password']) < 2:
            errors.append("Password is too short")
        if postData['password'] != postData['confirm_password']:
            errors.append("Passwords don't match")
        if len(errors) > 0:
            res['status'] = "bad"
            res['data'] = errors
        else:
            hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], password = hashed_pw, email = postData['email'])
            res['data'] = user
        return res

    def validate_log(self, postData):
        res = {
            "status" : "good",
            "data" : ""
        }
        errors = []
        try:
            the_user = User.objects.get(email = postData['email'])
        except:
            res['status'] = "bad"
            res['data'] = "Email and/or password are incorrect"
            return res
        if bcrypt.checkpw(postData['password'].encode(), the_user.password.encode()):
            res['data'] = the_user
            return res
        else:
            res['status'] = "bad"
            res['data'] = "Email and/or password are incorrect"
            return res

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return "<User: {}>".format(self.email)


class Product(models.Model):
    item = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, related_name = "user_uploads")
    wishlist = models.ManyToManyField(User, related_name = "user_list")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)