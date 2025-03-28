from django.contrib import admin
from HrAdmin.models import (Department,Role, Employee, Personal_Detail,
                             Attendance, Address, Experience, BankDetail,
                             Education, Todo, Holiday, Asset,Category, EmergencyContact)
# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'status']

class employeeSearch(admin.ModelAdmin):
    list_display = ('emp_id', 'firstName', 'lastName', 'email', 'department', 'role')
    search_fields = ('firstName', 'lastName', 'emp_id')
    list_filter = ('department', 'role')

class roleSearch(admin.ModelAdmin):
    list_display = ('title', 'department', 'status')

class personalDetail(admin.ModelAdmin):
    list_display=('employee','passportNumber','nationality','maritalStatus','SpouseName','childrens','birthday')

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Role, roleSearch)
admin.site.register(Employee,employeeSearch)
admin.site.register(Personal_Detail, personalDetail)
admin.site.register(Attendance)
admin.site.register(Address)
admin.site.register(Experience)
admin.site.register(BankDetail)
admin.site.register(Education)
admin.site.register(EmergencyContact)
admin.site.register(Asset)
admin.site.register(Category)
admin.site.register(Holiday)
admin.site.register(Todo)


