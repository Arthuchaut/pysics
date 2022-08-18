from abc import ABC, abstractmethod
from math import cos, pi, sin
from typing import Optional
from pysics.types import Color, ByteInt, PIndex, Vertex
from pysics._wrappers import gl, GL_QUADS, GL_LINE_LOOP, GL_POLYGON


class BaseShape(ABC):
    """The base shape that contains generic properties.

    Attributes:
        x: The x-axis of the shape position.
        y: The y-axis of the shape position.
        fill (Optional): The filling color of the shape. Default to transparent.
        stroke (Optional): The outline color of the shape. Default to None.
        stroke_weight (Optional): The outline width of the shape. Default to 1.0.
    """

    def __init__(
        self,
        x: PIndex,
        y: PIndex,
        *,
        fill: Optional[Color | ByteInt] = Color(0, 0, 0, 0),
        stroke: Optional[Color | ByteInt] = None,
        stroke_weight: Optional[int | float] = 1.0,
    ) -> None:
        """The constructor.
        Automatically render the shape by calling _render() after initialized
        the properties.

        Args:
            x: The x-axis of the shape position.
            y: The y-axis of the shape position.
            fill (Optional): The filling color of the shape. Default to transparent.
            stroke (Optional): The outline color of the shape. Default to None.
            stroke_weight (Optional): The outline width of the shape. Default to 1.
        """

        self.x: PIndex = x
        self.y: PIndex = y
        self.fill: Color = fill
        self.stroke: Color | None = stroke
        self.stroke_weight: float = float(stroke_weight)

        if isinstance(fill, int):
            self.fill = Color.from_unit(fill)
        if isinstance(stroke, int):
            self.stroke = Color.from_unit(stroke)

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
        self.fill = None

    def _render(self) -> None:
        """Render the line to the window."""

        if self.stroke:
            gl.color_4f(*self.stroke.ratios)
            gl.line_width(self.stroke_weight)
            gl.begin(GL_LINE_LOOP)
            gl.vertex_2f(self.x, self.y)
            gl.vertex_2f(self.dx, self.dy)
            gl.end()

    @classmethod
    def outline(
        cls,
        vertices: list[Vertex],
        *,
        stroke: Color | ByteInt,
        stroke_weight: Optional[int | float] = 1.0,
    ) -> None:
        """Create an outile from the given vertices.

        Args:
            vertices: The list of x, y coordinates that define the line shape.
            stoke: The color of the outline.
            stroke_weight (Optional): The outline width. Default to 1.0.
        """

        if isinstance(stroke, int):
            stroke = Color.from_unit(stroke)

        gl.color_4f(*stroke.ratios)
        gl.line_width(stroke_weight)
        gl.begin(GL_LINE_LOOP)

        for vertex in vertices:
            gl.vertex_2f(*vertex)

        gl.end()


