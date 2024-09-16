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
    return float(f"{float(amount / 1600):.2f}")


# def real_amount_value(amount):
#     cleaned_value = re.sub(r"[₦$,]", "", amount)
#     try:
#         float_val = float(cleaned_value)
#         return f"{float_val:.2f}"
#     except Exception as e:
#         return None
