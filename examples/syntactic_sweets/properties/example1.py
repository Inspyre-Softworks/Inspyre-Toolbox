from inspyre_toolbox.syntactic_sweets.properties import validate_type, validate_path, RestrictedSetter


# Write an example of how to use the @validate_type decorator.


class MyClass:
    my_restrictive_property = RestrictedSetter(
        'my_restrictive_property',
        allowed_types=(int, float),
        preferred_type=int,
        allowed_values=[10, 20, 30],
        restrict_setter=True,

    )

    def __init__(self, my_restrictive_property, my_property=None, my_path_property=None):
        self.__my_property = None
        self.__my_path_property = None

        self.my_restrictive_property = my_restrictive_property
        self.my_property = my_property if my_property is not None else "hello"
        self.my_path_property = my_path_property if my_property is not None else '.'

    @property
    def my_property(self):
        return self.__my_property

    @my_property.setter
    @validate_type(str, allowed_values=["hello", "world"], case_sensitive=False)
    def my_property(self, value):
        self.__my_property = value

    @property
    def my_path_property(self):
        return self.__my_path_property

    @my_path_property.setter
    @validate_path(create=True)
    def my_path_property(self, value):
        self.__my_path_property = value
