# Mini University Django REST API

A comprehensive Django REST API for managing a university system with separate apps for grades, sections, students, courses, and enrollments.

## Features

- Modular architecture with separate Django apps for each entity
- Class-based APIViews for better maintainability
- CRUD operations for all entities
- RESTful API endpoints
- Comprehensive serialization and validation
- Foreign key relationships with proper constraints
- Pagination and search functionality
- Admin interface for easy data management
- Proper error handling and validation messages

## Database Schema

### Grade
- id (Primary Key)
- name

### Section
- id (Primary Key)
- name
- grade_id (Foreign Key to Grade)

### Student
- id (Primary Key)
- name
- birthdate
- student_id (Unique identifier)
- grade_id (Foreign Key to Grade)
- section_id (Foreign Key to Section)

### Course
- id (Primary Key)
- name
- description

### Enrollment
- id (Primary Key)
- student_id (Foreign Key to Student)
- course_id (Foreign Key to Course)
- enrollment_date
- status (active, completed, dropped, failed)
- final_grade

## Setup

1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

## Project Structure

```
mini_university/
├── grades/          # Grade management app
├── sections/        # Section management app  
├── students/        # Student management app
├── courses/         # Course management app
├── enrollments/     # Enrollment management app
└── mini_university/ # Main project settings
```

## API Endpoints

### Grades
- **GET** `/api/grades/` - List all grades with pagination and search
- **POST** `/api/grades/` - Create a new grade
- **GET** `/api/grades/{id}/` - Retrieve a specific grade
- **PUT** `/api/grades/{id}/` - Update a specific grade
- **DELETE** `/api/grades/{id}/` - Delete a specific grade

### Sections
- **GET** `/api/sections/` - List all sections with filtering by grade
- **POST** `/api/sections/` - Create a new section
- **GET** `/api/sections/{id}/` - Retrieve a specific section
- **PUT** `/api/sections/{id}/` - Update a specific section
- **DELETE** `/api/sections/{id}/` - Delete a specific section

### Students
- **GET** `/api/students/` - List all students with filtering by grade/section
- **POST** `/api/students/` - Create a new student
- **GET** `/api/students/{id}/` - Retrieve a specific student
- **PUT** `/api/students/{id}/` - Update a specific student
- **DELETE** `/api/students/{id}/` - Delete a specific student

### Courses
- **GET** `/api/courses/` - List all courses with search functionality
- **POST** `/api/courses/` - Create a new course
- **GET** `/api/courses/{id}/` - Retrieve a specific course
- **PUT** `/api/courses/{id}/` - Update a specific course
- **DELETE** `/api/courses/{id}/` - Delete a specific course

### Enrollments
- **GET** `/api/enrollments/` - List all enrollments with filtering
- **POST** `/api/enrollments/` - Create a new enrollment
- **GET** `/api/enrollments/{id}/` - Retrieve a specific enrollment
- **PUT** `/api/enrollments/{id}/` - Update a specific enrollment
- **DELETE** `/api/enrollments/{id}/` - Delete a specific enrollment

## Query Parameters

All list endpoints support the following query parameters:
- `search` - Search across relevant fields
- `page` - Page number for pagination
- `page_size` - Number of items per page (default: 20)

Additional filtering:
- Sections: `grade` - Filter by grade ID
- Students: `grade`, `section` - Filter by grade/section ID  
- Enrollments: `student`, `course`, `status` - Filter by student/course ID or status