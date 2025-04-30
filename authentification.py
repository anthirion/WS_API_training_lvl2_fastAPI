from .schemas import User


def check_token(token) -> bool:
    print("TOKEN FORWARDE AU BACKEND:")
    print(token)


def get_user_from_token(token) -> User:
    pass
