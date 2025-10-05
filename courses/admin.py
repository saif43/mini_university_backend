from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'enrollments_count', 'active_enrollments_count', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    def enrollments_count(self, obj):
        return obj.enrollments.count()
    enrollments_count.short_description = 'Total Enrollments'
    
    def active_enrollments_count(self, obj):
        return obj.enrollments.filter(status='active').count()
    active_enrollments_count.short_description = 'Active Enrollments'
