from uuid import UUID, uuid4

__all__ = (
    "generate_uuid",
    "generate_request_id",
    "is_valid_uuid",
)


def generate_uuid() -> str:
    return str(uuid4())


def generate_request_id() -> str:
    return generate_uuid()


def is_valid_uuid(uuid_to_test: str, version: int = 4) -> bool:
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except (ValueError, TypeError):
        return False
    return str(uuid_obj) == uuid_to_test
