from abc import ABCMeta, abstractmethod
import uuid

from school.services.application_models.base import BaseResponse
from school.repositories.student_repository import StudentRepository
from school.services.application_models.student import CreateStudentRequest, CreateStudentResponse
from django.contrib.auth.models import User
from school.models import Student

class StudentService(metaclass=ABCMeta):
    @abstractmethod
    def create(self, student: CreateStudentRequest)-> CreateStudentResponse:
        """Create a student record"""
        raise NotImplementedError
        
    
class DefaultStudentService(StudentService):
    repository: StudentRepository
    
    def __init__(self, repository: StudentRepository):
        self.repository = repository
        
    def create(self, request: CreateStudentRequest) -> CreateStudentResponse:
        is_password_valid = self.__validate_password(request.password, request.confirm_password)
        if not is_password_valid:
            return BaseResponse(
                status=False,
                message="Unable to create student, password dose not match"
            )
        student_exist = self.__check_if_student_exist(request)
        if student_exist:
            return BaseResponse(
                status=False,
                message=f"Student with email {request.email} already exist"
            ) 
        user = User()
        user.username = request.username
        user.email = request.email
        user.set_password(request.password)
        
        student = Student()
        student.id = uuid.uuid4()
        student.matric_number = str(uuid.uuid4()).split("-")[0]
        student.phone_number = request.phone_number
        student.name = request.name
        student.user = user
        student.image_path = request.image_path
        student = self.repository.create(student) 
        return CreateStudentResponse(status=True, message="Student created successfully", email=student.user.email, name=student.name, username=student.user.username, phone_number=student.phone_number)  
    
    def __validate_password(self, password: str, confrim_password: str) -> bool:
        return password == confrim_password
    
    def __check_if_student_exist(self, request: CreateStudentRequest) -> bool:
        student = self.repository.get_by_email(request.email)
        if student:
            return True