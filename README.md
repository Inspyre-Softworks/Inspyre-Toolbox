# Inspyre Toolbox

----
*A collection of kinda useful tools*


[![Python package](https://github.com/tayjaybabee/Inspyre-Toolbox/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/tayjaybabee/Inspyre-Toolbox/actions/workflows/python-package.yml)


## ...But Why?

----

This toolkit was developed by me in an effort to cut down on having to write the same things over and over again for the various applications I've made. I don't expect that many will find it super useful, but hey, who knows.

----

Getting Started
----

----

## The Goodies

*(...a word which here means 'the modules and packages'....)*


### Live Timer

----

## Brief Overview of the Evolution of Inspyre Toolbox


### Older Changes

#### Added in v1.0.0a9

* #### proc_man

  A new insert to the toolbox that provides easy-access to ways to manage your system processes!
  <br></br>
  **Included in this release**:
  
  * ***Two* new functions**
    * **find_all_by_name**:

      Find all currently running processes with names that include your query string.
  
      ```python
      
      ```

    <br></br>
    * **kill_all_by_name**:
  
      Find all currently running processes with names that include your query string _and kill them_.

#### Added in v1.0.0a7:

* spanners:
  Spanners are kinda like extensions or plugins to standard libraries. The first one (which is
  included from this version on) is an extension to the 'argparse' library:
  * **SubparserActionAliases**:
        An extension of argparse that allows you to alias sub-commands.
    (See the example [included](./examples/spanners/subcommand_aliases_demo.py))
  
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

