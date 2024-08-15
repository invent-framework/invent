from ...utils import getmembers_static
from .property import Property


class Model:
    """
    Base for a class which contains Properties.
    """

    def __init__(self, **kwargs):
        # MicroPython incorrectly calls __set_name__ with the Model instance,
        # not the class. And it doesn't call it early enough on Layout classes
        # for some reason, which would cause the default values loop below to
        # fail.
        for key, prop in self.properties().items():
            prop.__set_name__(type(self), key)

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

    def as_dict(self):
        properties = {}
        for property_name, property_obj in sorted(self.properties().items()):
            from_datastore = self.get_from_datastore(property_name)
            if from_datastore:
                property_value = repr(from_datastore)
            else:
                property_value = getattr(self, property_name)

            properties[property_name] = property_value

        return properties

    def get_from_datastore(self, property_name):
        """
        Return the "from_datastore" instance for a property, or None if it is
        an unbound property.
        """
        return self.properties()[property_name].get_from_datastore(self)

    def set_from_datastore(self, property_name, *args, **kwargs):
        """
        Set the "from_datastore" instance for a property. Pass None to make it
        an unbound property.
        """
        self.properties()[property_name].set_from_datastore(
            self, *args, **kwargs
        )
