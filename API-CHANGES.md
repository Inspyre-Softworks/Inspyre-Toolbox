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

