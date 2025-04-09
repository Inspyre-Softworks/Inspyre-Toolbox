"""
Author: 
    Inspyre Softworks

Project:
    Inspyre-Toolbox

File: 
    inspyre_toolbox/chrono/sleep.py

"""
import time
from typing import Optional

from inspy_logger import Loggable

from inspyre_toolbox.log_engine import ROOT_LOGGER as PARENT_LOGGER
from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type

MOD_LOGGER = PARENT_LOGGER.get_child_logger(name=__name__)


class NegateSwitch(Loggable):
    def __init__(self, initial_state=True):
        super().__init__(MOD_LOGGER)
        self.__state = None
        self.class_logger.debug(f'Initializing NegateSwitch with initial state: {initial_state}')

        self.state = initial_state

    @property
    def state(self):
        return self.__state

    @state.setter
    @validate_type(bool)
    def state(self, new):
        log = self.method_logger
        log.debug(f'Setting state to {new}')
        self.__state = new


def sleep(
        seconds,
        precision=0.001,
        negate_obj=None,
        do_not_return_remaining=False,
        always_return_remaining=False,
        pass_kbi_up=False
):
    """
    A sleep function that can be interrupted by KeyboardInterrupt.

    Parameters:

        seconds (float):
            Number of seconds to sleep.

        precision (float):
            The interval in seconds to check for interruption. Default is 0.1 seconds.

        negate_obj (object, optional):
            `sleep` will change the value of this object to `False` if the sleep is interrupted. Default is None.
            
        do_not_return_remaining (bool):
            if True, the remaining time will not be returned once the sleep has been interrupted. Default is False. 
            Aditionally, if the `always_return_remaining` parameter is True, this parameter is ignored.
            
        always_return_remaining (bool):
            If True, the remaining time will always be returned, regardless of whether it was interrupted or not. De-
            -fault is False. Additionally, if this is True, the `do_not_return_remaining` parameter is ignored.
            
            Note:
                The remaining will not be returned if the sleep was interrupted by a `KeyboardInterrupt` exception and 
                the function has been configured to pass the exception up to the caller (i.e. `pass_kbi_up` is True).
            
        pass_kbi_up (bool):
            If True, the KeyboardInterrupt exception will be passed up to the caller, otherwise it will be caught and 
            logged before breaking the sleep loop. Default is False.

    Returns:
        Optional[float]:
            The remaining time in seconds if the sleep was interrupted, otherwise None. If `do_not_return_remaining` is 
            True, None is returned no matter what.
            
        Note:
            A warning will be logged if the loop is interrupted by a 'KeyboardInterrupt' exception, whether the remaining
            time is returned or not.

    Raises:
        KeyboardInterrupt:
            If the user interrupts the sleep loop with a keyboard interrupt (Ctrl+C), this exception will be raised if
            `pass_kbi_up` is True. Otherwise, nothing is raised with the sleep loop exiting gracefully, while logging
            the interrupt.

    Since:
        v1.6.0

    Example Usage:
        >>> from inspyre_toolbox.chrono import sleep
        >>> sleep(5)
        Sleeping for 5 seconds...
        (User interrupts after 3 seconds)
        Sleep interrupted by user.
    """
    start_time = time.time()
    log = MOD_LOGGER.get_child('sleep')
    log.debug(f"Starting interruptible_sleep for {seconds} seconds with precision {precision} seconds.")

    switch = negate_obj

    if switch is None:
        log.warning("Negate object is None, using NegateSwitch instead.")
        switch = NegateSwitch()

    switch.state = True
    remaining = seconds

    while switch.state:
        try:
            remaining = seconds - (time.time() - start_time)
            log.debug(f"Remaining time: {remaining:.2f} seconds.")
            if remaining <= 0:
                log.debug("Sleep duration completed.")
                break
            time.sleep(min(precision, remaining))
        except KeyboardInterrupt as e:
            log.debug("Sleep interrupted by user.")
            switch.state = False
            if pass_kbi_up:
                raise KeyboardInterrupt("Sleep interrupted by user.") from e

    if remaining > 0:
        log.info(f'Sleep interrupted, remaining time: {remaining:.2f} seconds.')
        if not do_not_return_remaining:
            log.debug('Returning remaining time.')
            return remaining
    else:
        log.debug('Sleep completed successfully!')
        return remaining if always_return_remaining else None

    return None if do_not_return_remaining else remaining
