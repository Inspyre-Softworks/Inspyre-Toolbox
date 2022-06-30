"""

An example script to show a simple way to use inspyre-toolbox.live-timer.Timer in the CLI

Author: Taylor-Jayde Blackstone
Created: 12/12/2020 - 12:37AM

"""

from time import sleep

from inspyre_toolbox.live_timer import Timer

timer = Timer()
timer.start()
acc = 0
while True:
    acc += 1
    if acc == 10:
        timer.pause()
    elif acc == 25:
        timer.unpause()

    print(timer.get_elapsed())
    if acc == 31:
        print(timer.get_elapsed(True))
        break
    else:
        sleep(1)
