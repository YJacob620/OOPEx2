from My_User import User
import My_Aux_Functions as Aux


class SocialNetwork:
    """
    Class that represents a social network according to the assignment.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):  # singleton initialization of SocialNetwork
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.__name: str = args[0]
            cls.__registered_users: list = []
            print(f"The social network {args[0]} was created!")
        else:
            print(f"Error: Cannot initialize a new network '{args[0]}' because the network '{cls._instance.get_name()}' already exists.")
        return cls._instance

    def get_name(self) -> str:
        return self.__name

    def sign_up(self, username: str, password: str) -> User | None:
        """
        Signs up a user to this network.
        :param username: New user's name.
        :param password: New user's password
        :return: A new User with these credentials, or None if there was an error when trying to create one.
        """
        user = User(username, password)
        can_insert, index = Aux.can_insert_user(self.__registered_users, user)
        if not can_insert:  # if a user with same name as 'username' already exists in '__registered_users'
            print(f"Error: Username '{username}' is already taken.")
            return
        pass_len = len(password)
        if pass_len < 4 | pass_len > 8:
            print("Error: Password should be between 4 to 8 characters (inclusive).")
            return
        self.__registered_users.insert(index, user)
        return user

    def log_out(self, username: str) -> None:
        """
        Disconnects a user from the network.
        :param username: Name of the user to log out.
        :return:
        """
        temp = User(username, "1234")
        can_insert, index = Aux.can_insert_user(self.__registered_users, temp)
        if not can_insert:  # if a user with the name 'username' truly exists in '__registered_users'
            user = self.__registered_users[index]
            if user.is_online:  # if user truly is logged in
                self.__registered_users[index].is_online = False
                print(f"{username} disconnected")
                return
        print(f"Error: No such user '{username}' is currently logged in.")

    def log_in(self, username: str, password: str) -> None:
        """
        Connects a user to the network.
        :param username: Name of the user to log in.
        :param password: Password of the user.
        :return:
        """
        temp = User(username, "1234")
        can_insert, index = Aux.can_insert_user(self.__registered_users, temp)
        if not can_insert:  # if a user with the name 'username' truly exists in '__registered_users'
            user = self.__registered_users[index]
            if not user.get_pass() == password:
                Aux.password_error()
                return
            if not user.is_online:  # if user truly is logged out
                self.__registered_users[index].is_online = True
                print(f"{username} connected")
                return
        print(f"Error: No such user '{username}' is currently logged out.")

    def __str__(self):
        return f"{self.__name} social network:\n" + '\n'.join(map(str, self.__registered_users)) + "\n"
