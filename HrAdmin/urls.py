from django.urls import path, include
from HrAdmin import views
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from HrAdmin import views

# # Create a router and register our ViewSets with it.
# router = DefaultRouter()
# router.register(r'roles', rolesViewSet, basename='roleViewSet')
# urlpatterns = router.urls

urlpatterns = [

    # Login page

    path('login/', views.login, name='login'),  # This is for rendering the login page
    path('doLogin/', views.doLogin, name='doLogin'), 
    
    # Dashboard page
    path('', views.dashboard, name='dashboard'),

    # Departments list page
    path('departments/', views.departments, name='departments'),

    # Remove department, with department ID
    path("department/<department_id>/", views.removeDepartment, name="deleteDepartment"),

    # Edit department, with department ID
    path('edit_department/<int:department_id>', views.edit_department, name='edit_department'),

    
    path("forgot-password/", views.forgot_password, name="forgot-password"),
    path("employee-salary/", views.employee_salary, name="employees-salary"),
    path("employees/", views.employees, name="employees"),
    path("employee-details/<int:employee_id>/", views.employees_details, name="employees-details"),
    path("designations/", views.designations, name="designations"),
    path("roles/<role_id>", views.deleteRole, name="deleteRole"),
    path("roles/edit/<role_id>", views.roleEdit, name="editRole"),
   
    
    path("holidays/", views.holidays, name="holidays"),
    path("holiday/<int:id>/", views.deleteHoliday, name="Deleteholiday"),
    path("holiday/edit/<int:id>/", views.updateHoliday, name="updateHoliday"),

    path("leaves/", views.leaves, name="leaves"),
    path("attendance-employee/", views.attendance_employee, name="attendance-employee"),
    path("leaves-request/", views.leaves_request, name="leaves-request"),

    
    path('assets-category/', views.assets_category, name='assets-category'),
    path('<int:id>/', views.deleteAssets_category, name='deleteAssets-category'),
    path('assets-category/<int:id>/', views.updateAssets_category, name='updateAssetsCategory'),

    path('assets/', views.assets, name='assets'),
    path('assets/<int:id>/', views.deleteAsset, name='deleteAsset'),
    path('<int:id>/', views.editAsset, name='editAsset'),

    path('todo/', views.todo, name='todo'),
    
    
]