from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import os


def next_day_morning():
    """
    Returns the next day's morning (8:00 AM) as a datetime object.
    """
    now = datetime.now()
    next_day = now + timedelta(days=1)
    return next_day.replace(hour=8, minute=0, second=0, microsecond=0)
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    reminder_schedule = models.DateTimeField(default=next_day_morning())
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
