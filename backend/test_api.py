#!/usr/bin/env python3
"""
Simple API test script for the Expense Tracker backend.
This script tests the main API endpoints to ensure they're working correctly.
"""

import requests
import json
from datetime import date

BASE_URL = 'http://localhost:5000'

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f'{BASE_URL}/api/health')
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_user_registration():
    """Test user registration."""
    print("🔍 Testing user registration...")
    try:
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
        if response.status_code == 201:
            print("✅ User registration passed")
            return True
        elif response.status_code == 409:
            print("⚠️ User already exists (this is expected on subsequent runs)")
            return True
        else:
            print(f"❌ User registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ User registration error: {e}")
        return False

def test_user_login():
    """Test user login and return token."""
    print("🔍 Testing user login...")
    try:
        data = {
            "username": "testuser",
            "password": "password123"
        }
        response = requests.post(f'{BASE_URL}/api/auth/login', json=data)
        if response.status_code == 200:
            token = response.json().get('token')
            print("✅ User login passed")
            return token
        else:
            print(f"❌ User login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ User login error: {e}")
        return None

def test_get_categories():
    """Test getting expense categories."""
    print("🔍 Testing get categories...")
    try:
        response = requests.get(f'{BASE_URL}/api/expenses/categories')
        if response.status_code == 200:
            categories = response.json().get('categories', [])
            print(f"✅ Categories retrieved: {len(categories)} categories")
            return True
        else:
            print(f"❌ Get categories failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get categories error: {e}")
        return False

def test_create_expense(token):
    """Test creating an expense."""
    print("🔍 Testing create expense...")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            "amount": 25.50,
            "description": "Test lunch expense",
            "category": "Food",
            "date": str(date.today())
        }
        response = requests.post(f'{BASE_URL}/api/expenses', json=data, headers=headers)
        if response.status_code == 201:
            expense_id = response.json().get('expense', {}).get('id')
            print("✅ Expense creation passed")
            return expense_id
        else:
            print(f"❌ Expense creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Expense creation error: {e}")
        return None

def test_get_expenses(token):
    """Test getting expenses."""
    print("🔍 Testing get expenses...")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{BASE_URL}/api/expenses', headers=headers)
        if response.status_code == 200:
            expenses = response.json().get('expenses', [])
            print(f"✅ Expenses retrieved: {len(expenses)} expenses")
            return True
        else:
            print(f"❌ Get expenses failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get expenses error: {e}")
        return False

def test_update_expense(token, expense_id):
    """Test updating an expense."""
    if not expense_id:
        print("⚠️ Skipping expense update test (no expense ID)")
        return True
    
    print("🔍 Testing update expense...")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            "amount": 30.00,
            "description": "Updated test lunch expense"
        }
        response = requests.put(f'{BASE_URL}/api/expenses/{expense_id}', json=data, headers=headers)
        if response.status_code == 200:
            print("✅ Expense update passed")
            return True
        else:
            print(f"❌ Expense update failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Expense update error: {e}")
        return False

def test_get_user_profile(token):
    """Test getting user profile."""
    print("🔍 Testing get user profile...")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{BASE_URL}/api/user/profile', headers=headers)
        if response.status_code == 200:
            print("✅ User profile retrieval passed")
            return True
        else:
            print(f"❌ User profile retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ User profile retrieval error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Expense Tracker API Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 8
    
    # Test 1: Health check
    if test_health_check():
        tests_passed += 1
    
    # Test 2: User registration
    if test_user_registration():
        tests_passed += 1
    
    # Test 3: User login
    token = test_user_login()
    if token:
        tests_passed += 1
    
    # Test 4: Get categories
    if test_get_categories():
        tests_passed += 1
    
    if token:
        # Test 5: Create expense
        expense_id = test_create_expense(token)
        if expense_id:
            tests_passed += 1
        
        # Test 6: Get expenses
        if test_get_expenses(token):
            tests_passed += 1
        
        # Test 7: Update expense
        if test_update_expense(token, expense_id):
            tests_passed += 1
        
        # Test 8: Get user profile
        if test_get_user_profile(token):
            tests_passed += 1
    else:
        print("⚠️ Skipping authenticated tests due to login failure")
    
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the API implementation.")

if __name__ == '__main__':
    main()