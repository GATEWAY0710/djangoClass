from abc import ABCMeta, abstractmethod
from typing import List, Optional
from uuid import UUID

from school.models import Student


class StudentRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self, student: Student) -> Student:
         """Create a student record"""
         raise NotImplementedError
     
    @abstractmethod
    def update(self, student_id: UUID, student_to_update: Student) -> Student:
        """Update a student record"""
        raise NotImplementedError
    
    @abstractmethod
    def get(self, pk: UUID) -> Optional[Student]:
        """Get a student by PK"""
        raise NotImplementedError
    
    @abstractmethod
    def get_by_matric_number(self, matric_number: str) -> Optional[Student]:
        """Get student by matric number"""
        raise NotImplementedError
    
    @abstractmethod
    def get_by_email(self, email: str)-> Student:
        """Get by a student by email"""
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, student: Student) -> None:
        """Delete a student record"""
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> List[Student]:
        """List students"""
        raise NotImplementedError
    
    
     
class DjangoORMStudentReposiotry(StudentRepository):
    def create(self, student: Student) -> Student:
        student.user.save()
        student.save()
        return student
    
    def update(self, student_id: UUID, student_to_update: Student) -> Student:
        student_to_update.save()
        return student_to_update
    
    def get(self, pk: UUID) -> Optional[Student]:
        try:
            return Student.objects.select_related("user").get(pk=pk)
        except Exception:
            return None
        
    def get_by_email(self, email: str) -> Optional[Student]:
        try:
            return Student.objects.select_related("user").get(user__email=email)
        except Student.DoesNotExist:
            return None
        
    def get_by_matric_number(self, matric_number):
        try:
            return Student.objects.select_related("user").get(matric_number=matric_number)
        except Student.DoesNotExist:
            return None
        
    def delete(self, student: Student):
        return Student.objects.delete()
    
    def list(self) -> List[Student]:
        return Student.objects.select_related("user").all()
    