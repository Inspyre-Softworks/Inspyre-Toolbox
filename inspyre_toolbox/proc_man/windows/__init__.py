import win32api
import win32con
import win32security

# Constants for integrity levels
SECURITY_MANDATORY_UNTRUSTED_RID = 0x00000000
SECURITY_MANDATORY_LOW_RID = 0x00001000
SECURITY_MANDATORY_MEDIUM_RID = 0x00002000
SECURITY_MANDATORY_HIGH_RID = 0x00003000
SECURITY_MANDATORY_SYSTEM_RID = 0x00004000


def is_process_elevated(pid):
    try:
        # Open a handle to the process
        hProcess = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
    except Exception as e:
        print(f"Failed to open process {pid}: {e}")
        return False
    try:
        # Open the access token associated with the process
        hToken = win32security.OpenProcessToken(hProcess, win32con.TOKEN_QUERY)
    except Exception as e:
        print(f"Failed to open process token: {e}")
        win32api.CloseHandle(hProcess)
        return False
    try:
        # Retrieve the integrity level of the process
        label = win32security.GetTokenInformation(hToken, win32security.TokenIntegrityLevel)
        sid = label[0]
        # Get the integrity level RID
        integrity_level = win32security.GetSidSubAuthority(sid, 0)
        # Check if the integrity level indicates elevated privileges
        is_elevated = integrity_level >= SECURITY_MANDATORY_HIGH_RID
    except Exception as e:
        print(f"Failed to get token integrity level: {e}")
        is_elevated = False
    finally:
        # Clean up handles
        win32api.CloseHandle(hToken)
        win32api.CloseHandle(hProcess)
    return is_elevated
