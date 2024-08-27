from django.db import models

# Create your models here.



class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Auditory(models.Model):
    number = models.IntegerField()
    floor = models.IntegerField()

class StudyGroup(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.ManyToManyField(Teacher, related_name='study_group')
    schedule = models.ManyToManyField(Auditory, related_name='study_group')

class Shedule(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='shedule')
    auditory = models.ForeignKey(Auditory, on_delete=models.CASCADE, related_name='shedule')
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    day_of_week = models.IntegerField()