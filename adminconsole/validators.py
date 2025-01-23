from django.db import models
from django.core.exceptions import ValidationError

def validate_image_file_type(file):
    """
    Validate the file type and size of the uploaded image.
    Allow only JPEG, PNG, and WEBP formats, and ensure the file size is less than or equal to 1 MB.
    """
    # Allowed file extensions
    valid_extensions = ['jpeg', 'jpg', 'png', 'webp']
    # Maximum file size in bytes (1 MB)
    max_file_size = 1 * 1024 * 1024  

    # Validate file extension
    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in valid_extensions:
        raise ValidationError(f"Invalid file type: {file_extension}. Only JPEG, PNG, and WEBP files are allowed.")

    # Validate file size
    if file.size > max_file_size:
        raise ValidationError(f"File size exceeds 1 MB. Current size: {file.size / (1024 * 1024):.2f} MB.")

def validate_image(file):
    """
    Validate the file type and size of the uploaded image.
    Allow only JPEG, PNG, and WEBP formats, and ensure the file size is less than or equal to 1 MB.
    """
    # Allowed file extensions
    valid_extensions = ['jpeg', 'jpg', 'png', 'webp']
    # Maximum file size in bytes (1 MB)
    max_file_size = 1 * 1024 * 1024  

    # Validate file extension
    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in valid_extensions:
        raise ValidationError(f"Invalid file type: {file_extension}. Only JPEG, PNG, and WEBP files are allowed.")

    # Validate file size
    if file.size > max_file_size:
        raise ValidationError(f"File size exceeds 1 MB. Current size: {file.size / (1024 * 1024):.2f} MB.")
    
    
def validate_video(file):
    """
    Validate the file type and size of the uploaded video.
    Allow only MP4 format and ensure the file size is less than or equal to 10 MB.
    """
    # Allowed file extension
    valid_extension = 'mp4'
    # Maximum file size in bytes (10 MB)
    max_file_size = 10 * 1024 * 1024  

    # Validate file extension
    file_extension = file.name.split('.')[-1].lower()
    if file_extension != valid_extension:
        raise ValidationError(f"Invalid file type: {file_extension}. Only MP4 files are allowed.")

    # Validate file size
    if file.size > max_file_size:
        raise ValidationError(f"File size exceeds 10 MB. Current size: {file.size / (1024 * 1024):.2f} MB.")