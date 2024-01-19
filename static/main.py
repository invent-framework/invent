import pytest


pytest.main(["-v", "--cov=invent", "--cov-report", "term-missing", "tests/"])

