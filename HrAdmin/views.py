import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Department
from django.contrib.auth.decorators import login_required
from datetime import datetime

def login(request):
    return render(request, "login.html")

import requests
from django.shortcuts import redirect
from django.contrib import messages

def doLogin(request):
    auth_api = "http://127.0.0.1:8000/hrAdmin/api/auth/login/"

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        auth_data = {
            "username": email,
            "password": password
        }

        print(auth_data)
        
        try:
            response = requests.post(auth_api, json=auth_data)

            if response.status_code == 200:

                user_data = response.json()
                request.session['auth_token'] = user_data.get('token')
                request.session['user_email'] = email
                return render(request, "HrAdmin/index.html", {'user_data':user_data})

            else:
                print(f"Error: {response.status_code} - {response.text}")
                messages.error(request, "Invalid username and password.")
                return redirect('login')

        except requests.exceptions.RequestException as e:
            # Catch any exceptions during the request (e.g., network issues)
            print(f"An error occurred: {e}")
            messages.error(request, "An error occurred while processing your request. Please try again.")
            return redirect('login')

    else:
        # If the method is not POST, redirect back to the login page
        return redirect('login')


# @login_required
def dashboard (request):
    allEmp_api = "http://127.0.0.1:8000/hrAdmin/api/getEmployeeList"
    response = requests.get(allEmp_api)
    empData = response.json()

    empData = empData[:5]

    for employee in empData: 
        if 'joining_Date' in employee:
            employee['joining_Date'] = datetime.strptime( employee['joining_Date'], '%Y-%m-%d').strftime('%d %b %Y') 
    return render(request, "HrAdmin/index.html", {'empData':empData})

def login (request):
    return render(request, "HrAdmin/login.html")

def forgot_password (request):
    return render(request, "HrAdmin/forgot-password.html")

def employees (request):
    allEmp_api = "http://127.0.0.1:8000/hrAdmin/api/getEmployeeList"
    response = requests.get(allEmp_api)
    empData = response.json()
    Activecount = 0
    InactiveCount = 0
    for employee in empData:
        if employee['status']=='Active':
            Activecount = Activecount+1
        if employee['status'] == "Inactive":
            InactiveCount=InactiveCount+1

    totalCount = Activecount+InactiveCount
    for employee in empData: 
        if 'joining_Date' in employee:
            employee['joining_Date'] = datetime.strptime( employee['joining_Date'], '%Y-%m-%d').strftime('%d %b %Y')      

    return render(request, "HrAdmin/employees.html", {'empData': empData, 'Activecount': Activecount, 'InactiveCount':InactiveCount, 'totalCount':totalCount})

def employees_details(request, employee_id):
    print(employee_id)
    get_emp_detail_url = f"http://127.0.0.1:8000/hrAdmin/api/employeeDetail/{employee_id}"

    try:
        emp_response = requests.get(get_emp_detail_url)
        if emp_response.status_code == 200:
            emp_detail = emp_response.json()

            personal_detail = emp_detail.get('personal_detail', None)
            if personal_detail is not None:
                if 'birthday' in personal_detail:
                    personal_detail['birthday'] = datetime.strptime(personal_detail['birthday'], '%Y-%m-%d').strftime('%d %b %Y')
            else:
                print("Error: 'personal_detail' is None")
         
            experiences = emp_detail.get('experiences', [])
            for exp in experiences:
                if 'start_date' in exp:
                    exp['start_date'] = datetime.strptime(exp['start_date'], '%Y-%m-%d').strftime('%Y')
                if 'end_date' in exp:
                    if exp['end_date'] in ["Present", None, ""]:
                        exp['end_date'] = 'Present'
                    else:
                        try:
                            exp['end_date'] = datetime.strptime(exp['end_date'], '%Y-%m-%d').strftime('%Y')
                        except ValueError:
                            exp['end_date'] = 'Invalid Date'

            # Ensure 'employee_asset' is a list, even if it's None
            employee_asset = emp_detail.get('employee_asset', [])
            for asset in employee_asset:
                if 'assigned_date' in asset:
                    asset['assigned_date'] = datetime.strptime(asset['assigned_date'], '%Y-%m-%d').strftime('%b %d %Y')

            # Ensure 'joining_Date' exists before formatting it
            if 'joining_Date' in emp_detail:
                emp_detail['joining_Date'] = datetime.strptime(emp_detail['joining_Date'], '%Y-%m-%d').strftime('%d %b %Y')

            # Ensure 'educations' is a list, even if it's None
            educations = emp_detail.get('educations', [])
            for exp in educations:
                if 'start_date' in exp:
                    exp['start_date'] = datetime.strptime(exp['start_date'], '%Y-%m-%d').strftime('%Y')
                if 'end_date' in exp:
                    exp['end_date'] = datetime.strptime(exp['end_date'], '%Y-%m-%d').strftime('%Y')

            return render(request, "HrAdmin/employee-details.html", {"employeeDetail": emp_detail})
        else:
            return render(request, "employee-details.html", {"error": "Employee details not found."})

    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {str(e)}")
        return render(request, "employee-details.html", {
            "error": f"An error occurred while retrieving data: {str(e)}"
        })

