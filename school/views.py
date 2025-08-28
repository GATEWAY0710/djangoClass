from django.http import HttpResponse
from django.shortcuts import redirect, render
import uuid
from django.contrib.auth.models import User

from school.services.application_models.student import CreateStudentRequest
from school.service_provider import container
from school.models import Student

# Create your views here.
def index(request):
    return render(request, "school/index.html", {"school_name": "Bole School", "is_successful" : False})

def create(request):
    if request.method == "GET":
        return render(request, "school/create.html", {"school_name": "Bole School", "is_successful" : True})
    username = request.POST.get("username", "")
    email = request.POST.get("email", "")
    phone_number = request.POST.get("phone_number", "")
    name = request.POST.get("name", "")
    password = request.POST.get("password", "")
    confrim_password = request.POST.get("confirm_password", "")
    response = container.student_service().create(CreateStudentRequest(email, name, password, confrim_password, username, phone_number))
    if response.status is False:
        return render(request, "school/create.html", {"school_name": "Bole School", "is_successful" : response.status, "message": response.message})
    return redirect("list")

def list(request):
    students = container.student_repository().list()
    return render(request, "school/list.html", {"students": students, "is_successful": False})

def view(request, student_id: uuid):
    student = container.student_repository().get(student_id)
    return render(request, "school/view.html", {"student": student})

def delete(request, student_id: uuid):
    student = container.student_repository().get(student_id)
    student.delete()
    return redirect("list")