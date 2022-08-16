from typing import Any, Callable
import pytest
import glfw
from pytest_mock import MockerFixture
from pysics.pysics import Pysics, Canvas
from pysics.types import Color


@pytest.mark.unit
class TestCanvas:
    @pytest.mark.parametrize(
        "args, kwargs, expected",
        [
            (
                (200, 200),
                dict(),
                dict(
                    _window=(..., None),
                    width=(..., 200),
                    height=(..., 200),
                    fill=(..., None),
                ),
            ),
            (
                (200, 200),
                dict(fill=255),
                dict(
                    _window=(..., None),
                    width=(..., 200),
                    height=(..., 200),
                    fill=(..., Color.from_unit(255)),
                ),
            ),
            (
                (200, 200),
                dict(fill=Color.from_unit(0)),
                dict(
                    _window=(..., None),
                    width=(..., 200),
                    height=(..., 200),
                    fill=(..., Color.from_unit(0)),
                ),
            ),
        ],
    )
    def test_init(
        self,
        args: Any,
        kwargs: Any,
        expected: dict[str, Any],
        assert_getattr: Callable[..., None],
    ) -> None:
        canvas: Canvas = Canvas(*args, **kwargs)
        assert_getattr(canvas, expected)


@pytest.mark.unit
class TestPysics:
    class _FakeCanvas:
        ...

    @pytest.mark.parametrize(
        "args, expected",
        [
            (
                (),
                dict(_canvas=(..., None), _loop=(..., False), _delay=(..., 0.0)),
            ),
            (
                (_FakeCanvas(),),
                dict(_canvas=(_FakeCanvas, ...), _loop=(..., False), _delay=(..., 0.0)),
            ),
        ],
    )
    def test_init(
        self, args: Any, expected: dict[str, Any], assert_getattr: Callable[..., None]
    ) -> None:
        engine: Pysics = Pysics(*args)
        assert_getattr(engine, expected)
