from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    one_time_password = models.CharField(default='', max_length=100)
    pasword_expiry_time = models.DateTimeField(default=timezone.now() + datetime.timedelta(minutes=5))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
class AllowedDomains(models.Model):
    domain = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.domain
    
    class Meta:
        verbose_name_plural = "Allowed Domains"