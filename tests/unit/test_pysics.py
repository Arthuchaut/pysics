from typing import Any, Callable
from unittest.mock import MagicMock
import pytest
import glfw
from pytest_mock import MockerFixture
from pysics.pysics import Pysics, Canvas
from pysics.types import Color
from pysics import _wrappers
from pysics._wrappers import _GLFWWrapper, _GLWrapper


@pytest.mark.unit
class TestCanvas:
    class _FakeWindow:
        ...

    @pytest.mark.parametrize(
        "args, kwargs, expected",
        [
            (
                (200, 200),
                dict(),
                dict(
                    _window=(..., None),
                    width=(..., 200),
                    height=(..., 200),
                    fill=(..., None),
                ),
            ),
            (
                (200, 200),
                dict(fill=255),
                dict(
                    _window=(..., None),
                    width=(..., 200),
                    height=(..., 200),
                    fill=(..., Color.from_unit(255)),
                ),
            ),
            (
                (200, 200),
                dict(fill=Color.from_unit(0)),
                dict(
                    _window=(..., None),
                    width=(..., 200),
                    height=(..., 200),
                    fill=(..., Color.from_unit(0)),
                ),
            ),
        ],
    )
    def test_init(
        self,
        args: Any,
        kwargs: Any,
        expected: dict[str, Any],
        assert_getattr: Callable[..., None],
        mocker: MockerFixture,
    ) -> None:
        init_window_mock: MagicMock = mocker.patch.object(Canvas, "_init_window")
        canvas: Canvas = Canvas(*args, **kwargs)
        assert_getattr(canvas, expected)
        init_window_mock.assert_called_once()

    @pytest.mark.parametrize(
        "init_ret, crw_ret, throwable",
        [
            (1, _FakeWindow(), None),
            (0, _FakeWindow(), RuntimeError),
            (1, None, RuntimeError),
        ],
    )
    def test_init_window(
        self,
        init_ret: int,
        crw_ret: _FakeWindow | None,
        throwable: type[RuntimeError] | None,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch.object(_GLFWWrapper, "init", lambda: init_ret)
        glfw_init_spy: MagicMock = mocker.spy(_GLFWWrapper, "init")
        mocker.patch.object(_GLFWWrapper, "create_window", lambda *a, **k: crw_ret)
        glfw_crw_spy: MagicMock = mocker.spy(_GLFWWrapper, "create_window")
        mocker.patch.object(_GLFWWrapper, "get_frame_buffer_size", lambda _: (400, 400))
        glfw_fsize_spy: MagicMock = mocker.spy(_GLFWWrapper, "get_frame_buffer_size")
        glfw_ctx_mock: MagicMock = mocker.patch.object(
            _GLFWWrapper, "make_context_current"
        )
        initial_state: Any = Canvas._init_window
        mocker.patch.object(Canvas, "_init_window")
        canvas: Canvas = Canvas(200, 200)
        canvas._init_window = lambda: initial_state(canvas)
        assert canvas._window is None

        if throwable:
            with pytest.raises(throwable):
                canvas._init_window()
        else:
            canvas._init_window()
            glfw_init_spy.assert_called_once()
            glfw_crw_spy.assert_called_once_with(
                200, 200, canvas._WINDOW_TITLE, None, None
            )
            glfw_fsize_spy.assert_called_once()
            glfw_ctx_mock.assert_called_once()
            assert isinstance(canvas._window, self._FakeWindow)
            assert canvas.width, canvas.height == (400, 400)

    def test_clear_window(self, mocker: MockerFixture) -> None:
        mocker.patch.object(Canvas, "_init_window")
        mocker.patch.object(_GLFWWrapper, "get_frame_buffer_size", lambda _: (400, 400))
        glfw_fsize_spy: MagicMock = mocker.spy(_GLFWWrapper, "get_frame_buffer_size")
        gl_viewport_mock: MagicMock = mocker.patch.object(_GLWrapper, "viewport")
        gl_matrix_mock: MagicMock = mocker.patch.object(_GLWrapper, "matrix_mode")
        gl_load_mock: MagicMock = mocker.patch.object(_GLWrapper, "load_identity")
        gl_ortho_mock: MagicMock = mocker.patch.object(_GLWrapper, "ortho")
        gl_clear_mock: MagicMock = mocker.patch.object(_GLWrapper, "clear")
        canvas: Canvas = Canvas(200, 200)
        canvas._clear_window()
        glfw_fsize_spy.assert_called_once_with(canvas._window)
        gl_viewport_mock.assert_called_once_with(0, 0, canvas.width, canvas.height)
        gl_matrix_mock.call_count == 2
        gl_load_mock.call_count == 3
        gl_ortho_mock.assert_called_once_with(0, canvas.width, 0, canvas.height, 0, 1)
        gl_clear_mock.assert_called_once_with(
            _wrappers.GL_COLOR_BUFFER_BIT | _wrappers.GL_DEPTH_BUFFER_BIT
        )
        assert canvas.width, canvas.height == (400, 400)


@pytest.mark.unit
class TestPysics:
    class _FakeCanvas:
        ...

    @pytest.mark.parametrize(
        "args, expected",
        [
            (
                (),
                dict(_canvas=(..., None), _loop=(..., False), _delay=(..., 0.0)),
            ),
            (
                (_FakeCanvas(),),
                dict(_canvas=(_FakeCanvas, ...), _loop=(..., False), _delay=(..., 0.0)),
            ),
        ],
    )
    def test_init(
        self, args: Any, expected: dict[str, Any], assert_getattr: Callable[..., None]
    ) -> None:
        engine: Pysics = Pysics(*args)
        assert_getattr(engine, expected)
