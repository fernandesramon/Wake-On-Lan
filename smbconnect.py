"""Connects to an SMB share
"""

import subprocess
import os
from dotenv import load_dotenv

REMOTE_NAME = None
SHARE_NAME = None

def has_valid_env():
    """Check to make sure .env file exists and contains the necessary variables
    """
    global REMOTE_NAME, SHARE_NAME
    REMOTE_NAME = os.getenv("REMOTE_NAME")
    SHARE_NAME = os.getenv("SHARE_NAME")

    if not os.path.isfile(".env") or REMOTE_NAME is None or SHARE_NAME is None:
        return False

    return True

def create_env():
    """Prompt for env values and store in new env file
    """
    global REMOTE_NAME, SHARE_NAME
    if REMOTE_NAME is None:
        REMOTE_NAME = input("Target computer name: ")
    if SHARE_NAME is None:
        SHARE_NAME = input("Targe SMB share name: ")

    with open(".env", 'w') as file:
        file.write("REMOTE_NAME={}\n".format(REMOTE_NAME))
        file.write("SHARE_NAME={}\n".format(SHARE_NAME))

def main():
    """Main runner
    """
    global REMOTE_NAME, SHARE_NAME

    # Load environment variables
    load_dotenv()
    if not has_valid_env():
        create_env()
    SAMBA_PATH = "{}/{}".format(REMOTE_NAME, SHARE_NAME)

    # Connect to Samba
    subprocess.run(["open", "smb://{}".format(SAMBA_PATH)], check=False)

if __name__ == "__main__":
    main()
