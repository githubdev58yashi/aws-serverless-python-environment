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
from pynamodb.models import Model


class Table1(Model):
    class Meta:
        table_name = "Table1"
        region = "us-east-1"

    # Attribute
    pk1 = UnicodeAttribute(attr_name="pk1")
    sk1 = UnicodeAttribute(attr_name="sk1")
    val1 = UnicodeAttribute(attr_name="val1")
    val_binary = BinaryAttribute(attr_name="val_binary")
    val_num = NumberAttribute(attr_name="val_num")
    val_null = BooleanAttribute(attr_name="val_null")
    val_str_set = UnicodeSetAttribute(attr_name="val_str_set")
    val_binary_set = BinarySetAttribute(attr_name="val_binary_set")
    val_bool = BooleanAttribute(attr_name="val_bool")
    val_map = MapAttribute(attr_name="val_map")
    val_list = ListAttribute(attr_name="val_list")
