from typing import List

from PIL import Image

__all__ = [
        'PIL_FORMATS',
        'PIL_EXTENSIONS',
        'IMAGE_FORMATS',
        'VALID_IMAGE_EXTENSIONS',
        ]


def __get_PIL_formats() -> List[tuple[str, str]]:
    """
    Get all the image formats supported by the Python Imaging Library (PIL).

    Returns:
        List[tuple[str, str]]:
            A list of supported image formats.
    """
    formats = Image.registered_extensions()

    return [(ext.replace('.', ''), Image.MIME[fmt]) for ext, fmt in formats.items() if fmt in Image.MIME]


PIL_FORMATS = __get_PIL_formats()
"""
A list of tuples containing information on the formats supported by the Python Imaging Library (PIL).

Each tuple contains two elements:
    1. The file extension.
    2. The MIME type.
    
Example:
    [('bmp', 'image/bmp'), ('dib', 'image/bmp'), ('dcx', 'image/pcx'), ('eps', 'application/postscript'),
    ('ps', 'application/postscript'), ('gif', 'image/gif'), ('im', 'image/x-portable-bitmap'), ('jpg', 'image/jpeg'),
    ('jpe', 'image/jpeg'), ('jpeg', 'image/jpeg'), ('pcd', 'image/pcd'), ('pcx', 'image/pcx'), ('pbm', 'image/x-portable-bitmap'),
    ('pgm', 'image/x-portable-graymap'), ('png', 'image/png'), ('ppm', 'image/x-portable-pixmap'), ('psd', 'image/vnd.adobe.photoshop'),
    ('tif', 'image/tiff'), ('tiff', 'image/tiff'), ('xbm', 'image/x-xbitmap'), ('xpm', 'image/x-xpixmap')]

Note:
    Here's some important things to note:
        - The file extension is the key.
            - The file extension is a string.
            - The file extension is in the format 'ext' (note the absence of a '.').
        - The MIME type is the value.
            - The MIME type is a string.
            - The MIME type is in the format 'type/subtype'.
"""

del __get_PIL_formats  # Cleanup

PIL_EXTENSIONS = [pair[0] for pair in PIL_FORMATS]
"""
A list of the file extensions supported by the Python Imaging Library (PIL).

Example:
    [
        'bmp', 'dib', 'dcx', 'eps', 'ps', 'gif', 'im',
        'jpg', 'jpe', 'jpeg', 'pcd', 'pcx', 'pbm', 'pgm',
        'png', 'ppm', 'psd', 'tif', 'tiff', 'xbm', 'xpm'
    ]
"""

__temp = []

for pair in PIL_FORMATS:
    info = pair[1]
    type, desc = info.split('/')

    if type == 'image':
        __temp.append(pair)

IMAGE_FORMATS = __temp
"""
A list of tuples containing information on the image formats supported by the Python Imaging Library (PIL).
"""

del __temp  # Cleanup

VALID_IMAGE_EXTENSIONS = [pair[0] for pair in IMAGE_FORMATS]
"""
A list of the file extensions for valid image formats supported by the Python Imaging Library (PIL).
"""
