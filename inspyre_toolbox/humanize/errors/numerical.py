#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
#  Added in v1.1


class NumericalErrors(object):
    def __init__(self):
        self.NotANumberError = NotANumberError


class NotANumberError(Exception):
    
    def __init__(self, var, var_name: str = None, msg: str = None, skip_print: bool = False, redirect_print=None) :
        """

        Raised when a parameter is provided that is not an integer or a float where one was expectecd.

        Args:
            var (Any): The variable which triggered the raising of this exception.
            var_name (str, optional): The name of the variable that was passed to raise this exception. Defaults to
            None.
            msg (str, optional): The message you'd like the end-user to see upon raising. Defaults to None.
            skip_print (bool, optional): Should we skip printing the message on initialization. Defaults to False.
            redirect_print (any output, optional): An object to redirect our printing to. Ignored if 'skip_print' is
            True. Defaults to None.


        Returns:
            None.

        """
        
        if var_name is None :
            msg1 = "The variable provided is neither an integer or a float. One or the other is needed."
        else :
            var_type = type(var)
            msg1 = f"{var_name} has a value of {var} and is of type {var_type}. An integer or float was needed."
        
        if msg is None :
            msg = msg1
        else :
            msg = msg1 + ' ' + msg
        
        self.msg = msg
        self.message = self.msg
        
        if not skip_print :
            if redirect_print :
                redirect_print(self.message)
            else :
                print(self.message)