class Rect(BaseShape):
    """A rectangural shape.

    Attributes:
        x: The x-axis of the shape position.
        y: The y-axis of the shape position.
        width: The width of the shape.
        height: The height of the shape.
        fill (Optional): The filling color of the shape. Default to transparent.
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
        fill: Optional[Color | ByteInt] = Color(0, 0, 0, 0),
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
            fill (Optional): The filling color of the shape. Default to transparent.
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
            gl.color_4f(*self.fill.ratios)

        gl.begin(GL_POLYGON)

        for vertex in vertices:
            gl.vertex_2f(*vertex)

        gl.end()

        if self.stroke:
            Line.outline(vertices, stroke=self.stroke, stroke_weight=self.stroke_weight)


class Ellipse(BaseShape):
    """An ellipsis shape.

    Attributes:
        x: The x-axis of the shape position (begin at the center of the circle).
        y: The y-axis of the shape position (begin at the center of the circle).
        rx: The x-axis of the radius position.
        ry: The y-acis of the radius position.
        segments (Optional): The number of segments that composes the circle.
            Higher is the value smoother is the shape. Default to 50.
        fill (Optional): The filling color of the shape. Default to transparent.
        stroke (Optional): The outline color of the shape. Default to None.
        stroke_weight (Optional): The outline width of the shape. Default to 1.0.
    """

    def __init__(
        self,
        x: PIndex,
        y: PIndex,
        rx: float,
        ry: float,
        *,
        segments: int = 50,
        fill: Optional[Color | ByteInt] = Color(0, 0, 0, 0),
        stroke: Optional[Color | ByteInt] = None,
        stroke_weight: Optional[int | float] = 1,
    ) -> None:
        """The constructor.

        Args:
            x: The x-axis of the shape position (begin at the center of the circle).
            y: The y-axis of the shape position (begin at the center of the circle).
            rx: The x-axis of the radius position.
            ry: The y-acis of the radius position.
            segments (Optional): The number of segments that composes the circle.
                Higher is the value smoother is the shape. Default to 50.
            fill (Optional): The filling color of the shape. Default to transparent.
            stroke (Optional): The outline color of the shape. Default to None.
            stroke_weight (Optional): The outline width of the shape. Default to 1.0.
        """

        self.rx: float = rx
        self.ry: float = ry
        self.segments: int = segments
        super().__init__(x, y, fill=fill, stroke=stroke, stroke_weight=stroke_weight)

    def _render(self) -> None:
        """Render the circle in the window.
        First compute and store all the vertices, then render the filled
        circle if a filling color exists and render the outline if a stroke
        color exists.
        """

        theta: float = 2 * pi / self.segments
        cos_t: float = cos(theta)
        sin_t: float = sin(theta)
        transform: float = 0.0
        cx: float = 1.0
        cy: float = 0.0
        vertices: list[Vertex] = []

        for _ in range(self.segments):
            vertices.append((cx * self.rx + self.x, cy * self.ry + self.y))
            transform = cx
            cx = cos_t * cx - sin_t * cy
            cy = sin_t * transform + cos_t * cy

        if self.fill and self.fill.a > 0:
            gl.color_4f(*self.fill.ratios)
            gl.begin(GL_POLYGON)

            for vertex in vertices:
                gl.vertex_2f(*vertex)

            gl.end()

        if self.stroke:
            Line.outline(vertices, stroke=self.stroke, stroke_weight=self.stroke_weight)


class Circle(Ellipse):
    """A circle shape.
    This class is a shortcut of Ellipse with a radius parameter instead of
    (rx, ry) coordinates.

    Attributes:
        x: The x-axis of the shape position (begin at the center of the circle).
        y: The y-axis of the shape position (begin at the center of the circle).
        rx: The x-axis of the radius position.
        ry: The y-acis of the radius position.
        segments (Optional): The number of segments that composes the circle.
            Higher is the value smoother is the shape. Default to 50.
        fill (Optional): The filling color of the shape. Default to transparent.
        stroke (Optional): The outline color of the shape. Default to None.
        stroke_weight (Optional): The outline width of the shape. Default to 1.0.
    """

    def __init__(
        self,
        x: PIndex,
        y: PIndex,
        radius: float,
        *,
        segments: int = 50,
        fill: Optional[Color | ByteInt] = Color(0, 0, 0, 0),
        stroke: Optional[Color | ByteInt] = None,
        stroke_weight: Optional[int | float] = 1,
    ) -> None:
        """The constructor.

        Args:
            x: The x-axis of the shape position (begin at the center of the circle).
            y: The y-axis of the shape position (begin at the center of the circle).
            radius: The radius length.
            segments (Optional): The number of segments that composes the circle.
                Higher is the value smoother is the shape. Default to 50.
            fill (Optional): The filling color of the shape. Default to transparent.
            stroke (Optional): The outline color of the shape. Default to None.
            stroke_weight (Optional): The outline width of the shape. Default to 1.0.
        """

        super().__init__(
            x,
            y,
            radius,
            radius,
            segments=segments,
            fill=fill,
            stroke=stroke,
            stroke_weight=stroke_weight,
        )
