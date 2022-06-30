#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
import os


def add_to_path(program_path: str):
    """
    The add_to_path function adds the program path to the system's PATH variable.
    This allows for easy access to programs from any terminal window.

    Args:
        program_path (str):
            The full path to the directory you'd like to add to your system's PATH
            environment variable.

    Returns:
        None
    """
    if os.name == "nt":  # Windows systems
        import winreg  # Allows access to the Windows registry
        import ctypes  # Allows interface with low-level C APIs

        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:  # Get the current user registry
            with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:  # Go to the environment key
                existing_path_value = winreg.EnumValue(key, 3)[1]  # Grab the current path value

                # | v |  Takes the current path value and appends the new program
                # | v |  path
                new_path_value = existing_path_value + program_path + ";"

                # | v |  Update path variable with update path value | v |
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ,
                                  new_path_value)

            # Tell other processes to update their environment
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x1A
            SMTO_ABORTIFHUNG = 0x0002
            result = ctypes.c_long()
            SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
            SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u"Environment", SMTO_ABORTIFHUNG, 5000,
                                ctypes.byref(result), )
    else:  # If system is *nix
        with open(f"{os.getenv('HOME')}/.bashrc", "a") as bash_file:  # Open bashrc file
            bash_file.write(f'\nexport PATH="{program_path}:$PATH"\n')  # Add program path to Path variable
        os.system(f". {os.getenv('HOME')}/.bashrc")  # Update bash source
    print(f"Added {program_path} to path, please restart shell for changes to take effect")
