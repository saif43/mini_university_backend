from django.urls import path
from . import views

app_name = 'grade_course'

urlpatterns = [
    # Basic CRUD operations
    path('', views.GradeCourseListCreateView.as_view(), name='grade-course-list-create'),
    path('<int:pk>/', views.GradeCourseDetailView.as_view(), name='grade-course-detail'),
    
    # Specialized views
    path('grade/<int:grade_id>/courses/', views.CoursesByGradeView.as_view(), name='courses-by-grade'),
    path('course/<int:course_id>/grades/', views.GradesByCourseView.as_view(), name='grades-by-course'),
    path('summary/', views.GradeCourseSummaryView.as_view(), name='grade-course-summary'),
    
    # Bulk operations
    path('bulk-assign/', views.BulkAssignCoursesToGradeView.as_view(), name='bulk-assign-courses'),
]