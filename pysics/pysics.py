from time import time
from typing import Final, Optional
import glfw
from pysics.types import ByteInt, Color, DrawCallback, Duration, Timestamp
from pysics._wrappers import (
    _GLWrapper,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_PROJECTION,
    GL_MODELVIEW,
    GL_BLEND,
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA,
)


class Canvas:
    """The window and render manager.

    Attributes:
        width: The window width.
        height: The windw height.
        background: The window background color. Default to 0.
    """

    _WINDOW_TITLE: Final[str] = "Sketch"

    def __init__(
        self, width: int, height: int, *, background: Optional[Color | ByteInt] = 0
    ) -> None:
        """The constructor that's also init the OpenGL components.

        Args:
            width: The window width.
            height: The window height.
            background (Optional): The window background color. Default to 0.
        """

        self._window: glfw._GLFWwindow | None = None
        self.width: int = width
        self.height: int = height
        self.background: Color = (
            Color.from_unit(background) if isinstance(background, int) else background
        )
        self._init_window()

    def _init_window(self) -> None:
        """Init the OpenGL components.
        Notice that the width and height are also updated to prevent
        diffrent types of pixels density (thanks Apple).

        Raises:
            RuntimeError: If any error occurs on the components initialization.
        """

        if not glfw.init():
            raise RuntimeError("Error on the OpenGL initialization.")

        self._window = glfw.create_window(
            self.width, self.height, self._WINDOW_TITLE, None, None
        )

        if not self._window:
            raise RuntimeError("Error on the window initialization.")

        self.width, self.height = glfw.get_framebuffer_size(self._window)
        glfw.make_context_current(self._window)
        _GLWrapper.enable(GL_BLEND)
        _GLWrapper.blend_func(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def _clear_window(self) -> None:
        """Reset the window state.
        Erase all the rendered pixels and updated the width and height dimensions.
        """

        self.width, self.height = glfw.get_framebuffer_size(self._window)
        _GLWrapper.clear_color(*self.background.ratios)
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

        glfw.swap_buffers(self._window)


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
        self, width: int, height: int, *, background: Optional[Color | ByteInt] = 0
    ) -> Canvas:
        """Create and returns a new canvas.

        Args:
            width: The canvas width.
            height: The canvas height.
            background (Optional): The canvas background color. Default to 0.

        Returns:
            Canvas: The created canvas.
        """

        self.canvas = Canvas(width, height, background=background)
        return self.canvas

    def run_loop(self, callback: DrawCallback) -> None:
        """Loop through the rendering process 'til the window close event is triggered.

        Notice that the window rendering is depending of:
            - The _loop attribute which must be True;
            - The timer that blocks the rendering during the time of the _delay.

        Also notice that the event listener is not blocked by these mechanisms.

        Args:
            callback: The drawing function which will be called at each iteration.

        Raises:
            RuntimeError: If the canvas is not initialized.
        """

        if not isinstance(self.canvas, Canvas):
            raise RuntimeError(
                "The canvas must be initialized. You should use the create_canvas() "
                "method or pass a canvas to the constructor instead."
            )

        self._loop = True
        self._reset_timer()

        while not glfw.window_should_close(self.canvas._window):
            if self._loop and self._time_elapsed():
                self.canvas._clear_window()
                callback()
                self.canvas._swap_buffers()
                self._reset_timer()

            glfw.poll_events()

        glfw.terminate()

    def no_loop(self) -> None:
        """Tell to the rendering loop to stop refreshing the window."""

        self._loop = False

    def wait(self, delay: Duration) -> None:
        """Tell to the rendeing loop to wait until the given duration.

        Args:
            delay: The duration to wait in seconds.
        """

        self._delay = delay

    def _reset_timer(self) -> None:
        """Reset the reference timestamp for the timer."""

        self._tref = time()

    def _time_elapsed(self) -> bool:
        """Check if the time is reached.

        Returns:
            bool: True if the time is exceeded, else False.
        """

        return time() - self._tref >= self._delay
