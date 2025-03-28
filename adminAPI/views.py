from HrAdmin.models import (Department, Role, Employee, Personal_Detail, 
                            Address, Experience, Attendance, BankDetail, 
                            Education, Holiday, Todo, Asset, Category, EmergencyContact)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, filters
from HrAdmin.serializers import (departmentserializer, roleSerializers, getroleSerializers, 
                                 employeeSerializer, getEmployeeSerilizer, personalDetailSerializer, 
                                 EmployeeAddressSerializer, ExperienceSerializer, AttendanceSerializer, 
                                 BankDetailSerializer, EducationSerializer, EmergencyContactSerializer, 
                                 TodoSerializer, HolidaySerializer, AssetCategorySerializer,AssetSerializer,getAssetSerializer,
                                )
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
import django_filters
from rest_framework.response import Response
from rest_framework import status
from HrAdmin.serializers import LoginSerializer


# Search Department
class searchDepartment(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = departmentserializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
   
#Filter Department
class DepartmentFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Department.STATUS_CHOICES)

    class Meta:
        model = Department
        fields = ['status'] 

class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = departmentserializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = DepartmentFilter 
    ordering_fields = ['name', 'status']  
    ordering = ['name']    

#Search Role
class searchRole(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = roleSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title','department__name']

#Role Filter 
class RoleListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = roleSerializers
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['title', 'department']  
    ordering = ['title']

@api_view(['POST'])
def login_view(request):
    """
    Login API to authenticate user and return JWT tokens.
    """
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        # If validation is successful, return the user and tokens
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def getDepartment_List(request):
    try:
        departments = Department.objects.all()
        if not departments:
            return Response({'message': 'No department found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = departmentserializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        print(str(e))
        return Response({'message': 'Something went wrong', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def addDepartment(request):
    if request.method =='POST':
        objData = request.data
        serializer = departmentserializer(data=objData)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({'message': 'Department name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
def removeDepartment(request, department_id):
    try:
        objData = Department.objects.get(department_id=department_id)
        objData.delete()
        return Response({'message': 'Department deleted successfully'}, status=status.HTTP_200_OK)       
    except Department.DoesNotExist:
        return Response({'message': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)   
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
def updateDepartment(request, department_id):
    department = get_object_or_404(Department, department_id=department_id)
    serializer = departmentserializer(department, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Department updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK) 
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
def roleDetail(request, role_id):
    objData = Role.objects.get(role_id=role_id)
    serializer = roleSerializers(objData)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def addRole(request):
    if  request.method == 'POST':
        objs = request.data
        serializer = roleSerializers(data = objs)
        print(serializer)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'Role is already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def getRoleList(request):
    if request.method == "GET":
        try:
            objList = Role.objects.all()
            serializer = getroleSerializers(objList, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response({'message':'Roles are not found'})
    

@api_view(['Put'])
def updateRole(request, role_id):
    if request.method =="PUT":
        role = get_object_or_404(Role, role_id=role_id)
        serializer = roleSerializers(role, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Role updated successfully', 'data': serializer.data }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['DELETE'])
def removeRole(request,role_id ):
    querySet = Role.objects.get(role_id=role_id)
    if querySet:
        querySet.delete()
        return Response({'message': 'Role deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getEmployeeList(request):
    try:
        empData = Employee.objects.all()
        serializer = getEmployeeSerilizer(empData, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message':'Internal server error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def addEmployee(request):
    print(request.data)
    if request.method == "POST":
        objData = request.data
        serializer = employeeSerializer(data = objData)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'message': 'Email id already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def updateDeleteEmployee(request, employee_id):
    if request.method == "PUT":
        try:
            obj = get_object_or_404(Employee, employee_id=employee_id)
            serializer = getEmployeeSerilizer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updatedsuccessfully", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
  
        except Exception as e:
            print(e)
            return Response({"message": "Error fetching user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if request.method == "DELETE":
        try:
            obj = Employee.objects.get(employee_id=employee_id)
            if obj:
                obj.delete()
                return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"message": "Error deleting user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET'])        
def employeeDetail(request, employee_id):
    try:
        employee = Employee.objects.get(employee_id=employee_id)
        serializer = getEmployeeSerilizer(employee, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except NotFound:
        return Response({'message': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        print(e)
        return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def personalDetail(request):
    try:
        objData = Personal_Detail.objects.all()
        if objData:
            serializer = personalDetailSerializer(objData, many=True)
            return Response(
                {'message':'Personal detail fetched successfully', 
                'data' : serializer.data}, 
                status=status.HTTP_200_OK
                )
        else:
            return Response(
                {'message':'No record found', 
                'data' : []},  
                status=status.HTTP_200_OK
                )
    except Exception as e:
        print(e)
        return Response(
            {"message": "Error fetching personal details"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

@api_view(['POST'])
def addPersonalDetail(request):
   if request.method == "POST":
        Objdata = request.data
        serializer = personalDetailSerializer(data=Objdata)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'message': 'Data added successfully!', 'data': serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'message': 'Unable to save data', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": "Error saving personal details"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

@api_view(['Put', 'DELETE'])
def updateDeletePersonalDetail(request, id):
    if request.method == "PUT":
        try:
            obj = get_object_or_404(Personal_Detail, id=id)
            serializer = personalDetailSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
  
        except Exception as e:
            print(e)
            return Response({"message": "Error fetching user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == "DELETE":
        try:
            objData = get_object_or_404(Personal_Detail, id=id)
            if objData:
                objData.delete()
                return Response({"message": "Personal detail deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Personal detail not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"message": "Error deleting personal detail"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET'])
def empPersonalDetail(request, id):
    try:
        objData = get_object_or_404(Personal_Detail, id=id)
        serializer = personalDetailSerializer(objData, many=False)
        return Response({'message' : 'Data fetched successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
    except NotFound:
        return Response({'message': 'Personal details not found for this ID'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({'message':'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        


# Address APIs
@api_view(['GET', 'POST'])
def address_list(request):
    if request.method == 'GET':
        addresses = Address.objects.all()
        serializer = EmployeeAddressSerializer(addresses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def address_detail(request, pk):
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeAddressSerializer(address)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployeeAddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
def experience_list(request):
    if request.method == 'GET':
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def experience_detail(request, pk):
    try:
        experience = Experience.objects.get(pk=pk)
    except Experience.DoesNotExist:
        return Response({"error": "Experience not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExperienceSerializer(experience)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExperienceSerializer(experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', 'POST'])
def attendance_list(request):
    if request.method == 'GET':
        attendances = Attendance.objects.all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def attendance_detail(request, pk):
    try:
        attendance = Attendance.objects.get(pk=pk)
    except Attendance.DoesNotExist:
        return Response({"error": "Attendance record not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        attendance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def bank_detail_list(request):
    if request.method == 'GET':
        bank_details = BankDetail.objects.all()
        serializer = BankDetailSerializer(bank_details, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BankDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def bank_detail_detail(request, pk):
    try:
        bank_detail = BankDetail.objects.get(pk=pk)
    except BankDetail.DoesNotExist:
        return Response({"error": "Bank Detail not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BankDetailSerializer(bank_detail)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BankDetailSerializer(bank_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        bank_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def education_list(request):
    if request.method == 'GET':
        # Get all education records
        educations = Education.objects.all()
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new education record
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get, update or delete an education record by ID
@api_view(['GET', 'PUT', 'DELETE'])
def education_detail(request, pk):
    try:
        education = Education.objects.get(pk=pk)
    except Education.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Get the details of the education record
        serializer = EducationSerializer(education)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the education record
        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the education record
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
def emergency_number(request):
    if request.method == 'GET':
        contacts = EmergencyContact.objects.all()
        # Use `many=True` as you're returning a list of EmergencyNumber instances
        serializer = EmergencyContactSerializer(contacts, many=False)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmergencyContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
def holiday_list(request):
    if request.method == 'GET':
        # Retrieve all holidays
        holidays = Holiday.objects.all()
        serializer = HolidaySerializer(holidays, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new holiday
        serializer = HolidaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def holiday_detail(request, id):
    try:
        holiday = Holiday.objects.get(id=id)
    except Holiday.DoesNotExist:
        return Response({'detail': 'Holiday not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HolidaySerializer(holiday)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HolidaySerializer(holiday, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        holiday.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def asset_category(request):
    if request.method == "GET":
        assetObj = Category.objects.all()
        if not assetObj.exists():
            return Response({'detail': 'Asset category not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssetCategorySerializer(assetObj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = AssetCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def addAsset_category(request):
    if request.method == "POST":
        serializer = AssetCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['DELETE'])
def deleteAssetCategory(request, id):
    if request.method == "DELETE":
        if id is not None:
            try:
                category = Category.objects.get(id=id)
                category.delete()
                return Response({'detail': 'Asset category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            except Category.DoesNotExist:
                return Response({'detail': 'Asset category not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Category ID is required for deletion.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editAssetCategory(request, id):
     print(id)
     if request.method == "PUT":
        if id is not None:
            try:
                category = Category.objects.get(id=id)
                serializer = AssetCategorySerializer(category, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()  # Update the existing category
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Category.DoesNotExist:
                return Response({'detail': 'Asset category not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def asset(request):
    if request.method == "GET":
        assetObj = Asset.objects.all()
        if assetObj:
            serializer = getAssetSerializer(assetObj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Asset not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def addAsset(request):
    if request.method == "POST":
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
def deleteAsset(request, id):
    if request.method == "DELETE":
        if id is not None:
            try:
                category = Asset.objects.get(id=id)
                category.delete()
                return Response({'detail': 'Asset deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            except Category.DoesNotExist:
                return Response({'detail': 'Asset not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Category ID is required for deletion.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def editAsset(request, id):
     if request.method == "PUT":
        if id is not None:
            try:
                category = Asset.objects.get(id=id)
                serializer = AssetSerializer(category, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()  # Update the existing category
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Category.DoesNotExist:
                return Response({'detail': 'Asset category not found.'}, status=status.HTTP_404_NOT_FOUND)
            

@api_view(['GET'])
def todo_list_create(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    

@api_view(['POST'])
def add_todo(request):
    if request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def todo_detail(request, pk): 
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({'detail': 'Todo not found.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({'detail': 'Todo not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response({'detail': 'Todo not found.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        todo.delete()
        return Response({'detail': 'Todo deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

