import argparse

from inspyre_toolbox.core_helpers.clipboard import add_text_to_clipboard


class VersionAction(argparse.Action):
    def __init__(self, option_strings, version=None, **kwargs):
        self.version = version
        super().__init__(option_strings, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if self.version is None:
            parser.error("VersionAction requires a version string.")

        prog_name = 'Inspyre Toolbox' if parser.prog == 'ist-version-tool' else parser.prog
        version_str = f'{prog_name} | {self.version}'
        print(namespace)

        if getattr(namespace, 'copy_to_clipboard', False):
            add_text_to_clipboard(version_str)
            print(f"Version information copied to clipboard: {version_str}")
        else:
            print(version_str)

        parser.exit()
