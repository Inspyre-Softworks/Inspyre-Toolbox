# from threading import Thread
from os import makedirs
from pathlib import Path
from time import time


class TimerHistory(object):

    def __init__(self, elapsed_method):
        self.get_elapsed = elapsed_method
        self.ledger = []
        self.actions = [
            "START",
            "STOP",
            "PAUSE",
            "UNPAUSE",
            "RESET",
            "CREATE"
        ]
        self.add("CREATE")

    def add(self, action: str = "START"):
        action = action.upper()
        entry = {
            "time": time(),
            "elapsed_since_last": "",
            "action": action,
            "rt_at_create": ""
        }
        if action == "CREATE":
            entry['elapsed_since_last'] = 0.00
        else:
            entry['elapsed_since_last'] = self.get_elapsed(self.ledger[-1]['time'])
            entry['rt_at_create'] = self.get_elapsed(self.ledger[0]['time'])

        self.ledger.append(entry)

    def write(self):
        data_path = Path("~/Inspyre-Softworks/Inspyre-Toolbox/data").expanduser()

        filename = "ledger_" + str(time()).split('.')[0]
        filepath = str(str(data_path) + "/" + filename + ".txt")

        filepath = str(Path(filepath).resolve())

        if not data_path.exists():
            makedirs(data_path)

        with open(filepath, "w") as fp:
            fp.write(str(self.ledger))


def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60 * 60)
    seconds %= (60 * 60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)


class Timer(object):

    def __init__(self):
        # Thread.__init__(self)

        # Define some default attribute values
        # ToDo:
        #     Assess if in-fact all of these are needed for a comprehensive/informative experience
        self.start_time = None
        self.is_running = False
        self.pause_start = time()
        self.pause_end = None
        self.total_pause_time = 0
        self.started = False
        self.paused = False
        self.was_paused = False
        self.mark_2 = None

        # Start a Timer history object to track times for resets
        self.history = TimerHistory(self.get_elapsed)

    def get_elapsed(self, ts=None, sans_pause: bool = False):
        if ts is None:
            diff_time = self.start_time
        else:
            diff_time = ts

        self.mark_2 = time()
        # print(self.mark_2)
        # print(self.start_time)

        diff = self.mark_2 - diff_time
        # print(format_seconds_to_hhmmss(diff))
        if sans_pause:
            return format_seconds_to_hhmmss(diff)

        tpt = 0
        # print(self.total_pause_time)
        if self.paused:
            tpt += time() - self.pause_start

        tpt += self.total_pause_time
        diff = diff - tpt
        return format_seconds_to_hhmmss(diff)

    def reset(self):
        """

        Reset the 'self.start_time' attribute to this moment, effectively resetting the timer to '00:00:00'

        """
        self.history.add(action="RESET")
        self.start()

    def start(self):
        """

        Store the time the thread was started and assign the attribute 'self.started' to 'True' to indicate this.

        """
        self.start_time = time()
        self.started = True
        self.history.add()

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
            self.history.add("PAUSE")
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
            self.history.add("UNPAUSE")
        else:
            return False
