from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sections_count', 'students_count', 'created_at']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    def sections_count(self, obj):
        return obj.sections.count()
    sections_count.short_description = 'Sections'
    
    def students_count(self, obj):
        return obj.students.count()
    students_count.short_description = 'Students'
