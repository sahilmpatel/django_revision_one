from django.db import models

# Create your models here.
from django.db.models.signals import pre_save

from Revision_django.utills import unique_slug_generator


class PersonDetails(models.Model):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    gender = models.CharField(max_length=2, choices=GENDER, default='M')
    address = models.TextField()

    def __str__(self):
        return self.name

class Experiment(models.Model):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10,default=0)
    gender = models.CharField(max_length=2, choices=GENDER, default='M')
    def __str__(self):
        return self.name

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(rl_pre_save_receiver, sender=Experiment)


class Customer(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='vehicle'
    )
    def __str__(self):
        return self.name


class Accounts(models.Model):
    name = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='account'
    )

    def __str__(self):
        return self.name

class Banks(models.Model):
    name = models.CharField(max_length=255)
    customer = models.ManyToManyField(
        Customer,

        related_name='bank'
    )

    def __str__(self):
        return self.name



class Xyz(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name