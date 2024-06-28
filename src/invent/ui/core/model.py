from ...compatability import getmembers_static
from .property import Property


class Model:
    """
    Base for a class which contains Properties.
    """

    def __init__(self, **kwargs):
        self.update(**kwargs)

        # Set default values.
        for property_name, property_obj in type(self).properties().items():
            if property_name not in kwargs:
                if property_obj.default_value is not None:
                    setattr(self, property_name, property_obj.default_value)

    @classmethod
    def properties(cls):
        return {
            name: value
            for name, value in getmembers_static(cls)
            if isinstance(value, Property)
        }

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise AttributeError(k)
