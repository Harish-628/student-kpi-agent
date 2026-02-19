# API Testing Guide - Student KPI Management System

This guide provides detailed examples for testing all API endpoints.

## 📌 API Base URL

```
http://localhost:8000
```

## 🔑 Authentication

All endpoints except login and register require JWT authentication.

### 1. Login (Get Access Token)

**Endpoint:** `POST /api/auth/login`

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "student123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 4,
    "email": "student@example.com",
    "name": "John Student",
    "role": "student",
    "department": "CSE"
  }
}
```

**Note:** Copy the `access_token` value. You'll need it for subsequent API calls.

### 2. Register New User

**Endpoint:** `POST /api/auth/register`

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "newpass123",
    "name": "New User",
    "role": "student",
    "department": "CSE"
  }'
```

**Response:**
```json
{
  "id": 5,
  "email": "newuser@example.com",
  "name": "New User",
  "role": "student",
  "department": "CSE",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "last_login": null
}
```

### 3. Get Current User Info

**Endpoint:** `GET /api/auth/me`

**Request:**
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "email": "admin@example.com",
  "role": "admin",
  "name": "Admin User"
}
```

---

## 👥 Student Management Endpoints

### 1. Add New Student

**Endpoint:** `POST /api/student/add`

**Authorization:** Required (Admin, Coordinator, Faculty)

**Request:**
```bash
curl -X POST http://localhost:8000/api/student/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "student_id": "STU005",
    "name": "Jane Doe",
    "email": "jane@example.com",
    "department": "ECE",
    "section": "A",
    "year": 3,
    "gpa": 8.5,
    "phone": "9876543210",
    "date_of_birth": "2002-05-15",
    "enrollment_date": "2021-06-01"
  }'
```

**Response:**
```json
{
  "student_id": "STU005",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "department": "ECE",
  "section": "A",
  "year": 3,
  "gpa": 8.5,
  "phone": "9876543210"
}
```

### 2. Get Student Details

**Endpoint:** `GET /api/student/{student_id}`

**Request:**
```bash
curl -X GET http://localhost:8000/api/student/STU001 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "student_id": "STU001",
  "name": "John Doe",
  "email": "john@example.com",
  "department": "CSE",
  "section": "A",
  "year": 4,
  "gpa": 8.75,
  "phone": "9123456789"
}
```

### 3. Update Student Information

**Endpoint:** `PUT /api/student/{student_id}`

**Authorization:** Required (Admin, Coordinator)

**Request:**
```bash
curl -X PUT http://localhost:8000/api/student/STU001 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "gpa": 8.9,
    "year": 4
  }'
```

**Response:**
```json
{
  "student_id": "STU001",
  "name": "John Doe",
  "email": "john@example.com",
  "department": "CSE",
  "gpa": 8.9,
  "year": 4
}
```

### 4. List All Students

**Endpoint:** `GET /api/students`

**Query Parameters:**
- `department` (optional) - Filter by department
- `year` (optional) - Filter by year
- `skip` (optional) - Pagination offset (default: 0)
- `limit` (optional) - Results per page (default: 100)

**Request:**
```bash
# Get all students
curl -X GET http://localhost:8000/api/students \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get CSE department students
curl -X GET "http://localhost:8000/api/students?department=CSE" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get 3rd year students
curl -X GET "http://localhost:8000/api/students?year=3" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Pagination: Get 5 students starting from 10th
curl -X GET "http://localhost:8000/api/students?skip=10&limit=5" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "student_id": "STU001",
    "name": "John Doe",
    "email": "john@example.com",
    "department": "CSE",
    "year": 4,
    "gpa": 8.75
  },
  {
    "student_id": "STU002",
    "name": "Jane Doe",
    "email": "jane@example.com",
    "department": "ECE",
    "year": 3,
    "gpa": 8.5
  }
]
```

### 5. Delete Student

**Endpoint:** `DELETE /api/student/{student_id}`

**Authorization:** Required (Admin only)

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/student/STU005 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "Student STU005 deleted successfully"
}
```

---

## 📊 KPI Management Endpoints

### 1. Add KPI Data

**Endpoint:** `POST /api/kpi/add`

**Authorization:** Required (Admin, Coordinator, Faculty)

**Request:**
```bash
curl -X POST http://localhost:8000/api/kpi/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "student_id": "STU001",
    "internships": 2,
    "certifications": 3,
    "hackathons": 1,
    "publications": 0,
    "workshops": 5,
    "projects": 4,
    "club_activities": 2,
    "industrial_visits": 3,
    "research_papers": 0,
    "patents": 0
  }'
```

