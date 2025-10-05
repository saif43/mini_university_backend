#!/usr/bin/env python
"""
Sample data creation script for Mini University API
"""
import os
import sys
import django
from datetime import date, datetime

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_university.settings')
django.setup()

from grades.models import Grade
from sections.models import Section
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment


def create_sample_data():
    """Create sample data for testing the API"""
    
    print("Creating sample data...")
    
    # Create Grades
    grades_data = [
        "Kindergarten",
        "Grade 1",
        "Grade 2",
        "Grade 3", 
        "Grade 4",
        "Grade 5"
    ]
    
    grades = []
    for grade_name in grades_data:
        grade, created = Grade.objects.get_or_create(name=grade_name)
        grades.append(grade)
        if created:
            print(f"Created grade: {grade_name}")
    
    # Create Sections
    sections_data = [
        ("A", 0), ("B", 0), ("C", 0),  # Kindergarten
        ("A", 1), ("B", 1),           # Grade 1
        ("A", 2), ("B", 2), ("C", 2), # Grade 2
        ("A", 3), ("B", 3),           # Grade 3
        ("A", 4), ("B", 4), ("C", 4), # Grade 4
        ("A", 5), ("B", 5),           # Grade 5
    ]
    
    sections = []
    for section_name, grade_idx in sections_data:
        section, created = Section.objects.get_or_create(
            name=section_name,
            grade=grades[grade_idx]
        )
        sections.append(section)
        if created:
            print(f"Created section: {grades[grade_idx].name} - {section_name}")
    
    # Create Courses
    courses_data = [
        ("Mathematics", "Basic mathematics including arithmetic, geometry, and problem solving"),
        ("English Language", "Reading, writing, speaking, and listening skills development"),
        ("Science", "Introduction to natural sciences, experiments, and scientific thinking"),
        ("Social Studies", "History, geography, and social awareness"),
        ("Art", "Creative expression through drawing, painting, and crafts"),
        ("Physical Education", "Physical fitness, sports, and healthy lifestyle"),
        ("Music", "Musical instruments, singing, and rhythm"),
        ("Computer Skills", "Basic computer literacy and digital skills")
    ]
    
    courses = []
    for course_name, description in courses_data:
        course, created = Course.objects.get_or_create(
            name=course_name,
            defaults={'description': description}
        )
        courses.append(course)
        if created:
            print(f"Created course: {course_name}")
    
    # Create Students
    students_data = [
        ("Alice Johnson", date(2018, 3, 15), "STU001", 0, 0),
        ("Bob Smith", date(2018, 7, 22), "STU002", 0, 1),
        ("Charlie Brown", date(2017, 11, 8), "STU003", 1, 3),
        ("Diana Prince", date(2017, 4, 30), "STU004", 1, 4),
        ("Eve Wilson", date(2016, 9, 12), "STU005", 2, 5),
        ("Frank Miller", date(2016, 1, 25), "STU006", 2, 6),
        ("Grace Lee", date(2016, 6, 18), "STU007", 2, 7),
        ("Henry Davis", date(2015, 10, 3), "STU008", 3, 8),
        ("Ivy Chen", date(2015, 2, 14), "STU009", 3, 9),
        ("Jack Taylor", date(2014, 8, 7), "STU010", 4, 10),
    ]
    
    students = []
    for name, birthdate, student_id, grade_idx, section_idx in students_data:
        student, created = Student.objects.get_or_create(
            student_id=student_id,
            defaults={
                'name': name,
                'birthdate': birthdate,
                'grade': grades[grade_idx],
                'section': sections[section_idx]
            }
        )
        students.append(student)
        if created:
            print(f"Created student: {name} ({student_id})")
    
    # Create Enrollments
    enrollments_data = [
        (0, 0, 'active'),     # Alice - Mathematics
        (0, 1, 'active'),     # Alice - English
        (0, 4, 'active'),     # Alice - Art
        (1, 0, 'completed'),  # Bob - Mathematics  
        (1, 1, 'active'),     # Bob - English
        (2, 0, 'active'),     # Charlie - Mathematics
        (2, 1, 'active'),     # Charlie - English
        (2, 2, 'active'),     # Charlie - Science
        (3, 1, 'completed'),  # Diana - English
        (3, 2, 'active'),     # Diana - Science
    ]
    
    for student_idx, course_idx, status in enrollments_data:
        enrollment_data = {
            'student': students[student_idx],
            'course': courses[course_idx],
            'status': status
        }
        
        if status == 'completed':
            enrollment_data['final_grade'] = 85.50
        
        enrollment, created = Enrollment.objects.get_or_create(
            student=students[student_idx],
            course=courses[course_idx],
            defaults=enrollment_data
        )
        
        if created:
            print(f"Created enrollment: {students[student_idx].name} -> {courses[course_idx].name}")
    
    print("\nSample data creation completed!")
    print(f"Created {Grade.objects.count()} grades")
    print(f"Created {Section.objects.count()} sections") 
    print(f"Created {Course.objects.count()} courses")
    print(f"Created {Student.objects.count()} students")
    print(f"Created {Enrollment.objects.count()} enrollments")


if __name__ == '__main__':
    create_sample_data()