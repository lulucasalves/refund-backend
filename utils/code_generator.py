import random
import string


def generate_code(length=6, type="numeric"):
    if type == "numeric":
        return "".join(random.choices(string.digits, k=length))

    return "".join(
        random.choices(
            string.ascii_letters + string.digits, k=length
        )
    )
