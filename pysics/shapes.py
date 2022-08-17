from abc import ABC, abstractmethod
from typing import Optional
from pysics.types import Color, ByteInt, PIndex, Vertex
from pysics._wrappers import _GLWrapper, GL_QUADS, GL_LINE_LOOP


class BaseShape(ABC):
    """The base shape that contains generic properties.

    Attributes:
        x: The x-axis of the shape position.
        y: The y-axis of the shape position.
        fill (Optional): The filling color of the shape. Default to None.
        stroke (Optional): The outline color of the shape. Default to None.
        stroke_weight (Optional): The outline width of the shape. Default to 1.0.
    """

    def __init__(
        self,
        x: PIndex,
        y: PIndex,
        *,
        fill: Optional[Color | ByteInt] = None,
        stroke: Optional[Color | ByteInt] = None,
        stroke_weight: Optional[int | float] = 1.0,
    ) -> None:
        """The constructor.
        Automatically render the shape by calling _render() after initialized
        the properties.

        Args:
            x: The x-axis of the shape position.
            y: The y-axis of the shape position.
            fill (Optional): The filling color of the shape. Default to None.
            stroke (Optional): The outline color of the shape. Default to None.
            stroke_weight (Optional): The outline width of the shape. Default to 1.
        """

        self.x: PIndex = x
        self.y: PIndex = y
        self.fill: Color | None = (
            Color.from_unit(fill) if isinstance(fill, int) else fill
        )
        self.stroke: Color | None = (
            Color.from_unit(stroke) if isinstance(stroke, int) else stroke
        )
        self.stroke_weight: float = float(stroke_weight)
        self._render()

    @abstractmethod
    def _render(self) -> None:
        """The abtract method to render the shape."""

        ...


class Line(BaseShape):
    """A line started from x to y coordinates.

    Attributes:
        x: The x-axis of the shape position.
        y: The y-axis of the shape position.
        dx: The x-axis of the shape end position.
        dy: The y-axis of the shape end position.
        stroke (Optional): The outline color of the shape. Default to None.
        stroke_weight (Optional): The outline width of the shape. Default to 1.0.
    """

    def __init__(
        self,
        x: PIndex,
        y: PIndex,
        dx: PIndex,
        dy: PIndex,
        *,
        stroke: Optional[Color | ByteInt] = None,
        stroke_weight: Optional[int | float] = 1,
    ) -> None:
        """The constructor.

        Args:
            x: The x-axis of the shape begin position.
            y: The y-axis of the shape begin position.
            dx: The x-axis of the shape end position.
            dy: The y-axis of the shape end position.
            stroke (Optional): The outline color of the shape. Default to None.
            stroke_weight (Optional): The outline width of the shape. Default to 1.0.
        """

        self.dx: PIndex = dx
        self.dy: PIndex = dy
        super().__init__(x, y, stroke=stroke, stroke_weight=stroke_weight)

    def _render(self) -> None:
        """Render the line to the window."""

        if self.stroke:
            _GLWrapper.color_4f(*self.stroke.ratios)
            _GLWrapper.line_width(self.stroke_weight)
            _GLWrapper.begin(GL_LINE_LOOP)
            _GLWrapper.vertex_2f(self.x, self.y)
            _GLWrapper.vertex_2f(self.dx, self.dy)
            _GLWrapper.end()

    @classmethod
    def outline(
        cls,
        vertices: list[Vertex],
        *,
        stroke: Color | ByteInt,
        stroke_weight: Optional[int | float] = 1,
    ) -> None:
        """Create an outile from the given vertices.

        Args:
            vertices: The list of x, y coordinates that define the line shape.
            stoke: The color of the outline.
            stroke_weight (Optional): The outline width. Default to 1.
        """

        for i in range(len(vertices)):
            cls(
                *vertices[i],
                *vertices[(i + 1) % len(vertices)],
                stroke=stroke,
                stroke_weight=stroke_weight,
            )


class Rect(BaseShape):
    """A rectangural shape.

    Attributes:
        x: The x-axis of the shape position.
        y: The y-axis of the shape position.
        width: The width of the shape.
        height: The height of the shape.
        fill (Optional): The filling color of the shape. Default to None.
        stroke (Optional): The outline color of the shape. Default to None.
        stroke_weight (Optional): The outline width of the shape. Default to 1.0.
    """

    def __init__(
        self,
        x: PIndex,
        y: PIndex,
        width: float,
        height: float,
        *,
        fill: Optional[Color | ByteInt] = None,
        stroke: Optional[Color | ByteInt] = None,
        stroke_weight: Optional[int | float] = 1.0,
    ) -> None:
        """The constructor.
        First initialize its own properties, then init its inherited shape.

        Args:
            x: The x-axis of the shape position.
            y: The y-axis of the shape position.
            width: The width of the shape.
            height: The height of the shape.
            fill (Optional): The filling color of the shape. Default to None.
            stroke (Optional): The outline color of the shape. Default to None.
            stroke_weight (Optional): The outline width of the shape. Default to 1.
        """

        self.width: float = width
        self.height: float = height
        super().__init__(x, y, fill=fill, stroke=stroke, stroke_weight=stroke_weight)

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

        if self.stroke:
            Line.outline(vertices, stroke=self.stroke, stroke_weight=self.stroke_weight)
