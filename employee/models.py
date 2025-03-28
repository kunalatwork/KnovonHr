from django.db import models

# # Create your models here.
# from django.db import models
# from django.db.models import Max
# import os

# # Create your models here.

# class Department(models.Model):
#     ACTIVE = 'Active'
#     INACTIVE = 'Inactive'
#     STATUS_CHOICES = [ (ACTIVE, 'Active'),(INACTIVE, 'Inactive')]

#     department_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     status = models.CharField( max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    
#     def __str__(self):
#         return self.name

# class Role(models.Model):
#     role_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=100)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='roles')

#     def __str__(self):
#         return self.title
    



# class Employee(models.Model):
#     ACTIVE = 'Active'
#     INACTIVE = 'Inactive'
    
#     STATUS_CHOICES = [
#         (ACTIVE, 'Active'),
#         (INACTIVE, 'Inactive'),
#     ]
#     employee_id = models.AutoField(primary_key=True)
#     emp_id = models.CharField(max_length=10, unique=True, blank=True)
#     firstName = models.CharField(max_length=100)
#     LastName = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     joining_Date = models.DateField()
#     # image = models.ImageField(upload_to='static/assets/img/', null=True, blank=True) 
#     role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
#     salary = models.DecimalField(max_digits=10, decimal_places=2)
#     about = models.TextField(null=True, blank=True)
#     gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender'), ('Other','Other')],null=True, blank=True)
#     status = models.CharField(max_length=10,choices=STATUS_CHOICES,default=ACTIVE,)
#     def __str__(self):
#         return f"{self.firstName} {self.LastName} ({self.employee_id})"

# class Personal_Detail(models.Model):
#     passportNumber = models.CharField(max_length=20, unique=True, blank=True, null=True)
#     nationality = models.CharField(max_length=50, null=True, blank=True)
#     maritalStatus = models.CharField(
#         max_length=50,
#         choices=[('Married', 'Married'),('Single','Single'),
#                  ('In a Relationship','In a Relationship'),
#                  ('Other', "Other")],
#                  null=True,
#                  blank=True)
#     SpouseName = models.CharField(max_length=50, null=True, blank=True)
#     childrens = models.IntegerField(null=True, blank=True)
#     birthday = models.DateField(null=True, blank=True)
#     employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=False, blank=False, related_name="personal_detail")


# class Address(models.Model):
#     address_id = models.AutoField(primary_key=True) 
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='addresses')
#     address = models.CharField(max_length=255, null=False, blank=False)
#     landmark = models.CharField(max_length=255, null=True, blank=True)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=20)
#     country = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.street_address}, {self.city}, {self.state} {self.postal_code}"
    

# class Attendance(models.Model):
#     attendance_id = models.AutoField(primary_key=True)
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
#     date = models.DateField()
#     check_in = models.TimeField()
#     check_out = models.TimeField()
#     status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')])

#     def __str__(self):
#         return f"{self.employee.first_name} {self.employee.last_name} - {self.date} - {self.status}"

