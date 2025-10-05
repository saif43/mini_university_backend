from rest_framework import serializers
from .models import Student
from grades.models import Grade
from sections.models import Section


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model.
    """
    grade_name = serializers.CharField(source='grade.name', read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    age = serializers.SerializerMethodField()
    enrollments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'name', 'birthdate', 'student_id', 'grade', 'grade_name',
            'section', 'section_name', 'age', 'enrollments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_age(self, obj):
        return obj.age
    
    def get_enrollments_count(self, obj):
        return obj.enrollments.count()


class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Student model.
    """
    class Meta:
        model = Student
        fields = ['name', 'birthdate', 'student_id', 'grade', 'section']
    
    def validate_name(self, value):
        """
        Validate student name.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Student name cannot be empty.")
        return value.strip()
    
    def validate_student_id(self, value):
        """
        Validate student ID format and uniqueness.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Student ID cannot be empty.")
        
        value = value.strip().upper()
        
        # Check uniqueness
        if self.instance:
            # Update case - exclude current instance
            if Student.objects.filter(student_id=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A student with this ID already exists.")
        else:
            # Create case
            if Student.objects.filter(student_id=value).exists():
                raise serializers.ValidationError("A student with this ID already exists.")
        
        return value
    
    def validate(self, data):
        """
        Validate that section belongs to the selected grade.
        """
        section = data.get('section')
        grade = data.get('grade')
        
        if section and grade and section.grade != grade:
            raise serializers.ValidationError(
                "The selected section does not belong to the selected grade."
            )
        return data