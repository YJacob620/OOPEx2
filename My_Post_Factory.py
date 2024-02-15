from My_Post import Post, TextPost, ImagePost, SalePost


def create_post(poster, post_type: str, content: str, price: int, place: str) -> Post | None:
    """
    Factory function to create different kinds of Post types. Not all variables will be used in every construction of a Post.
    :param poster: The User who owns this post.
    :param post_type: Type of the post (according to the assignment).
    :param content: Content of the post.
    :param price: Relevant only for a SalePost - price of the item.
    :param place: Relevant only for a SalePost - place to pick the item from.
    :return:
    """
    if post_type == "Text":
        post = TextPost(poster, content)
    elif post_type == "Image":
        post = ImagePost(poster, content)
    elif post_type == "Sale":
        post = SalePost(poster, content, price, place)
    else:
        print(f"Error: Invalid post type '{post_type}'.")
        return
    print(str(post))
    return post
