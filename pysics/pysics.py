from typing import Optional
import glfw
from pysics.types import ByteInt, Color


class Canvas:
    def __init__(
        self, width: int, height: int, *, fill: Optional[Color | ByteInt] = None
    ) -> None:
        self._window: glfw._GLFWwindow | None = None
        self.width: int = width
        self.height: int = height
        self.fill: Color | None = (
            Color.from_unit(fill) if isinstance(fill, int) else fill
        )


class Pysics:
    def __init__(self, canvas: Optional[Canvas] = None) -> None:
        self._canvas: Canvas | None = canvas
        self._loop: bool = False
        self._delay: float = 0.0
