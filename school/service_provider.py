from typing import Callable, Container
from dependency_injector import containers, providers

from school.services.student_service import StudentService, DefaultStudentService
from school.repositories.student_repository import DjangoORMStudentReposiotry, StudentRepository

class Continer(containers.DeclarativeContainer):
     config = providers.Configuration()
     
     student_repository: Callable[[], StudentRepository] = providers.Factory(
        DjangoORMStudentReposiotry
     )
     student_service: Callable[[], StudentService] = providers.Factory(
        DefaultStudentService,
        repository=student_repository
     )

container = Continer()