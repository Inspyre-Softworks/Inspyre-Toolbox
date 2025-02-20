"""
Module: process_utils

Description:
    This module provides utilities for retrieving process IDs, including
    a function to get the process ID of the current running process.

Functions:
    - get_pid(name: str = None, inspy_logger_device=NoLog()) -> int:
        Retrieves the process ID of a given process by name. If no name
        is provided, it returns the process ID of the current process.

    - get_own_pid() -> int:
        Returns the process ID of the current running process.

Dependencies:
    - os
    - inspyre_toolbox.sys_man.processes (for `get_own_pid`)
    - inspyre_toolbox.log_engine.no_log (for `NoLog`)

Example Usage:
    ```python
    from inspyre_toolbox.sys_man.processes import get_pid

    pid = get_pid("python")
    print(f"PID of python: {pid}")

    my_pid = get_pid()
    print(f"My PID: {my_pid}")
    ```
"""

from inspyre_toolbox.log_engine.no_log import NoLog
from inspyre_toolbox.sys_man.processes import get_own_pid  # Use centralized version


def get_pid(name: str = None, inspy_logger_device=None) -> int:
    """
    Retrieves the process ID of a given process by name.

    Parameters:
        name (str, optional): The name of the process to find. If None, returns own PID.
        inspy_logger_device: The logging device used for logging warnings.

    Returns:
        int: The process ID of the specified process, or the current process if no name is provided.

    Example Usage:
        ```python
        pid = get_pid("python")
        print(f"PID of python: {pid}")

        my_pid = get_pid()
        print(f"My PID: {my_pid}")
        ```
    """
    if inspy_logger_device is None:
        inspy_logger_device = NoLog()

    log = inspy_logger_device.get_child('get_pid')

    log.debug(f'Attempting to find PID for "{name}"')

    if not name:
        log.warning('No name provided, returning own PID')
        return get_own_pid()
