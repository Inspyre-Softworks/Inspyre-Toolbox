"""

In this example we demonstrate simple usage of the humanize module in conjunction with the 'live_timer' module.

"""
from inspyre_toolbox.humanize import Numerical  # Numerical is the only class in humanize that would be remotely useful to anyone
from inspyre_toolbox.live_timer import Timer  # Just demonstrating the timer, the timer is not needed to utilize Numerical
from time import sleep

class Logging:
    def __init__(self):
        from inspy_logger import InspyLogger
        isl = InspyLogger()
        isl_dev = isl.LogDevice("HumanizeExample1", 'debug')
        log = isl_dev.start()
        log.debug("Logger online, exposing logger API to the rest of the class")
        self.log_dev = isl_dev


def do_it(do_log=False, no_sleep=False, num_iters=1000):
    global out

    timer = Timer()

    if do_log:
        logger = Logging()
        log = logger.log_dev.add_child("do_it")
        log.debug("Logger started, starting iteration")
        out = log.debug
    else:
        out = print

    out("Starting timer")

    timer.start()

    for i in range(num_iters):
        num = Numerical(i)
        iter_count = num.count_noun('iteration', count_to_words=True, capitalize=True)
        elapsed = Numerical(timer.get_elapsed(seconds=True))
        elapsed_count = elapsed.count_noun('second', count_to_words=True, capitalize=True, round_num=2)
        out(f"{iter_count}. | {elapsed_count}.")
        if not no_sleep:
            sleep(.1)

do_it(do_log=True, no_sleep=True, num_iters=1500)
