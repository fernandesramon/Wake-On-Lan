"""Wakes a Windows computer using wake-on-lan and connects to an SMB share
"""

import subprocess
import sys
import os
from wakeonlan import send_magic_packet
from smb.SMBConnection import SMBConnection
from smb.base import SMBTimeout, NotConnectedError
from dotenv import load_dotenv

MAC_ADDRESS = None
IP_ADDRESS = None
REMOTE_NAME = None
SHARE_NAME = None

def has_valid_env():
    """Check to make sure .env file exists and contains the necessary variables
    """
    global MAC_ADDRESS, IP_ADDRESS, REMOTE_NAME, SHARE_NAME
    MAC_ADDRESS = os.getenv("MAC_ADDRESS")
    IP_ADDRESS = os.getenv("IP_ADDRESS")
    REMOTE_NAME = os.getenv("REMOTE_NAME")
    SHARE_NAME = os.getenv("SHARE_NAME")

    if not os.path.isfile(".env") or MAC_ADDRESS is None or \
       IP_ADDRESS is None or REMOTE_NAME is None or SHARE_NAME is None:
        return False

    return True

def create_env():
    """Prompt for env values and store in new env file
    """
    global MAC_ADDRESS, IP_ADDRESS, REMOTE_NAME, SHARE_NAME
    if MAC_ADDRESS is None:
        MAC_ADDRESS = input("Target Mac Address: ")
    if IP_ADDRESS is None:
        IP_ADDRESS = input("Target IP Address: ")
    if REMOTE_NAME is None:
        REMOTE_NAME = input("Target computer name: ")
    if SHARE_NAME is None:
        SHARE_NAME = input("Targe SMB share name: ")

    with open(".env", 'w') as file:
        file.write("MAC_ADDRESS={}\n".format(MAC_ADDRESS))
        file.write("IP_ADDRESS={}\n".format(IP_ADDRESS))
        file.write("REMOTE_NAME={}\n".format(REMOTE_NAME))
        file.write("SHARE_NAME={}\n".format(SHARE_NAME))

def main():
    """Main runner
    """
    global MAC_ADDRESS, IP_ADDRESS, REMOTE_NAME, SHARE_NAME

    # Load environment variables
    load_dotenv()
    if not has_valid_env():
        create_env()
    SAMBA_PATH = "{}/{}".format(REMOTE_NAME, SHARE_NAME)

    # Wake Computer
    send_magic_packet(MAC_ADDRESS)

    print("Waiting for computer to boot...")

    # Wait for share to load
    retry = True
    conn = SMBConnection("", "", "", REMOTE_NAME)
    while retry:
        try:
            conn.connect(IP_ADDRESS)
        except SMBTimeout:
            sys.exit(1)
        except NotConnectedError:
            pass
        except ConnectionRefusedError:
            pass
        else:
            conn.close()
            retry = False

    # Connect to Samba
    subprocess.run(["open", "smb://{}".format(SAMBA_PATH)], check=False)

if __name__ == "__main__":
    main()
