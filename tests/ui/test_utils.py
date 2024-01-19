from invent.ui import utils


def test_random_id_default():
    """
    A valid random id is created with the expected default args.
    """
    test_id = utils.random_id()
    assert test_id.startswith("invent-")
    assert len(test_id[7:]) == 10


def test_random_id_bespoke():
    """
    A valid random id is created with the custom args.
    """
    test_id = utils.random_id(prefix="test", separator="_", length=4)
    assert test_id.startswith("test_")
    assert len(test_id[5:]) == 4


def test_sanitize():
    """
    Ensure raw (unsafe) user input is sanitized into something HTML safe.
    """
    result = utils.sanitize("<script>alert('boom & busted');</script>")
    assert result == "&lt;script&gt;alert('boom &amp; busted');&lt;/script&gt;"
