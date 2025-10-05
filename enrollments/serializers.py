from rest_framework import serializers
from .models import Enrollment
from students.models import Student
from courses.models import Course


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Enrollment model.
    """
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_id_display = serializers.CharField(source='student.student_id', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'student_id_display',
            'course', 'course_name', 'enrollment_date', 'status', 'final_grade',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'enrollment_date', 'created_at', 'updated_at']


class EnrollmentCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Enrollment model.
    """
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status', 'final_grade']
    
    def validate(self, data):
        """
        Custom validation for enrollment.
        """
        student = data.get('student')
        course = data.get('course')
        status = data.get('status', 'active')
        final_grade = data.get('final_grade')
        
        # Check if student is already enrolled in the course
        if self.instance:
            # Update case - exclude current instance
            if Enrollment.objects.filter(
                student=student,
                course=course
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "This student is already enrolled in this course."
                )
        else:
            # Create case
            if Enrollment.objects.filter(student=student, course=course).exists():
                raise serializers.ValidationError(
                    "This student is already enrolled in this course."
                )
        
        # Validate final_grade based on status
        if status in ['completed', 'failed'] and final_grade is None:
            raise serializers.ValidationError(
                "Final grade is required when status is 'completed' or 'failed'."
            )
        
        if status in ['active', 'dropped'] and final_grade is not None:
            raise serializers.ValidationError(
                "Final grade should not be provided when status is 'active' or 'dropped'."
            )
        
        return data