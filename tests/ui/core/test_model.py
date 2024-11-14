from invent.ui import core


def test_model_init():
    class TestModel(core.Model):
        pass

    model = TestModel()
    assert model.as_dict() == {}
