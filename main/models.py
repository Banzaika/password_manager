from django.db import models

class Password(models.Model):
    service = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'passwords'