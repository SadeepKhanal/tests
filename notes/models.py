from django.core.exceptions import ValidationError
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def clean(self):
        if len(self.content) < 10:
            raise ValidationError("Content must contain at least 10 characters.")

    def __str__(self):
        return self.title