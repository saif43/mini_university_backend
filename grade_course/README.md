# Grade-Course App Documentation

## Overview
The `grade_course` app manages the many-to-many relationship between grades and courses in the Mini University system. It defines which courses are available for specific grades.

## Features
- ✅ Create grade-course relationships
- ✅ List all grade-course relationships with filtering
- ✅ Get courses by grade
- ✅ Get grades by course
- ✅ Bulk assign courses to grades
- ✅ Summary view of relationships
- ✅ Full CRUD operations
- ✅ Admin interface integration
- ✅ Comprehensive API documentation

## Model Structure

### GradeCourse Model
```python
class GradeCourse(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grade_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grade_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Constraints:**
- Unique together: `(grade, course)` - prevents duplicate relationships
- Cascade delete: When a grade or course is deleted, related relationships are also deleted

## API Endpoints

### Basic CRUD Operations

#### 1. List/Create Grade-Course Relationships
- **GET** `/api/grade-courses/` - List all relationships
- **POST** `/api/grade-courses/` - Create new relationship

**Query Parameters for GET:**
- `search` - Search by grade or course name
- `grade` - Filter by grade ID
- `course` - Filter by course ID
- `page` - Page number for pagination
- `page_size` - Items per page

**POST Request Body:**
```json
{
  "grade": 1,
  "course": 1
}
```

#### 2. Grade-Course Detail Operations
- **GET** `/api/grade-courses/{id}/` - Get specific relationship
- **PUT** `/api/grade-courses/{id}/` - Update relationship
- **DELETE** `/api/grade-courses/{id}/` - Delete relationship

### Specialized Views

#### 3. Courses by Grade
- **GET** `/api/grade-courses/grade/{grade_id}/courses/`
- Returns all courses assigned to a specific grade

**Response Format:**
```json
{
  "id": 1,
  "name": "Grade 1",
  "courses": [
    {
      "id": 1,
      "name": "Mathematics",
      "description": "Basic math concepts",
      "grade_course_id": 1
    }
  ]
}
```

#### 4. Grades by Course
- **GET** `/api/grade-courses/course/{course_id}/grades/`
- Returns all grades that have this course assigned

**Response Format:**
```json
{
  "id": 1,
  "name": "Mathematics",
  "description": "Basic math concepts",
  "grades": [
    {
      "id": 1,
      "name": "Grade 1",
      "grade_course_id": 1
    }
  ]
}
```

#### 5. Summary View
- **GET** `/api/grade-courses/summary/`
- Returns simplified list of all relationships

#### 6. Bulk Assignment
- **POST** `/api/grade-courses/bulk-assign/`
- Assign multiple courses to a grade at once

**Request Body:**
```json
{
  "grade_id": 1,
  "courses": [
    {"course_id": 1},
    {"course_id": 2},
    {"course_id": 3}
  ]
}
```

**Response:**
```json
{
  "created": [...],
  "created_count": 3,
  "errors": []
}
```

## Serializers

### GradeCourseSerializer
Full serializer with related data and enrollment counts.

### GradeCourseCreateUpdateSerializer
Simplified serializer for create/update operations with validation.

### GradeCourseSummarySerializer
Minimal serializer for summary views.

### CoursesByGradeSerializer
Shows all courses for a specific grade.

### GradesByCourseSerializer
Shows all grades for a specific course.

## Usage Examples

### 1. Create a Grade-Course Relationship
```bash
curl -X POST http://127.0.0.1:8000/api/grade-courses/ \
  -H "Content-Type: application/json" \
  -d '{"grade": 1, "course": 1}'
```

### 2. Get All Courses for Grade 1
```bash
curl http://127.0.0.1:8000/api/grade-courses/grade/1/courses/
```

### 3. Get All Grades for Mathematics Course
```bash
curl http://127.0.0.1:8000/api/grade-courses/course/1/grades/
```

### 4. Bulk Assign Courses to a Grade
```bash
curl -X POST http://127.0.0.1:8000/api/grade-courses/bulk-assign/ \
  -H "Content-Type: application/json" \
  -d '{
    "grade_id": 1,
    "courses": [
      {"course_id": 1},
      {"course_id": 2}
    ]
  }'
```

### 5. Search Relationships
```bash
curl "http://127.0.0.1:8000/api/grade-courses/?search=mathematics"
```

## Admin Interface

The admin interface provides:
- List view with grade, course, and enrollment counts
- Filtering by grade, course, and creation date
- Search functionality across grade and course names
- Inline editing capabilities
- Optimized queries with select_related

## Validation Rules

1. **Unique Constraint**: Each grade-course combination can only exist once
2. **Foreign Key Validation**: Grade and course must exist
3. **Cascade Delete**: Relationships are deleted when parent objects are deleted

## Integration with Other Apps

### Enrollments Integration
The grade_course relationships work with the enrollments system:
- Students can only enroll in courses assigned to their grade
- Enrollment counts are calculated per grade-course relationship

### Usage in Views
```python
# Get courses available for a student's grade
student_grade = student.grade
available_courses = Course.objects.filter(
    grade_courses__grade=student_grade
)
```

## Testing

### Run Unit Tests
```bash
python manage.py test grade_course
```

### Run API Tests
```bash
python test_grade_course_api.py
```

## Files Structure

```
grade_course/
├── __init__.py
├── admin.py          # Admin configuration
├── apps.py           # App configuration
├── models.py         # GradeCourse model
├── serializers.py    # DRF serializers
├── tests.py          # Unit tests
├── urls.py           # URL routing
├── views.py          # API views
└── migrations/       # Database migrations
```

## Performance Considerations

1. **Query Optimization**: Uses `select_related()` for foreign key fields
2. **Pagination**: Built-in pagination for large datasets
3. **Indexing**: Unique constraint creates database index
4. **Bulk Operations**: Efficient bulk assignment endpoint

## Future Enhancements

Potential features that could be added:
- Course prerequisites based on grade progression
- Academic year/semester constraints
- Course capacity management per grade
- Advanced reporting and analytics

The grade_course app provides a solid foundation for managing the curriculum structure in the Mini University system! 🎓