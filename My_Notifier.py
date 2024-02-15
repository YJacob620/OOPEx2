class Notifier:
    """
    An observer class for User types. Notifies some other users (such as followers) about this user's actions.
    """

    def __init__(self, username: str, followers: list):
        """
        :param followers: List of users that follow the user with the name 'username'.
        """
        self.__username = username
        self.__followers = followers

    def post_notify(self) -> None:
        """
        Notifies all followers about new post.
        """
        for user in self.__followers:
            message = self.__username + " has a new post"
            user.add_notification(message)

    def like_notify(self, user_to_notify) -> str | None:
        """
        Notifies another user about liking their post.
        :param user_to_notify: User to notify.
        :return: The notification message (or None if there isn't any).
        """
        notifier_name = self.__username  # the name of the owner of this Notifier
        to_notify_name = user_to_notify.get_name()  # the name of the notified user
        if notifier_name == to_notify_name:  # if someone liked their own post, no need to notify them about it
            return None
        message = notifier_name + " liked your post"
        user_to_notify.add_notification(message)
        prefix = f"notification to {to_notify_name}: "
        return prefix + message

    def comment_notify(self, user_to_notify, comment: str) -> str | None:
        """
        Notifies another user about commenting on their post.
        :param user_to_notify: User to notify.
        :param comment: Content of the comment
        :return: The notification message (or None if there isn't any).
        """
        notifier_name = self.__username  # the name of the owner of this Notifier
        to_notify_name = user_to_notify.get_name()  # the name of the notified user
        if notifier_name == to_notify_name:  # if someone commented on their own post, no need to notify them about it
            return None
        message = notifier_name + " commented on your post"
        user_to_notify.add_notification(message)
        prefix = f"notification to {to_notify_name}: "
        return prefix + message + ": " + comment
