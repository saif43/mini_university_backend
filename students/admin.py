from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'student_id', 'grade', 'section', 'birthdate', 'age', 'created_at']
    list_filter = ['grade', 'section']
    search_fields = ['name', 'student_id', 'grade__name', 'section__name']
    ordering = ['name']
    readonly_fields = ['age', 'created_at', 'updated_at']
    
    def age(self, obj):
        return obj.age
    age.short_description = 'Age'
