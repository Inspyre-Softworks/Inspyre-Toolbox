v1.0-alpha5 ~> v1.0-alpha6
==========================

## Version

1.0 alpha build #6

----

* Humanize.Numerical.count_noun() now returns a string with the first part being the number being counted, commified, the second part will be the plural noun


### Dependencies

#### Production

None

#### Development

* Inspy-Logger: Added to be utilized in the new example file at `examples/humanize/example_1.py`.


### Repo Changes

* Added `examples/humanize/example_1.py`.


### Added Classes

#### Exceptions

##### Added

* __inspyre_toolbox.humanize.NotANumberError__ (Exception): Raised when a function is passed something other than an integer or float when it was expecting an integer or a float.


### Call Changes

* __inspyre_toolbox.humanize__:
    * __Numerical.count_noun__:
        * Additional Parameters:
            * __count__ (int/float): (Default: Numerical.number) The number of 'NOUN' that exists
            * __only_noun__ (bool): (Default: False) If True; only return with the properly pluralized noun and not the number
            * __skip_commify__ (bool): ((Default: False) *Ignored if 'only_noun' is True* Skip commifying the the number of 'NOUN'.
            * __count_to_words__ (bool, optional): Return as usual but with the number of 'noun' formatted into words.
            * __capitalize__ (bool, optional): If True return the count words with the first letter capitalized. Defaults to False, ignored if 'count_to_words' is False.
            * __round_num__ (int, optional): If populated will round the number to a given precision in decimal digits. Defaults to None.

* __inspyre_toolbox.live_timer__:
    * __Timer.get_elapsed__:
        * Additional Parameters:
            * __seconds__ (bool, optional): If true don't format the result, just return the number of seconds elapsed as an integer. Defaults to False.

v1.0-alpha4 ~> v1.0-alpha5
==========================


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
