#!/usr/bin/env python3
"""
Test script for Grade-Course API endpoints
Run this script to test the grade-course relationship functionality
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_grade_course_basic_operations():
    """Test basic CRUD operations for grade-course relationships"""
    print("🔗 Testing Grade-Course Basic Operations...")
    
    # Get all grade-course relationships
    response = requests.get(f"{BASE_URL}/grade-courses/")
    print(f"GET /grade-courses/ - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['count']} grade-course relationships")
    
    # Create a new grade-course relationship (assuming grade 1 and course 1 exist)
    new_relationship = {
        "grade": 1,
        "course": 1
    }
    response = requests.post(f"{BASE_URL}/grade-courses/", json=new_relationship)
    print(f"POST /grade-courses/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        created_data = response.json()
        relationship_id = created_data['id']
        print(f"Created grade-course relationship with ID: {relationship_id}")
        
        # Get the specific relationship
        response = requests.get(f"{BASE_URL}/grade-courses/{relationship_id}/")
        print(f"GET /grade-courses/{relationship_id}/ - Status: {response.status_code}")
        
        # Delete the relationship
        response = requests.delete(f"{BASE_URL}/grade-courses/{relationship_id}/")
        print(f"DELETE /grade-courses/{relationship_id}/ - Status: {response.status_code}")

def test_courses_by_grade():
    """Test getting courses for a specific grade"""
    print("\n📚 Testing Courses by Grade...")
    
    grade_id = 1  # Assuming grade with ID 1 exists
    response = requests.get(f"{BASE_URL}/grade-courses/grade/{grade_id}/courses/")
    print(f"GET /grade-courses/grade/{grade_id}/courses/ - Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Grade '{data['name']}' has {len(data['courses'])} courses:")
        for course in data['courses']:
            print(f"  - {course['name']}")

def test_grades_by_course():
    """Test getting grades for a specific course"""
    print("\n🎓 Testing Grades by Course...")
    
    course_id = 1  # Assuming course with ID 1 exists
    response = requests.get(f"{BASE_URL}/grade-courses/course/{course_id}/grades/")
    print(f"GET /grade-courses/course/{course_id}/grades/ - Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Course '{data['name']}' is assigned to {len(data['grades'])} grades:")
        for grade in data['grades']:
            print(f"  - {grade['name']}")

def test_bulk_assign_courses():
    """Test bulk assigning courses to a grade"""
    print("\n📝 Testing Bulk Course Assignment...")
    
    bulk_data = {
        "grade_id": 2,  # Assuming grade with ID 2 exists
        "courses": [
            {"course_id": 2},  # Assuming course with ID 2 exists
            {"course_id": 3}   # Assuming course with ID 3 exists
        ]
    }
    
    response = requests.post(f"{BASE_URL}/grade-courses/bulk-assign/", json=bulk_data)
    print(f"POST /grade-courses/bulk-assign/ - Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"Successfully created {data['created_count']} relationships")
        if data['errors']:
            print("Errors encountered:")
            for error in data['errors']:
                print(f"  - {error}")

def test_summary():
    """Test getting grade-course summary"""
    print("\n📊 Testing Grade-Course Summary...")
    
    response = requests.get(f"{BASE_URL}/grade-courses/summary/")
    print(f"GET /grade-courses/summary/ - Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total grade-course relationships: {len(data)}")
        for relationship in data[:5]:  # Show first 5
            print(f"  - {relationship['grade_name']} → {relationship['course_name']}")

def main():
    """Main test function"""
    print("🚀 STARTING GRADE-COURSE API TESTS")
    print("Make sure the Django server is running on http://127.0.0.1:8000")
    
    try:
        # Test connection
        response = requests.get(f"{BASE_URL}/grade-courses/")
        if response.status_code not in [200, 404]:
            print("❌ Server is not responding properly. Please check the Django server.")
            return
        
        print("✅ Server is running. Starting tests...")
        
        test_grade_course_basic_operations()
        test_courses_by_grade()
        test_grades_by_course()
        test_bulk_assign_courses()
        test_summary()
        
        print("\n🎉 ALL GRADE-COURSE TESTS COMPLETED!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Please make sure Django server is running.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()