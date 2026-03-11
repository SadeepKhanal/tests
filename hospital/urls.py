# urls.py
from django.urls import path
from .views import PatientListAPIView, PatientDetailAPIView

urlpatterns = [
    path('', PatientListAPIView.as_view(), name='patients'),
    path('<int:pk>/', PatientDetailAPIView.as_view(), name='patient-info'),
]