from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Course
from .serializers import CourseSerializer, CourseCreateUpdateSerializer


class CourseListCreateView(APIView):
    """
    List all courses or create a new course.
    """
    
    def get(self, request):
        """
        Retrieve all courses with optional search and pagination.
        """
        search = request.query_params.get('search', '')
        courses = Course.objects.all()
        
        if search:
            courses = courses.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        # Pagination
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        paginator = Paginator(courses, page_size)
        page_obj = paginator.get_page(page_number)
        
        serializer = CourseSerializer(page_obj, many=True)
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'next': page_obj.has_next(),
            'previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        })
    
    def post(self, request):
        """
        Create a new course.
        """
        serializer = CourseCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            response_serializer = CourseSerializer(course)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    """
    Retrieve, update or delete a course instance.
    """
    
    def get_object(self, pk):
        """
        Get course object or raise 404.
        """
        return get_object_or_404(Course, pk=pk)
    
    def get(self, request, pk):
        """
        Retrieve a specific course.
        """
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Update a specific course.
        """
        course = self.get_object(pk)
        serializer = CourseCreateUpdateSerializer(course, data=request.data)
        if serializer.is_valid():
            updated_course = serializer.save()
            response_serializer = CourseSerializer(updated_course)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Delete a specific course.
        """
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
