from django.contrib import admin
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'student', 'course', 'enrollment_date', 
        'status', 'final_grade', 'created_at'
    ]
    list_filter = ['status', 'enrollment_date', 'course', 'student__grade']
    search_fields = [
        'student__name', 'student__student_id', 'course__name'
    ]
    ordering = ['-enrollment_date']
    date_hierarchy = 'enrollment_date'
    readonly_fields = ['enrollment_date', 'created_at', 'updated_at']
