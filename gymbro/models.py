from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        filter_email = User.objects.filter(email=postData['form_email'])
        if len(filter_email) > 0:
            errors['email_taken'] = "An account with this email already exists"
            # First Name
        if len(postData['form_first_name']) == 0:
            errors['blank_first_name'] = "First name is required."
        elif len(postData['form_first_name']) < 2:
            errors["name_length"] = "First name should be at least 2 characters"
        elif not postData['form_first_name'].isalpha():
            errors['letters_only_first_name'] = "First name can only contain letters"
            # Last Name
        if len(postData['form_last_name']) == 0:
            errors['blank_last_name'] = "Last name is required."
        elif len(postData['form_last_name']) < 2:
            errors["name_length"] = "Last name should be at least 2 characters"
        elif not postData['form_last_name'].isalpha():
            errors['letters_only_last_name'] = "Last name can only contain letters"
            # Email Regex Check
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['form_email']):
            errors["invalid_email"] = "Not a valid email"
            # Password Check
        if postData['form_password'] != postData['form_confirm']:
            errors["confirm_password"] = "Passwords do not match"
        elif len(postData['form_password']) < 8:
            errors["password_length"] = "Passwords must be at least 8 characters"
            #convert date time from a string to a number
            # make sure release date is in the past
        return errors

    def login_validator(self, postData):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['form_email']) < 3:
            errors["invalid_email"] = "Not a valid email"
        elif not email_regex.match(postData['form_email']):
            errors["invalid_email"] = "Not a valid email"
        return errors

    def edit_form_validator(self, postData):
        errors = {}

        if len(postData['form_first_name']) == 0:
            errors['form_first_name'] = "First name is required."
        elif len(postData['form_first_name']) < 2:
            errors["form_first_name"] = "First name should be at least 2 characters"
        elif not postData['form_first_name'].isalpha():
            errors['form_first_name'] = "First name can only contain letters"

        if len(postData['form_last_name']) == 0:
            errors['form_last_name'] = "Last name is required."
        elif len(postData['form_last_name']) < 2:
            errors["form_last_name"] = "Last name should be at least 2 characters"
        elif not postData['form_last_name'].isalpha():
            errors['form_last_name'] = "Last name can only contain letters"

        if len(postData['form_desc']) == 0:
            errors['form_desc'] = "Description is required."
        elif len(postData['form_desc']) > 180:
            errors['form_desc'] = "Description cannot exceed 180 characters."

        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    desc = models.TextField()
    email = models.CharField(max_length=30)
    weight = models.IntegerField()
    password = models.CharField(max_length=70)
    profile_picture = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# Workout Models
class Workout(models.Model):
    name = models.CharField(max_length=45)
    weekday = models.CharField(max_length=15)
    users = models.ManyToManyField(User, related_name="workouts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Exercise(models.Model):
    name = models.CharField(max_length=45)
    workout = models.ManyToManyField(Workout, related_name="exercises")
    goalrep = models.IntegerField(default=8)
    rest = models.IntegerField(default=90)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Set(models.Model):
    reps =models.IntegerField()
    weight = models.IntegerField()
    exercise = models.ForeignKey(Exercise, related_name="sets",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Stat(models.Model):
    user = models.ForeignKey(User, related_name="stats", on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, related_name="stats", on_delete=models.CASCADE)
    lbs_rep = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
