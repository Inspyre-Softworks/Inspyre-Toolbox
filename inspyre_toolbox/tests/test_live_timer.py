from time import sleep
import unittest
from inspyre_toolbox.live_timer import Timer

timer = Timer()

class TimerTest(unittest.TestCase):
    def test(self):

        timer.start()
        for i in range(30):
            elapsed = timer.get_elapsed
            if i >= 19 and i <= 24:
                sp = True
            else:
                sp = False
            t_elapsed = elapsed(sans_pause=sp)
            if i == 10:
                timer.pause()
            if i == 25:
                timer.unpause()
            if i in list(range(11)):
                print(i)
                secs = int(t_elapsed.split(':')[-1])
                print(secs)
                self.assertTrue(i == secs)
            sleep(1)
