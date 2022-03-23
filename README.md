# Inspyre Toolbox

----
*A collection of kinda useful tools*


[![Python package](https://github.com/tayjaybabee/Inspyre-Toolbox/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/tayjaybabee/Inspyre-Toolbox/actions/workflows/python-package.yml)
![Lines of Code](https://badgen.net/codeclimate/loc/tayjaybabee/Inspyre-Toolbox)
[![CodeQL](https://github.com/tayjaybabee/Inspyre-Toolbox/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/tayjaybabee/Inspyre-Toolbox/actions/workflows/codeql-analysis.yml)
![Latest Github Release](https://badgen.net/github/release/tayjaybabee/Inspyre-Toolbox)
![Latest Stable Release](https://badgen.net/github/release/tayjaybabee/Inspyre-Toolbox/stable)
![PyPi Version](https://badgen.net/pypi/v/Inspyre-Toolbox)
![PyPi Version](https://badgen.net/pypi/python/Inspyre-Toolbox)

## ...But Why?

----

This toolkit was developed by me in an effort to cut down on having to write the same things over and over again for the various applications I've made. I don't expect that many will find it super useful, but hey, who knows.

----

Getting Started
----

----

## The Goodies

*(...a word which here means 'the modules and packages'....)*

* .live_timer: <br>
  
  * Timer: <br>
    A class that keeps real time accurate to the second for you, allowing you to query 'get_elapsed' and get how much time has elapsed since the timer started. Functions include:
  
    * **start**: <br>
      Start the timer.
    * **pause**: <br>
      Pause the timer.
    * **unpause**: <br>
      Unpause a paused timer.
    
* .humanize: <br>
  
  * Numerical: <br>
    A class that allows you to deal with numbers in your Python programs a little easier. Functions include:
    
    * **commify**: <br>
      Return your principle number to you in a commified string form.
    * **count_noun**: <br>
      Return your number and the proper plural form of the thing your number is representing a count of if it's needed. If it's a singular item, (or, the number is 1)

* .spanners: <br>

  * **.spanner_arg_parse**: <br>
    Extend argparse's ArgumentParser by allowing your sub-commands to have aliases!
    
* .proc_man: <br>
  
  A module that contains a way to easily find or kill processes by their name. Functions include:
  
  * **kill_all_by_name**: <br>
  
    Kills all processes with names with a substring that include the string provided as an argument.
    
   * **list_all_by_name**: <br>
     
     Lists all running processes with names with a substring that include the string provided as an argument.
     
* .syntactic_sweets: <br>
  
  Contains miscellaneous helpers to help make your Python programming a little easier. Right now there's one function:
  
    * suppress_stdout:
      A file object that while in-use supporesses standard output from the console.
  
### Live Timer

----

