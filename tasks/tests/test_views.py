from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_add_task_view(self):
        """Test that a task is added via the add_task view"""
        response = self.client.post(reverse('add_task'), {
            'title': "New Task",
            'description': "Task Description",
            'reminder_schedule': (datetime.now() + timedelta(hours=2)).isoformat(),
        })
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, "New Task")

    def test_view_tasks_page(self):
        """Test that the view_tasks page loads and shows tasks"""
        Task.objects.create(
            user=self.user,
            title="Test Task",
            reminder_schedule=make_aware(datetime.now() + timedelta(hours=2)),
        )
        response = self.client.get(reverse('view_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")
