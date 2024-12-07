import base64

from inspyre_toolbox.filesystem.file.images.constants import *

__all__ = [
        'ImageFile',
        'VALID_IMAGE_EXTENSIONS',
        'IMAGE_FORMATS',
        'PIL_EXTENSIONS',
        'PIL_FORMATS',
        ]

from inspyre_toolbox.filesystem.file import File
from inspyre_toolbox.filesystem.file.images.helpers import is_image_file


class ImageFile(File):
    """
    A class for handling image files.
    """

    def __init__(self, path):
        """
        Initialize the ImageFile object.

        Args:
            path (str): The path to the image file.
        """
        super().__init__(path)

        self._format = self.get_format()

        if not self.is_valid():
            raise ValueError(f'Invalid image file: {self.path}')

    def get_base64(self):
        """
        Get the base64 encoded image data.

        Returns:
            str: The base64 encoded image data.
        """
        with open(self.path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')

    def get_format(self):
        """
        Get the format of the image file.

        Returns:
            str: The format of the image file.
        """
        return self.get_extension()

    def is_valid(self):
        """
        Check if the image file is valid.

        Returns:
            bool: True if the image file is valid, False otherwise.
        """
        return is_image_file(self.path)
