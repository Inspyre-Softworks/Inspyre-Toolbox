"""
This module contains decorators for class methods that allow you to add aliases for them.

Decorators:
    method_alias:
        Decorator to add alias names to a decorated method.

    add_aliases:
        Decorator to add aliases to a class's methods.
"""


def method_alias(*alias_names):
    """
    A decorator that allows you to add aliases to a class's method.

    This decorator adds an attribute '_alias_names' to the method, which stores the alias names.
    When the 'add_aliases' decorator is applied to the class, it uses these alias names to create
    additional references to the method.

    Parameters:
        *alias_names (str, list[str]):
            The name(s) of the alias(es) to add. You can pass multiple alias names as arguments.

    Returns:
        method:
            The decorated method with an '_alias_names' attribute.

    Example Usage:
        @method_alias('alias1', 'alias2')
        def my_method(self):
            print("Method called")

    Since:
        v1.6.0
    """

    def method_decorator(meth):
        meth._alias_names = alias_names  # Add alias names as an attribute to the method
        return meth

    return method_decorator


def add_aliases(cls):
    """
    A decorator to add aliases to a class's methods.

    This decorator iterates over the class's methods and checks if they have an '_alias_names'
    attribute. For each alias name found in '_alias_names', it creates an alias method in the class.

    Parameters:
        cls (class):
            The class to add aliases to.

    Returns:
        class:
            The decorated class with alias methods added.

    Example Usage:
        @add_aliases
        class MyClass:

            @method_alias('alias1', 'alias2')
            def original_method(self):
                print("Original method called")

        # After decoration, MyClass will have 'alias1' and 'alias2' as aliases for 'original_method'.
        obj = MyClass()
        obj.original_method()  # Output: Original method called
        obj.alias1()           # Output: Original method called
        obj.alias2()           # Output: Original method called

    Since:
        v1.6.0
    """

    for name, method in list(cls.__dict__.items()):  # Iterate over class's attributes
        if hasattr(method, '_alias_names'):  # Check if method has _alias_names attribute
            for alias_name in method._alias_names:  # For each alias name
                setattr(cls, alias_name, method)  # Add the alias as a method of the class
    return cls
