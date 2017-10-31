def deserialize(raw):
    """
    Yields a new stream of the input data, untouched
    """
    for chunk in raw:
        yield chunk


def serialize(item):
    """
    Identity function
    """
    return item
