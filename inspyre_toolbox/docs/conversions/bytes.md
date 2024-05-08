
# ByteConverter Class Documentation

## Overview
The `ByteConverter` class is designed to facilitate the conversion between different units of digital information. This utility can be particularly useful in various programming and data processing scenarios where handling data sizes in different units is necessary.

## Features
- Supports conversion between bytes, kilobytes, megabytes, gigabytes, terabytes, petabytes, exabytes, zetabytes, yottabytes, bits, kilobits, megabits, gigabits, terabits, petabits, exabits, zetabits, and yottabits.
- Easy to use with a straightforward initialization and conversion method.

## Class Attributes
- `units`: A dictionary holding the conversion ratios for different units of digital information.

## Methods
### `__init__(self, value, unit)`
Initializes a new instance of the `ByteConverter` class.

#### Parameters
- `value` : `int`  
  The numeric value to be converted.
- `unit` : `str`  
  The unit of the initial value.

### `convert(self, unit)`
Converts the stored digital information value to the specified unit.

#### Parameters
- `unit` : `str`  
  The unit to which the value is to be converted.

#### Returns
- `float`  
  The converted value in the specified unit.

## Property Methods
The class also provides property methods for each unit, allowing easy access to the value in any supported unit without explicitly calling the convert method.

## Usage Examples
### Converting Bytes to Megabytes
```python
converter = ByteConverter(2048, 'byte')
print(converter.convert('megabyte'))  # Output: 0.001953125
```

### Initializing with Gigabytes and Accessing Value in Terabytes
```python
converter = ByteConverter(1, 'gigabyte')
print(converter.terabytes)  # Output: 0.0009765625
```

This class is an effective tool for anyone needing to work with digital information units, offering flexibility and ease of use for various programming needs.
