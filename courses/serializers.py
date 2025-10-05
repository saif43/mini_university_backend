from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    """
    enrollments_count = serializers.SerializerMethodField()
    active_enrollments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'enrollments_count', 'active_enrollments_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_enrollments_count(self, obj):
        return obj.enrollments.count()
    
    def get_active_enrollments_count(self, obj):
        return obj.enrollments.filter(status='active').count()


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Course model.
    """
    class Meta:
        model = Course
        fields = ['name', 'description']
    
    def validate_name(self, value):
        """
        Validate course name.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Course name cannot be empty.")
        return value.strip()