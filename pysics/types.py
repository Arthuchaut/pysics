from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, TypeAlias

Ratio: TypeAlias = float  # Define a ratio between 0 to 1.
DrawCallback: TypeAlias = Callable[..., None]
Vertex: TypeAlias = tuple[float, float]  # Define a (x, y) coordinate.
Timestamp: TypeAlias = float
Duration: TypeAlias = float


class ByteInt(int):
    """An int type with ranged values.
    This integer handles value from 0 to 255.
    """

    def __init__(self, x: int) -> None:
        """The constructor.

        Args:
            x: The integer value.

        Raises:
            ValueError: If the x value does not match into the [0..255] interval.
        """

        if (0 > x) ^ (255 < x):
            raise ValueError(f"Expected a value in 0..255. {x} given.")


@dataclass
class Color:
    """A color dataclass with usefull properties.

    Attributes:
        r: The red color value (from 0 to 255). Default to 255.
        g: The green color value (from 0 to 255). Default to 255.
        b: The blue color value (from 0 to 255). Default to 255.
        a: The alpha value (from 0 to 255). Default to 255.
    """

    r: ByteInt = 255
    g: ByteInt = 255
    b: ByteInt = 255
    a: ByteInt = 255

    @property
    def values(self) -> tuple[ByteInt, ByteInt, ByteInt, ByteInt]:
        """Get the color in tuple format.

        Returns:
            tuple[ByteInt, ByteInt, ByteInt, ByteInt]: The color in tuple format.
        """

        return self.r, self.g, self.b, self.a

    @property
    def ratios(self) -> tuple[Ratio, Ratio, Ratio, Ratio]:
        """Get the color in ratio format (each value from 0 to 1).

        Returns:
            tuple[Ratio, Ratio, Ratio, Ratio]: The color in ratio format.
        """

        return tuple(map(lambda x: x / 255, self.values))

    @classmethod
    def from_unit(cls, value: ByteInt) -> Color:
        """Create a new color from a unit RGB value.

        Args:
            value: The value to pass each RGB color.

        Returns:
            Color: The created color.
        """

        return cls(*[value] * 3)
