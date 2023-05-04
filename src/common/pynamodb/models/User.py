import uuid
from typing import Any, Optional

from pynamodb.attributes import UnicodeAttribute

from common.pynamodb.models.BaseModel import BaseModel
from common.python.ini_reader import IniReader

_KeyType = Any
ini = IniReader()

PREFIX = ini.get("dynamodb", "prefix")
REGION = ini.get("dynamodb", "region")


class User(BaseModel):
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
        table_name = f"User{PREFIX}"
        region = REGION

    # Attribute
    id = UnicodeAttribute(hash_key=True)
    user_name = UnicodeAttribute(attr_name="userName")
    email = UnicodeAttribute()
    password = UnicodeAttribute()
