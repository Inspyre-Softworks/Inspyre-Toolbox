v1.0-alpha4 ~> v1.0-alpha5
==========================

### New Calls

N/A

### Dependency Changes

*




v1.0-alpha3 ~> v1.0-alpha4
==========================

### New Calls

#### New Tool

A new tool was added to Inspyre-Toolbox

  * __inspyre_toolbox.humanize__:
    * __.Numerical__: A class which is initialized with a number (preferrably an integer) which you can then perform a few operations on and have it returned in various forms.
      * number: Call to get the exact value you provided when initializing.
      * to_str: Call to get the exact value you provided when initializing but inside str().
      * to_words: Call to get the value you provided but in a string containing the words representing the value.


v1.0-alpha2 -> v1.0-alpha3
==========================

#### New Calls
Let's look at some of the new calls/objects that have been added since a2:

  * __inspyre_toolbox.live_timer.Timer.history__:

      * __Timer.history__

          * __.ledger__ : _(list)_ A dictionary containing entries for
                                   each state-change of the timer device
          * __.add__: _(function)_ Add a new entry to the aforementioned
                                   ledger
          * __.write__: _(function)_ Write the history ledger to disk.
                                     ($USERHOME/Inspyre-Softworks/data/$TIMESTAMP_ledger.txt)
