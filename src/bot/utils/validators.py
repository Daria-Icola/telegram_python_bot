import re

def km_validation(km):
    KM_CORRECT = r"^[0-9][0-9 -]{0,9}$"
    return re.match(KM_CORRECT, str(km))

