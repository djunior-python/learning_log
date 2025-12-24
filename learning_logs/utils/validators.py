from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size = 10 * 1024 * 1024 # 10 MB
    if file.size > max_size:
        raise ValidationError(f"File size should not exceed {max_size / (1024 * 1024)} MB.")
    
    
def validate_image_size(image):
    max_size = 5 * 1024 * 1024 # 5 MB
    if image.size > max_size:
        raise ValidationError(f"Image size should not exceed {max_size / (1024 * 1024)} MB.")