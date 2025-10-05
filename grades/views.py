from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Grade
from .serializers import GradeSerializer, GradeCreateUpdateSerializer


class GradeListCreateView(APIView):
    """
    List all grades or create a new grade.
    """
    
    def get(self, request):
        """
        Retrieve all grades with optional search and pagination.
        """
        search = request.query_params.get('search', '')
        grades = Grade.objects.all()
        
        if search:
            grades = grades.filter(name__icontains=search)
        
        # Pagination
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        paginator = Paginator(grades, page_size)
        page_obj = paginator.get_page(page_number)
        
        serializer = GradeSerializer(page_obj, many=True)
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
        Create a new grade.
        """
        serializer = GradeCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            grade = serializer.save()
            response_serializer = GradeSerializer(grade)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GradeDetailView(APIView):
    """
    Retrieve, update or delete a grade instance.
    """
    
    def get_object(self, pk):
        """
        Get grade object or raise 404.
        """
        return get_object_or_404(Grade, pk=pk)
    
    def get(self, request, pk):
        """
        Retrieve a specific grade.
        """
        grade = self.get_object(pk)
        serializer = GradeSerializer(grade)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Update a specific grade.
        """
        grade = self.get_object(pk)
        serializer = GradeCreateUpdateSerializer(grade, data=request.data)
        if serializer.is_valid():
            updated_grade = serializer.save()
            response_serializer = GradeSerializer(updated_grade)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Delete a specific grade.
        """
        grade = self.get_object(pk)
        grade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
