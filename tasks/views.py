from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils.timezone import make_aware

def next_day_morning():
    now = datetime.now()
    next_day = now + timedelta(days=1)
    # Ensure the datetime is timezone-aware
    return make_aware(next_day.replace(hour=8, minute=0, second=0, microsecond=0))

@login_required(login_url='login') 
def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        reminder_schedule = request.POST['reminder_schedule']
        attachment = request.FILES.get('attachment')

        if not reminder_schedule:
            reminder_schedule = next_day_morning()
        else:
            # Parse the datetime string and make it timezone-aware
            reminder_schedule = make_aware(datetime.fromisoformat(reminder_schedule))
            
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            reminder_schedule=reminder_schedule,
            attachment=attachment,
        )
        messages.success(request, f'Task "{title}" has been added successfully!')
        return redirect('view_tasks')

@login_required(login_url='login') 
def view_tasks(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'view_tasks.html', {'tasks': tasks})

@login_required(login_url='login')
def mark_task_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    messages.success(request, f'Task "{task.title}" has been marked as completed!')
    return redirect('view_tasks')


@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, f'Task "{task.title}" has been deleted successfully!')
    return redirect('view_tasks')

