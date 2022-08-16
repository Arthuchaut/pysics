from typing import Final, Optional
import glfw
from pysics.types import ByteInt, Color
from pysics._wrappers import _GLFWWrapper


class Canvas:
    """The window and render manager.

    Attributes:
        width: The window width.
        height: The windw height.
        fill: The window bacckground. Default to None (transparent).
    """

    _WINDOW_TITLE: Final[str] = "Sketch"

    def __init__(
        self, width: int, height: int, *, fill: Optional[Color | ByteInt] = None
    ) -> None:
        """The constructor that's also init the OpenGL components.

        Args:
            width: The window width.
            height: The window height.
            fill (Optional): The window background. Default to None.
        """

        self._window: glfw._GLFWwindow | None = None
        self.width: int = width
        self.height: int = height
        self.fill: Color | None = (
            Color.from_unit(fill) if isinstance(fill, int) else fill
        )
        self._init_window()

    def _init_window(self) -> None:
        """Init the OpenGL components.
        Notice that the width and height are also updated to prevent
        diffrent types of pixels density (thanks Apple).

        Raises:
            RuntimeError: If any error occurs on the components initialization.
        """

        if not _GLFWWrapper.init():
            raise RuntimeError("Error on the OpenGL initialization.")

        self._window = _GLFWWrapper.create_window(
            self.width, self.height, self._WINDOW_TITLE, None, None
        )

        if not self._window:
            raise RuntimeError("Error on the window initialization.")

        self.width, self.height = _GLFWWrapper.get_frame_buffer_size(self._window)
        _GLFWWrapper.make_context_current(self._window)


class Pysics:
    """The main manager that's handle the render and events loops."""

    def __init__(self, canvas: Optional[Canvas] = None) -> None:
        """The constructor.

        Args:
            canvas (Optional): The canvas to manage. Default to None.
                If None, we need to call the create_canvas() method instead.
        """

        self._canvas: Canvas | None = canvas
        self._loop: bool = False
        self._delay: float = 0.0
