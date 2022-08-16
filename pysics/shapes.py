from abc import ABC, abstractmethod
from typing import Optional
from pysics.types import Color, ByteInt, PIndex


class BaseShape(ABC):
    def __init__(
        self, x: PIndex, y: PIndex, *, fill: Optional[Color | ByteInt] = None
    ) -> None:
        self.x: PIndex = x
        self.y: PIndex = y
        self.fill: Color | None = (
            Color.from_unit(fill) if isinstance(fill, int) else fill
        )
        self._render()

    @abstractmethod
    def _render(self) -> None:
        ...
