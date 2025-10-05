#!/usr/bin/env python
"""
API Testing Script for Mini University
This script demonstrates all CRUD operations for each endpoint.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def print_response(response, title):
    """Print formatted API response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_grades_api():
    """Test Grades API endpoints"""
    print("\n🎓 TESTING GRADES API")
    
    # List all grades
    response = requests.get(f"{BASE_URL}/grades/")
    print_response(response, "GET /api/grades/ - List All Grades")
    
    # Create a new grade
    new_grade = {"name": "Grade 6"}
    response = requests.post(f"{BASE_URL}/grades/", json=new_grade)
    print_response(response, "POST /api/grades/ - Create New Grade")
    
    if response.status_code == 201:
        grade_id = response.json()['id']
        
        # Get specific grade
        response = requests.get(f"{BASE_URL}/grades/{grade_id}/")
        print_response(response, f"GET /api/grades/{grade_id}/ - Get Specific Grade")
        
        # Update grade
        updated_grade = {"name": "Grade 6 - Updated"}
        response = requests.put(f"{BASE_URL}/grades/{grade_id}/", json=updated_grade)
        print_response(response, f"PUT /api/grades/{grade_id}/ - Update Grade")
        
        # Delete grade
        response = requests.delete(f"{BASE_URL}/grades/{grade_id}/")
        print_response(response, f"DELETE /api/grades/{grade_id}/ - Delete Grade")

def test_sections_api():
    """Test Sections API endpoints"""
    print("\n📚 TESTING SECTIONS API")
    
    # List all sections
    response = requests.get(f"{BASE_URL}/sections/")
    print_response(response, "GET /api/sections/ - List All Sections")
    
    # Create a new section (assuming grade with ID 1 exists)
    new_section = {"name": "D", "grade": 1}
    response = requests.post(f"{BASE_URL}/sections/", json=new_section)
    print_response(response, "POST /api/sections/ - Create New Section")
    
    if response.status_code == 201:
        section_id = response.json()['id']
        
        # Get specific section
        response = requests.get(f"{BASE_URL}/sections/{section_id}/")
        print_response(response, f"GET /api/sections/{section_id}/ - Get Specific Section")
        
        # Update section
        updated_section = {"name": "D-Updated", "grade": 1}
        response = requests.put(f"{BASE_URL}/sections/{section_id}/", json=updated_section)
        print_response(response, f"PUT /api/sections/{section_id}/ - Update Section")
        
        # Delete section
        response = requests.delete(f"{BASE_URL}/sections/{section_id}/")
        print_response(response, f"DELETE /api/sections/{section_id}/ - Delete Section")

def test_courses_api():
    """Test Courses API endpoints"""
    print("\n📖 TESTING COURSES API")
    
    # List all courses
    response = requests.get(f"{BASE_URL}/courses/")
    print_response(response, "GET /api/courses/ - List All Courses")
    
    # Create a new course
    new_course = {
        "name": "Advanced Mathematics",
        "description": "Advanced mathematical concepts and problem solving"
    }
    response = requests.post(f"{BASE_URL}/courses/", json=new_course)
    print_response(response, "POST /api/courses/ - Create New Course")
    
    if response.status_code == 201:
        course_id = response.json()['id']
        
        # Get specific course
        response = requests.get(f"{BASE_URL}/courses/{course_id}/")
        print_response(response, f"GET /api/courses/{course_id}/ - Get Specific Course")
        
        # Update course
        updated_course = {
            "name": "Advanced Mathematics - Updated",
            "description": "Updated description for advanced mathematical concepts"
        }
        response = requests.put(f"{BASE_URL}/courses/{course_id}/", json=updated_course)
        print_response(response, f"PUT /api/courses/{course_id}/ - Update Course")
        
        # Delete course
        response = requests.delete(f"{BASE_URL}/courses/{course_id}/")
        print_response(response, f"DELETE /api/courses/{course_id}/ - Delete Course")

