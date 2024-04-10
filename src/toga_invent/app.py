from . import stub_methods


class App:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self


stub_methods(App, "create_menus")