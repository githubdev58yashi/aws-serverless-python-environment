import json
from typing import Tuple

import boto3
import inflection

from common.python.local_file_handler import LocalFileHandler

lh = LocalFileHandler()

REGION_NAME = "us-east-1"


class ImportFunctions:
    """自動生成した際に、不要なimport文は作成したくないのでここで管理する"""

    def __init__(self) -> None:
        self.indexes: list[str] = []
        self.attributes: list[str] = []

    def add_indexes(self, func: str):
        if func not in self.indexes:
            self.indexes.append(func)

    def add_attributes(self, func: str):
        if func not in self.attributes:
            self.attributes.append(func)


def main():
    """すでに存在しているdynamodbのテーブルの情報を元にpynamodbのモデルクラスを作成する

    ・初期値等の設定はしていないので、必要な箇所は都度追加してください。
    ・作成したファイルは一度フォーマットしてから使用してください。
    """

    # JSONから対象のテーブル取得
    target_tables = get_target_tables_by_json()

    # dynamoDBからテーブルの情報取得
    tables_info = get_tables_info(target_tables)

    # クラス作成
    create_model_class(tables_info)


def get_target_tables_by_json() -> list:
    """JSONから対象テーブルを取得

    Returns:
        list: 対象テーブル
    """

    with open(
        lh.target("tools/create_dynamodb_table_model/target_table.json"), "r"
    ) as f:
        json_data = json.load(f)

    prefix = json_data.get("prefix", [])
    suffix = json_data.get("suffix", [])
    tables = json_data.get("tables", [])

    target_tables = [f"{prefix}{table}{suffix}" for table in tables]

    return target_tables


def get_tables_info(target_tables: list) -> dict:
    """テーブルにある属性をすべて取得したいため、全件取得する"""

    def get_table_items(table: str) -> list:
        """テーブルのitemを全件取得"""

        options = {"TableName": table, "Limit": 10000}
        items = []
        res = client.scan(**options)
        items.extend(res["Items"])
        while "LastEvaluatedKey" in res:
            options["ExclusiveStartKey"] = res["LastEvaluatedKey"]
            res = client.scan(**options)
            items.extend(res["Items"])

        return items

    resource = boto3.resource("dynamodb", region_name=REGION_NAME)
    client = boto3.client("dynamodb", region_name=REGION_NAME)

    tables_info: dict = {}
    for table in target_tables:
        tables_info[table] = {}
        client_table = client.describe_table(TableName=table)
        tables_info[table]["client"] = client_table["Table"]
        resource_table = resource.Table(table)
        tables_info[table]["resource"] = resource_table
        tables_info[table]["scan"] = get_table_items(table)

    return tables_info


def create_model_class(tables_info: dict):

    for table_name, info in tables_info.items():
        print(f"========== {table_name} ==========")

        # class名なのでキャメルケースに変換
        class_name = inflection.camelize(table_name, uppercase_first_letter=True)

        # 使用してるimport文
        import_functions = ImportFunctions()

        # LSI
        lsi_class_content, lsi_class_names = get_lsi_class_content(
            info, import_functions
        )
        lsi_content = get_lsi_content(lsi_class_names)
        # GSI
        gsi_class_content, gsi_class_names = get_gsi_class_content(
            info, import_functions
        )
        gsi_content = get_gsi_content(gsi_class_names)
        # class文
        class_content = get_class_content(class_name, table_name)
        # 属性
        attribute_content = get_attribute_content(info, import_functions)
        # import文　※使用する関数のみ定義したいので最後に作成する。
        import_content = get_import_content(import_functions)

        content = create_content(
            import_content,
            lsi_class_content,
            lsi_content,
            gsi_class_content,
            gsi_content,
            class_content,
            attribute_content,
        )
        # ファイル作成
        file_name = f"{table_name}.py"
        create_file(file_name, content)


def get_import_content(import_functions: ImportFunctions) -> str:

    indexes_functions = ",".join(import_functions.indexes)
    attributes_functions = ",".join(import_functions.attributes)

    content = "from pynamodb.models import Model\n"
    if indexes_functions:
        content += f"from pynamodb.indexes import {indexes_functions}\n"
    if attributes_functions:
        content += f"from pynamodb.attributes import {attributes_functions}\n"
    return content


