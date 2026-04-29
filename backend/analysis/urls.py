from django.urls import path
from .views import AnalysisTaskView

urlpatterns = [
    path('tasks/<uuid:task_id>/', AnalysisTaskView.as_view(),
         name='analysis_task_id'),
]
