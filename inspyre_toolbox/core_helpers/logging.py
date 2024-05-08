# ==============================================================================
#  Copyright (c) Inspyre Softworks 2022.                                       =
#                                                                              =
#  Author:                 T. Blackstone                                       =
#  Author Email:    <t.blackstone@inspyre.tech>                                =
#  Created:              2/10/22, 9:49 PM                                      =
# ==============================================================================

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
INSPY_LOG_LEVEL = 'info'
from inspy_logger import Logger as ISL
import inspyre_toolbox.settings as it_settings

prog = 'InspyreToolbox'

root_ISL = ISL(prog, it_settings.log_level.upper())

ROOT_ISL_DEVICE = root_ISL

PROG_LOGGERS = {}


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


class Manifest(list):

    def __init__(self, *arg, **kw):
        # assert isinstance(comp, dict), '"comp" requires a dictionary!'
        #
        # for x, y in comp.items():
        #     assert isinstance(x, str), f"Invalid key {x}. Please input a string, not {type(x).__name__}"
        #     assert type(y).__name__ == 'Logger', f"Invalid value, the value should be a 'Logger' device. Instead got " \
        #                                          f"type {type(y).__name__}"
        #
        # self.__comp = comp
        # self.__get_comp_map()
        super(Manifest, self).__init__(*arg, **kw)
        self.__slots__ = ()

    def __get_comp_map(self):
        self.__comp_map = [(x, y1) for x, y in self.__comp.items() for y1 in y]

    @staticmethod
    def __sum_lists(lists):
        lt = []
        for lst in lists:
            lt += lst
        return lt

    def __get_all(self):
        return self.__sum_lists(map(list, self.__comp.values()))

    def __repr__(self):
        return str(self.__get_all())


def add_isl_child(name, isl_device=ROOT_ISL_DEVICE):
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
    return ROOT_ISL_DEVICE.get_child(name)
