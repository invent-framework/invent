"""
Tests the __init__ for pypercard exports the expected objects in __all__
"""
import pypercard


def test_all():
    """
    Ensure only the expected objects are exported in this module.
    """
    assert pypercard.__all__ == ["Card", "CardApp", "Inputs", "palette"]
