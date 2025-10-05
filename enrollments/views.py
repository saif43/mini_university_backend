from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Enrollment
from .serializers import EnrollmentSerializer, EnrollmentCreateUpdateSerializer


class EnrollmentListCreateView(APIView):
    """
    List all enrollments or create a new enrollment.
    """
    
    def get(self, request):
        """
        Retrieve all enrollments with optional search and pagination.
        """
        search = request.query_params.get('search', '')
        student_id = request.query_params.get('student', '')
        course_id = request.query_params.get('course', '')
        status_filter = request.query_params.get('status', '')
        enrollments = Enrollment.objects.select_related('student', 'course').all()
        
        if search:
            enrollments = enrollments.filter(
                Q(student__name__icontains=search) |
                Q(student__student_id__icontains=search) |
                Q(course__name__icontains=search)
            )
        
        if student_id:
            enrollments = enrollments.filter(student_id=student_id)
        
        if course_id:
            enrollments = enrollments.filter(course_id=course_id)
        
        if status_filter:
            enrollments = enrollments.filter(status=status_filter)
        
        # Pagination
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        paginator = Paginator(enrollments, page_size)
        page_obj = paginator.get_page(page_number)
        
        serializer = EnrollmentSerializer(page_obj, many=True)
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
        Create a new enrollment.
        """
        serializer = EnrollmentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            enrollment = serializer.save()
            response_serializer = EnrollmentSerializer(enrollment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentDetailView(APIView):
    """
    Retrieve, update or delete an enrollment instance.
    """
    
    def get_object(self, pk):
        """
        Get enrollment object or raise 404.
        """
        return get_object_or_404(Enrollment, pk=pk)
    
    def get(self, request, pk):
        """
        Retrieve a specific enrollment.
        """
        enrollment = self.get_object(pk)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Update a specific enrollment.
        """
        enrollment = self.get_object(pk)
        serializer = EnrollmentCreateUpdateSerializer(enrollment, data=request.data)
        if serializer.is_valid():
            updated_enrollment = serializer.save()
            response_serializer = EnrollmentSerializer(updated_enrollment)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Delete a specific enrollment.
        """
        enrollment = self.get_object(pk)
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
