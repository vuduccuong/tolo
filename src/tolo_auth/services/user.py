from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager

User = get_user_model()


class UserService(BaseUserManager):
    def create_normal_user(self, email: str, username: str, password: str = None):
        user = User(email=email, username=username)
        if not password:
            password = self.make_random_password()
        user.set_password(password)
        user.save(using=self._db)
        return user
