## Changelog

### Features

- **workspace:**
    - **Update Logging and Version Handling**:
        - Updated the logging functionality in `inspyre_toolbox/core_helpers/logging.py`[1].
        - Added `inspyre_toolbox/common/meta.py`[2] for constants related to the project.
        - Created version handling class in `inspyre_toolbox/version.py`[3].
        - Updated Python version requirement in `pyproject.toml`[4] to 3.9.
        - Adjusted package version.

- **generations:**
    - **Add Random Decimal Generator Function**:
        - Added function in the `generations`[5] module for generating random decimal numbers.

- **solve_kit:**
    - **Add Function to Calculate Iterations Until Target**:
        - Added function in the `solve_kit`[6] module for calculating iterations until reaching a target average.

- **proc_man:**
    - **Improve Admin Check and Process Killing**:
        - Enhanced the `is_admin`[7] function in the `proc_man`[8] module.

- **workspace:**
    - **Add About Module and Update Gitignore**:
        - Added `__about__.py`[9] in `inspyre_toolbox`[10] for version and author information.
        - Updated `.gitignore`[11] to exclude "*.log" files.
        - Modified `example_1.py`[12] in `examples/humanize`[12] for correct logger method.

### Fixes

- **humanize:**
    - **Change Log Access Method**:
        - Changed log access method in `humanize`[13] module to `get_child`.


[1]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/inspyre_toolbox/core_helpers/logging.py
[2]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/inspyre_toolbox/common/meta.py
[3]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/inspyre_toolbox/version.py
[4]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/pyproject.toml
[5]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/inspyre_toolbox/generations/__init__.py
[6]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/inspyre_toolbox/solve_kit/__init__.py
[7]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/inspyre_toolbox/proc_man/__init__.py#L51-L63
[8]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/inspyre_toolbox/proc_man/__init__.py
[9]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/inspyre_toolbox/__about__.py
[10]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/inspyre_toolbox/
[11]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/.gitignore
[12]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/examples/humanize/example_1.py
[13]: https://github.com/tayjaybabee/Inspyre-Toolbox/blob/main/inspyre_toolbox/humanize/__init__.py
