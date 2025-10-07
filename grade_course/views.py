from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import GradeCourse
from grades.models import Grade
from courses.models import Course
from .serializers import (
    GradeCourseSerializer, 
    GradeCourseCreateUpdateSerializer,
    GradeCourseSummarySerializer,
    CoursesByGradeSerializer,
    GradesByCourseSerializer
)


class GradeCourseListCreateView(APIView):
    """
    List all grade-course relationships or create a new one.
    """
    permission_classes = [permissions.AllowAny]  # Adjust as needed
    
    @swagger_auto_schema(
        operation_description="List all grade-course relationships",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by grade or course name", type=openapi.TYPE_STRING),
            openapi.Parameter('grade', openapi.IN_QUERY, description="Filter by grade ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('course', openapi.IN_QUERY, description="Filter by course ID", type=openapi.TYPE_INTEGER),

            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER),
        ],
        responses={200: GradeCourseSerializer(many=True)}
    )
    def get(self, request):
        """
        Retrieve all grade-course relationships with optional filtering and pagination.
        """
        search = request.query_params.get('search', '')
        grade_id = request.query_params.get('grade', '')
        course_id = request.query_params.get('course', '')
        
        grade_courses = GradeCourse.objects.select_related('grade', 'course').all()
        
        # Apply filters
        if search:
            grade_courses = grade_courses.filter(
                Q(grade__name__icontains=search) | 
                Q(course__name__icontains=search) |
                Q(course__description__icontains=search)
            )
        
        if grade_id:
            grade_courses = grade_courses.filter(grade_id=grade_id)
        
        if course_id:
            grade_courses = grade_courses.filter(course_id=course_id)
        
        # Pagination
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        paginator = Paginator(grade_courses, page_size)
        page_obj = paginator.get_page(page_number)
        
        serializer = GradeCourseSerializer(page_obj, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.has_next(),
            'previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        })
    
    @swagger_auto_schema(
        operation_description="Create a new grade-course relationship",
        request_body=GradeCourseCreateUpdateSerializer,
        responses={
            201: GradeCourseSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request):
        """
        Create a new grade-course relationship.
        """
        serializer = GradeCourseCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            grade_course = serializer.save()
            response_serializer = GradeCourseSerializer(grade_course)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GradeCourseDetailView(APIView):
    """
    Retrieve, update or delete a grade-course relationship.
    """
    permission_classes = [permissions.AllowAny]  # Adjust as needed
    
    def get_object(self, pk):
        """Get grade-course object or raise 404."""
        return get_object_or_404(GradeCourse, pk=pk)
    
    @swagger_auto_schema(
        operation_description="Retrieve a specific grade-course relationship",
        responses={200: GradeCourseSerializer}
    )
    def get(self, request, pk):
        """
        Retrieve a specific grade-course relationship.
        """
        grade_course = self.get_object(pk)
        serializer = GradeCourseSerializer(grade_course)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Update a specific grade-course relationship",
        request_body=GradeCourseCreateUpdateSerializer,
        responses={
            200: GradeCourseSerializer,
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        """
        Update a specific grade-course relationship.
        """
        grade_course = self.get_object(pk)
        serializer = GradeCourseCreateUpdateSerializer(grade_course, data=request.data)
        if serializer.is_valid():
            updated_grade_course = serializer.save()
            response_serializer = GradeCourseSerializer(updated_grade_course)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete a specific grade-course relationship",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, pk):
        """
        Delete a specific grade-course relationship.
        """
        grade_course = self.get_object(pk)
        grade_course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoursesByGradeView(APIView):
    """
    Get all courses for a specific grade.
    """
    permission_classes = [permissions.AllowAny]  # Adjust as needed
    
    @swagger_auto_schema(
        operation_description="Get all courses for a specific grade",
        responses={200: CoursesByGradeSerializer}
    )
    def get(self, request, grade_id):
        """
        Get all courses assigned to a specific grade.
        """
        grade = get_object_or_404(Grade, pk=grade_id)
        serializer = CoursesByGradeSerializer(grade)
        return Response(serializer.data)


class GradesByCourseView(APIView):
    """
    Get all grades for a specific course.
    """
    permission_classes = [permissions.AllowAny]  # Adjust as needed
    
    @swagger_auto_schema(
        operation_description="Get all grades for a specific course",
        responses={200: GradesByCourseSerializer}
    )
    def get(self, request, course_id):
        """
        Get all grades that have this course assigned.
        """
        course = get_object_or_404(Course, pk=course_id)
        serializer = GradesByCourseSerializer(course)
        return Response(serializer.data)


class GradeCourseSummaryView(APIView):
    """
    Get a summary of all grade-course relationships.
    """
    permission_classes = [permissions.AllowAny]  # Adjust as needed
    
    @swagger_auto_schema(
        operation_description="Get a summary of all grade-course relationships",
        responses={200: GradeCourseSummarySerializer(many=True)}
    )
    def get(self, request):
        """
        Get a simplified list of all grade-course relationships.
        """
        grade_courses = GradeCourse.objects.select_related('grade', 'course').all()
        serializer = GradeCourseSummarySerializer(grade_courses, many=True)
        return Response(serializer.data)


class BulkAssignCoursesToGradeView(APIView):
    """
    Bulk assign multiple courses to a grade.
    """
    permission_classes = [permissions.AllowAny]  # Adjust as needed
    
    @swagger_auto_schema(
        operation_description="Bulk assign multiple courses to a grade",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'grade_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'courses': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'course_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }
                    )
                )
            }
        ),
        responses={
            201: "Courses assigned successfully",
            400: "Bad Request"
        }
    )
    def post(self, request):
        """
        Bulk assign multiple courses to a specific grade.
        """
        grade_id = request.data.get('grade_id')
        courses_data = request.data.get('courses', [])
        
        if not grade_id:
            return Response({'error': 'grade_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not courses_data:
            return Response({'error': 'courses list is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            grade = Grade.objects.get(pk=grade_id)
        except Grade.DoesNotExist:
            return Response({'error': 'Grade not found'}, status=status.HTTP_404_NOT_FOUND)
        
        created_relationships = []
        errors = []
        
        for course_data in courses_data:
            course_id = course_data.get('course_id')
            
            try:
                course = Course.objects.get(pk=course_id)
                
                # Check if relationship already exists
                if GradeCourse.objects.filter(grade=grade, course=course).exists():
                    errors.append(f"Course '{course.name}' is already assigned to grade '{grade.name}'")
                    continue
                
                grade_course = GradeCourse.objects.create(
                    grade=grade,
                    course=course
                )
                created_relationships.append(GradeCourseSerializer(grade_course).data)
                
            except Course.DoesNotExist:
                errors.append(f"Course with ID {course_id} not found")
            except Exception as e:
                errors.append(f"Error creating relationship for course {course_id}: {str(e)}")
        
        response_data = {
            'created': created_relationships,
            'created_count': len(created_relationships),
            'errors': errors
        }
        
        if created_relationships:
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
