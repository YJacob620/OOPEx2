import My_Aux_Functions as Aux
from matplotlib import pyplot as plt


# noinspection SpellCheckingInspection
class Post:
    """
    Class that represents a post in a social network according to the assignment.
    """
    def __init__(self, poster):
        """
        :param poster: The User (type) who is the owner of this post.
        """
        self._poster = poster  # the user who is the owner of this post
        self.__likers: list = []  # sorted list of users (by usernames) who like this post
        self._comments: list = []  # list of comments (strings)

    def like(self, user) -> None:
        """
        Adds a like to this post.
        :param user: The user who liked this post.
        :return:
        """
        if not user.is_online:
            Aux.offline_error(user)
            return
        can_insert, index = Aux.can_insert_user(self.__likers, user)
        if not can_insert:
            print(f"Error: The user '{user.get_name()}' already likes this post.")
            return
        self.__likers.insert(index, user)
        noti = user.get_notifier().like_notify(self._poster)  # uses observer of user (Notifier)
        if noti is not None:
            print(noti)

    def comment(self, user, text: str) -> None:
        """
        Adds a comment to this post.
        :param user: The user who commented on this post.
        :param text: The content of the comment.
        :return:
        """
        if not user.is_online:
            Aux.offline_error(user)
            return
        self._comments.append(text)
        noti = user.get_notifier().comment_notify(self._poster, text)  # uses observer (Notifier)
        print(noti)


class TextPost(Post):
    """
    Class that represents a TextPost according to the assignment.
    """
    def __init__(self, poster, text: str):
        super().__init__(poster)
        self.__text = text

    def __str__(self):
        poster_name = self._poster.get_name()
        return f'{poster_name} published a post:\n"{self.__text}"' + "\n"


class ImagePost(Post):
    """
    Class that represents an ImagePost according to the assignment.
    """
    def __init__(self, poster, image_path: str):
        super().__init__(poster)
        self.__image_path = image_path

    def display(self) -> None:
        """
        Displays the image using matplotlib.pyplot library.
        :return:
        """
        print("Shows picture")
        image = plt.imread(self.__image_path)
        plt.imshow(image)
        plt.axis('off')
        plt.show()

    def __str__(self):
        poster_name = self._poster.get_name()
        return poster_name + " posted a picture" + "\n"


class SalePost(Post):
    """
    Class that represents a SalePost according to the assignment.
    """
    def __init__(self, poster, desc: str, price: float, place: str):
        super().__init__(poster)
        self.__desc = desc
        self.__price = price
        self.__place = place
        self.__available = True  # New published products are available for sale by default

    def discount(self, disc: float, password: str) -> None:
        """
        Makes a discount on the item of this post.
        :param disc: Amount to discount in percentages.
        :param password: Password of the User who owns this post.
        :return:
        """
        accessible = self.__can_change_post(password)
        if not accessible:
            return
        if disc > 100:
            print(f"ERROR: Invalid discount amount '{disc}'.")
            return
        multiplier = 1 - disc / 100
        new_price = self.__price * multiplier
        self.__price = new_price
        poster_name = self._poster.get_name()
        print("Discount on " + poster_name + " product! the new price is: " + str(new_price))

    def sold(self, password: str) -> None:
        """
        Declares the item in this post as sold.
        :param password: Password of the User who owns this post.
        :return:
        """
        accessible = self.__can_change_post(password)
        if not accessible:
            return
        self.__available = False
        poster_name = self._poster.get_name()
        print(poster_name + "'s product is sold")

    def __can_change_post(self, password: str) -> bool:
        """
        Checks if the poster can make changes to their SalePost.
        :param password: Password of the User who owns this post.
        :return: True if the poster is online, if 'password' is the same as their password and if the product
                 in this post is still available. False otherwise.
        """
        if not self._poster.is_online:  # poster can only change SalePost when logged in
            Aux.offline_error(self._poster)
            return False
        poster_pass = self._poster.get_pass()
        if not poster_pass == password:  # poster can only change SalePost when password is correct
            Aux.password_error()
            return False
        if not self.__available:  # poster can only change SalePost if it's still available
            print("Error: This product is no longer available and therefore cannot be changed.")
            return False
        return True

    def __str__(self):
        if self.__available:
            prefix = "For sale! "
        else:
            prefix = "Sold! "
        poster_name = self._poster.get_name()
        return poster_name + " posted a product for sale:\n" + \
            prefix + self.__desc + ", price: " + str(self.__price) + ", pickup from: " + self.__place + "\n"
