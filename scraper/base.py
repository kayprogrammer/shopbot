from pathlib import Path
import os, re

BASE_DIR = Path(__file__).resolve().parent.parent
DRIVER_LOCATION = os.path.join(BASE_DIR, "geckodriver")


def find_first_number(s):
    # Regular expression pattern to match both integers and decimals
    pattern = r"\b\d+(\.\d+)?\b"
    match = re.search(pattern, s)
    if match:
        return float(match.group())
    else:
        return None


def convert_to_dollars(amount):
    return amount / 1600


def real_amount_value(amount):
    cleaned_value = re.sub(r"[₦$,]", "", amount)
    try:
        return int(cleaned_value)
    except:
        return None
