from django.urls import path
from HrAdmin import views
from .views import searchDepartment, searchRole, DepartmentListView
from adminAPI import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [

    #Login
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/login/', views.login_view, name='login'),

    # Department API
    path("getDepartmentList/", views.getDepartment_List, name="getDepartmentList"),
    path("addDepartment", views.addDepartment, name="addDepartment"),
    path("removeDepartment/<int:department_id>/", views.removeDepartment, name="removeDepartment"),
    path("updateDepartment/<int:department_id>", views.updateDepartment, name="updateDepartment"),
    path('department/search/', searchDepartment.as_view(), name='department-search'),
    path('department/filter/', DepartmentListView.as_view(), name='department-list'),


    # Role API
    path("getRoleList", views.getRoleList, name="getRoleList"),
    path("addRole", views.addRole, name="addRole"),
    path("removeRole/<int:role_id>", views.removeRole, name="removeRole"),
    path("updateRole/<int:role_id>", views.updateRole, name="updateRole"),
    path("roleDetail/<int:role_id>", views.roleDetail, name="roleDetail"),
    path('roles/search/', searchRole.as_view(), name='role-search'),


    # Employee API
    path('getEmployeeList', views.getEmployeeList, name='getEmployeeList'),
    path('addEmployee', views.addEmployee, name='addEmployee'),
    path('updateDeleteEmployee/<int:employee_id>', views.updateDeleteEmployee, name='updateDeleteEmployee'),
    path('employeeDetail/<int:employee_id>', views.employeeDetail, name='employeeDetail'),

    # Peronal Detail API
    path('personalDetail/', views.personalDetail, name="personalDetail"),
    path('addPersonalDetail/', views.addPersonalDetail, name="addPersonalDetail"),
    path('updateDeletePersonalDetail/<int:id>', views.updateDeletePersonalDetail, name='updateDeletePersonalDetail'),
    path('empPersonalDetail/<int:id>', views.empPersonalDetail, name='empPersonalDetail'),

    # Address API
    path('addresses/', views.address_list, name='address-list'),
    path('addresses/<int:pk>/', views.address_detail, name='address-detail'),

    # Experience API
    path('experiences/', views.experience_list, name='experience-list'),
    path('experiences/<int:pk>/', views.experience_detail, name='experience-detail'),

    # Attendances API
    path('attendances/', views.attendance_list, name='attendance-list'),
    path('attendances/<int:pk>/', views.attendance_detail, name='attendance-detail'),

    # BAnk Detail API
    path('bank-details/', views.bank_detail_list, name='bank-detail-list'),
    path('bank-details/<int:pk>/', views.bank_detail_detail, name='bank-detail-detail'),

    #Education API
    path('educations/', views.education_list, name='education-list'),
    path('educations/<int:pk>/', views.education_detail, name='education-detail'), 

    #path('emergency-contact/', views.emergency_contact, name='emergency-contact'),


    path('holiday-list/', views.holiday_list, name='holiday-list'),
    path('holiday-detail/<int:id>/', views.holiday_detail, name='holiday_detail'),

    path("getAssetCategoryList/", views.asset_category, name="asset-category"),
    path("addAssetCategory/", views.addAsset_category, name="addAsset-category"),
    path('editAssetCategory/edit/<int:id>/', views.editAssetCategory, name="editassetCategory"),
    path('deleteAssetCategory/delete/<int:id>/', views.deleteAssetCategory, name="deleteassetCategory"),

    path("getAssetList/", views.asset, name="asset"),
    path("addAsset/", views.addAsset, name="addAsset"),
    path('editAsset/edit/<int:id>/', views.editAsset, name="editasset"),
    path('deleteAsset/delete/<int:id>/', views.deleteAsset, name="deleteasset"),

    path('getTodosList/', views.todo_list_create, name='get-todo-list'),
    path('addTodos/', views.add_todo, name='add-get-todo'),
    path('getTodoDetail/<int:pk>/', views.todo_detail, name='get-todo-listDetail'),
    path('updateTodo/<int:pk>/', views.update_todo, name='update-todo-list'),
    path('deleteTodo/<int:pk>/', views.delete_todo, name='delete-todo-list'),

 ]