# Inspyre Toolbox
----
*A collection of kinda useful tools*

## ...But Why?
----

This toolkit was developed by me in an effort to cut down on having to write the same things over and over again for the various applications I've made. I don't expect that many will find it super useful, but hey, who knows.

----
## Getting Started
----

### The Goodies
*(...a word which here means 'the modules and packages'....)*

* .live_timer:
  * `Timer`: A class-object that allows you to keep a stopwatch-like timer with ease!
    * `.start()`: The timer doesn't start when you initialize the class, it waits for you!
    * `.pause()`: Pause the timer with a single function...
    * `.unpause()`: ...and unpause it, too!
    * `.get_elapsed(sans_pause=False)`: Get the current elapsed time with or without the time paused taken into account!
    * [See the wiki](https://github.com/tayjaybabee/Inspyre-Toolbox/wiki) (coming soon) for more!
* .packages.pypi:
  * `up_to_date(name)`: Just provide a package name and 'up_to_date' will check to see if it's the latest version offered by [PyPi](https://www.pypi.org) or not.

----

### Live Timer




```python
from inspyre_toolbox.live_timer import Timer
from time import sleep

# Initialize the 'Timer' class
timer = Timer()


def time_it():
	"""
	
	An example function that utilizes `inspyre_toolbox.live_timer.Timer`
	
	Returns:
	    None
	
	"""
    timer.start()
    for i in range(45):
        if i >= 21 and i <= 29:
            sp = True
        else:
            sp = False
        time_elapsed = timer.get_elapsed(sans_pause=sp)
        print(f"Iteration #{i} | Time elapsed: {time_elapsed}")
        if i == 15:
            timer.pause()
        if i == 40:
            timer.unpause()
        sleep(1)
		
# Run the example function `time_it`
time_it()

```

Which outputs:

```shell
    Iteration #0 | Time elapsed: 00:00:00
    Iteration #1 | Time elapsed: 00:00:01
    Iteration #2 | Time elapsed: 00:00:02
    Iteration #3 | Time elapsed: 00:00:03
    Iteration #4 | Time elapsed: 00:00:04
    Iteration #5 | Time elapsed: 00:00:05
    Iteration #6 | Time elapsed: 00:00:06
    Iteration #7 | Time elapsed: 00:00:07
    Iteration #8 | Time elapsed: 00:00:08
    Iteration #9 | Time elapsed: 00:00:09
    Iteration #10 | Time elapsed: 00:00:10
    Iteration #11 | Time elapsed: 00:00:11
    Iteration #12 | Time elapsed: 00:00:12
    Iteration #13 | Time elapsed: 00:00:13
    Iteration #14 | Time elapsed: 00:00:14
    Iteration #15 | Time elapsed: 00:00:15
    Iteration #16 | Time elapsed: 00:00:15
    Iteration #17 | Time elapsed: 00:00:15
    Iteration #18 | Time elapsed: 00:00:15
    Iteration #19 | Time elapsed: 00:00:15
    Iteration #20 | Time elapsed: 00:00:15
    Iteration #21 | Time elapsed: 00:00:21
    Iteration #22 | Time elapsed: 00:00:22
    Iteration #23 | Time elapsed: 00:00:23
    Iteration #24 | Time elapsed: 00:00:24
    Iteration #25 | Time elapsed: 00:00:25
    Iteration #26 | Time elapsed: 00:00:26
    Iteration #27 | Time elapsed: 00:00:27
    Iteration #28 | Time elapsed: 00:00:28
    Iteration #29 | Time elapsed: 00:00:29
    Iteration #30 | Time elapsed: 00:00:15
    Iteration #31 | Time elapsed: 00:00:15
    Iteration #32 | Time elapsed: 00:00:15
    Iteration #33 | Time elapsed: 00:00:15
    Iteration #34 | Time elapsed: 00:00:15
    Iteration #35 | Time elapsed: 00:00:15
    Iteration #36 | Time elapsed: 00:00:15
    Iteration #37 | Time elapsed: 00:00:15
```

You can see an example of the above test running here:
[![asciicast](https://asciinema.org/a/smnPlsJCI4UBw3ZHVnxxMoRQr.svg)](https://asciinema.org/a/smnPlsJCI4UBw3ZHVnxxMoRQr)

Or; here's a shorter gif:
[![The thing](https://raw.githubusercontent.com/tayjaybabee/Inspyre-Toolbox/v1.0-a4-dev/repo_assets/live_timer.gif)](https://raw.githubusercontent.com/tayjaybabee/Inspyre-Toolbox/v1.0-a4-dev/repo_assets/live_timer.gif)