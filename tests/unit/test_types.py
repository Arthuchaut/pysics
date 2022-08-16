from typing import Any
import pytest
from pysics.types import ByteInt, Color


@pytest.mark.unit
class TestByteInt:
    @pytest.mark.parametrize(
        "x, throwable",
        [
            (0, None),
            (255, None),
            (100, None),
            (-1, ValueError),
            (256, ValueError),
        ],
    )
    def test_init(self, x: int, throwable: type[ValueError] | None) -> None:
        if throwable:
            with pytest.raises(throwable):
                ByteInt(x)
        else:
            value = ByteInt(x)
            assert value == x


@pytest.mark.unit
class TestColor:
    @pytest.mark.parametrize(
        "kwargs, expected",
        [
            (dict(), Color(255, 255, 255, 255)),
            (dict(r=150), Color(150, 255, 255, 255)),
            (dict(g=150), Color(255, 150, 255, 255)),
            (dict(b=150), Color(255, 255, 150, 255)),
            (dict(a=150), Color(255, 255, 255, 150)),
            (dict(r=20, g=140, b=5), Color(20, 140, 5, 255)),
        ],
    )
    def test_init(self, kwargs: Any, expected: Color) -> None:
        color: Color = Color(**kwargs)
        assert color == expected

    @pytest.mark.parametrize(
        "kwargs, expected",
        [
            (dict(), dict(values=(255, 255, 255, 255), ratios=(1.0, 1.0, 1.0, 1.0))),
            (
                dict(r=200, g=40, b=0, a=180),
                dict(
                    values=(200, 40, 0, 180),
                    ratios=(
                        0.7843137254901961,
                        0.1568627450980392,
                        0.0,
                        0.7058823529411765,
                    ),
                ),
            ),
        ],
    )
    def test_properties(
        self, kwargs: Any, expected: dict[str, tuple[Any, ...]]
    ) -> None:
        color: Color = Color(**kwargs)

        for prop_name, exp_value in expected.items():
            assert getattr(color, prop_name) == exp_value

    @pytest.mark.parametrize(
        "value, expected",
        [
            (0, Color(0, 0, 0)),
            (255, Color(255, 255, 255)),
            (140, Color(140, 140, 140)),
        ],
    )
    def test_from_unit(self, value: ByteInt, expected: Color) -> None:
        assert Color.from_unit(value) == expected
