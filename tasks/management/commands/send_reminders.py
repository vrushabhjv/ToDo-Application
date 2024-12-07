from django.core.management.base import BaseCommand
from tasks.tasks import send_reminder_emails

class Command(BaseCommand):
    help = 'Send reminders for tasks due in the next hour'

    def handle(self, *args, **kwargs):
        send_reminder_emails()
        self.stdout.write(self.style.SUCCESS('Successfully sent reminders'))
