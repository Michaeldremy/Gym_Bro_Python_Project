from django.db import models

# Create your models here.


# Workout Models
class Workout(models.Model):
    name = models.CharField(max_length=45)
    weekday = models.CharField(max_length=15)
    user = models.ForeignKey(User, related_name="workouts",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Exercise(models.Model):
    name = models.CharField(max_length=45)
    weight = models.IntegerField()
    workout = models.ForeignKey(Workout, related_name="exercises", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Set(models.Model):
    rep =models.IntegerField()
    weight = models.IntegerField()
    rest = models.IntegerField()
    exercise = models.ForeignKey(Exercise, related_name="sets", on_delete=models.CASCADE)