**Response:**
```json
{
  "id": 1,
  "student_id": "STU001",
  "internships": 2,
  "certifications": 3,
  "hackathons": 1,
  "publications": 0,
  "workshops": 5,
  "projects": 4,
  "club_activities": 2,
  "industrial_visits": 3,
  "research_papers": 0,
  "patents": 0,
  "last_updated": "2024-01-15T10:30:00"
}
```

### 2. Update KPI Data

**Endpoint:** `PUT /api/kpi/{student_id}`

**Authorization:** Required (Admin, Coordinator, Faculty)

**Request:**
```bash
curl -X PUT http://localhost:8000/api/kpi/STU001 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "internships": 3,
    "hackathons": 2
  }'
```

**Response:**
```json
{
  "id": 1,
  "student_id": "STU001",
  "internships": 3,
  "hackathons": 2,
  "last_updated": "2024-01-15T11:00:00"
}
```

### 3. Get KPI Data

**Endpoint:** `GET /api/student/{student_id}/kpi`

**Request:**
```bash
curl -X GET http://localhost:8000/api/student/STU001/kpi \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "student_id": "STU001",
  "internships": 2,
  "certifications": 3,
  "hackathons": 1,
  "publications": 0,
  "workshops": 5,
  "projects": 4,
  "club_activities": 2,
  "industrial_visits": 3,
  "research_papers": 0,
  "patents": 0
}
```

### 4. Bulk Upload KPI via CSV

**Endpoint:** `POST /api/kpi/upload`

**Authorization:** Required (Admin, Coordinator)

**CSV Format:**
```csv
student_id,internships,certifications,hackathons,publications,workshops,projects,club_activities,industrial_visits
STU001,2,3,1,0,5,4,2,3
STU002,1,2,0,1,3,2,1,2
STU003,3,4,2,0,6,5,3,4
```

**Request (using curl with file):**
```bash
curl -X POST http://localhost:8000/api/kpi/upload \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@kpi_data.csv"
```

**Response:**
```json
{
  "message": "CSV upload completed",
  "imported": 3,
  "failed": 0,
  "errors": []
}
```

---

## 🎯 Score & Performance Endpoints

### 1. Get Student Score

**Endpoint:** `GET /api/student/{student_id}/score`

**Request:**
```bash
curl -X GET http://localhost:8000/api/student/STU001/score \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "student_id": "STU001",
  "kpi_score": 78.5,
  "percentile_rank": 85,
  "overall_performance": 78.5,
  "academic_strength": 85,
  "professional_development": 75,
  "leadership_score": 70
}
```

### 2. Calculate & Store Student Score

**Endpoint:** `POST /api/student/{student_id}/calculate-score`

**Authorization:** Required (Admin, Coordinator, Faculty)

**Request:**
```bash
curl -X POST http://localhost:8000/api/student/STU001/calculate-score \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "student_id": "STU001",
  "kpi_score": 78.5,
  "career_readiness": 82.3
}
```

---

## 🏆 Milestone Endpoints

### 1. Add Milestone

**Endpoint:** `POST /api/student/{student_id}/milestone`

**Request:**
```bash
curl -X POST http://localhost:8000/api/student/STU001/milestone \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Published Research Paper",
    "description": "Published a paper on Machine Learning in ACM Conference",
    "category": "research",
    "achievement_date": "2024-01-10",
    "target_date": "2024-01-10",
    "status": "achieved",
    "impact_score": 8.5
  }'
```

**Response:**
```json
{
  "id": 1,
  "student_id": "STU001",
  "title": "Published Research Paper",
  "description": "Published a paper on Machine Learning in ACM Conference",
  "category": "research",
  "achievement_date": "2024-01-10",
  "status": "achieved",
  "impact_score": 8.5
}
```

### 2. Get Milestones

**Endpoint:** `GET /api/student/{student_id}/milestones`

**Query Parameters:**
- `status` (optional) - Filter by status (achieved, in_progress, pending)

