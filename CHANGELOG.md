# Changelog for Version 1.6.0 (v1.5.3 -> v1.6.0-dev.3)

Previous Version: [1.5.3](https://github.com/Inspyre-Softworks/Inspyre-Toolbox/releases/tag/v1.5.3)

## New Features

### ByteConverter Class:

  - Added a new method get_lowest_safe_conversion() to the ByteConverter class. This method helps users determine the safest conversion level for a given byte value.
download_time Function:

  - Introduced a new [download_time](https://github.com/Inspyre-Softworks/Inspyre-Toolbox/blob/425d981f045a1436a2a06662928b992a25a0124d/inspyre_toolbox/solve_kit/__init__.py#L78) function in the [solve_kit](https://github.com/Inspyre-Softworks/Inspyre-Toolbox/blob/425d981f045a1436a2a06662928b992a25a0124d/inspyre_toolbox/solve_kit/__init__.py) module. This function provides an estimate of the time required to download a file of a specific size given a certain bandwidth.

  - Command-line utility for converting bytes between different units of measurement. This utility is accessible via the 'ist-byte-converter' command and provides a simple interface for converting byte values.


### log_engine Module:

  - Added a centralized logging system via the new log_engine module. This module provides a root logger for the project, enabling consistent and configurable logging across various components.


## Enhancements

### ByteConverter Class:

  - Refactored to include enhanced logging capabilities, providing more detailed insights during byte conversions.
  - Added new attributes to the ByteConverter class, enabling better customization and functionality for advanced users.


### solve_kit Module:

  - Logging has been added to the solve_kit module, improving transparency and debugging capabilities.
  - Version information is now included within the module for better tracking and management.


## Deprecated Features

None


## Breaking Changes
None
