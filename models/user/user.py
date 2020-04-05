import uuid
from dataclasses import dataclass, field
from typing import Dict

from common.utils import Utils, hash_password
from models.model import Model
import models.user.errors as UserErrors


@dataclass
class User(Model):
    collection: str = field(init=False, default='users')
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by(('email', email))
        except TypeError:
            raise UserErrors.UserNotFoundError('A user with this email was not found')

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('This email does not have the right format.')
        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError('The email ypu used already exists.')
        except UserErrors.UserNotFoundError as e:
            User(email, hash_password(password)).save_to_mongo()

        return True

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }
