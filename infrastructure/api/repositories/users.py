import sys

sys.path.append('..')
sys.path.append('../..')

from auth_service.application.user.user_storage import UserStorage
from auth_service.application.user.user_dto import UserDto
from auth_service.application.user.user_services import UserService
from models.users import Users

class UserRepository(UserStorage):
    def get_user_by_username(self, username) -> UserDto:
        return Users.query.filter_by(username=username).first()
