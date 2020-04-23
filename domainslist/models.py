import uuid
from django.db import models
from django.utils import timezone

class Domain(models.Model):
	fqdn = models.CharField(max_length=30)
	datetime_creation = models.DateTimeField()
	datetime_expiration = models.DateTimeField(blank=True, null=True)
	datetime_deletion = models.DateTimeField(blank=True, null=True)


class DomainFlag(models.Model):
	TYPE_CHOICES = [
		('EXPIRED', 'Expired'),
		('OUTZONE', 'Outzone'),
		('DELETE_CANDIDATE', 'Delete candidate'),
	]
	domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
	type = models.CharField(
		max_length = 20,
		choices = TYPE_CHOICES)
	datetime_from = models.DateTimeField()
	datetime_to = models.DateTimeField(blank=True, null=True)
	
	def is_active(self):
		return self.datetime_from <= timezone.now() and (self.datetime_to == None or self.datetime_to >= timezone.now())
