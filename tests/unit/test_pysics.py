from datetime import datetime
from time import time
from typing import Any, Callable, ClassVar
from unittest.mock import ANY, MagicMock
import pytest
from pytest_mock import MockerFixture
from freezegun import freeze_time
import glfw
from glfw.GLFW import GLFW_SAMPLES
from pysics.pysics import Pysics, Canvas
from pysics.types import Color
from pysics._wrappers import (
    gl,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_BLEND,
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_MULTISAMPLE,
)


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
                    background=(..., Color.from_unit(0)),
                ),
            ),
            (
                (200, 200),
                dict(background=255),
                dict(
                    _window=(..., None),
                    width=(..., 200),
                    height=(..., 200),
                    background=(..., Color.from_unit(255)),
                ),
            ),
            (
                (200, 200),
                dict(background=Color.from_unit(120)),
                dict(
                    _window=(..., None),
                    width=(..., 200),
                    height=(..., 200),
                    background=(..., Color.from_unit(120)),
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
        mocker.patch.object(glfw, "init", lambda: init_ret)
        glfw_init_spy: MagicMock = mocker.spy(glfw, "init")
        mocker.patch.object(glfw, "create_window", lambda *a, **k: crw_ret)
        glfw_crw_spy: MagicMock = mocker.spy(glfw, "create_window")
        mocker.patch.object(glfw, "get_framebuffer_size", lambda _: (400, 400))
        glfw_fsize_spy: MagicMock = mocker.spy(glfw, "get_framebuffer_size")
        glfw_ctx_mock: MagicMock = mocker.patch.object(glfw, "make_context_current")
        gl_enable_mock: MagicMock = mocker.patch.object(gl, "enable")
        gl_blend_mock: MagicMock = mocker.patch.object(gl, "blend_func")
        glfw_wh_mock: MagicMock = mocker.patch.object(glfw, "window_hint")
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
            gl_enable_mock.assert_called()
            glfw_wh_mock.assert_called_once_with(GLFW_SAMPLES, canvas._SAMPLES)
            gl_blend_mock.assert_called_once_with(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            assert isinstance(canvas._window, self._FakeWindow)
            assert canvas.width, canvas.height == (400, 400)

    def test_clear_window(self, mocker: MockerFixture) -> None:
        mocker.patch.object(Canvas, "_init_window")
        mocker.patch.object(glfw, "get_framebuffer_size", lambda _: (400, 400))
        glfw_fsize_spy: MagicMock = mocker.spy(glfw, "get_framebuffer_size")
        gl_clearc_mock: MagicMock = mocker.patch.object(gl, "clear_color")
        gl_viewport_mock: MagicMock = mocker.patch.object(gl, "viewport")
        gl_matrix_mock: MagicMock = mocker.patch.object(gl, "matrix_mode")
        gl_load_mock: MagicMock = mocker.patch.object(gl, "load_identity")
        gl_ortho_mock: MagicMock = mocker.patch.object(gl, "ortho")
        gl_clear_mock: MagicMock = mocker.patch.object(gl, "clear")
        canvas: Canvas = Canvas(200, 200)
        canvas._clear_window()
        glfw_fsize_spy.assert_called_once_with(canvas._window)
        gl_clearc_mock.assert_called_once_with(*canvas.background.ratios)
        gl_viewport_mock.assert_called_once_with(0, 0, canvas.width, canvas.height)
        gl_matrix_mock.call_count == 2
        gl_load_mock.call_count == 3
        gl_ortho_mock.assert_called_once_with(0, canvas.width, 0, canvas.height, 0, 1)
        gl_clear_mock.assert_called_once_with(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        assert canvas.width, canvas.height == (400, 400)

    def test_swap_buffers(self, mocker: MockerFixture) -> None:
        mocker.patch.object(Canvas, "_init_window")
        glfw_swap_mock: MagicMock = mocker.patch.object(glfw, "swap_buffers")
        canvas: Canvas = Canvas(200, 200)
        canvas._swap_buffers()
        glfw_swap_mock.assert_called_once_with(canvas._window)


@pytest.mark.unit
class TestPysics:
    _LOOP_ITERATION: ClassVar[int] = 0
    _CALLBACK_ITERATION: ClassVar[int] = 0

    class _FakeCanvas:
        ...

    @pytest.mark.parametrize(
        "args, expected",
        [
            (
                (),
                dict(
                    canvas=(..., None),
                    _loop=(..., False),
                    _delay=(..., 0.0),
                    _tref=(..., None),
                ),
            ),
            (
                (_FakeCanvas(),),
                dict(
                    canvas=(_FakeCanvas, ...),
                    _loop=(..., False),
                    _delay=(..., 0.0),
                    _tref=(..., None),
                ),
            ),
        ],
    )
    def test_init(
        self, args: Any, expected: dict[str, Any], assert_getattr: Callable[..., None]
    ) -> None:
        engine: Pysics = Pysics(*args)
        assert_getattr(engine, expected)

    @pytest.mark.parametrize(
        "args, kwargs, exp_args, exp_kwargs",
        [
            (
                (200, 200),
                dict(),
                (200, 200),
                dict(background=0),
            ),
            (
                (200, 200),
                dict(background=255),
                (200, 200),
                dict(background=255),
            ),
            (
                (200, 200),
                dict(background=Color.from_unit(120)),
                (200, 200),
                dict(background=Color.from_unit(120)),
            ),
        ],
    )
    def test_create_canvas(
        self,
        args: Any,
        kwargs: Any,
        exp_args: Any,
        exp_kwargs: Any,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch.object(Canvas, "_init_window")
        canvas_spy: MagicMock = mocker.spy(Canvas, "__init__")
        engine: Pysics = Pysics()
        canvas: Canvas = engine.create_canvas(*args, **kwargs)
        canvas_spy.assert_called_once_with(ANY, *exp_args, **exp_kwargs)
        assert isinstance(canvas, Canvas)
        assert engine.canvas == canvas

    @freeze_time(datetime.now())
    def test_reset_timer(self) -> None:
        engine: Pysics = Pysics()
        freezed_ts: float = time()
        assert engine._tref is None
        engine._reset_timer()
        assert engine._tref == freezed_ts

    @freeze_time(datetime.fromtimestamp(1660681241.0), auto_tick_seconds=5)
    @pytest.mark.parametrize(
        "delay, expected",
        [
            (6, False),
            (5.1, False),
            (5, True),
            (4.9, True),
            (2, True),
            (0, True),
        ],
    )
    def test_time_elapsed(self, delay: float, expected: bool) -> None:
        engine: Pysics = Pysics()
        engine._delay = delay
        engine._reset_timer()
        assert engine._time_elapsed() == expected

    @pytest.mark.parametrize(
        "with_canvas, loop_iterations, loop_stop, throwable",
        [
            (True, 5, 5, None),
            (True, 5, 2, None),
            (False, 0, 0, RuntimeError),
        ],
    )
    def test_run_loop(
        self,
        with_canvas: bool,
        loop_iterations: int,
        loop_stop: int,
        throwable: type[RuntimeError] | None,
        mocker: MockerFixture,
    ) -> None:
        self._LOOP_ITERATION = 0
        self._CALLBACK_ITERATION = 0
        canvas: Canvas | None = None

        def fake_callback() -> None:
            self._CALLBACK_ITERATION += 1

            if self._CALLBACK_ITERATION >= loop_stop:
                engine._loop = False

        def poll_events_patch():
            self._LOOP_ITERATION += 1

        if with_canvas:
            mocker.patch.object(Canvas, "_init_window")
            clear_mock: MagicMock = mocker.patch.object(Canvas, "_clear_window")
            swap_mock: MagicMock = mocker.patch.object(Canvas, "_swap_buffers")
            canvas = Canvas(200, 200)

        mocker.patch.object(glfw, "poll_events", poll_events_patch)
        glfw_pe_spy: MagicMock = mocker.spy(glfw, "poll_events")
        glfw_term_mock: MagicMock = mocker.patch.object(glfw, "terminate")
        mocker.patch.object(
            glfw,
            "window_should_close",
            lambda _: self._LOOP_ITERATION >= loop_iterations,
        )
        engine: Pysics = Pysics(canvas)

        if throwable:
            with pytest.raises(throwable):
                engine.run_loop(fake_callback)
        else:
            engine.run_loop(fake_callback)
            clear_mock.call_count == loop_stop
            swap_mock.call_count == loop_stop
            glfw_pe_spy.call_count == loop_iterations
            glfw_term_mock.assert_called_once()
            assert self._CALLBACK_ITERATION == loop_stop
            assert self._LOOP_ITERATION == loop_iterations

    def test_no_loop(self) -> None:
        engine: Pysics = Pysics()
        engine._loop = True
        engine.no_loop()
        assert engine._loop == False

    def test_wait(self) -> None:
        engine: Pysics = Pysics()
        engine._delay = 0.0
        engine.wait(10)
        assert engine._delay == 10
