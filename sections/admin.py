from django.contrib import admin
from .models import Section


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'grade', 'students_count', 'created_at']
    list_filter = ['grade']
    search_fields = ['name', 'grade__name']
    ordering = ['grade__name', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    def students_count(self, obj):
        return obj.students.count()
    students_count.short_description = 'Students'
