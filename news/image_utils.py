from PIL import Image
import os
from django.core.files.storage import FileSystemStorage

class ImageOptimizer:
    """
    Helper class for image optimization
    """
    
    @staticmethod
    def optimize_image(image_path, max_width=1200, max_height=800, quality=85):
        """
        Optimize and resize image
        
        Args:
            image_path: Path to the image file
            max_width: Maximum width
            max_height: Maximum height  
            quality: JPEG quality (1-100)
        
        Returns:
            bool: True if successful
        """
        try:
            img = Image.open(image_path)
            
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Resize if image is too large
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
            
            return True
        except Exception as e:
            print(f"Error optimizing image: {e}")
            return False
    
    @staticmethod
    def validate_image(file_obj, max_size_mb=5, allowed_formats=None):
        """
        Validate uploaded image
        
        Args:
            file_obj: Uploaded file object
            max_size_mb: Maximum file size in MB
            allowed_formats: List of allowed formats (default: ['JPEG', 'PNG', 'GIF'])
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if allowed_formats is None:
            allowed_formats = ['JPEG', 'PNG', 'GIF', 'JPG']
        
        # Check file size
        max_size_bytes = max_size_mb * 1024 * 1024
        if file_obj.size > max_size_bytes:
            return False, f"File size exceeds {max_size_mb}MB limit"
        
        # Check if it's an image
        try:
            img = Image.open(file_obj)
            img.verify()
            
            # Check format
            if img.format.upper() not in allowed_formats:
                return False, f"Invalid format. Allowed: {', '.join(allowed_formats)}"
            
            # Reset file pointer after verify
            file_obj.seek(0)
            
            return True, None
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    @staticmethod
    def create_thumbnail(image_path, thumb_path, size=(300, 300)):
        """
        Create thumbnail from image
        
        Args:
            image_path: Source image path
            thumb_path: Thumbnail save path
            size: Thumbnail size (width, height)
        
        Returns:
            bool: True if successful
        """
        try:
            img = Image.open(image_path)
            
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumb_path, 'JPEG', quality=85, optimize=True)
            
            return True
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return False
