from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_task_creation(self):
        """Test that a task is created with correct defaults"""
        task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="Test Description",
            reminder_schedule=make_aware(datetime.now() + timedelta(hours=2)),
        )
        self.assertEqual(task.title, "Test Task")
        self.assertFalse(task.completed)  # Default value
        self.assertFalse(task.reminder_sent)  # Default value
