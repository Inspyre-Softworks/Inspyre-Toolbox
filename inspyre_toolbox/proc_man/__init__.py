#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
import contextlib
import os
from datetime import datetime

import psutil
from pypattyrn.behavioral.null import Null

import inspyre_toolbox.settings as it_settings
from inspyre_toolbox.core_helpers.logging import ISL as InspyLogger, add_isl_child, force_lowkey_log_name
from inspyre_toolbox.humanize import Numerical
from inspyre_toolbox.proc_man.errors import NoFoundProcessesError

fts = datetime.fromtimestamp

ISL = InspyLogger('InspyreToolBox.ProcMan', it_settings.log_level.upper())

LOG = ISL


class Colors(object):
    def __init__(self, return_null=True):
        """
        Initializes a Colors object.

        Args:
            return_null (bool, optional):
                If True, instantiate the Colors object with Null values for each color attribute.

                If False, instantiate the Colors object with actual color values.Defaults to True.
        """
        if return_null:
            self.red       = Null()
            self.yellow    = Null()
            self.blue      = Null()
            self.green     = Null()
            self.end_color = Null()
        else:
            from inspyred_print import Color, Format
            color = Color()
            fmt = Format()
            self.red       = color.red
            self.yellow    = color.yellow
            self.blue      = color.blue
            self.green     = color.green
            self.end_color = fmt.end_mod


