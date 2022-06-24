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

from inspyre_toolbox.live_timer.errors import TimerNotStartedError, TimerNotRunningError
from inspyre_toolbox.live_timer.history import TimerHistory

from inspyre_toolbox.core_helpers.logging import add_isl_child, ROOT_LOGGER, ROOT_ISL_DEVICE, PROG_LOGGERS


LOG_NAME = 'InspyreToolbox.live_timer'

LOG = add_isl_child(LOG_NAME)

ROOT_ISL_DEVICE.adjust_level('debug')

LOG.debug('Log started!')


def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)


class Timer(object):
    def __repr__(self):
        statement = "Timer("\
                    f"Started: {self.started} |"
        if self.started:
            runtime = time() - self.start_time
            runtime = format_seconds_to_hhmmss(runtime)
            statement += f" Started: {self.start_time} - Current Runtime: {runtime}"

    def __init__(self, auto_start=False):
        
        self.log_name = LOG_NAME + '.Timer'
        
        # Set up logger
        self.log = add_isl_child(self.log_name)
        
        # Define some default attribute values
        
        self.running       = False
        self.mark_2           = None
        self.pause_end        = None
        self.pause_start      = time()
        self.paused           = False
        self.start_time       = None
        self.started          = False
        self.stopped          = False
        self.total_pause_time = 0
        self.was_paused       = False
        
        self.log.debug('Set up class attributes.')

        # Start a Timer history object to track times for resets
        self.history = TimerHistory(self.__get_elapsed)
        
        self.log.debug('Timer class instantiated!')

    def __get_elapsed(self, ts=None, sans_pause: bool = False, seconds=False):
        """
        
        Args:
            ts:
            sans_pause:
            seconds:

        Returns:

        """
        log = add_isl_child(self.log_name + '__get_elapsed')
        
        
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
        if self.running:
            self.history.add("QUERY")
            return self.__get_elapsed(*args, **kwargs)
        else:
            if self.stopped:
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
        
        return Timer()
        
        # if self.running:
        #     self.stop()
        # self.total_pause_time = 0
        # self.pause_start = None
        # self.pause_end = None
        # self.started = False
        
    def restart(self):
        self.reset()
        if not self.started:
            self.start()

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

        This function will pause the running timer. What this really means in this context is that this function will
        fill the 'self.pause_start' time with the current time. When you unpause at a later time the 'self.unpause'
        function will reference 'self.pause_start' for comparison.

        This function also sets the 'self.paused' variable to 'True'.

        :return:
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
tim
        Un-Pause the running timer.

        This function will unpause the running timer. What that really means in this context is that since it marks the
        time that one paused the timer previously and this will compare the time elapsed between when the pause function
        was called and when this is called and keeps track of it.

        Whenever get_elapsed is called, it looks at the amount of seconds that have been added by this function and
        removes that total from the number of seconds elapsed before passing them to be naturalized.

        :return:
              bool
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
        else:
            return False

    def stop(self):
        if not self.started:
            raise TimerNotStartedError()
        if self.running:
            self.running = False
            self.paused = False
            self.stopped = True
            self.mark_2 = time()
        else:
            raise TimerNotRunningError()

