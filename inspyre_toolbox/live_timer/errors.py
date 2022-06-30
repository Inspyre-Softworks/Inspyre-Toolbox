"""

This file contains custom exceptions for Inspyre_Toolbox.live_timer.

"""
from inspyre_toolbox.core_helpers.debugging import who_rang


class TimerNotRunningError(Exception):
    default_message = 'This timer is not running!'

    def __init__(self, message=default_message, skip_print=False, caller=who_rang()):
        self.actual_caller = who_rang()
        self.caller_msg = f'Erroneous call from: {self.actual_caller}'

        if self.actual_caller != caller:
            self.caller_msg += f' which claims it was called by {caller}'

        msg = f'{self.default_message} {self.caller_msg}'

        if message != self.default_message:
            msg += f"Further information from caller: {message}"

        self.message = msg

        if not skip_print:
            print(self.message)


class TimerNotStartedError(TimerNotRunningError):
    default_message = 'Timer has not yet been started!'

    def __init__(self, message=default_message, skip_print=False, caller=who_rang(), **kwargs):
        super(TimerNotStartedError, self).__init__(kwargs)
