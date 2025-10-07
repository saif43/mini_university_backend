from django.db import models
from django.utils import timezone
from grades.models import Grade
from courses.models import Course


class GradeCourse(models.Model):
    """
    Represents the relationship between grades and courses.
    Defines which courses are available for specific grades.
    """
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grade_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grade_courses')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['grade__name', 'course__name']
        unique_together = ['grade', 'course']
        db_table = 'grade_courses'
        verbose_name = 'Grade Course'
        verbose_name_plural = 'Grade Courses'
    
    def __str__(self):
        return f"{self.grade.name} - {self.course.name}"