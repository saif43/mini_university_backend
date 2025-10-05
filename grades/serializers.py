from rest_framework import serializers
from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    """
    Serializer for Grade model.
    """
    sections_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Grade
        fields = ['id', 'name', 'sections_count', 'students_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_sections_count(self, obj):
        return obj.sections.count()
    
    def get_students_count(self, obj):
        return obj.students.count()


class GradeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Grade model.
    """
    class Meta:
        model = Grade
        fields = ['name']
    
    def validate_name(self, value):
        """
        Validate that the grade name is not empty and properly formatted.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Grade name cannot be empty.")
        return value.strip()