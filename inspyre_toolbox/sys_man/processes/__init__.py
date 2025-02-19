import os

from inspyre_toolbox.log_engine.no_log import NoLog


def get_pid(name: str = None, inspy_logger_device=NoLog()) -> int:
    log = inspy_logger_device.get_child('get_pid')

    if not name:
        log.warning('No name provided, returning own PID')
        return get_own_pid()


def get_own_pid():
    return os.getpid()