def departments(request):
    departmentList_api = "http://127.0.0.1:8000/hrAdmin/api/getDepartmentList"
    addDepartment_api = "http://127.0.0.1:8000/hrAdmin/api/addDepartment"
    
    if request.method=="GET":
        try:
            response = requests.get(departmentList_api)
            if response.status_code == 200:
                departmentJsonData = response.json()
                return render(request, "HrAdmin/departments.html", {'departmentData':departmentJsonData})
            else:
                messages.error(request, 'Failed to fetch department data.')
                return render(request, "HrAdmin/departments.html")
        except requests.exceptions.RequestException as e:
            messages.error("Failed to fatch department data")
            return render(request, "HrAdmin/departments.html")
        
    if request.method == "POST":
        data = request.POST 
        departmentName = data.get("departmentName")
        status = data.get("status")
        try:
            response = requests.get(departmentList_api)
            if response.status_code == 200:
                departmentJsonData = response.json()
                if any(department['name'].lower() == departmentName.lower() for department in departmentJsonData):
                    messages.error(request, 'A department with this name already exists.')
                    return redirect('departments')
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Error checking for duplicate department. Please try again later.'}, status=500)
    
        department_data={
            "name" : departmentName,
            "status" : status
        }
        try:
            requests.post(addDepartment_api, json=department_data)
            print(response.status_code)
            if response.status_code == 200:
                messages.success(request, 'Department added successfully!')
                return redirect('departments')
            else:
                messages.error(request, 'Failed to add department. Please try again.')
                return redirect('departments')

        except requests.exceptions.RequestException as e:
            return render(request, "HrAdmin/departments.html", {'error': 'Something went wrong. Please try again later.'})

def removeDepartment(request, department_id):
    delete_api = f"http://127.0.0.1:8000/hrAdmin/api/removeDepartment/{department_id}/"
    try:
        response = requests.delete(delete_api)
        if response.status_code==200:
            messages.success(request, 'Department deleted successfully!')
            return redirect('departments')
        else:
            messages.error(request, 'Failed to delete department. Please try again.')
            return redirect('departments')
    except requests.exceptions.RequestException as e:
        print("Error during delete request:", e)
        messages.error(request, "Something went wrong while deleting the department.")

    return redirect('departments')

def edit_department(request, department_id):
    updateDepartment_api = f"http://127.0.0.1:8000/hrAdmin/api/updateDepartment/{department_id}"
    data = request.POST
    department = data.get("department")
    status = data.get("status")

    departmentData = {
        "department": department,
        "status": status
    }

    try:
        response = requests.put(updateDepartment_api, data=departmentData)
        if response.status_code == 200:
            print("Department updated successfully")
        else:
            print(f"Failed to update department. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while updating department: {e}")
    return redirect("departments")

