"""

This file contains custom exceptions for Inspyre_Toolbox.live_timer.

"""
from inspyre_toolbox.core_helpers.debugging import who_rang


class TimerNotStartedError(Exception):

    default_message='Timer has not yet been started!'

    def __init__(self, message=default_message, skip_print=False, caller=who_rang()):

        actual_caller = who_rang()

        caller_msg = f'Erroneous call from: {actual_caller}'

        if actual_caller != caller:
            caller_msg += f' which claims it was called by {caller}'

        msg = f'{self.default_message} {caller_msg}'

        if message != self.default_message:
            msg += f"Further information from caller: {message}"

        self.message = msg

        super(TimerNotStartedError, self).__init__(self.message)

        if not skip_print:
            print(self.message)
