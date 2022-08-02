"""STIX 2.1 Bundle Representation."""

from collections import OrderedDict

from ..properties import (
    IDProperty, ListProperty, STIXObjectProperty, TypeProperty,
)
from .base import _STIXBase21


class Bundle(_STIXBase21):
    """For more detailed information on this object's properties, see
    `the STIX 2.1 specification <https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_nuwp4rox8c7r>`__.
    """

    _type = 'bundle'
    _properties = OrderedDict([
        ('type', TypeProperty(_type, spec_version='2.1')),
        ('id', IDProperty(_type, spec_version='2.1')),
        ('objects', ListProperty(STIXObjectProperty(spec_version='2.1'))),
    ])

    def __init__(self, *args, **kwargs):
        # Add any positional arguments to the 'objects' kwarg.
        if args:
            obj_list = []
            for arg in args:
                if isinstance(arg, list):
                    obj_list = obj_list + arg
                else:
                    obj_list.append(arg)

            kwargs['objects'] = obj_list + kwargs.get('objects', [])

        self._allow_custom = kwargs.get('allow_custom', False)
        self._properties['objects'].contained.allow_custom = kwargs.get('allow_custom', False)

        super(Bundle, self).__init__(**kwargs)

    def get_obj(self, obj_uuid):
        if "objects" not in self._inner:
            raise KeyError("There are no objects in this empty bundle")
        if found_objs := [elem for elem in self.objects if elem['id'] == obj_uuid]:
            return found_objs
        else:
            raise KeyError("'%s' does not match the id property of any of the bundle's objects" % obj_uuid)

    def __getitem__(self, key):
        try:
            return super(Bundle, self).__getitem__(key)
        except KeyError:
            try:
                return self.get_obj(key)
            except KeyError:
                raise KeyError("'%s' is neither a property on the bundle nor does it match the id property of any of the bundle's objects" % key)
