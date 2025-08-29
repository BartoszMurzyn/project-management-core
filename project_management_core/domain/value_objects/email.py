import re
REGEX = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

class Email:
    def __init__(self, email) -> None:
        if not re.fullmatch(REGEX, email):
            raise ValueError("Email is incorrect")
        self.email = email