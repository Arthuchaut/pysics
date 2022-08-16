from time import time
from typing import Final, Optional
import glfw
from pysics.types import ByteInt, Color, Duration, Timestamp
from pysics._wrappers import (
    _GLFWWrapper,
    _GLWrapper,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_PROJECTION,
    GL_MODELVIEW,
)


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

    def _clear_window(self) -> None:
        """Reset the window state.
        Erase all the rendered pixels and updated the width and height dimensions.
        """

        self.width, self.height = _GLFWWrapper.get_frame_buffer_size(self._window)
        _GLWrapper.clear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        _GLWrapper.load_identity()
        _GLWrapper.viewport(0, 0, self.width, self.height)
        _GLWrapper.matrix_mode(GL_PROJECTION)
        _GLWrapper.load_identity()
        _GLWrapper.ortho(0, self.width, 0, self.height, 0, 1)
        _GLWrapper.matrix_mode(GL_MODELVIEW)
        _GLWrapper.load_identity()

    def _swap_buffers(self) -> None:
        """Swap the window buffers."""

        _GLFWWrapper.swap_buffers(self._window)


class Pysics:
    """The main manager that's handle the render and events loops.

    Attributes:
        canvas: The window. If no canvas is given in the constructor, we
            have to call the create_canvas() method to create it.
    """

    def __init__(self, canvas: Optional[Canvas] = None) -> None:
        """The constructor.

        Args:
            canvas (Optional): The canvas to manage. Default to None.
                If None, we need to call the create_canvas() method instead.
        """

        self.canvas: Canvas | None = canvas
        self._loop: bool = False
        self._delay: Duration = 0.0
        self._tref: Timestamp | None = None

    def create_canvas(
        self, width: int, height: int, *, fill: Optional[Color | ByteInt] = None
    ) -> Canvas:
        """Create and returns a new canvas.

        Args:
            width: The canvas width.
            height: The canvas height.
            fill (Optional): The canvas background. Default to None.

        Returns:
            Canvas: The created canvas.
        """

        self.canvas = Canvas(width, height, fill=fill)
        return self.canvas

    def _reset_timer(self) -> None:
        """Reset the reference timestamp for the timer."""

        self._tref = time()

    def _time_elapsed(self) -> bool:
        """Check if the time is reached.

        Returns:
            bool: True if the time is exceeded, else False.
        """

        return time() - self._tref >= self._delay
