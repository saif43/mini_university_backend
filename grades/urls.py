from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    path('', views.GradeListCreateView.as_view(), name='grade-list-create'),
    path('<int:pk>/', views.GradeDetailView.as_view(), name='grade-detail'),
]