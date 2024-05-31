from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class SpaUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
