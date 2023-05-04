from pynamodb.attributes import (
    BinaryAttribute,
    BinarySetAttribute,
    BooleanAttribute,
    ListAttribute,
    MapAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UnicodeSetAttribute,
)
from pynamodb.indexes import (
    AllProjection,
    GlobalSecondaryIndex,
    IncludeProjection,
    KeysOnlyProjection,
    LocalSecondaryIndex,
)
from pynamodb.models import Model


class Lsk2Index(LocalSecondaryIndex):
    class Meta:
        index_name = "lsk2-index"
        projection = KeysOnlyProjection()
    part_key_1 = UnicodeAttribute(hash_key=True)
    lsk2 = UnicodeAttribute(range_key=True)

class Lsk3Index(LocalSecondaryIndex):
    class Meta:
        index_name = "lsk3-index"
        projection = IncludeProjection(['include_key'])
    part_key_1 = UnicodeAttribute(hash_key=True)
    lsk3 = UnicodeAttribute(range_key=True)

class Lsk1Index(LocalSecondaryIndex):
    class Meta:
        index_name = "lsk1-index"
        projection = AllProjection()
    part_key_1 = UnicodeAttribute(hash_key=True)
    lsk1 = UnicodeAttribute(range_key=True)


class Pk1Sk1Index(GlobalSecondaryIndex):
    class Meta:
        index_name = "pk1-sk1-index"
        projection = KeysOnlyProjection()
    pk1 = UnicodeAttribute(hash_key=True)
    sk1 = UnicodeAttribute(range_key=True)

class PartKey1SortKey1Index(GlobalSecondaryIndex):
    class Meta:
        index_name = "part_key_1-sort_key_1-index"
        projection = AllProjection()
    part_key_1 = UnicodeAttribute(hash_key=True)
    sort_key_1 = UnicodeAttribute(range_key=True)

class Pk1SortKey1Index(GlobalSecondaryIndex):
    class Meta:
        index_name = "pk1-sort_key_1-index"
        projection = IncludeProjection(['sk1'])
    pk1 = UnicodeAttribute(hash_key=True)
    sort_key_1 = UnicodeAttribute(range_key=True)

class Table2(Model):
    class Meta:
        table_name = "Table2"
        region = "us-east-1"
    # LSI
    lsk2_index = Lsk2Index()
    lsk3_index = Lsk3Index()
    lsk1_index = Lsk1Index()
    # GSI
    pk1_sk1_index = Pk1Sk1Index()
    part_key_1_sort_key_1_index = PartKey1SortKey1Index()
    pk1_sort_key_1_index = Pk1SortKey1Index()
    # Attribute
    lsk1 = UnicodeAttribute(attr_name='lsk1')
    lsk2 = UnicodeAttribute(attr_name='lsk2')
    lsk3 = UnicodeAttribute(attr_name='lsk3')
    part_key_1 = UnicodeAttribute(attr_name='part_key_1')
    pk1 = UnicodeAttribute(attr_name='pk1')
    sk1 = UnicodeAttribute(attr_name='sk1')
    sort_key_1 = UnicodeAttribute(attr_name='sort_key_1')
    val_num = NumberAttribute(attr_name='val_num')
    val_null = BooleanAttribute(attr_name='val_null')
    val_str_set = UnicodeSetAttribute(attr_name='val_str_set')
    val_binary = BinaryAttribute(attr_name='val_binary')
    val1 = UnicodeAttribute(attr_name='val1')
    val_binary_set = BinarySetAttribute(attr_name='val_binary_set')
    val_bool = BooleanAttribute(attr_name='val_bool')
    val_map = MapAttribute(attr_name='val_map')
    val_list = ListAttribute(attr_name='val_list')
