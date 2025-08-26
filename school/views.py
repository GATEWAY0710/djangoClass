from django.http import HttpResponse
from django.shortcuts import redirect, render
import uuid
from django.contrib.auth.models import User

from school.models import Student

# Create your views here.
def index(request):
    return render(request, "school/index.html", {"school_name": "Bole School", "is_successful" : False})

def create(request):
    if request.method == "GET":
         return render(request, "school/create.html", {"school_name": "Bole School", "is_successful" : False})
    username = request.POST.get("username", "")
    email = request.POST.get("email", "")
    phone_number = request.POST.get("phone_number", "")
    name = request.POST.get("name", "")
    password = request.POST.get("password", "")
    matric_number = str(uuid.uuid4()).split("-")[0]
    
    user = User.objects.create_user(username=username, email=email, password=password)
    student = Student()
    student.id = uuid.uuid4()
    student.user = user
    student.matric_number = matric_number
    student.phone_number = phone_number
    student.name = name
    student.save()
    
    return redirect("list")

def list(request):
    students = Student.objects.select_related('user').all()
    return render(request, "school/list.html", {"students": students, "is_successful": False})

def view(request, student_id: uuid):
    student = Student.objects.get(id=student_id)
    return render(request, "school/view.html", {"student": student})

def delete(request, student_id: uuid):
    student = Student.objects.get(id=student_id)
    student.delete()
    return redirect("list")