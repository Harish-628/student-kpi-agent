"""
Test script for Day 3 KPI Data Ingestion Module
Tests:
1. Adding students via API
2. Adding KPI data individually
3. Uploading KPI data via CSV
4. Retrieving and calculating KPI scores
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_add_students():
    """Add sample students to database"""
    print("\n=== Testing: Add Students ===")
    students = [
        {"student_id": "STU001", "name": "Alice Johnson", "department": "CSE", "section": "A", "year": 3},
        {"student_id": "STU002", "name": "Bob Smith", "department": "CSE", "section": "A", "year": 3},
        {"student_id": "STU003", "name": "Charlie Brown", "department": "CSE", "section": "B", "year": 3},
        {"student_id": "STU004", "name": "Diana Prince", "department": "ECE", "section": "A", "year": 3},
        {"student_id": "STU005", "name": "Eve Wilson", "department": "ECE", "section": "B", "year": 3},
    ]
    
    for student in students:
        try:
            response = requests.post(f"{BASE_URL}/student/add", json=student)
            if response.status_code == 200:
                print(f"✓ Added student: {student['student_id']} - {student['name']}")
            else:
                print(f"✗ Failed to add student {student['student_id']}: {response.text}")
        except Exception as e:
            print(f"✗ Error adding student {student['student_id']}: {str(e)}")

def test_add_single_kpi():
    """Test adding single KPI record"""
    print("\n=== Testing: Add Single KPI Record ===")
    kpi_data = {
        "student_id": "STU006",
        "internships": 1,
        "certifications": 2,
        "hackathons": 1,
        "publications": 0,
        "workshops": 1,
        "projects": 3,
        "club_activities": 2,
        "industrial_visits": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/kpi/add", json=kpi_data)
        if response.status_code == 200:
            print(f"✓ Added KPI for student STU006")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Failed to add KPI: {response.text}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_csv_upload():
    """Test uploading KPI data via CSV"""
    print("\n=== Testing: CSV Upload ===")
    
    with open('sample_kpi_data.csv', 'rb') as f:
        files = {'file': ('sample_kpi_data.csv', f, 'text/csv')}
        try:
            response = requests.post(f"{BASE_URL}/kpi/upload", files=files)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ CSV upload successful")
                print(f"  Imported: {result['imported']}")
                print(f"  Failed: {result['failed']}")
                if result['errors']:
                    print(f"  Errors: {result['errors']}")
            else:
                print(f"✗ CSV upload failed: {response.text}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

def test_get_kpi_score():
    """Test retrieving KPI scores"""
    print("\n=== Testing: Get KPI Score ===")
    test_students = ["STU001", "STU002", "STU003", "STU004", "STU005"]
    
    for student_id in test_students:
        try:
            response = requests.get(f"{BASE_URL}/student/{student_id}/kpi_score")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ {student_id}: Score={data['kpi_score']}, Readiness={data['career_readiness']}")
            else:
                print(f"✗ {student_id}: {response.text}")
        except Exception as e:
            print(f"✗ {student_id}: {str(e)}")

def test_get_student_kpi():
    """Test retrieving raw KPI data"""
    print("\n=== Testing: Get Student KPI Data ===")
    test_students = ["STU001", "STU002"]
    
    for student_id in test_students:
        try:
            response = requests.get(f"{BASE_URL}/student/{student_id}/kpi")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ {student_id}:")
                print(f"    Internships: {data.get('internships')}, Certifications: {data.get('certifications')}")
                print(f"    Hackathons: {data.get('hackathons')}, Publications: {data.get('publications')}")
            else:
                print(f"✗ {student_id}: {response.text}")
        except Exception as e:
            print(f"✗ {student_id}: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("DAY 3: KPI DATA INGESTION MODULE - TEST SUITE")
    print("=" * 60)
    
    # Wait a moment for server
    time.sleep(1)
    
    # Run tests
    test_add_students()
    time.sleep(1)
    test_add_single_kpi()
    time.sleep(1)
    test_csv_upload()
    time.sleep(1)
    test_get_student_kpi()
    time.sleep(1)
    test_get_kpi_score()
    
    print("\n" + "=" * 60)
    print("✓ Test Suite Complete!")
    print("=" * 60)
