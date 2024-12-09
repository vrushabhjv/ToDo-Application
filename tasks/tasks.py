from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import Task
from django.conf import settings
from django.utils.timezone import localtime

@shared_task
def send_reminder_emails():
    # Find tasks due within the next hour
    tasks_due = Task.objects.filter(
        reminder_schedule__lte=now() + timedelta(hours=1),
        reminder_schedule__gte=now(),
        completed=False,
        reminder_sent=False
    )
    print(tasks_due)

    # Group tasks by user
    tasks_by_user = {}
    for task in tasks_due:
        if task.user not in tasks_by_user:
            tasks_by_user[task.user] = []
        tasks_by_user[task.user].append(task)

    # Send one email per user
    for user, tasks in tasks_by_user.items():
        # Create the email content
        task_list = "\n".join(
            [f"- {task.title} (Due: {localtime(task.reminder_schedule)})" for task in tasks]
        )
        email_body = (
            f"Hi {user.username},\n\n"
            f"You have the following tasks due in the next hour:\n\n"
            f"{task_list}\n\n"
            f"If you wish to snooze any of these tasks, please log in to your account and click the 'Snooze' button next to the task. "
            f"This will reschedule the reminder for 1 hour later.\n\n"
            f"You can log in here: http://ec2-100-28-120-64.compute-1.amazonaws.com/todo/\n\n"
            f"Best regards,\nTaskTrack Team"
        )

        # Send the email
        send_mail(
            subject="Task Reminder",
            message=email_body,
            from_email=settings.EMAIL_HOST_USER,  # Replace with your sender email
            recipient_list=[user.email],
            fail_silently=False,
        )
        print(f"Reminder email sent to {user.email}")

        # Mark all tasks for this user as reminder sent
        for task in tasks:
            task.reminder_sent = True
            task.save()