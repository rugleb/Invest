import pytest

from invest_api.utils import is_valid_uuid


@pytest.mark.parametrize("value,status", [
    ("c9bf9e57-1685-4c89-bafb-ff5af830be8a", True),
    ("16fd2706-8baf-433b-82eb-8c7fada847da", True),
    ("a8098c1af86e11dab2d1a00112444be1e", False),
    ("16fd27068baf433b82eb8c7f1da847da", False),
    ("uuid", False),
    ("", False),
])
def test_is_valid_uuid_method(value: str, status: bool) -> None:
    assert is_valid_uuid(value) is status