def get_class_content(class_name: str, table_name: str) -> str:

    content = f"""
class {class_name}(Model):
    class Meta:
        table_name = "{table_name}"
        region = "{REGION_NAME}"
"""

    return content


def get_attribute_content(info: dict, import_functions: ImportFunctions) -> str:

    # 対象の属性取得

    # Attribute
    attr_definitions = info["client"].get("AttributeDefinitions", [])
    attribute_definitions = {
        x["AttributeName"]: x["AttributeType"] for x in attr_definitions
    }
    # 存在する属性
    scan_definitions = {}
    if 1 <= len(info["scan"]):
        scan_items = info["scan"]
        for item in scan_items:
            for attr_name, attr_item in item.items():
                for attr_type, _ in attr_item.items():
                    scan_definitions[attr_name] = attr_type

    # 属性の重複を取り除く
    definitions = attribute_definitions | scan_definitions

    content = """    # Attribute\n"""
    for column_name, column_type in definitions.items():

        if column_type == "S":
            content += (
                f"    {column_name} = UnicodeAttribute(attr_name='{column_name}')\n"
            )
            import_functions.add_attributes("UnicodeAttribute")
        elif column_type == "N":
            content += (
                f"    {column_name} = NumberAttribute(attr_name='{column_name}')\n"
            )
            import_functions.add_attributes("NumberAttribute")
        elif column_type == "L":
            content += f"    {column_name} = ListAttribute(attr_name='{column_name}')\n"
            import_functions.add_attributes("ListAttribute")
        elif column_type == "M":
            content += f"    {column_name} = MapAttribute(attr_name='{column_name}')\n"
            import_functions.add_attributes("MapAttribute")
        elif column_type == "BOOL":
            content += (
                f"    {column_name} = BooleanAttribute(attr_name='{column_name}')\n"
            )
            import_functions.add_attributes("BooleanAttribute")
        elif column_type == "B":
            content += (
                f"    {column_name} = BinaryAttribute(attr_name='{column_name}')\n"
            )
            import_functions.add_attributes("BinaryAttribute")
        elif column_type == "NULL":
            content += (
                f"    {column_name} = BooleanAttribute(attr_name='{column_name}')\n"
            )
            import_functions.add_attributes("BooleanAttribute")
        elif column_type == "SS":
            content += (
                f"    {column_name} = UnicodeSetAttribute(attr_name='{column_name}')\n"
            )
            import_functions.add_attributes("UnicodeSetAttribute")
        elif column_type == "NS":
            content += (
                f"    {column_name} = NumberSetAttribute(attr_name='{column_name}')\n"
            )
            import_functions.add_attributes("NumberSetAttribute")
        elif column_type == "BS":
            content += (
                f"    {column_name} = BinarySetAttribute(attr_name='{column_name}')\n"
            )
            import_functions.add_attributes("BinarySetAttribute")

    return content


def get_gsi_class_content(
    info: dict, import_functions: ImportFunctions
) -> Tuple[str, dict]:

    # GSI取得
    global_secondary_indexes = info["resource"].global_secondary_indexes
    if global_secondary_indexes is None:
        return "", {}

    import_functions.add_indexes("GlobalSecondaryIndex")
    class_names = {}
    content = "\n"
    for index in global_secondary_indexes:
        index_name: str = index["IndexName"]
        partition_key: str = index["KeySchema"][0]["AttributeName"]
        sort_key = None
        if 2 <= len(index["KeySchema"]):
            sort_key = index["KeySchema"][1]["AttributeName"]
        projection_type: str = index["Projection"]["ProjectionType"]

        # projection
        projection_func = ""
        if projection_type == "ALL":
            projection_func = "AllProjection()"
            import_functions.add_indexes("AllProjection")
        elif projection_type == "KEYS_ONLY":
            projection_func = "KeysOnlyProjection()"
            import_functions.add_indexes("KeysOnlyProjection")
        elif projection_type == "INCLUDE":
            non_key_attributes = index["Projection"]["NonKeyAttributes"]
            projection_func = f"IncludeProjection({non_key_attributes})"
            import_functions.add_indexes("IncludeProjection")

        # class周り

        # -を_に変換することで_抜きのキャメルケースに変換させる
        replace_index_name = index_name.replace("-", "_")
        class_name = inflection.camelize(
            replace_index_name, uppercase_first_letter=True
        )
        content += f"""
class {class_name}(GlobalSecondaryIndex):
    class Meta:
        index_name = "{index_name}"
        projection = {projection_func}
"""
        # key周り
        content += f"    {partition_key} = UnicodeAttribute(hash_key=True)\n"
        if sort_key is not None:
            content += f"    {sort_key} = UnicodeAttribute(range_key=True)\n"

        import_functions.add_attributes("UnicodeAttribute")
        class_names[replace_index_name] = class_name

    return content, class_names


