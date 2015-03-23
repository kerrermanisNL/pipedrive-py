# encoding:utf-8
import datetime
from schematics.types import DateType, BaseType
from schematics.exceptions import ConversionError


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


class PipedriveModelType(BaseType):
    MESSAGES = {
        'value_type': 'Value must be of type %s, dict or int'
    }

    def __init__(self, model_class, *args, **kwargs):
        super(PipedriveModelType, self).__init__(*args, **kwargs)
        self.model_class = model_class

    def to_native(self, value, context=None):
        if isinstance(value, self.model_class):
            return value

        if isinstance(value, int):
            return self.model_class({'id': value})

        if isinstance(value, dict):
            return dict_to_model(value, self.model_class)

        raise ConversionError(self.messages['value_type'] % self.model_class)            

    def to_primitive(self, value, context=None):
        return value.id