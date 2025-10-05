from rest_framework import serializers
from .models import Section
from grades.models import Grade
from grades.serializers import GradeSerializer


class SectionSerializer(serializers.ModelSerializer):
    """
    Serializer for Section model.
    """
    grade_name = serializers.CharField(source='grade.name', read_only=True)
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Section
        fields = ['id', 'name', 'grade', 'grade_name', 'students_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_students_count(self, obj):
        return obj.students.count()


class SectionCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Section model.
    """
    class Meta:
        model = Section
        fields = ['name', 'grade']
    
    def validate(self, data):
        """
        Validate that section name is unique within the grade.
        """
        name = data.get('name', '').strip()
        grade = data.get('grade')
        
        if not name:
            raise serializers.ValidationError({'name': 'Section name cannot be empty.'})
        
        data['name'] = name
        
        # Check uniqueness
        if self.instance:
            # Update case - exclude current instance
            if Section.objects.filter(
                name=name,
                grade=grade
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "A section with this name already exists in the selected grade."
                )
        else:
            # Create case
            if Section.objects.filter(name=name, grade=grade).exists():
                raise serializers.ValidationError(
                    "A section with this name already exists in the selected grade."
                )
        return data