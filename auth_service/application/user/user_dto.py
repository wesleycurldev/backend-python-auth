from auth_service.domain.user.entities import User


# UserDto tem a responsabilidade de transportar dados de uma camada para a outra.
class UserDto(object):
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_domain(self):
        return User(self.username, self.password)
    