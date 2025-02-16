import logging
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

def process_and_save_avatar(user, avatar_file):
    """
    Processes the uploaded avatar image: 
    - Crops it to a square
    - Resizes it to 300x300
    - Saves it to AWS S3 using Django's ImageField
    """

    try:
        logger.debug("Opening the image.")
        # Open the image
        image = Image.open(avatar_file)

        logger.debug("Image opened successfully. Cropping to square.")
        # Crop to square
        width, height = image.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2
        image = image.crop((left, top, right, bottom))

        logger.debug("Image cropped successfully. Resizing to 300x300.")
        # Resize to 300x300 using Pillow (backward compatibility for old versions)
        if hasattr(Image, "Resampling"):  
            image = image.resize((300, 300), Image.Resampling.LANCZOS)  # Newer versions
        else:
            image = image.resize((300, 300), Image.LANCZOS)  # Compatibility fallback

        logger.debug("Image resized successfully. Saving image to S3 (in memory).")
        # Save image to S3 (in memory)
        image_io = BytesIO()
        file_extension = avatar_file.name.split('.')[-1].lower()
        file_format = "JPEG" if file_extension == "jpg" else file_extension.upper()
        image.save(image_io, format=file_format)

        logger.debug(f"Image saved in memory with format {file_format}. Saving to user avatar.")
        # **Use Django's upload_to path, so no "avatars/avatars/" issue**
        user.avatar.save(f"{user.username}.{file_extension}", image_io, save=True)

        logger.info(f"Avatar successfully uploaded to S3 for user: {user.username}")

    except Exception as e:
        logger.error(f"Error processing avatar: {e}", exc_info=True)
        return False

    return True