def designations (request):
    addRole_api = "http://127.0.0.1:8000/hrAdmin/api/addRole"
    getDepartment_api = "http://127.0.0.1:8000/hrAdmin/api/getDepartmentList"
    getRole_api = "http://127.0.0.1:8000/hrAdmin/api/getRoleList"
    response = requests.get(getDepartment_api)
    querySet = requests.get(getRole_api)

    if  request.method=="GET":  
        if response.status_code == 200:
            designationData = response.json()
            if querySet:
                roleData = querySet.json()
                return render(request, 
                            "HrAdmin/designations.html" , 
                            {'designationData':designationData,
                            'roleData':roleData})
            else:
                return render(request, "HrAdmin/designations.html" , {'designationData':designationData})
    
    if request.method=="POST":   
        designationName = request.POST.get("designationName")
        department = request.POST.get("department")
        status = request.POST.get("status")

        set_data = {
            "title" :  designationName,
            "department" :department,
            "status" : status
            }
        try:
            requests.post(addRole_api, data=set_data)
            return redirect("designations") 

        except requests.exceptions.RequestException as e:
            messages.error("Unable to save role")
            return redirect("designations") 
            
    return redirect("designations")

def deleteRole(request, role_id):
    getRole_api = f"http://127.0.0.1:8000/hrAdmin/api/removeRole/{role_id}"
    requests.delete(getRole_api)
    return redirect("designations")

def roleEdit(request, role_id):
    editRole_api = f"http://127.0.0.1:8000/hrAdmin/api/updateRole/{role_id}"

    title = request.POST.get("title")
    department = request.POST.get("department")
    status = request.POST.get("status")
    roleData = {
        "title":title,
        "department":department,
        "status":status
    }
    requests.put(editRole_api, data=roleData)
    return redirect("designations")

def holidays(request):
    if request.method == 'GET':
        holidayList_api = "http://127.0.0.1:8000/hrAdmin/api/holiday-list/"
        try:
            response = requests.get(holidayList_api)
            response.raise_for_status()
            holidayData = response.json()
            getData =  response.json()
        
            for holiday in holidayData:
                holiday_date = datetime.strptime(holiday['date'], "%Y-%m-%d").date()
                holiday['date'] = datetime.strptime(holiday['date'], "%Y-%m-%d").strftime('%d %b %Y')
                if holiday_date > datetime.now().date():
                    holiday['status'] = "Upcoming"
                else:
                    holiday['status'] = "Spend"

            if not holidayData:
                messages.info(request, "No holidays available at the moment.")
            
            return render(request, "HrAdmin/holidays.html", {'holidayData': holidayData, "getData":getData})
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching holiday data: {e}")
            messages.error(request, "Failed to fetch holiday data. Please try again later.")
            
            return render(request, "HrAdmin/holidays.html", {'holidayData': []})
    
    if request.method == "POST":
        addHoliday_api = "http://127.0.0.1:8000/hrAdmin/api/holiday-list/"
        holiday = request.POST
        title = holiday.get("title")
        date = holiday.get("date")
        description = holiday.get("description")

        holidayData={
            "title":title,
            "date":date,
            "description": description
            }
        try:
            requests.post(addHoliday_api, data=holidayData)
            return redirect("holidays")
        except Exception as e:
            print("Unable to add holiday:", {e})

        return redirect("holidays")

def deleteHoliday(request, id):
    holiday_api = f"http://127.0.0.1:8000/hrAdmin/api/holiday-detail/{id}/"

    try:
        response = requests.delete(holiday_api)
        if response.status_code == 204:
            messages.success(request, "Holiday deleted successfully!")
        else:
            messages.error(request, "Failed to delete holiday. Please try again.")
    except requests.exceptions.RequestException as e:
        print("Error during delete request:", e)
        messages.error(request, "Something went wrong while deleting the holiday.")
    return redirect("holidays")

def updateHoliday(request, id):
    data = request.POST
    Holiday_api = f"http://127.0.0.1:8000/hrAdmin/api/holiday-detail/{id}/"

    title = data.get("title")
    date = data.get("date")
    description = data.get("description")

    holiday_data = {
        "title": title,
        "date": date,
        "description": description
    }
    print(holiday_data)
    try:
        response = requests.put(Holiday_api, json=holiday_data)
        if response.status_code == 200:
            messages.success(request, "Holiday updated successfully!")
        else:
            messages.error(request, "Failed to update holiday. Please try again.")
    except requests.exceptions.RequestException as e:
        print("Something went wrong", e)
        messages.error(request, "Something went wrong while updating the holiday.")
    return redirect("holidays")

