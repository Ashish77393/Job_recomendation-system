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
from django.db import models

class JobRole(models.Model):
    # List of job roles as choices
    JOB_CHOICES = [
        ('UI/UX Designer', 'UI/UX Designer'),
        ('DevOps Engineer', 'DevOps Engineer'),
        ('Web Developer', 'Web Developer'),
        ('Machine Learning Engineer', 'Machine Learning Engineer'),
        ('Cybersecurity Analyst', 'Cybersecurity Analyst'),
        ('Project Manager', 'Project Manager'),
        ('Cloud Engineer', 'Cloud Engineer'),
        ('Blockchain Developer', 'Blockchain Developer'),
        ('Software Engineer', 'Software Engineer'),
        ('Data Analyst', 'Data Analyst'),
        ('Database Administrator', 'Database Administrator'),
        ('Data Scientist', 'Data Scientist'),
        ('AI Engineer', 'AI Engineer'),
        ('Big Data Engineer', 'Big Data Engineer'),
        ('Business Analyst', 'Business Analyst'),
        ('Mobile App Developer', 'Mobile App Developer'),
    ]

    name = models.CharField(max_length=50, choices=JOB_CHOICES, unique=True)

    def __str__(self):
        return self.name


class JobQuestion(models.Model):
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_role.name} - {self.question[:50]}..."
