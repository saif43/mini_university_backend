from django.db import models
from django.core.validators import RegexValidator
from grades.models import Grade
from sections.models import Section


class Student(models.Model):
    """
    Represents a student in the university system.
    """
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    student_id = models.CharField(
        max_length=20, 
        unique=True,
        validators=[RegexValidator(
            regex='^[A-Z0-9]+$',
            message='Student ID must contain only uppercase letters and numbers.'
        )]
    )
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='students')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        db_table = 'students'
    
    def __str__(self):
        return f"{self.name} ({self.student_id})"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birthdate.year - (
            (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
        )