def assets (request):
    asset_api = "http://127.0.0.1:8000/hrAdmin/api/getAssetList"
    
    try:
        response = requests.get(asset_api)
        if response.status_code == 200:
            assetData = response.json()
            
            for asset in assetData:
                if 'assigned_date' in asset:
                    try:
                        asset['assigned_date'] = datetime.strptime(asset['assigned_date'], '%Y-%m-%d').strftime('%d %b %Y')
                    except ValueError as e:
                        print(f"Error parsing date: {e}")
                        asset['assigned_date'] = "Invalid Date" 

            messages.success(request, "Asset fetched successfully!")
            return render(request, "HrAdmin/assets.html", {"asset": assetData})
        else:
            messages.error(request, f"Failed to fetch asset. Status Code: {response.status_code}")
            return render(request, "HrAdmin/assets.html")
    
    except Exception as e:
        print(e)
        messages.error(request, "An error occurred while fetching asset.")
        return render(request, "HrAdmin/assets.html")
    

def deleteAsset(request, id):
    pass

def editAsset(request, id):
    pass

def assets_category(request):

    if request.method == "GET":
        assetCategory_api = "http://127.0.0.1:8000/hrAdmin/api/getAssetCategoryList"
        
        try:
            response = requests.get(assetCategory_api)
        
            if response.status_code == 200:
                categoryData = response.json()
                messages.success(request, "Categories fetched successfully!")
                return render(request, "HrAdmin/asset-categories.html", {"category": categoryData})
            else:
                messages.error(request, f"Failed to fetch categories. Status Code: {response.status_code}")
                return render(request, "HrAdmin/asset-categories.html")
        
        except Exception as e:
            print(e)
            messages.error(request, "An error occurred while fetching categories.")
            return render(request, "HrAdmin/asset-categories.html")
    
    if request.method == "POST":
        addAssetCategory_api = "http://127.0.0.1:8000/hrAdmin/api/addAssetCategory/"

        name = request.POST.get("name")
        status = request.POST.get("status")

        asset_data = {
            "name": name,
            "status": status
        }

        try:
            response = requests.post(addAssetCategory_api, json=asset_data)
            if response.status_code == 201:
                messages.success(request, "Asset category added successfully!")
            else:
                messages.error(request, f"Failed to add category. Status Code: {response.status_code}")
            return redirect("assets-category")

        except Exception as e:
            print(e)
            messages.error(request, "An error occurred while adding the category.")
            return redirect("assets-category")
    
def deleteAssets_category(request, id):
    assetCategory_api = f"http://127.0.0.1:8000/hrAdmin/api/deleteAssetCategory/delete/{id}"
    try:
        response = requests.delete(assetCategory_api)
        if response.status_code == 204:
            messages.success(request, "Holiday deleted successfully!")
        else:
            messages.error(request, "Failed to delete holiday. Please try again.")
    except requests.exceptions.RequestException as e:
        print("Error during delete request:", e)
        messages.error(request, "Something went wrong while deleting the holiday.")
    return redirect("assets-category")

def updateAssets_category(request, id):
    assetCategory_api = f"http://127.0.0.1:8000/hrAdmin/api/editAssetCategory/edit/{id}/"
    
    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        status = data.get("status")

        updateCategory_data = {
            "name": name,
            "status": status
        }
        try:
            response = requests.put(assetCategory_api, json=updateCategory_data)
            if response.status_code == 200 or response.status_code == 204:
                messages.success(request, "Category updated successfully!")
            else:
                messages.error(request, f"Failed to update category. Status Code: {response.status_code}")
            return redirect("assets-category")
        except Exception as e:
            print(e)
            messages.error(request, "An error occurred while updating the category.")
            return redirect("assets-category")


def todo (request):
    return render(request, "HrAdmin/todo.html")

def leaves (request):
    return render(request, "HrAdmin/leaves.html")

def attendance_employee (request):
    return render(request, "HrAdmin/attendance-employee.html")

def leaves_request (request):
    return render(request, "HrAdmin/leaves-request.html")

def employee_salary (request):
    return render(request, "HrAdmin/employee-salary.html")

    

