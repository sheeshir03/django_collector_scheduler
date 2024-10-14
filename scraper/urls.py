# scraper/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

router = DefaultRouter()
router.register(r'scraper-tasks', views.ScraperTaskViewSet, basename='scrapertask')
router.register(r'scraper-scripts', views.ScraperScriptViewSet, basename='scraperscript')
router.register(r'scraped-data', views.ScrapedDataViewSet, basename='scrapeddata')
router.register(r'scraper-logs', views.ScraperLogViewSet, basename='scraperlog')
router.register(r'users', views.UserViewSet, basename='user')  # Optional

urlpatterns = [
    # JWT Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Endpoints from Router
    path('api/', include(router.urls)),
]
