from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model
from pynamodb.settings import OperationSettings

from common.python.dateutil import to_jst_dynamodb_formatted, utc_datetime


class BaseModel(Model):
    # Attribute
    created_at = UTCDateTimeAttribute(attr_name="createdAt")
    jst_created_at = UnicodeAttribute(attr_name="jstCreatedAt")
    updated_at = UTCDateTimeAttribute(attr_name="updatedAt")
    jst_updated_at = UnicodeAttribute(attr_name="jstUpdatedAt")
    updated_user = UnicodeAttribute(attr_name="updatedUser")

    def save(self, condition=None, settings=OperationSettings.default):
        now = utc_datetime()
        if not self.created_at:
            self.created_at = now
            self.jst_created_at = to_jst_dynamodb_formatted(now)

        # 更新日時は常に更新
        self.updated_at = now
        self.jst_updated_at = to_jst_dynamodb_formatted(now)
        super(BaseModel, self).save(condition=condition, settings=settings)
