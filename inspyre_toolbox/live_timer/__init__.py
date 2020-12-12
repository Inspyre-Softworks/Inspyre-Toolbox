from threading import Thread
from time import time, sleep

WIN_TITLE = 'Duel Tracker'


class TimerHistory(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.ledger = []

    def add(self, run_time):
        pass

    def write(self):
        pass

    def run(self):
        pass


def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)


class Timer(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.start_time = None
        self.is_running = False
        self.pause_start = time()
        self.pause_end = None
        self.total_pause_time = 0
        self.started = False
        self.paused = False
        self.was_paused = False
        self.mark_2 = None

    def get_elapsed(self, sans_pause: bool = False):

        self.mark_2 = time()
        # print(self.mark_2)
        # print(self.start_time)

        diff = self.mark_2 - self.start_time
        # print(format_seconds_to_hhmmss(diff))
        if sans_pause:
            return format_seconds_to_hhmmss(diff)

        # print(self.total_pause_time)
        diff = diff - self.total_pause_time
        return format_seconds_to_hhmmss(diff)

    def reset(self):
        """

        Reset the 'self.start_time' attribute to this moment, effectively resetting the timer to '00:00:00'

        """
        self.start_time = time()

    def run(self):
        """

        Store the time the thread was started and assign the attribute 'self.started' to 'True' to indicate this.

        """
        self.start_time = time()
        self.started = True

    def pause(self):
        """

        Pause the running timer.

        This function will pause the running timer. What this really means in this context is that this function will
        fill the 'self.pause_start' time with the current time. When you unpause at a later time the 'self.unpause'
        function will reference 'self.pause_start' for comparison.

        This function also sets the 'self.paused' variable to 'True'.

        :return:
        """
        if not self.paused:
            self.pause_start = time()
            self.paused = True
        else:
            return False

    def unpause(self):
        """

        Un-Pause the running timer.

        This function will unpause the running timer. What that really means in this context is that since it marks the
        time that one paused the timer previously and this will compare the time elapsed between when the pause function
        was called and when this is called and keeps track of it.

        Whenever get_elapsed is called, it looks at the amount of seconds that have been added by this function and
        removes that total from the number of seconds elapsed before passing them to be naturalized.

        :return:
              bool
        """
        if self.paused:
            self.pause_end = time()
            diff = self.pause_end - self.pause_start
            self.total_pause_time += diff
            self.paused = False
        else:
            return False
