from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import GradeCourse
from grades.models import Grade
from courses.models import Course


class GradeCourseModelTestCase(TestCase):
    """Test cases for GradeCourse model"""
    
    def setUp(self):
        self.grade = Grade.objects.create(name="Grade 1")
        self.course = Course.objects.create(name="Mathematics", description="Basic math")
    
    def test_grade_course_creation(self):
        """Test creating a grade-course relationship"""
        grade_course = GradeCourse.objects.create(
            grade=self.grade,
            course=self.course
        )
        self.assertEqual(str(grade_course), "Grade 1 - Mathematics")
        self.assertEqual(grade_course.grade, self.grade)
        self.assertEqual(grade_course.course, self.course)
    
    def test_unique_constraint(self):
        """Test that the same grade-course combination cannot be created twice"""
        GradeCourse.objects.create(grade=self.grade, course=self.course)
        
        with self.assertRaises(Exception):
            GradeCourse.objects.create(grade=self.grade, course=self.course)


class GradeCourseAPITestCase(APITestCase):
    """Test cases for GradeCourse API endpoints"""
    
    def setUp(self):
        self.grade1 = Grade.objects.create(name="Grade 1")
        self.grade2 = Grade.objects.create(name="Grade 2")
        self.course1 = Course.objects.create(name="Mathematics")
        self.course2 = Course.objects.create(name="English")
        
        self.grade_course = GradeCourse.objects.create(
            grade=self.grade1,
            course=self.course1
        )
    
    def test_list_grade_courses(self):
        """Test listing grade-course relationships"""
        url = reverse('grade_course:grade-course-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_grade_course(self):
        """Test creating a new grade-course relationship"""
        url = reverse('grade_course:grade-course-list-create')
        data = {
            'grade': self.grade2.id,
            'course': self.course2.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(GradeCourse.objects.filter(grade=self.grade2, course=self.course2).exists())
    
    def test_get_grade_course_detail(self):
        """Test retrieving a specific grade-course relationship"""
        url = reverse('grade_course:grade-course-detail', kwargs={'pk': self.grade_course.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['grade'], self.grade1.id)
        self.assertEqual(response.data['course'], self.course1.id)
    
    def test_courses_by_grade(self):
        """Test getting courses for a specific grade"""
        url = reverse('grade_course:courses-by-grade', kwargs={'grade_id': self.grade1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['courses']), 1)
        self.assertEqual(response.data['courses'][0]['name'], 'Mathematics')
    
    def test_grades_by_course(self):
        """Test getting grades for a specific course"""
        url = reverse('grade_course:grades-by-course', kwargs={'course_id': self.course1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['grades']), 1)
        self.assertEqual(response.data['grades'][0]['name'], 'Grade 1')
