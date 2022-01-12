#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
#  Added in v1.1

from inspyre_toolbox.humanize.errors.numerical import NumericalErrors


class HumanizeErrors(object):
    def __init__(self):
        self.NumericalErrors = NumericalErrors()

