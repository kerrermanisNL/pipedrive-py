# encoding:utf-8
import datetime
from schematics.types import DateType, IntType
from schematics.exceptions import ValidationError


class PipedriveDate(DateType):
    def to_native(self, value, context=None):
        return datetime.datetime.strptime(value, "%Y-%m-%d")


class PipedriveTime(DateType):
    def to_native(self, value, context=None):
        minutes, seconds = [int(x) for x in value.split(':')]
        return minutes * 60 + seconds

    def to_primitive(self, value, context=None):
        minutes, seconds = divmod(value, 60)
        return "%s:%s" % (minutes, seconds)


class PipedriveDateTime(DateType):
    def to_native(self, value, context=None):
        return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


class PipedriveBoolean(IntType):
    TRUE = 1
    FALSE = 0
    VALID_VALUES = (
        TRUE, FALSE
    )

    def to_native(self, value, context=None):
        return PipedriveBoolean.TRUE if value else PipedriveBoolean.FALSE

    def validate(self, value):
        if value not in PipedriveBoolean.VALID_VALUES:
            raise ValidationError([
                "%s should be 0 (FALSE) or 1 (TRUE)" % value])
