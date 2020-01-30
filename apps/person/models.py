from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    vector = ArrayField(models.FloatField(), blank=True, null=True)
