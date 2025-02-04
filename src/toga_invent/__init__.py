# Helper for defining required methods which aren't relevant to this backend.
def stub_methods(obj, *names):
    for name in names:
        setattr(obj, name, lambda *args, **kwargs: None)
