from abc import ABC, abstractmethod
from typing import Optional
from pysics.types import Color, ByteInt, PIndex, Vertex
from pysics._wrappers import _GLWrapper, GL_QUADS


class BaseShape(ABC):
    """The base shape that contains generic properties.

    Attributes:
        x: The x-axis of the shape position.
        y: The y-axis of the shape position.
        fill (Optional): The filling color of the shape. Default to None.
    """

    def __init__(
        self, x: PIndex, y: PIndex, *, fill: Optional[Color | ByteInt] = None
    ) -> None:
        """The constructor.
        Automatically render the shape by calling _render() after initialized
        the properties.

        Args:
            x: The x-axis of the shape position.
            y: The y-axis of the shape position.
            fill (Optional): The filling color of the shape. Default to None.
        """

        self.x: PIndex = x
        self.y: PIndex = y
        self.fill: Color | None = (
            Color.from_unit(fill) if isinstance(fill, int) else fill
        )
        self._render()

    @abstractmethod
    def _render(self) -> None:
        """The abtract method to render the shape."""

        ...


class Rect(BaseShape):
    """A rectangural shape.

    Attributes:
        x: The x-axis of the shape position.
        y: The y-axis of the shape position.
        width: The width of the shape.
        height: The height of the shape.
        fill (Optional): The filling color of the shape. Default to None.
    """

    def __init__(
        self,
        x: PIndex,
        y: PIndex,
        width: float,
        height: float,
        *,
        fill: Optional[Color | ByteInt] = None
    ) -> None:
        """The constructor.
        First initialize its own properties, then init its inherited shape.

        Args:
            x: The x-axis of the shape position.
            y: The y-axis of the shape position.
            width: The width of the shape.
            height: The height of the shape.
            fill (Optional): The filling color of the shape. Default to None.
        """

        self.width: float = width
        self.height: float = height
        super().__init__(x, y, fill=fill)

    def _render(self) -> None:
        """Render the rectangle to the window."""

        vertices: list[Vertex] = [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height),
        ]

        if self.fill:
            _GLWrapper.color_4f(*self.fill.ratios)

        _GLWrapper.begin(GL_QUADS)

        for vertex in vertices:
            _GLWrapper.vertex_2f(*vertex)

        _GLWrapper.end()
