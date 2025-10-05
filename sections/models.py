from django.db import models
from grades.models import Grade


class Section(models.Model):
    """
    Represents a section within a grade.
    """
    name = models.CharField(max_length=50)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='sections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['grade__name', 'name']
        unique_together = ['name', 'grade']
        db_table = 'sections'
    
    def __str__(self):
        return f"{self.grade.name} - {self.name}"
