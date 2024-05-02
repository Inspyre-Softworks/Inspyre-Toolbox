"""
File: inspyre_toolbox/live_timer/__init__.py
Created: ??

Description:
    inspyre_toolbox.live_timer gives you access to a class and functions that make running a live
    timer that's not only easily to initialize, but easy to query, reset, and pause your timers.
    This module also contains a class named 'TimerHistory' that keeps a history of all timer actions.
    
    To find out more about usage please see:
    
    GIT_REPO_ROOT/examples/live_timer

"""

from time import time

from inspy_logger import Loggable

from inspyre_toolbox.core_helpers.logging import add_isl_child
from inspyre_toolbox.live_timer.errors import TimerNotRunningError, TimerNotStartedError
from inspyre_toolbox.live_timer.history import TimerHistory

LOG_NAME = 'live_timer'

LOG = add_isl_child(LOG_NAME)

#ROOT_ISL_DEVICE.adjust_level('debug')

LOG.debug('Log started!')


def format_seconds_to_hhmmss(seconds):
    """
    The format_seconds_to_hhmmss function accepts a number of seconds and returns a string
    representing the amount of time represented by those seconds in HH:MM:SS format.

    Args:
        seconds (int):
            The number of seconds to be converted. (Required)

    Returns:
        A string with the number of hours, minutes and seconds
    """
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)


