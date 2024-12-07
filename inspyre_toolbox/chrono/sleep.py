"""
Author: 
    Inspyre Softworks

Project:
    Inspyre-Toolbox

File: 
    inspyre_toolbox/chrono/sleep.py

"""
import time

from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type


class NegateSwitch:
    def __init__(self, initial_state=True):
        self.__state = None

    @property
    def state(self):
        return self.__state

    @state.setter
    @validate_type(bool)
    def state(self, new):
        self.__state = new




def sleep(seconds, precision=0.001, negate_obj=None):
    """
    A sleep function that can be interrupted by KeyboardInterrupt.

    Parameters:

        seconds (float):
            Number of seconds to sleep.

        precision (float):
            The interval in seconds to check for interruption. Default is 0.1 seconds.

        negate_obj (object, optional):
            `sleep` will change the value of this object to `False` if the sleep is interrupted. Default is None.

    Returns:
        None

    Raises:
        KeyboardInterrupt:
            If the user interrupts the sleep.

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
    print(f"[DEBUG] Starting interruptible_sleep for {seconds} seconds with precision {precision} seconds.")

    switch = True if negate_obj is None else negate_obj

    if switch is None:
        switch = NegateSwitch()
        switch.state = True

    while switch.state:
        try:
            remaining = seconds - (time.time() - start_time)
            print(f"[DEBUG] Remaining time: {remaining:.2f} seconds.")
            if remaining <= 0:
                print("[DEBUG] Sleep duration completed.")
                break
            time.sleep(min(precision, remaining))
        except KeyboardInterrupt:
            print("\n[DEBUG] Sleep interrupted by user.")

            if negate_obj is not None:
                negate_obj = False
            raise
