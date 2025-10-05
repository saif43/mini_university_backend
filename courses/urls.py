from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListCreateView.as_view(), name='course-list-create'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
]