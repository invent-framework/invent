import pytest


pytest.main(["-vv", "--cov=invent", "--cov-report", "term-missing", "tests/"])

