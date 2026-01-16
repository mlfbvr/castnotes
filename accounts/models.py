
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
	"""Custom user model with additional fields for CastNotes."""
	full_name = models.CharField(max_length=255)
	bio = models.TextField(blank=True)
	location = models.CharField(max_length=255, blank=True)
	profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

	def __str__(self):
		return self.username
