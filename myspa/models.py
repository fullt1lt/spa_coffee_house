from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class SpaUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True) 
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    

class Salon(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name


class MassageTherapist(models.Model):
    user = models.OneToOneField(SpaUser, on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='therapists')
    
    def __str__(self):
        return f"{self.user.username} {self.salon}" 