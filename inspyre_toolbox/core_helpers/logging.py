#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
from pypattyrn.behavioral.null import Null


force_lowkey_log_name = False
"""

This variable should be a boolean indicating whether or not InspyreToolbox should leave itself out when it's
functions name their child loggers.

Note:


For Example:

    Let's look at how 'inspyre_toolbox.proc_man.find_all_by_name' would name it's loggers in each of the situations we
    could find ourselves in;
   
    Note:
        [ROOT_LOGGER_NAME] is just a placeholder for whatever the name of the root logging device is.

    Case 1 (lowkey_log_name evaluates to bool(False)):
        
        [ROOT_LOGGER_NAME].InspyreToolbox.proc_man.find_all_by_name
        
    Case 2 (lowkey_log_name evaluates to any value seen as bool(True)):
        
        [ROOT_LOGGER_NAME].proc_man.find_all_by_name
        

"""


class InvalidLogDeviceError(Exception):

    def __init__(self):
        """

        Raised when one of the functions in InspyreToolbox are given a value to "inspy_logger_device" and it's found
        that the object provided is not properly configured, thus receiving an AttributeError when trying to check
        inspy_logger_device.started for a bool() value.

        Note:
            'inspy_logger_device.started' will exist in all cases where the logger device was given a name and
            log-level on instantiation (or later through setter methods). If the logging device hasn't been set up,
            an AttributeError will cause the following functions to raise InvalidLogDeviceError:

                * find_by_name
                * kill_all_by_name

        """
        self.message = 'The passed device does not appear to have been initialized, or is not an InspyLogger device!'


def add_isl_child(name, isl_device):
    """

    Manage using an InspyLogger device with Inspyre Toolbox.

    Args:
        name:
            The name you'd like for your log-device.

        isl_device (inspy_logger.InspyLogger.device | None):
            An instantiated inspy-logger device.

    Returns:
        The log device.

    """
    if isl_device:
        try:
            if not isl_device.started:
                log = isl_device.start()
        except AttributeError:
            raise InvalidLogDeviceError()

        log = isl_device.add_child(name)
    else:
        log = Null()

    return log
