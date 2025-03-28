from django.shortcuts import render, HttpResponse
from django.contrib import redirects
from django.http import response
# from .models import Department
# from HrAdmin.serializers import DepartmentSerializer
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.


# def dashboard (request):
#     return render(request, "employee/index.html")

# def login (request):
#     return render(request, "employee/login.html")

def forgot_password (request):
    return render(request, "employee/forgot-password.html")

def employee_salary (request):
    return render(request, "employee/employee-salary.html")

def employees (request):
    return render(request, "employee/employees.html")

def employees_details (request):
    return render(request, "employee/employee-details.html")

def employees_dashboard (request):
    return render(request, "employee/employee-dashboard.html")

def Emp_departments (request):
    return render(request, "employee/departments.html")

def designations (request):
    return render(request, "employee/designations.html")


def holidays (request):
    return render(request, "employee/holidays.html")

def leaves (request):
    return render(request, "employee/leaves.html")

def attendance_employee (request):
    return render(request, "employee/attendance-employee.html")

# @api_view(['GET'])
# def department_List(request):
#     try:
#         departmentListData = Department.objects.all()
#         if not departmentListData:
#             return response({"detail": "No department found"}, status= status.HTTP_404_NOT_FOUND)
#         serializer = DepartmentSerializer(departmentListData, many=True)
#         return response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)