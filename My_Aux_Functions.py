from bisect import bisect_right
from typing import Tuple


def can_insert_user(users: list, user) -> Tuple[bool, int]:
    """
    Checks if a given sorted list of users doesn't contain a user who has the same name as a given user.
    Runtime complexity of O(log n) using function from module bisect.
    :param users: Given sorted list of users.
    :param user: Given user.
    :return: A tuple consisting of a bool type and an int type:
             Bool type will be set True if above condition is True, False otherwise.
             Int type will be set to the index where 'user' will have to be inserted to in 'users', such that 'users' will still be sorted,
             or alternatively the index of a user in 'users' that has the same name as 'user' (if such user exists).
    """
    length = len(users)
    if length == 0:
        return True, 0
    index = bisect_right(users, user)
    if 0 < index <= length:
        if users[index - 1].get_name() == user.get_name():  # if 'users' already has a user with the same name as 'suer'
            return False, index - 1
    return True, index


def offline_error(user) -> None:
    """
    Prints an error message which occurs if a given user tries to perform an action while offline.
    :param user: Given user
    :return:
    """
    print(f"Error: The user '{user.get_name()}' is offline. Log in to do this action.")


def password_error() -> None:
    """
    Prints incorrect password error.
    :return:
    """
    print("Error: Incorrect password")
