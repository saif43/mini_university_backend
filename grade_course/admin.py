from django.contrib import admin
from .models import GradeCourse


@admin.register(GradeCourse)
class GradeCourseAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'grade', 'course', 'enrollments_count', 'created_at'
    ]
    list_filter = ['grade', 'course', 'created_at']
    search_fields = ['grade__name', 'course__name', 'course__description']
    ordering = ['grade__name', 'course__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('grade', 'course')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def enrollments_count(self, obj):
        """Get count of enrollments for this course in this grade"""
        from enrollments.models import Enrollment
        return Enrollment.objects.filter(
            course=obj.course,
            student__grade=obj.grade
        ).count()
    enrollments_count.short_description = 'Enrollments'
    
    def get_queryset(self, request):
        """Optimize queries by selecting related objects"""
        return super().get_queryset(request).select_related('grade', 'course')
