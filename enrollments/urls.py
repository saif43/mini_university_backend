from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    path('', views.EnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment-detail'),
]