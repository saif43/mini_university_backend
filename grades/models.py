from django.db import models


class Grade(models.Model):
    """
    Represents a grade level in the university system.
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        db_table = 'grades'
    
    def __str__(self):
        return self.name
