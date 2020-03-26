from django.db import models
from django.utils import timezone

# Create your models here.
class Clients(models.Model):
	title = models.CharField(max_length=250,null=False,unique=True)
	ipaddress = models.CharField(max_length=25, null=False)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.title


class Sensors(models.Model):
    client = models.ForeignKey(
      Clients, on_delete=models.CASCADE, related_name='sensorclient')
    temperature = models.IntegerField(null=True)
    luminosuty = models.IntegerField(null=True)
    humidity = models.IntegerField(null=True)
    date = models.DateTimeField(default=timezone.now)
