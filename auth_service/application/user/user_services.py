from auth_service.application.user.user_dto import UserDto

from auth_service.domain.user.exceptions import UserError
from auth_service.domain.user.enums import ErrorCodes
from .user_storage import UserStorage


class UserService(object):
    user: UserStorage

    def __init__(self, storage: UserStorage) -> None:
        self.storage = storage
    
    def get_user_by_username(self, user_dto: UserDto):
        domain_object = user_dto.to_domain()
        
        try:
            user = self.storage.get_user_by_username(domain_object.username)
            return user
        except UserError as e:
            return {'message': e.message, 'code': ErrorCodes.USER_ERROR}
        except Exception as e:
            return {'message': e.message, 'code': ErrorCodes.UNDEFINED_ERROR}
