from django.db import models


class Course(models.Model):
    """
    Represents a course in the university system.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        db_table = 'courses'
    
    def __str__(self):
        return self.name