class Timer(Loggable):
    def __repr__(self):
        """
        Return a string representation of the Timer object.

        Returns:
            str: A formatted string representing the Timer object.
        """
        status = "Running" if self.running else "Stopped"
        state = "Paused" if self.paused else "Not Paused"
        start_info = f"Started at: {self.start_time}" if self.started else "Not Started"
        runtime_info = ""
        if self.started:
            runtime = time() - self.start_time
            runtime_info = f" | Runtime: {format_seconds_to_hhmmss(runtime)}"
        return f"Timer(Status: {status} | State: {state} | {start_info}{runtime_info})"

    def __init__(self, auto_start=False, history=None):
        super().__init__(parent_log_device=LOG)

        self.log = self.class_logger

        self.__auto_start = False
        self._status = 'Stopped'

        self.class_logger.debug('Setting up Timer class attributes...')

        # Define some default attribute values

        self.running = False
        self.mark_2 = None
        self.pause_end = None
        self.pause_start = time()
        self.paused = False
        self.start_time = None
        self.started = False

        self.stopped = False
        self.total_pause_time = 0
        self.was_paused = False

        self.log.debug('Set up class attributes.')

        # Start a Timer history object to track times for resets
        self.history = TimerHistory(self.__get_elapsed) if history is None else history

        self.log.debug('Timer class instantiated!')

        self.auto_start = auto_start

    @property
    def auto_start(self):
        return self.__auto_start

    @auto_start.setter
    def auto_start(self, new: bool):
        if new and not self.started:
            self.start()

        self.__auto_start = new

    @property
    def elapsed(self):
        return self.get_elapsed(seconds=True)

    @property
    def num_resets(self):
        return self.history.num_resets

    def __get_elapsed(self, ts=None, sans_pause: bool = False, seconds=False):
        """
        The __get_elapsed function is a private function that is called by the public functions
        start(), pause(), and stop(). It returns the elapsed time in seconds, or as a string if
        seconds=False. The __get_elapsed function does not take any parameters. If you call this
        private function directly, it will return an error

        Args:
            self:
                Access variables that belongs to the class

            ts (int|float):
                Pass in the current timestamp, (Optional, defaults to time.time())

            sans_pause (bool):
                Determine whether or not to include the time that the timer was
                paused in the elapsed time. (Optional; defaults to True)

            seconds (bool):
                Return the elapsed time as number of seconds. (Optional; defaults
                to False)

        Returns:
            The time elapsed since the start of the timer
        """
        log = self.create_child_logger()

        diff_time = self.start_time if ts is None else ts

        # ver1.2.7
        # If we were running but are now stopped, we will skip marking
        if not self.stopped:
            self.mark_2 = time()

        diff = self.mark_2 - diff_time

        if sans_pause:
            return format_seconds_to_hhmmss(diff)

        tpt = 0
        # print(self.total_pause_time)
        if self.paused:
            tpt += time() - self.pause_start

        tpt += self.total_pause_time
        diff = diff - tpt

        return diff if seconds else format_seconds_to_hhmmss(diff)

    def get_elapsed(self, *args, **kwargs):
        """
        The get_elapsed function returns the elapsed time since the timer was started.
        If the timer is not running, it returns None. If it has been stopped,
        it returns the elapsed time from start to stop.

        Args:
            self: Access the attributes and methods of the class in python
            *args: Pass a non-keyworded, variable-length argument list
            **kwargs: Pass a keyworded, variable-length argument list

        Returns:
            The current elapsed time since the timer was started

        """
        if not self.running and self.stopped or self.running:
            self.history.add("QUERY")
            return self.__get_elapsed(*args, **kwargs)
        else:
            try:
                raise TimerNotStartedError(skip_print=True)
            except TimerNotStartedError as e:
                print(e.message)

    def reset(self):
        """

        Reset the 'self.start_time' attribute to this moment, effectively resetting the timer to '00:00:00'

        """
        self.history.add(action="RESET")

        return Timer(history=self.history)

        # if self.running:
        #     self.stop()
        # self.total_pause_time = 0
        # self.pause_start = None
        # self.pause_end = None
        # self.started = False

    def restart(self):
        """
        The restart function resets the timer to its original state and starts it running.

        This method modifies the current instance instead of creating a new one.

        Returns:
            None
        """
        self.reset()
        if not self.started:
            self.start()
        # Update the current instance instead of creating a new one
        self.__dict__.update(Timer(history=self.history).__dict__)

    def start(self):
        """

        Store the time the thread was started and assign the attribute 'self.started' to 'True' to indicate this.

        """
        self.start_time = time()
        self.started = True
        self.history.add()
        self.running = True

    def pause(self):
        """

        Pause the running timer.

        This function will pause the running timer.

        What this really means in this context is that this function will fill the
        'self.pause_start' time with the current time. When you unpause at a later
        time the 'self.unpause' function will reference 'self.pause_start' for
        comparison.

        Note:
            This function also sets the 'self.paused' variable to 'True'.

        """
        if not self.started:
            raise TimerNotStartedError()
        if not self.running:
            raise TimerNotRunningError()
        if self.paused:
            return False
        self.pause_start = time()
        self.paused = True
        self.was_paused = True
        self.history.add("PAUSE")

    def unpause(self):
        """

        Un-Pause the running timer.

        This function will unpause the running timer. What that really means in this
        context is that since it marks the time that one paused the timer previously
        and this will compare the time elapsed between when the pause function
        was called and when this is called and keeps track of it.

        Whenever get_elapsed is called, it looks at the amount of seconds that
        have been added by this function's operation process and removes that
        total from the number of seconds elapsed before passing them to be
        naturalized.

        Returns:
            bool:
                If;
                    * True:
                        The timer was successfully un-paused
                    * False:
                        The timer was no successfully un-paused (most likely due to its
                        state not actually being paused),
        """
        if not self.started:
            raise TimerNotStartedError()
        if not self.running:
            raise TimerNotRunningError()
        if self.paused:
            self.pause_end = time()
            diff = self.pause_end - self.pause_start
            self.total_pause_time += diff
            self.paused = False
            self.history.add("UNPAUSE")
            return True
        else:
            return False

    def stop(self):
        """
        The 'stop' function stops the timer, but leaves it in a paused state.
        The 'resume' function resumes the timer from where it was stopped.

        Args:
            self: Reference the object itself

        Returns:
            The time when the timer is stopped
        """
        if not self.started:
            raise TimerNotStartedError()
        if self.running:
            self.running = False
            self.paused = False
            self.stopped = True
            self.mark_2 = time()
        else:
            raise TimerNotRunningError()
