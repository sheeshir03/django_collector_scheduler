import json
from rest_framework import viewsets, permissions

from scraper.tasks import run_scraper_task
from .models import User, ScraperTask, ScraperScript, ScrapedData, ScraperLog
from .serializers import UserSerializer, ScraperTaskSerializer, ScraperScriptSerializer, ScraperLogSerializer, ScrapedDataSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_celery_beat.models import PeriodicTask, CrontabSchedule

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ScraperScriptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScraperScript.objects.all()
    serializer_class = ScraperScriptSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ScraperTaskViewSet(viewsets.ModelViewSet):
    queryset = ScraperTask.objects.all()
    serializer_class = ScraperTaskSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(f"Authenticated User: {self.request.user}")  # Debugging line
        task = serializer.save(created_by=self.request.user)
        if task.run_type == 'once':
            run_scraper_task.apply_async(args=[task.id], eta=task.run_once_time)
        elif task.run_type == 'recurring':
            crontab_schedule, created = CrontabSchedule.objects.get_or_create(
                minute=task.schedule_time.minute,
                hour=task.schedule_time.hour,
                day_of_week='*',
                day_of_month="*",
                month_of_year="*",
            )

            PeriodicTask.objects.create(
                crontab=crontab_schedule,
                name=f"{task.name} - {task.id}",
                task='scraper.tasks.run_scraper_task',
                args=json.dumps([task.id]),
            )

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        task = self.get_object()
        run_scraper_task(task.id)
        print("Task started via run action")
        return Response({
            'status': 'Task Started'
        })

class ScrapedDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScrapedData.objects.all()
    serializer_class = ScrapedDataSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScraperLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScraperLog.objects.all()
    serializer_class = ScraperLogSerializer
    permission_classes = [permissions.IsAuthenticated]