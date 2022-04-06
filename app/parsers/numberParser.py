import re


def parseNumber(number: str):
    res = re.sub("\D", "", number)
    return res
