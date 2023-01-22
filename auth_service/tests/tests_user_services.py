import sys
import unittest

from mocks.user_services_mocks import user_data, user_database_mock 

sys.path.append('..')
sys.path.append('../..')

from application.user.user_storage import UserStorage
from application.user.user_dto import UserDto
from application.user.user_services import UserService

# Mock user
class DummyStorage(UserStorage):
    def get_user_by_username(self, username) -> UserDto:
        data = user_database_mock()
        
        user_dto = UserDto(
            password=data["password"], 
            username=data["username"]
        )
        if username == user_dto.username:
            return user_dto
        else:
            return None


class UserTests(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        self.dummy_storage = DummyStorage()
        super().__init__(methodName)
    
    def test_get_user_by_username(self):
        data = user_data()
        data['username'] = "esseusuarionexiste"
        
        service = UserService(self.dummy_storage)
        user_dto = UserDto(
            password=data["password"],
            username=data["username"]
        )
        user = service.get_user_by_username(user_dto)
        self.assertIsNone(user)
        
if __name__ == '__main__':
    unittest.main()
