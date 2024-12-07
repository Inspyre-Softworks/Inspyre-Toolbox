import os
from typing import List


def separate_path_str(path_str: str) -> List[str]:
    """
    Separate a PATH environment variable string into a list of directories.

    Parameters:
        path_str (str):

    Returns:
        List[str]:
            A list of directories in the PATH environment variable.
    """
    return path_str.split(os.pathsep)
