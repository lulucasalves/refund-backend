import random
import string


def generateCode(length=6):
    return "".join(random.choices(string.digits, k=length))