def find_all_by_name(name, case_sensitive=False, inspy_logger_device=None, on_the_dl=False, colorful_logging=False):
    """

    Find a running program by name.

    Args:
        name (str):
            The name of the program you're looking for.

        case_sensitive (bool):
            Should the function care about letter casing when searching for the given program? (
            Optional) - Defaults to bool(False)

        inspy_logger_device (inspy_logger.InspyLogger().device):
            The instantiated device object from the inspy_logger package. (Optional, defaults to None)

            Note:
                If a value other than NoneType is passed to this parameter, the function will check the
                InspyLogger.device attribute 'started' to see if the logger has already been started elsewhere. One
                of three situations could result from this:

                    1) The attribute 'started' exists, and evaluates to bool(False):

                       In this case the function will attempt to start the log-device by calling it's 'start' method
                       before calling 'add_child' on the log-device in the hopes of receiving it's own logging object.

                    2) The attribute 'started' exists and evaluates to bool(False):

                       In this case the function will attempt to call 'add_child' on the log-device in the hopes of
                       receiving it's own logging object.

                    3) The attribute 'started' does not exist:

                       In this case, the function will receive a raised AttributeError from the passed object. If
                       this occurs; the function will raise a more relevant 'InvalidLogDeviceError'

        on_the_dl (bool):
            Should InspyreToolbox leave itself out of the the logging name? (Optional, Defaults to bool(False))

        colorful_logging (bool):
            Should the function log colorfully? (Optional, Defaults to bool(False))


    Returns:
        procs_found (list): A list of the currently running processes that match the given name.

    """

    def add_readable_times(process_list):
        for proc in process_list:
            proc['create_time_readable'] = fts(proc['create_time'])

        return process_list

    isl_dev = inspy_logger_device

    prefix = '' if on_the_dl else 'InspyreToolbox.'
    log_name = f'{prefix}proc_man.find_by_name'

    log = add_isl_child(log_name, isl_dev)

    r_null = force_lowkey_log_name or not colorful_logging
    colors = Colors(return_null=not colorful_logging)

    procs_found = []

    # If we're not being case-sensitive we'll lower the case on 'name'
    if not case_sensitive:
        log.debug('Searching in case insensitive mode!')
        name = name.lower()

    log.debug(f'Search query: {name}')

    # Iterate through the process list
    for proc in psutil.process_iter():
        with contextlib.suppress(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Gather the information of all the currently running processes
            proc_info = proc.as_dict(
                    attrs=['pid', 'name', 'create_time', 'username'])
            log.debug(proc_info)

            # If we're not caring about case let's go ahead and make both
            # things we're comparing lowercase.
            proc_name = proc_info['name'] if case_sensitive else proc_info['name'].lower()
            if name in proc_name:
                log.debug(f'{colors.green}Found match: {colors.blue}{proc_info["name"]}'
                          f'({colors.yellow}{proc_info["pid"]}{colors.blue})')

                # Add find to the list we're returning to the caller.
                procs_found.append(proc_info)

                log.debug(
                        f'{colors.green}Added {proc_info["pid"]} to found process list')
    num_found = Numerical(len(procs_found), noun='process')

    log.debug(f'Found: {colors.yellow}{num_found.count_noun()}')

    procs_found = add_readable_times(procs_found)

    # Return found process list to caller
    return procs_found


def kill_all_in_list(kill_list, inspy_logger_device=None, on_the_dl=False, colorful_logging=False):
    """

    When provided a list of processes, kill each process in the list.

    Args:
        kill_list:
            A list of processes in the format of a dictionary

        inspy_logger_device:
            An instantiated inspy-logger device.

        on_the_dl:
            Don't include 'InspyreToolbox' in the name of the logger.

        colorful_logging:
            Should logging be colorful?

    Returns:
        None

    """

    prefix = '' if on_the_dl else 'InspyreToolbox.'
    log_name = f'{prefix}ProcMan.kill_all_in_list'

    log = add_isl_child(log_name, ISL.device)

    log.debug('Logging active')

    colors = Colors(return_null=not colorful_logging)

    missing = 0

    for proc in kill_list:
        log.debug(f'Killing {colors.yellow}{proc["pid"]}')
        os.kill(proc['pid'], 2)
        # try:
        #         subprocess.check_output("Taskkill /PID %d /F" % proc['pid'])
        #     if os.name == 'nt':
        #     else:
        #         os.kill(proc['pid'], 2)
        # except subprocess.CalledProcessError:
        #     missing += 1
        #     if missing >= 20:
        #         kill_all_by_name(proc['name'])
        #         break
        # log.debug(
        #     f'{colors.green}Kill signal sent to {colors.yellow}{proc["pid"]}')


def kill_all_by_name(
        name,
        case_sensitive=False,
        inspy_logger_device=None,
        on_the_dl=False,
        colorful_logging=False
):
    """

    Kill all currently running programs (and all instances thereof) which have a name containing the string given as a
    value to the 'name' parameter.

    Note:
        Unless you are running this as administrator, any programs that you don't have permission to kill will not be
        killed.

        IF YOU ARE RUNNING AS ADMINISTRATOR EVERY PROCESS THAT MATCHES WILL BE KILLED REGARDLESS OF WHO INSTANTIATED
        THE PROCESS!!!!

    Args:
        name (str):
            The name of the program you'd like to kill all instances of. Whatever
            you provide here will be used as a query to find all programs that have
            a name that contains this string.

        case_sensitive (bool):
            Tell the function that the letter casing is irrelevant to finding matching
             programs. (Optional, defaults to False)

        inspy_logger_device (inspy_logger.InspyLogger().device):
            The instantiated device object from the inspy_logger package. (Optional, defaults to None)

            Note:
                If a value other than NoneType is passed to this parameter, the function will check the
                InspyLogger.device attribute 'started' to see if the logger has already been started elsewhere. One
                of three situations could result from this:

                    1) The attribute 'started' exists, and evaluates to bool(False):

                       In this case the function will attempt to start the log-device by calling it's 'start' method
                       before calling 'add_child' on the log-device in the hopes of receiving it's own logging object.

                    2) The attribute 'started' exists and evaluates to bool(False):

                       In this case the function will attempt to call 'add_child' on the log-device in the hopes of
                       receiving it's own logging object.

                    3) The attribute 'started' does not exist:

                       In this case, the function will receive a raised AttributeError from the passed object. If
                       this occurs; the function will raise a more relevant 'InvalidLogDeviceError'

        on_the_dl (bool):
            Should InspyreToolbox leave itself out of the the logging name? (Optional, Defaults to bool(False))

        colorful_logging (bool):
            Should the function log colorfully? (Optional, Defaults to bool(False))

    Returns:
        None

    """
    from time import sleep

    # Get a logger for logging in logging is enabled.
    log = add_isl_child('proc_man.kill_all_by_name', inspy_logger_device)

    # Get colors for colorful logging if colorful_logging is bool(True)
    color = Colors(return_null=not colorful_logging)

    log.debug(f'{color.yellow}Checking to see if there are, any running programs with "'
              f'{color.green}{name}{color.yellow}" in their name.')

    # Get a list of all the currently running processes that contains 'name' string.
    procs = find_all_by_name(name, case_sensitive,
                             inspy_logger_device, on_the_dl, colorful_logging)

    log.debug(procs)

    sleep(5)

    # Get the number of running processes found.
    num_running = Numerical(len(procs), noun='process')

    log.debug(f'Found {num_running.count_noun()}')

    # Gather the username of the current user.
    username = os.getlogin()

    # Find out if they are an administrator or not.
    __is_admin = is_admin()

    started_by_user = []

    if not __is_admin:
        for proc in procs:
            log.debug(proc['username'])
            if proc['username'].endswith(username):
                started_by_user.append(proc)

    started_by_user.reverse()

    kill_all_in_list(started_by_user)


def find_by_pid(pid, inspy_logger_device=None):
    if inspy_logger_device is None:
        log = InspyLogger('InspyreToolbox.ProcMan', it_settings.log_level.upper())
        log = log.get_child('find_by_pid')
    else:
        log = inspy_logger_device

    log.debug(f'Finding process with PID: {pid}')

    try:
        return psutil.Process(pid)
    except psutil.NoSuchProcess as e:
        raise NoFoundProcessesError(f'No process found with PID: {pid}') from e


def kill_by_pid(pid, inspy_logger_device=None):
    """
    Kill a process by its PID.

    Parameters::
        pid (int):
            The PID of the process to kill.

        inspy_logger_device:
            The InspyLogger device to use for logging.

    Returns:
        None

    Raises:
        NoFoundProcessesError:
            Raised if no process is found with the given
    """
    if inspy_logger_device is None:
        log = InspyLogger('InspyreToolbox.ProcMan', it_settings.log_level.upper())
    else:
        log = inspy_logger_device

    log.debug(f'Killing process with PID: {pid}')

    try:
        proc = find_by_pid(pid)
        proc.kill()
    except psutil.NoSuchProcess as e:
        raise NoFoundProcessesError(f'No process found with PID: {pid}') from e


def is_admin():
    """
    Check if the current user is an administrator.

    Returns:
        bool: True if the user is an administrator, False if they are not.
    """
    return os.getuid() == 0


def is_process_elevated(pid):
    """
    Check if a process is running with elevated privileges.

    Args:
        pid (int):
            The PID of the process to check.

    Returns:
        bool: True if the process is running with elevated privileges, False if it is not.
    """
    try:
        return psutil.Process(pid).is_running() and psutil.Process(pid).is_running()
    except psutil.NoSuchProcess:
        return False


def find_executable_path(pid):
    try:
        process = psutil.Process(pid)
        exe_path = process.exe()
        return os.path.dirname(exe_path)
    except psutil.NoSuchProcess:
        return f'No process with PID {pid} exists.'
    except psutil.AccessDenied:
        return f'Access to process with PID {pid} was denied.'
    except Exception as e:
        return f'An error occurred: {e}'
