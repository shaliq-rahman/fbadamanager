from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from PIL import Image
import pdb
from adminconsole.validators import validate_image, validate_video
from django.core.validators import MinValueValidator, MaxValueValidator
from autoslug import AutoSlugField
from django.contrib.postgres.fields import ArrayField


USER_STATUS =(
    (1,'Active'),
    (2,'Blocked'),
    (3,'Deleted'),
)

USER_TYPE =(
    (1,'Admin'),
    (2,'Sub Admin'),
    (3,'User'),
)

APPLICATION_STATUS =(
    (1,'Submitted'),
    (2,'Downloaded'),
)

PRIVILEGES = [
    "dashboard_access",
    "heading_access",
    "kids_courses_access",
    "subjects_access",
    "ielts_access",
    "blogs_access",
    "testimonials_access",
    "subadmin_access"
]

# CUSTOM USER MANAGER
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, retype_password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')

        # Check if passwords match
        if password and retype_password and password != retype_password:
            raise ValidationError("Passwords do not match.")

        # Validate password with Django's built-in validators
        if password:
            validate_password(password)
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, retype_password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, retype_password, **extra_fields)
    

class User(AbstractUser):
    name = models.CharField(max_length=250, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name='email address', max_length=255, null=True, blank=True)
    user_type = models.PositiveIntegerField(choices=USER_TYPE, null=False, blank=False, default=1)
    status = models.PositiveIntegerField(choices=USER_STATUS,null=False,blank=False,default=1)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    privilages = models.JSONField(models.CharField(max_length=50), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username