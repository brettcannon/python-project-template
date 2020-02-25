import importlib.metadata

import pytest

import pkg

def test_AttributeError():
    with pytest.raises(AttributeError):
        pkg.does_not_exist

def test___version__():
    try:
        pkg.__version__
    except importlib.metadata.PackageNotFoundError:
        pass
