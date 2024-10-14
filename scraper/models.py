from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = {
        ('admin', 'Admin'),
        ('user', 'User'),
    }
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username

class ScraperScript(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    script_path = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class ScraperTask(models.Model):
    RUN_TYPE_CHOICES = (
    ('once', 'Once'),
    ('recurring', 'Recurring'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    name = models.CharField(max_length=255)
    script = models.ForeignKey(ScraperScript, on_delete=models.CASCADE)
    run_type = models.CharField(max_length=10, choices=RUN_TYPE_CHOICES, default='once')
    schedule_time = models.TimeField(null=True, blank=True) 
    schedule_cron = models.CharField(max_length=255, blank=True) # Cron Created by celery CronTab schedul;er
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ScrapedData(models.Model):
    task = models.ForeignKey(ScraperTask, on_delete=models.CASCADE)
    data = models.JSONField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Data from {self.task.name} at {self.scraped_at}"

class ScraperLog(models.Model):
    task = models.ForeignKey(ScraperTask, on_delete=models.CASCADE)
    log_file_path = models.CharField(max_length=500, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Log for {self.task.name} at {self.created_at}"

