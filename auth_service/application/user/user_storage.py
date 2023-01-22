from abc import ABC, abstractclassmethod
from .user_dto import UserDto

class UserStorage(ABC):

    @abstractclassmethod
    def get_user_by_username(self, username) -> UserDto:
        pass
