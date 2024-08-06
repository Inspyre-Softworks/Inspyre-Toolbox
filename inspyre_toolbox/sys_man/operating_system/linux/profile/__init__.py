from inspyre_toolbox.path_man import provision_path

PROFILE_CONFIGS = {
        'bash': '~/.bashrc',
        'zsh':  '~/.zshrc',
        'fish': '~/.config/fish/config.fish',
        }


def get_profile_path(profile: str = None) -> "pathlib.Path":
    """
    Get the path of a profile file.

    Parameters:
        profile (str):
            The profile to get the path of.

    Returns:
        str: The path of the profile file.
    """

    if profile is None:
        import os

        profile = os.environ.get('SHELL').split('/')[-1]

    path = provision_path(PROFILE_CONFIGS.get(profile))

    if path.exists():
        return path
    else:
        raise FileNotFoundError(f"Profile file not found: '{path}'")
