from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
import uuid
from django.contrib.auth.models import User

from school.services.application_models.student import CreateStudentRequest
from school.service_provider import container
from school.models import Student

# Create your views here.
def index(request):
    return render(request, "school/index.html", {"school_name": "Bole School", "is_successful" : False})

@login_required
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
@login_required
def list(request):
    students = container.student_repository().list()
    return render(request, "school/list.html", {"students": students, "is_successful": False})

@login_required
def view(request, student_id: uuid):
    student = container.student_repository().get(student_id)
    return render(request, "school/view.html", {"student": student})

@login_required
def delete(request, student_id: uuid):
    student = container.student_repository().get(student_id)
    student.delete()
    return redirect("list")

def login_user(request: HttpRequest):
    if request.method == "GET":
        redirect_to = request.GET.get("next")
        if redirect_to != None or redirect_to != "":
            return render(request, "login.html", {"next_url": redirect_to})
        return render(request, "login.html")
    username: str = request.POST.get("username")
    password: str = request.POST.get("password")
    redirect_to = request.POST.get("next")
    user: User = authenticate(username=username, password=password)
    if user: 
        login(request, user)
        if redirect_to == None or redirect_to == "":
            return redirect("list")
        else:
            return redirect(redirect_to)
    return render(request, "login.html", context={"message": "Username or password incorrect"})


def logout_user(request: HttpRequest):
    logout(request)
    return redirect("index")