def get_gsi_content(gsi_class_names: dict) -> str:

    if 0 == len(gsi_class_names):
        return ""

    content = """    # GSI\n"""
    for index_name, class_name in gsi_class_names.items():
        content += f"    {index_name} = {class_name}()\n"

    return content


def get_lsi_class_content(
    info: dict, import_functions: ImportFunctions
) -> Tuple[str, dict]:

    local_secondary_indexes = info["resource"].local_secondary_indexes
    if local_secondary_indexes is None:
        return "", {}

    import_functions.add_indexes("LocalSecondaryIndex")
    class_names = {}
    content = "\n"
    for index in local_secondary_indexes:
        index_name: str = index["IndexName"]
        partition_key: str = index["KeySchema"][0]["AttributeName"]
        sort_key = None
        if 2 <= len(index["KeySchema"]):
            sort_key = index["KeySchema"][1]["AttributeName"]
        projection_type: str = index["Projection"]["ProjectionType"]

        # projection
        projection_func = ""
        if projection_type == "ALL":
            projection_func = "AllProjection()"
            import_functions.add_indexes("AllProjection")
        elif projection_type == "KEYS_ONLY":
            projection_func = "KeysOnlyProjection()"
            import_functions.add_indexes("KeysOnlyProjection")
        elif projection_type == "INCLUDE":
            non_key_attributes = index["Projection"]["NonKeyAttributes"]
            projection_func = f"IncludeProjection({non_key_attributes})"
            import_functions.add_indexes("IncludeProjection")

        # class周り

        # -を_に変換することで_抜きのキャメルケースに変換させる
        replace_index_name = index_name.replace("-", "_")
        class_name = inflection.camelize(
            replace_index_name, uppercase_first_letter=True
        )
        content += f"""
class {class_name}(LocalSecondaryIndex):
    class Meta:
        index_name = "{index_name}"
        projection = {projection_func}
"""
        # key周り
        content += f"    {partition_key} = UnicodeAttribute(hash_key=True)\n"
        if sort_key is not None:
            content += f"    {sort_key} = UnicodeAttribute(range_key=True)\n"

        import_functions.add_attributes("UnicodeAttribute")
        class_names[replace_index_name] = class_name

    return content, class_names


def get_lsi_content(lsi_class_names: dict) -> str:

    if 0 == len(lsi_class_names):
        return ""

    content = """    # LSI\n"""
    for index_name, class_name in lsi_class_names.items():
        content += f"    {index_name} = {class_name}()\n"

    return content


def create_content(
    import_content,
    lsi_class_content,
    lsi_content,
    gsi_class_content,
    gsi_content,
    class_content,
    attribute_content,
):

    has_lsi = False
    has_gsi = False
    content = ""
    # import文
    content += import_content
    # LSIクラス
    if lsi_class_content:
        content += lsi_class_content
        has_lsi = True
    # GSIクラス
    if gsi_class_content:
        content += gsi_class_content
        has_gsi = True
    # class文
    content += class_content
    # LSI
    if has_lsi:
        content += lsi_content
    # GSI
    if has_gsi:
        content += gsi_content
    # 属性
    content += attribute_content

    return content


def create_file(file_name, content):

    lh.make_dir("tools/create_dynamodb_table_model/models")
    file = lh.target(f"tools/create_dynamodb_table_model/models/{file_name}")
    with open(file, "w") as f:
        f.write(content)


main()
# if __name__ == 'main':
#     main()
