import uuid
from typing import Any, Optional

from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

from common.pynamodb.models.BaseModel import BaseModel
from common.python.ini_reader import IniReader

_KeyType = Any
ini = IniReader()

PREFIX = ini.get("dynamodb", "prefix")
REGION = ini.get("dynamodb", "region")


class IdCreatedAtIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "bookId-jstCreatedAt-index"
        projection = AllProjection()
        write_capacity_units = 1
        read_capacity_units = 1

    id = UnicodeAttribute(hash_key=True)
    created_at = UnicodeAttribute(range_key=True, attr_name="createdAt")


class Book(BaseModel):
    def __init__(
        self,
        hash_key: Optional[_KeyType] = None,
        range_key: Optional[_KeyType] = None,
        _user_instantiated: bool = True,
        **attributes: Any,
    ) -> None:
        super().__init__(hash_key, range_key, _user_instantiated, **attributes)
        if hash_key is None:
            # hash_keyの指定がない場合に別インスタンスとしたいため、ここでid生成
            id_value = str(uuid.uuid4())
            self.id = id_value

    class Meta:
        table_name = f"Book{PREFIX}"
        region = REGION

    # GSI
    book_id_jst_created_at_index = IdCreatedAtIndex()

    # Attribute
    id = UnicodeAttribute(hash_key=True)
    title = UnicodeAttribute()
    author = UnicodeAttribute()
    publisher = UnicodeAttribute()
    published_date = UnicodeAttribute(attr_name="publishedDate")
    isbn = UnicodeAttribute()
    cover_image_url = UnicodeAttribute(attr_name="coverImageUrl")
