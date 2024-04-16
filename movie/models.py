from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length = 10, null = True)
    gender = models.CharField(max_length = 10, choices = GENDER_CHOICES, null=True)

    @property
    def full_name(self):
        name = "%s %s" % (self.first_name, self.last_name)
        return name.strip()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.username) + " pk: " + str(self.pk)

# Create your models here.
