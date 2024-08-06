#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
from .operating_system.checks import is_windows

if is_windows():
    from .operating_system.win32 import *
else:
    from .operating_system.linux import *

__all__ = [
        'IS_ADMIN',
        ]
