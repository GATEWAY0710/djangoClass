import datetime
from uuid import UUID
import uuid
from django.db import models
from django.contrib.auth.models import User


class Role(models.TextChoices):
    ADMIN = 'A', 'Admin'
    STUDENT = 'S', 'Student'
    USER = 'U', 'User'
    
    
# Create your models here.
class BaseModel(models.Model):
    id: UUID = models.UUIDField(primary_key=True, default=uuid.uuid4())
    created_by: str = models.CharField(max_length=100, null=True, blank=True)
    modified_by: str = models.CharField(max_length=100, null=True, blank=True)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
class Student(BaseModel):
    name: str = models.CharField(max_length=50, null=False, blank=False)
    matric_number: str = models.CharField(max_length=20, null=False, blank=False, unique=True)
    phone_number: str = models.CharField(max_length=15)
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)