from dataclasses import dataclass
from school.services.application_models.base import BaseResponse

@dataclass
class CreateStudentRequest:
    email: str
    name: str
    password: str
    confirm_password: str
    username: str
    phone_number: str

@dataclass
class CreateStudentResponse(BaseResponse):
    email: str
    name: str
    username: str
    phone_number: str