def test_students_api():
    """Test Students API endpoints"""
    print("\n👨‍🎓 TESTING STUDENTS API")
    
    # List all students
    response = requests.get(f"{BASE_URL}/students/")
    print_response(response, "GET /api/students/ - List All Students")
    
    # Create a new student (assuming grade 1 and section 1 exist)
    new_student = {
        "name": "Test Student",
        "birthdate": "2018-05-15",
        "student_id": "TEST001",
        "grade": 1,
        "section": 1
    }
    response = requests.post(f"{BASE_URL}/students/", json=new_student)
    print_response(response, "POST /api/students/ - Create New Student")
    
    if response.status_code == 201:
        student_id = response.json()['id']
        
        # Get specific student
        response = requests.get(f"{BASE_URL}/students/{student_id}/")
        print_response(response, f"GET /api/students/{student_id}/ - Get Specific Student")
        
        # Update student
        updated_student = {
            "name": "Test Student - Updated",
            "birthdate": "2018-05-15",
            "student_id": "TEST001",
            "grade": 1,
            "section": 1
        }
        response = requests.put(f"{BASE_URL}/students/{student_id}/", json=updated_student)
        print_response(response, f"PUT /api/students/{student_id}/ - Update Student")
        
        # Delete student
        response = requests.delete(f"{BASE_URL}/students/{student_id}/")
        print_response(response, f"DELETE /api/students/{student_id}/ - Delete Student")

def test_enrollments_api():
    """Test Enrollments API endpoints"""
    print("\n📝 TESTING ENROLLMENTS API")
    
    # List all enrollments
    response = requests.get(f"{BASE_URL}/enrollments/")
    print_response(response, "GET /api/enrollments/ - List All Enrollments")
    
    # Create a new enrollment (assuming student 1 and course 3 exist)
    new_enrollment = {
        "student": 1,
        "course": 3,
        "status": "active"
    }
    response = requests.post(f"{BASE_URL}/enrollments/", json=new_enrollment)
    print_response(response, "POST /api/enrollments/ - Create New Enrollment")
    
    if response.status_code == 201:
        enrollment_id = response.json()['id']
        
        # Get specific enrollment
        response = requests.get(f"{BASE_URL}/enrollments/{enrollment_id}/")
        print_response(response, f"GET /api/enrollments/{enrollment_id}/ - Get Specific Enrollment")
        
        # Update enrollment
        updated_enrollment = {
            "student": 1,
            "course": 3,
            "status": "completed",
            "final_grade": 92.5
        }
        response = requests.put(f"{BASE_URL}/enrollments/{enrollment_id}/", json=updated_enrollment)
        print_response(response, f"PUT /api/enrollments/{enrollment_id}/ - Update Enrollment")
        
        # Delete enrollment
        response = requests.delete(f"{BASE_URL}/enrollments/{enrollment_id}/")
        print_response(response, f"DELETE /api/enrollments/{enrollment_id}/ - Delete Enrollment")

def test_search_and_filtering():
    """Test search and filtering capabilities"""
    print("\n🔍 TESTING SEARCH AND FILTERING")
    
    # Search grades
    response = requests.get(f"{BASE_URL}/grades/?search=Grade")
    print_response(response, "GET /api/grades/?search=Grade - Search Grades")
    
    # Filter sections by grade
    response = requests.get(f"{BASE_URL}/sections/?grade=1")
    print_response(response, "GET /api/sections/?grade=1 - Filter Sections by Grade")
    
    # Search students
    response = requests.get(f"{BASE_URL}/students/?search=Alice")
    print_response(response, "GET /api/students/?search=Alice - Search Students")
    
    # Filter enrollments by status
    response = requests.get(f"{BASE_URL}/enrollments/?status=active")
    print_response(response, "GET /api/enrollments/?status=active - Filter by Status")

def main():
    """Run all API tests"""
    print("🚀 STARTING MINI UNIVERSITY API TESTS")
    print("Make sure the Django server is running on http://127.0.0.1:8000")
    
    try:
        # Test connection
        response = requests.get(f"{BASE_URL}/grades/")
        if response.status_code != 200:
            print("❌ Server is not responding. Please start the Django server.")
            return
        
        print("✅ Server is running. Starting tests...")
        
        test_grades_api()
        test_sections_api() 
        test_courses_api()
        test_students_api()
        test_enrollments_api()
        test_search_and_filtering()
        
        print("\n🎉 ALL TESTS COMPLETED!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Please make sure Django server is running.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()