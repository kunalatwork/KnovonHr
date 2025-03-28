import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from HrAdmin.models import (Department, Role, Employee, Personal_Detail, 
                            Address, Attendance, Experience, BankDetail, 
                            Education, EmergencyContact, Asset, Category, Todo, Holiday)
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name'] 


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField() 
#     password = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')

#         # Authenticate user using the custom EmailAuthBackend
#         user = authenticate(request=self.context.get('request'), username=username, password=password)
        
#         if not user:
#             raise serializers.ValidationError("Invalid credentials")

#         # Serialize the user data
#         user_data = UserSerializer(user).data

#         # Generate JWT tokens (access and refresh)
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         refresh_token = str(refresh)

#         # Return serialized user data and tokens
#         return {
#             'user': user_data,
#             'access': access_token,
#             'refresh': refresh_token
#         }
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Change to email field
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Check if email and password are provided
        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        # Authenticate user using email instead of username
        user = authenticate(request=self.context.get('request'), username=email, password=password)
        
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        # Check if user is active (optional check)
        if not user.is_active:
            raise serializers.ValidationError("User account is deactivated.")

        # Serialize the user data
        user_data = UserSerializer(user).data

        # Generate JWT tokens (access and refresh)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Return serialized user data and tokens
        return {
            'user': user_data,
            'access': access_token,
            'refresh': refresh_token
        }    


class departmentserializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
    
    def validate_name(self, value):
        valid_name_pattern = r"^[a-zA-Z\s]+$"
        if not re.match(valid_name_pattern, value):
            raise serializers.ValidationError("Special characters and numbers are not allowed in name")

        if not value.strip():
            raise serializers.ValidationError("The department name cannot be empty or just spaces.")
        
        department_id = self.instance.department_id if self.instance else None

        if department_id:
            if Department.objects.filter(name=value).exclude(department_id=department_id).exists():
                raise serializers.ValidationError(f"A department with the name '{value}' already exists.")
        else:
            if Department.objects.filter(name=value).exists():
                raise serializers.ValidationError(f"A department with the name '{value}' already exists.")

        return value
    

class departmentserializerfields(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id','name']

class getroleSerializers(serializers.ModelSerializer):
    department = departmentserializerfields()
    class Meta:
        model = Role
        fields = ['role_id','title', 'department', 'status']


class roleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
    
    def validate_title(self, data):

        if not data.strip():
            raise serializers.ValidationError("Role title can not be empty")
        
        valid_name_pattern = r"^[a-zA-Z\s]+$"
        if not re.match(valid_name_pattern, data):
            raise serializers.ValidationError("Special characters and numbers are not allowed in name")
        
        role_id = self.instance.role_id if self.instance else None

        if role_id:
            if Role.objects.filter(title=data).exclude(role_id=role_id).exists():
                raise serializers.ValidationError(f"{data} role is already exists")
        else:
            if Role.objects.filter(title=data).exists():
                raise serializers.ValidationError(f"{data} role is already exists")
        return data   

class employeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class personalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal_Detail
        fields = "__all__"

class EmployeeAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        

class AttendanceSerializer(serializers.ModelSerializer):
    total_working_hours = serializers.ReadOnlyField()
    class Meta:
        model = Attendance
        fields = '__all__'
    
class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    asset = AssetCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Asset
        fields = '__all__'

class getAssetSerializer(serializers.ModelSerializer):
    employee = employeeSerializer()
    Category = AssetCategorySerializer()
    class Meta:
        model = Asset
        fields = '__all__'

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ['id', 'title', 'date', 'description']

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
    
class getEmployeeSerilizer(serializers.ModelSerializer):
    personal_detail = personalDetailSerializer(read_only=True)
    addresses = EmployeeAddressSerializer(many=True, read_only=True)
    department = departmentserializer(read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    attendances = AttendanceSerializer(many=True, read_only=True)
    role = roleSerializers(read_only=True)
    bank_detail = BankDetailSerializer(read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    emergency_contacts = EmergencyContactSerializer(many=True, read_only=True)
    employee_asset = getAssetSerializer(many=True, read_only=True)
   

    class Meta:
        model = Employee
        fields = "__all__"




