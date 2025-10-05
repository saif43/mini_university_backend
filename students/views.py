from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Student
from .serializers import StudentSerializer, StudentCreateUpdateSerializer


class StudentListCreateView(APIView):
    """
    List all students or create a new student.
    """
    
    def get(self, request):
        """
        Retrieve all students with optional search and pagination.
        """
        search = request.query_params.get('search', '')
        grade_id = request.query_params.get('grade', '')
        section_id = request.query_params.get('section', '')
        students = Student.objects.select_related('grade', 'section').all()
        
        if search:
            students = students.filter(
                Q(name__icontains=search) |
                Q(student_id__icontains=search) |
                Q(grade__name__icontains=search) |
                Q(section__name__icontains=search)
            )
        
        if grade_id:
            students = students.filter(grade_id=grade_id)
        
        if section_id:
            students = students.filter(section_id=section_id)
        
        # Pagination
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        paginator = Paginator(students, page_size)
        page_obj = paginator.get_page(page_number)
        
        serializer = StudentSerializer(page_obj, many=True)
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
        Create a new student.
        """
        serializer = StudentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            response_serializer = StudentSerializer(student)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    """
    Retrieve, update or delete a student instance.
    """
    
    def get_object(self, pk):
        """
        Get student object or raise 404.
        """
        return get_object_or_404(Student, pk=pk)
    
    def get(self, request, pk):
        """
        Retrieve a specific student.
        """
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Update a specific student.
        """
        student = self.get_object(pk)
        serializer = StudentCreateUpdateSerializer(student, data=request.data)
        if serializer.is_valid():
            updated_student = serializer.save()
            response_serializer = StudentSerializer(updated_student)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Delete a specific student.
        """
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
