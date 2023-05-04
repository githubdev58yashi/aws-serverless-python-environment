from pynamodb.models import Model

from common.pynamodb.models.Book import Book
from common.pynamodb.models.BookReview import BookReview
from common.pynamodb.models.User import User


def main():
    """pynamodbのmodelクラスを元にdynamodbにテーブルを作成

    pynamodbでインデックス含めて作成後、
    AWSコンソールのappSyncで「データソース」で新規データソースを作成し、
    対象テーブルを選択、「GraphQLを自動的に生成する」をチェックすると、
    インデックスのクエリも一緒に作成されます。
    """

    # 作成対象をここに記述する
    target_classes: list[Model] = [Book, BookReview, User]

    for model_class in target_classes:
        if not model_class.exists():
            try:
                print(f"===== 作成開始:{model_class.Meta.table_name} =====")
                model_class.create_table(
                    wait=True, read_capacity_units=1, write_capacity_units=1
                )

            except Exception as e:
                print(e)

        else:
            print(f"すでに存在しているため、作成対象外としました。:{model_class.Meta.table_name}")


main()
# if __name__ == 'main':
#     main()
