from django.db import models

#Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Department(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = [ (ACTIVE, 'Active'),(INACTIVE, 'Inactive')]

    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.CharField( max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    
    def __str__(self):
        return self.name

class Role(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = [ (ACTIVE, 'Active'),(INACTIVE, 'Inactive')]
    role_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True, related_name='roles')
    status = models.CharField( max_length=10, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return self.title


class Employee(models.Model):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    employee_id = models.AutoField(primary_key=True)
    emp_id = models.CharField(max_length=10, unique=True, blank=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    joining_Date = models.DateField()
    image = models.ImageField(upload_to='static/assets/img/', null=True, blank=True) 
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees') 
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True) 
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    about = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('Transgender', 'Transgender'), ('Other', 'Other')], null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)


    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.employee_id})"
    
    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"


def validate_birthday(value):
    if value > timezone.now().date():
        raise ValidationError("Birthday cannot be in the future.")
    


class Personal_Detail(models.Model):
    passportNumber = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    maritalStatus = models.CharField(
        max_length=50,
        choices=[('Married', 'Married'),('Single','Single'),
                 ('In a Relationship','In a Relationship'),
                 ('Other', "Other")],
                 null=True,
                 blank=True)
    SpouseName = models.CharField(max_length=50, null=True, blank=True)
    childrens = models.IntegerField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True, validators=[validate_birthday])
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=False, blank=False, related_name="personal_detail")
    
    
    def __str__(self):
        return f"{self.employee.firstName} {self.employee.lastName} - Personal Details"
    
    class PersonalDetail(models.Model):
        class Meta:
            verbose_name = "Personal Detail"
            verbose_name_plural = "Personal Details"


class Address(models.Model):
    address_id = models.AutoField(primary_key=True) 
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=255, null=False, blank=False)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address},{self.landmark}, {self.city}, {self.state} {self.postal_code}"
    

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')])

    def __str__(self):
        return f"{self.employee.firstName} {self.employee.lastName} - {self.date} - {self.status}"
    
    @property
    def total_working_hours(self):
        """Calculates the total working hours (difference between check-in and check-out times)."""
        check_in_time = timedelta(hours=self.check_in.hour, minutes=self.check_in.minute, seconds=self.check_in.second)
        check_out_time = timedelta(hours=self.check_out.hour, minutes=self.check_out.minute, seconds=self.check_out.second)
        working_hours = check_out_time - check_in_time
        return str(working_hours)
    
    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"
    

class Experience(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.start_date} - {self.end_date if self.end_date else 'Present'})"
    
    def start_year(self):
        return self.start_date.year if self.start_date else None
    
    def end_year(self):
        return self.end_date.year if self.end_date else 'Present'  
        
      
    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

class BankDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='bank_detail')
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=30, unique=True)
    account_type = models.CharField(
        max_length=20,
        choices=[('Savings', 'Savings'), ('Current', 'Current'), ('Salary', 'Salary')],
    )
    ifsc_code = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=255)
    branch_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Bank Details for {self.employee.firstName} {self.employee.lastName}"

    class Meta:
        verbose_name = "Bank Detail"
        verbose_name_plural = "Bank Details"


class Education(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=200)
    institution_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  #
    field_of_study = models.CharField(max_length=200, null=True, blank=True)
    grade = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.degree} from {self.institution_name} ({self.start_date} - {self.end_date if self.end_date else 'Present'})"

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"


class EmergencyContact(models.Model):  
    primary_name = models.CharField(max_length=100)
    primary_relationship = models.CharField(max_length=50)
    primary_phone_no_1 = models.CharField(max_length=15)
    primary_phone_no_2 = models.CharField(max_length=15, blank=True, null=True)
    secondary_name = models.CharField(max_length=100, blank=True, null=True)
    secondary_relationship = models.CharField(max_length=50, blank=True, null=True)
    secondary_phone_no_1 = models.CharField(max_length=15, blank=True, null=True)
    secondary_phone_no_2 = models.CharField(max_length=15, blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='emergency_contacts')

    def __str__(self):
        return f"{self.primary_name} ({self.primary_relationship})"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Active'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"



class Asset(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_asset', blank=True, null=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='asset')
    name = models.CharField(max_length=255, unique=True)
    purchased_date = models.DateField()
    purchase_from = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100)
    warranty = models.IntegerField(help_text="Warranty period in months")
    asset_user = models.CharField(max_length=255, blank=True, null=True)
    assigned_date = models.DateField(default=timezone.now, blank=True, null=True) 
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Under_maintenance', 'Under Maintenance'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"



class Holiday(models.Model):
    title = models.CharField(max_length=255, unique=True)
    date = models.DateField()
    description = models.TextField()
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Holiday"
        verbose_name_plural = "Holiday"


class Todo(models.Model):
    title = models.CharField(max_length=255)
    TAG_CHOICES = [
        ('Internal', 'Internal'),
        ('Meetings', 'Meetings'),
        ('Reminder', 'Reminder'),
    ]
    tag = models.CharField(max_length=100, choices=TAG_CHOICES)

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    priority = models.CharField(max_length=6,choices=PRIORITY_CHOICES,default='medium')
    description = models.TextField()
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='todos', null=True, blank=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=12,choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todos"


    

