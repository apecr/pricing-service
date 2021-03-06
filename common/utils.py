import re

from passlib.handlers.pbkdf2 import pbkdf2_sha512


class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        email_address_matcher = re.compile(r'[^@]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.fullmatch(email) else False


def hash_password(password: str) -> str:
    return pbkdf2_sha512.encrypt(password)


def check_hashed_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha512.verify(password, hashed_password)
