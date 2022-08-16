from abc import ABC
from typing import Any, Callable
import pytest
from pytest_mock import MockerFixture
from pysics.types import Color
from pysics.shapes import BaseShape


@pytest.mark.unit
class TestBaseShape:
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture) -> None:
        mocker.patch.object(BaseShape, "__abstractmethods__", set())

    def test_abstract_class(self) -> None:
        assert issubclass(BaseShape, ABC)

    @pytest.mark.parametrize(
        "args, kwargs, expected",
        [
            ((10, 20), dict(), dict(x=(..., 10), y=(..., 20), fill=(..., None))),
            (
                (10, 20),
                dict(fill=255),
                dict(x=(..., 10), y=(..., 20), fill=(..., Color.from_unit(255))),
            ),
            (
                (10, 20),
                dict(fill=Color.from_unit(0)),
                dict(x=(..., 10), y=(..., 20), fill=(..., Color.from_unit(0))),
            ),
        ],
    )
    def test_init(
        self,
        args: Any,
        kwargs: Any,
        expected: dict[str, tuple[type[Any], Any]],
        assert_getattr: Callable[..., None],
    ) -> None:
        shape: BaseShape = BaseShape(*args, **kwargs)
        assert_getattr(shape, expected)

    def test_abstract_methods(self) -> None:
        methods: list[Callable[..., Any]] = [BaseShape._render]

        for method in methods:
            assert method.__dict__.get("__isabstractmethod__")
