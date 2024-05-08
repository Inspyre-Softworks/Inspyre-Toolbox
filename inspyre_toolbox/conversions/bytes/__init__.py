
class ByteConverter:
    """
    A class to convert different units of digital information.

    ...

    Attributes
    ----------
    units : dict
        a dictionary holding the conversion units
    __bytes : int
        a private attribute to hold the value in bytes

    Methods
    -------
    convert(unit)
        Converts the bytes value to the specified unit.
    """
    # Dictionary holding the conversion units
    units = {
        'byte': 1,
        'kilobyte': 1024,
        'megabyte': 1024**2,
        'gigabyte': 1024**3,
        'terabyte': 1024**4,
        'petabyte': 1024**5,
        'exabyte': 1024**6,
        'zetabyte': 1024**7,
        'yottabyte': 1024**8,
        'bit': 1/8,
        'kilobit': 1024/8,
        'megabit': (1024**2)/8,
        'gigabit': (1024**3)/8,
        'terabit': (1024**4)/8,
        'petabit': (1024**5)/8,
        'exabit': (1024**6)/8,
        'zetabit': (1024**7)/8,
        'yottabit': (1024**8)/8,
    }

    def __init__(self, value, unit):
        """
        Constructs all the necessary attributes for the ByteConverter object.

        Parameters
        ----------
            value : int
                the value to be converted
            unit : str
                the unit of the value to be converted
        """
        # Convert the input value to bytes
        self.__bytes = value * self.units[unit]

    def convert(self, unit):
        """
        Converts the bytes value to the specified unit.

        Parameters
        ----------
            unit : str
                the unit to which the value is to be converted

        Returns
        -------
            float
                the converted value
        """
        # Convert the bytes value to the specified unit
        return self.__bytes / self.units[unit]

    # Below are property methods that return the value in a specific unit

    @property
    def bits(self):
        """Returns the value in bits"""
        return self.convert('bit')

    @property
    def kilobits(self):
        """Returns the value in kilobits"""
        return self.convert('kilobit')

    @property
    def megabits(self):
        """Returns the value in megabits"""
        return self.convert('megabit')

    @property
    def gigabits(self):
        """Returns the value in gigabits"""
        return self.convert('gigabit')

    @property
    def terabits(self):
        """Returns the value in terabits"""
        return self.convert('terabit')

    @property
    def petabits(self):
        """Returns the value in petabits"""
        return self.convert('petabit')

    @property
    def exabits(self):
        """Returns the value in exabits"""
        return self.convert('exabit')

    @property
    def zetabits(self):
        """Returns the value in zetabits"""
        return self.convert('zetabit')

    @property
    def yottabits(self):
        """Returns the value in yottabits"""
        return self.convert('yottabit')

    @property
    def bytes(self):
        """Returns the value in bytes"""
        return self.convert('byte')

    @property
    def kilobytes(self):
        """Returns the value in kilobytes"""
        return self.convert('kilobyte')

    @property
    def megabytes(self):
        """Returns the value in megabytes"""
        return self.convert('megabyte')

    @property
    def gigabytes(self):
        """Returns the value in gigabytes"""
        return self.convert('gigabyte')

    @property
    def terabytes(self):
        """Returns the value in terabytes"""
        return self.convert('terabyte')

    @property
    def petabytes(self):
        """Returns the value in petabytes"""
        return self.convert('petabyte')

    @property
    def exabytes(self):
        """Returns the value in exabytes"""
        return self.convert('exabyte')

    @property
    def zetabytes(self):
        """Returns the value in zetabytes"""
        return self.convert('zetabyte')

    @property
    def yottabytes(self):
        """Returns the value in yottabytes"""
        return self.convert('yottabyte')
