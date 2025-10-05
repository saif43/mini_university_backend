from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Section
from .serializers import SectionSerializer, SectionCreateUpdateSerializer


class SectionListCreateView(APIView):
    """
    List all sections or create a new section.
    """
    
    def get(self, request):
        """
        Retrieve all sections with optional search and pagination.
        """
        search = request.query_params.get('search', '')
        grade_id = request.query_params.get('grade', '')
        sections = Section.objects.select_related('grade').all()
        
        if search:
            sections = sections.filter(
                Q(name__icontains=search) | Q(grade__name__icontains=search)
            )
        
        if grade_id:
            sections = sections.filter(grade_id=grade_id)
        
        # Pagination
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 20)
        paginator = Paginator(sections, page_size)
        page_obj = paginator.get_page(page_number)
        
        serializer = SectionSerializer(page_obj, many=True)
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
        Create a new section.
        """
        serializer = SectionCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            section = serializer.save()
            response_serializer = SectionSerializer(section)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionDetailView(APIView):
    """
    Retrieve, update or delete a section instance.
    """
    
    def get_object(self, pk):
        """
        Get section object or raise 404.
        """
        return get_object_or_404(Section, pk=pk)
    
    def get(self, request, pk):
        """
        Retrieve a specific section.
        """
        section = self.get_object(pk)
        serializer = SectionSerializer(section)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        Update a specific section.
        """
        section = self.get_object(pk)
        serializer = SectionCreateUpdateSerializer(section, data=request.data)
        if serializer.is_valid():
            updated_section = serializer.save()
            response_serializer = SectionSerializer(updated_section)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Delete a specific section.
        """
        section = self.get_object(pk)
        section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
