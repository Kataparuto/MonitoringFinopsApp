from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    # HTML (como el curso)
    path('measurements/', views.measurement_list),
    path('measurementcreate/', csrf_exempt(views.measurement_create), name='measurementCreate'),

    # API (para JMeter)
    path('api/health/', views.health_check),
    path('api/reports/', views.api_report),
    path('api/costs/', views.api_create),
]
