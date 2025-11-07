from django.db import models
class About(models.Model):
    img=models.ImageField(upload_to='team_images/')
    name=models.CharField(max_length=30)
    role=models.CharField(max_length=50)
    github= models.CharField(max_length=100, null=True, blank=True)
class Resume_form(models.Model):
    input_skill = models.CharField(max_length=200)
    input_resume = models.FileField(upload_to='resumes/')
class Ques(models.Model):
    input=models.CharField(max_length=20)
    question1=models.TextField(max_length=1000)
    question2=models.TextField(max_length=1000)
    question3=models.TextField(max_length=1000)
    question4=models.TextField(max_length=1000)
    question5=models.TextField(max_length=1000)
# Create your models here.
