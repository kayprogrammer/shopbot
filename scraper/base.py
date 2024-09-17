from pathlib import Path
import os, re, platform

BASE_DIR = Path(__file__).resolve().parent.parent
system = platform.system()
driver = "geckodriver.exe" if system == "Windows" else "geckodriver"
DRIVER_LOCATION = os.path.join(BASE_DIR, driver)


def find_first_number(s):
    # Regular expression pattern to match both integers and decimals
    pattern = r"\b\d+(\.\d+)?\b"
    match = re.search(pattern, s)
    if match:
        return float(match.group())
    else:
        return None


def convert_to_dollars(amount):
    return float(f"{float(amount / 1600):.2f}")