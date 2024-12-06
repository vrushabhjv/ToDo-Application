from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import os

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    reminder_schedule = models.DateTimeField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        # Delete the attached file from the file system if it exists
        if self.attachment and os.path.isfile(self.attachment.path):
            os.remove(self.attachment.path)
        super().delete(*args, **kwargs)
