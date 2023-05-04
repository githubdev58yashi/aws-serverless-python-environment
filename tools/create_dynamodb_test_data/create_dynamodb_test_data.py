import json

from pynamodb.models import Model

from common.pynamodb.models.Book import Book
from common.pynamodb.models.BookReview import BookReview
from common.pynamodb.models.User import User

UPDATED_USER = "test_user"


def main():
    """jsonからdynamodbにデータを登録する"""

    create_user_data()
    create_book_data()
    create_book_review_data()


def create_user_data():
    print("User作成")
    json_data = get_json_data("./json/User.json")

    for data in json_data:
        user = User(
            hash_key=data["id"],
            user_name=data["userName"],
            email=data["email"],
            password=data["password"],
            updated_user=UPDATED_USER,
        )
        save(user)


def create_book_data():
    print("Book作成")
    json_data = get_json_data("./json/Book.json")

    for data in json_data:
        book = Book(
            title=data["title"],
            author=data["author"],
            publisher=data["publisher"],
            published_date=data["publishedDate"],
            isbn=data["isbn"],
            cover_image_url=data["coverImageUrl"],
            updated_user=UPDATED_USER,
        )
        save(book)


def create_book_review_data():
    print("BookReview作成")
    json_data = get_json_data("./json/BookReview.json")

    for data in json_data:
        book_review = BookReview(
            user_id=data["userId"],
            rating=data["rating"],
            review=data["review"],
            updated_user=UPDATED_USER,
        )
        save(book_review)


def get_json_data(filepath: str) -> list:
    with open(filepath) as f:
        data = json.load(f)

    return data


def save(model: Model):
    try:
        model.save()
    except Exception as e:
        print("エラー発生")
        print(e)


main()
# if __name__ == 'main':
#     main()
