from django.urls import path
from . import views

app_name = 'sections'

urlpatterns = [
    path('', views.SectionListCreateView.as_view(), name='section-list-create'),
    path('<int:pk>/', views.SectionDetailView.as_view(), name='section-detail'),
]