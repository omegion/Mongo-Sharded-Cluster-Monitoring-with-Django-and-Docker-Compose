from django.db import models
from django.core.validators import URLValidator
from django.utils import timezone
from django.db.models import Count, Sum, F


class Replica(models.Model): 
    name = models.CharField(max_length=150)
    shard = models.CharField(max_length=150)
    port = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

class Check(models.Model): 
    cpu = models.CharField(max_length=10, default=0)
    memory = models.CharField(max_length=10, default=0)
    io = models.CharField(max_length=10, default=0)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    # Foreign
    replica = models.ForeignKey(Replica, on_delete=models.CASCADE, related_name="checks")