**Request:**
```bash
# Get all milestones
curl -X GET http://localhost:8000/api/student/STU001/milestones \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get only achieved milestones
curl -X GET "http://localhost:8000/api/student/STU001/milestones?status=achieved" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "student_id": "STU001",
    "title": "Published Research Paper",
    "description": "Published a paper on Machine Learning in ACM Conference",
    "category": "research",
    "status": "achieved",
    "impact_score": 8.5
  },
  {
    "id": 2,
    "student_id": "STU001",
    "title": "Won Hackathon",
    "description": "First place in National Hackathon 2024",
    "category": "achievement",
    "status": "achieved",
    "impact_score": 9.0
  }
]
```

---

## 📈 Analytics & Reporting Endpoints

### 1. Get Dashboard Analytics

**Endpoint:** `GET /api/analytics/dashboard`

**Request:**
```bash
curl -X GET http://localhost:8000/api/analytics/dashboard \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "total_students": 50,
  "average_kpi": 75.3,
  "average_gpa": 7.8,
  "department_stats": [
    {
      "department": "CSE",
      "student_count": 20,
      "average_kpi": 78.5
    },
    {
      "department": "ECE",
      "student_count": 15,
      "average_kpi": 76.2
    },
    {
      "department": "ME",
      "student_count": 15,
      "average_kpi": 71.1
    }
  ],
  "top_performers": [
    {
      "student_id": "STU001",
      "name": "John Doe",
      "kpi_score": 92.3
    },
    {
      "student_id": "STU002",
      "name": "Jane Smith",
      "kpi_score": 89.7
    }
  ]
}
```

### 2. Get Peer Comparison

**Endpoint:** `GET /api/analytics/comparison/{student_id}`

**Request:**
```bash
curl -X GET http://localhost:8000/api/analytics/comparison/STU001 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "student_id": "STU001",
  "student_name": "John Doe",
  "kpi_score": 85.5,
  "department": "CSE",
  "department_percentile": 92.5,
  "department_rank": 2,
  "total_in_department": 20,
  "average_department_kpi": 78.3
}
```

### 3. Get Performance Trends

**Endpoint:** `GET /api/analytics/trends/{student_id}`

**Query Parameters:**
- `days` (optional) - Number of days to look back (default: 90)

**Request:**
```bash
# Get last 90 days
curl -X GET http://localhost:8000/api/analytics/trends/STU001 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get last 30 days
curl -X GET "http://localhost:8000/api/analytics/trends/STU001?days=30" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "student_id": "STU001",
  "dates": [
    "2023-10-15T10:30:00",
    "2023-11-15T10:30:00",
    "2023-12-15T10:30:00",
    "2024-01-15T10:30:00"
  ],
  "scores": [72.5, 75.3, 78.1, 85.5],
  "trend_direction": "up",
  "improvement_rate": 17.93,
  "current_score": 85.5,
  "starting_score": 72.5
}
```

---

## 🌐 Using Swagger UI (Interactive Testing)

The easiest way to test APIs is using Swagger UI:

1. **Open in Browser:** http://localhost:8000/docs
2. **Login First:** Find `/api/auth/login` endpoint
3. **Click "Try it out"**
4. **Fill in credentials:** 
   ```json
   {
     "email": "student@example.com",
     "password": "student123"
   }
   ```
5. **Copy the `access_token`** from response
6. **Click the "Authorize" button** (top right)
7. **Paste token** in format: `Bearer <token>`
8. **Test other endpoints** - they'll automatically include auth header

---

## ✅ Common Test Scenarios

### Scenario 1: Complete Workflow
1. Login → Get token
2. Add Student → Get student_id
3. Add KPI → Add data for that student
4. Calculate Score → Get performance metrics
5. View Analytics → Check dashboard

### Scenario 2: Bulk Data Import
1. Prepare CSV file with student data
2. Create students via POST /api/student/add
3. Upload KPI data via POST /api/kpi/upload
4. Calculate scores for all
5. Generate reports

### Scenario 3: Performance Analysis
1. Get student score
2. Get peer comparison
3. Get performance trends
4. Export data

---

## 🔐 Authentication Tips

- **Token Expiry:** 30 minutes
- **Header Format:** `Authorization: Bearer <token>`
- **Refresh:** Login again to get new token
- **Test with Swagger:** Use "Authorize" button

---

## 📝 Error Handling

### Common Error Responses

```json
{
  "detail": "Invalid credentials"
}
// Status Code: 401
```

```json
{
  "detail": "Student not found"
}
// Status Code: 404
```

```json
{
  "detail": "Only admin/coordinator can update students"
}
// Status Code: 403
```

---

For more information, see [README.md](README.md) and [SETUP_GUIDE.md](SETUP_GUIDE.md)
