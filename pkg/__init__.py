def __getattr__(name):
    if name == "__version__":
        import importlib.metadata
        return importlib.metadata.version(__name__)
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
