from rest_framework import serializers
from .models import GradeCourse
from grades.models import Grade
from courses.models import Course


class GradeCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for GradeCourse model with related data.
    """
    grade_name = serializers.CharField(source='grade.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_description = serializers.CharField(source='course.description', read_only=True)
    enrollments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GradeCourse
        fields = [
            'id', 'grade', 'grade_name', 'course', 'course_name', 'course_description',
            'enrollments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_enrollments_count(self, obj):
        """Get count of enrollments for this course in this grade"""
        from enrollments.models import Enrollment
        return Enrollment.objects.filter(
            course=obj.course,
            student__grade=obj.grade
        ).count()


class GradeCourseCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating GradeCourse model.
    """
    class Meta:
        model = GradeCourse
        fields = ['grade', 'course']
    
    def validate(self, data):
        """
        Custom validation for grade-course relationship.
        """
        grade = data.get('grade')
        course = data.get('course')
        
        # Check if this grade-course combination already exists
        if self.instance:
            # Update case - exclude current instance
            if GradeCourse.objects.filter(
                grade=grade,
                course=course
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "This course is already assigned to this grade."
                )
        else:
            # Create case
            if GradeCourse.objects.filter(grade=grade, course=course).exists():
                raise serializers.ValidationError(
                    "This course is already assigned to this grade."
                )
        
        return data


class GradeCourseSummarySerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing grade-course relationships.
    """
    grade_name = serializers.CharField(source='grade.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = GradeCourse
        fields = ['id', 'grade_name', 'course_name']


class CoursesByGradeSerializer(serializers.ModelSerializer):
    """
    Serializer to show all courses for a specific grade.
    """
    courses = serializers.SerializerMethodField()
    
    class Meta:
        model = Grade
        fields = ['id', 'name', 'courses']
    
    def get_courses(self, obj):
        """Get all courses for this grade"""
        grade_courses = GradeCourse.objects.filter(grade=obj).select_related('course')
        return [{
            'id': gc.course.id,
            'name': gc.course.name,
            'description': gc.course.description,
            'grade_course_id': gc.id
        } for gc in grade_courses]


class GradesByCourseSerializer(serializers.ModelSerializer):
    """
    Serializer to show all grades for a specific course.
    """
    grades = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'grades']
    
    def get_grades(self, obj):
        """Get all grades for this course"""
        grade_courses = GradeCourse.objects.filter(course=obj).select_related('grade')
        return [{
            'id': gc.grade.id,
            'name': gc.grade.name,
            'grade_course_id': gc.id
        } for gc in grade_courses]