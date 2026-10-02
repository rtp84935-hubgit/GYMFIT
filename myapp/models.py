from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Trainer(models.Model):
    tname=models.CharField(max_length=100)
    tage=models.IntegerField()
    tplace=models.CharField(max_length=100)
    temail=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default='pending')
    specification=models.CharField(max_length=100)
    experience=models.IntegerField()
    photo=models.FileField()
    LOGIN=models.OneToOneField(User,on_delete=models.CASCADE)



class Client(models.Model):
    cname=models.CharField(max_length=100)
    cage=models.CharField(max_length=100)
    cplace=models.CharField(max_length=100)
    cemail=models.CharField(max_length=100)
    LOGIN=models.OneToOneField(User,on_delete=models.CASCADE)

class Requests(models.Model):
    TRAINER=models.ForeignKey(Trainer,on_delete=models.CASCADE)
    CLIENT=models.ForeignKey(Client,on_delete=models.CASCADE)
    date=models.DateTimeField()
    status=models.CharField(max_length=100,default='pending')

class Tip(models.Model):
    TRAINER=models.ForeignKey(Trainer,on_delete=models.CASCADE)
    tip=models.TextField()
    date=models.DateTimeField()

class Dietplan(models.Model):
    CLIENT=models.ForeignKey(Client,on_delete=models.CASCADE)
    TRAINER=models.ForeignKey(Trainer,on_delete=models.CASCADE)
    date=models.DateTimeField()
    dietplan=models.TextField()

class PremiumMembership(models.Model):
    CLIENT=models.ForeignKey(Client,on_delete=models.CASCADE)
    duration=models.IntegerField()
    DOR=models.DateField()
    EXPD=models.DateField()
    Price=models.IntegerField()

class PremiumVideo(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField()
    date = models.DateField(auto_now_add=True)