import time


class Builder:
    def get_widgets(self):
        ...


    def do_something(self, obj):
        """Do something"""

        from pyscript import display
        display(f"builder.do_something: {time.gmtime()}")
        display(str(obj))
        display(str(type(obj)))
        display(str(dir(obj)))

        if hasattr(obj, 'a'):
            display(str(obj.a))
