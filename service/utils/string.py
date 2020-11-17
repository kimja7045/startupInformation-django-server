import uuid


def validate_uuid(value):
    try:
        uuid.UUID(value)
    except ValueError:
        return False
    return True
