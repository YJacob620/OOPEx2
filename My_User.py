import My_Post_Factory
from My_Notifier import Notifier
import My_Aux_Functions as Aux
from typing import List


class User:
    """
    Class that represents a user in a social network according to the assignment.
    """
    def __init__(self, username: str, password: str):
        self.__username: str = username
        self.__password: str = password
        self.__followers: List[User] = []  # sorted list of users who are followers (by username)
        self.is_online: bool = True  # no problems with online status having public access
        self.__notifications: List[str] = []  # list containing the notifications (strings) of this user
        self.__post_count: int = 0
        self.__notifier: Notifier = Notifier(self.__username, self.__followers)  # 'observer' for this user

    def get_name(self) -> str:
        return self.__username

    def get_pass(self) -> str:
        return self.__password

    def get_followers(self) -> list:
        return self.__followers

    def get_notifier(self):
        return self.__notifier

    def follow(self, to_follow: 'User') -> None:
        """
        Follows another user in the social network.
        :param to_follow: User to follow.
        :return:
        """
        if not self.is_online:
            Aux.offline_error(self)
            return
        if self is to_follow:
            print("Error: Invalid action - users cannot follow themselves.")
            return
        can_insert, index = Aux.can_insert_user(to_follow.__followers, self)
        if can_insert:  # if this user doesn't yet follow 'to_follow'
            to_follow.__followers.insert(index, self)
            print(self.__username + " started following " + to_follow.__username)
            return
        print("Error: " + self.__username + " already follows " + to_follow.__username)

    def unfollow(self, to_unfollow: 'User') -> None:
        """
        Unfollows another user in the social network.
        :param to_unfollow: User to unfollow.
        :return:
        """
        if not self.is_online:
            Aux.offline_error(self)
            return
        can_insert, index = Aux.can_insert_user(to_unfollow.__followers, self)
        if not can_insert:  # if this user truly is following 'to_unfollow'
            to_unfollow.__followers.pop(index)
            print(self.__username + " unfollowed " + to_unfollow.__username)
            return None
        print("Error: " + self.__username + " wasn't following " + to_unfollow.__username + " to begin with.")

    def __lt__(self, other):  # implement this magic function so that bisect() will work on a sorted list of users
        if self.__username < other.__username:
            return True
        return False

    def publish_post(self, post_type: str, content: str, price: int = -1, place: str = ""):
        """
        Publishes a post in the social network.
        :param post_type: Type of the post.
        :param content: Content of the post.
        :param price: Relevant only for a SalePost - price of the item.
        :param place: Relevant only for a SalePost - place to pick the item from.
        :return: The new published post, or None if there was an error when trying to create one.
        """
        if not self.is_online:
            Aux.offline_error(self)
            return None
        post = My_Post_Factory.create_post(self, post_type, content, price, place)  # factory design pattern
        self.__post_count += 1
        self.__notifier.post_notify()
        # self.__notify_followers_about_post()
        return post

    # def __notify_followers_about_post(self) -> None:
    #     """
    #     Notifies each follower of this user about a new post of this user.
    #     """
    #     notification = self.__username + " has a new post"
    #     for follower in self.__followers:
    #         follower.__notifications.append(notification)

    def add_notification(self, notification: str) -> None:
        """
        Adds a notification to 'notifications' of this user.
        :param notification: Notification to add (string).
        :return:
        """
        self.__notifications.append(notification)

    def print_notifications(self) -> None:
        """
        Prints every notification this user ever received from oldest to newest.
        :return:
        """
        print(f"{self.__username}'s notifications:")
        print('\n'.join(map(str, self.__notifications)))  # prints each notification in a new line

    def __str__(self):
        return f"User name: {self.__username}, Number of posts: {self.__post_count}, Number of followers: {len(self.__followers)}"
