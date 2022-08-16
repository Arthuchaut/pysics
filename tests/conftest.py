from typing import Any, Callable
import pytest


@pytest.fixture
def assert_getattr() -> Callable[..., None]:
    def wrapper(obj: Any, mapping: dict[str, tuple[type[Any], Any]]):
        for attr_name, exp_state in mapping.items():
            exp_type, exp_value = exp_state
            obj_value = getattr(obj, attr_name)

            if exp_type is not Ellipsis:
                assert type(obj_value) is exp_type
            if exp_value is not Ellipsis:
                assert obj_value == exp_value

    return wrapper
