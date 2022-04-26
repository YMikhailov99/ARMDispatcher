import re


def parseNumber(number: str):
    if not number is None:
        res = re.sub("\D", "", number)
        return res
    else:
        return None
