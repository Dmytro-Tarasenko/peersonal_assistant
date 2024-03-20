import datetime
from typing import Any, List
from collections import namedtuple

import mongoengine
import pydantic
from pydantic import BaseModel

from models.ABModels import ContactModel, PhoneModel, AddressModel

# ('StringField', 'URLField', 'EmailField', 'IntField', 'LongField',
# 'FloatField','DecimalField', 'BooleanField', 'DateTimeField', 'DateField',
# 'ComplexDateTimeField', 'EmbeddedDocumentField', 'ObjectIdField',
# 'GenericEmbeddedDocumentField', 'DynamicField', 'ListField',
# 'SortedListField', 'EmbeddedDocumentListField', 'DictField', 'MapField',
# 'ReferenceField', 'CachedReferenceField', 'LazyReferenceField',
# 'GenericLazyReferenceField', 'GenericReferenceField', 'BinaryField',
# 'GridFSError', 'GridFSProxy', 'FileField', 'ImageGridFsProxy',
# 'ImproperlyConfigured', 'ImageField', 'GeoPointField', 'PointField',
# 'LineStringField', 'PolygonField', 'SequenceField', 'UUIDField',
# 'EnumField', 'MultiPointField', 'MultiLineStringField',
# 'MultiPolygonField', 'GeoJsonBaseField', 'Decimal128Field')


PYTYPES_MDBFIELDS = {
    str: mongoengine.StringField,
    'str': mongoengine.StringField,
    'string': mongoengine.StringField,
    int: mongoengine.IntField,
    'int': mongoengine.IntField,
    'integer': mongoengine.IntField,
    list: mongoengine.ListField,
    'list': mongoengine.ListField,
    'array': mongoengine.ListField,
    float: mongoengine.FloatField,
    'float': mongoengine.FloatField,
    dict: mongoengine.DictField,
    'dict': mongoengine.DictField,
    'dictionary': mongoengine.DictField,
    bytes: mongoengine.BinaryField,
    'bytes': mongoengine.BinaryField,
    'binary': mongoengine.BinaryField,
    set: mongoengine.ListField,
    'set': mongoengine.ListField,
    datetime.datetime: mongoengine.DateTimeField,
    'time': mongoengine.DateTimeField,
    datetime.date: mongoengine.DateField,
    'date': mongoengine.DateField,
    'default': mongoengine.DynamicField
}

mongoengine.connect("odm_builder")

odm_gen = ContactModel.__name__
constructor = mongoengine.Document.__init__

fullname = PYTYPES_MDBFIELDS[str](required=True)

model_schema = ContactModel.model_json_schema()

FieldDescriptor = namedtuple('FieldDescriptor',
                             ('field', 'params', 'type',))

def schema_parser(schema: dict[str, Any]) -> List[FieldDescriptor]:
    result = []
    required = schema.setdefault('required', [])
    properties = schema.setdefault('properties', dict())
    for field, props in properties.items():
        field_type = props.setdefault('type', 'complex')
        is_required = (field in required)
        if field_type == 'complex':
            type_ = properties[field]['anyOf'][0].setdefault('type', 'default')
        else:
            type_ = field_type
        descriptor = FieldDescriptor(field=field,
                                     params=dict(required=is_required),
                                     type=type_)
        result.append(descriptor)

    return result

cls_fields = {'__init__': constructor}

for descriptor in schema_parser(model_schema):
    cls_fields[descriptor.field] = PYTYPES_MDBFIELDS[descriptor.type](**descriptor.params)

OdmGen = type(odm_gen, (mongoengine.Document,), cls_fields)


contact = ContactModel(name="John Doe",
                       email="some@where.com",
                       birthdate="1980-01-01",
                       phones=[{"phone": "1234567890"},
                               {"phone": "   123456 "}],
                       address={"city": "New York",
                                "country": "USA",
                                "zip": "12345",
                                "addr_string": "Some street 123"})

record = OdmGen(**contact.model_dump(warnings=False, exclude=["birthdate"]))

record.save()
