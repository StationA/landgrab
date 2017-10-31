def deserialize(raw):
    for chunk in raw:
        yield chunk


def serialize(item):
    return item
