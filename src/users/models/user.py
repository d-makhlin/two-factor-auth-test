import uuid
from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_no = models.CharField(max_length=20)
    photo = models.ImageField(blank=True, null=True)
