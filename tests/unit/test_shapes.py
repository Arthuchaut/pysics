from abc import ABC
from typing import Any, Callable
from unittest.mock import MagicMock
import pytest
from pytest_mock import MockerFixture
from pysics.types import Color, Vertex
from pysics._wrappers import gl, GL_QUADS, GL_LINE_LOOP, GL_POLYGON
from pysics.shapes import BaseShape, Circle, Ellipse, Line, Rect


@pytest.mark.unit
class TestBaseShape:
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture) -> None:
        mocker.patch.object(BaseShape, "__abstractmethods__", set())

    def test_inheritance(self) -> None:
        assert issubclass(BaseShape, ABC)

    @pytest.mark.parametrize(
        "args, kwargs, expected",
        [
            (
                (10, 20),
                dict(),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    fill=(..., Color(0, 0, 0, 0)),
                    stroke=(..., None),
                    stroke_weight=(..., 1.0),
                ),
            ),
            (
                (10, 20),
                dict(fill=255, stroke=100, stroke_weight=5),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    fill=(..., Color.from_unit(255)),
                    stroke=(..., Color.from_unit(100)),
                    stroke_weight=(..., 5.0),
                ),
            ),
            (
                (10, 20),
                dict(fill=Color.from_unit(0), stroke=Color.from_unit(100)),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    fill=(..., Color.from_unit(0)),
                    stroke=(..., Color.from_unit(100)),
                    stroke_weight=(..., 1.0),
                ),
            ),
        ],
    )
    def test_init(
        self,
        args: Any,
        kwargs: Any,
        expected: dict[str, tuple[type[Any], Any]],
        assert_getattr: Callable[..., None],
    ) -> None:
        shape: BaseShape = BaseShape(*args, **kwargs)
        assert_getattr(shape, expected)

    def test_abstract_methods(self) -> None:
        methods: list[Callable[..., Any]] = [BaseShape._render]

        for method in methods:
            assert method.__dict__.get("__isabstractmethod__")


@pytest.mark.unit
class TestRect:
    def test_inheritance(self) -> None:
        assert issubclass(Rect, BaseShape)

    @pytest.mark.parametrize(
        "args, kwargs, expected",
        [
            (
                (10, 20, 50, 60),
                dict(),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    width=(..., 50),
                    height=(..., 60),
                    fill=(..., Color(0, 0, 0, 0)),
                    stroke=(..., None),
                    stroke_weight=(..., 1.0),
                ),
            ),
            (
                (10, 20, 50, 60),
                dict(fill=255, stroke=100, stroke_weight=5),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    width=(..., 50),
                    height=(..., 60),
                    fill=(..., Color.from_unit(255)),
                    stroke=(..., Color.from_unit(100)),
                    stroke_weight=(..., 5.0),
                ),
            ),
            (
                (10, 20, 50, 60),
                dict(fill=Color.from_unit(0), stroke=Color.from_unit(100)),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    width=(..., 50),
                    height=(..., 60),
                    fill=(..., Color.from_unit(0)),
                    stroke=(..., Color.from_unit(100)),
                    stroke_weight=(..., 1.0),
                ),
            ),
        ],
    )
    def test_init(
        self,
        args: Any,
        kwargs: Any,
        expected: dict[str, tuple[type[Any], Any]],
        assert_getattr: Callable[..., None],
        mocker: MockerFixture,
    ) -> None:
        render_mock: MagicMock = mocker.patch.object(Rect, "_render")
        shape: Rect = Rect(*args, **kwargs)
        assert_getattr(shape, expected)
        render_mock.assert_called_once()

    @pytest.mark.parametrize(
        "bg, stroke",
        [
            (None, None),
            (Color.from_unit(0), Color.from_unit(0)),
        ],
    )
    def test_render(
        self, bg: Color | None, stroke: Color | None, mocker: MockerFixture
    ) -> None:
        gl_color_mock: MagicMock = mocker.patch.object(gl, "color_4f")
        gl_begin_mock: MagicMock = mocker.patch.object(gl, "begin")
        gl_end_mock: MagicMock = mocker.patch.object(gl, "end")
        gl_vertex_mock: MagicMock = mocker.patch.object(gl, "vertex_2f")
        outline_mock: MagicMock = mocker.patch.object(Line, "outline")
        vertices: list[Vertex] = [(10, 20), (50, 20), (50, 70), (10, 70)]
        initial_state: Any = Rect._render
        mocker.patch.object(Rect, "_render")
        shape: Rect = Rect(10, 20, 40, 50, fill=bg, stroke=stroke)
        shape._render = lambda: initial_state(shape)
        shape._render()

        if stroke:
            outline_mock.assert_called_once_with(
                vertices, stroke=shape.stroke, stroke_weight=shape.stroke_weight
            )

        gl_begin_mock.assert_called_once_with(GL_POLYGON)
        gl_end_mock.assert_called_once()

        for vertex, exp_args in zip(vertices, gl_vertex_mock.call_args_list):
            assert vertex == exp_args.args

        if bg:
            gl_color_mock.assert_called()
        else:
            gl_color_mock.assert_not_called()


@pytest.mark.unit
class TestLine:
    def test_inheritance(self) -> None:
        assert issubclass(Line, BaseShape)

    @pytest.mark.parametrize(
        "args, kwargs, expected",
        [
            (
                (10, 20, 40, 50),
                dict(),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    dx=(..., 40),
                    dy=(..., 50),
                    fill=(..., None),
                    stroke=(..., None),
                    stroke_weight=(..., 1.0),
                ),
            ),
            (
                (10, 20, 40, 50),
                dict(stroke=100, stroke_weight=5),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    dx=(..., 40),
                    dy=(..., 50),
                    fill=(..., None),
                    stroke=(..., Color.from_unit(100)),
                    stroke_weight=(..., 5.0),
                ),
            ),
            (
                (10, 20, 40, 50),
                dict(stroke=Color.from_unit(100)),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    dx=(..., 40),
                    dy=(..., 50),
                    fill=(..., None),
                    stroke=(..., Color.from_unit(100)),
                    stroke_weight=(..., 1.0),
                ),
            ),
        ],
    )
    def test_init(
        self,
        args: Any,
        kwargs: Any,
        expected: dict[str, tuple[type[Any], Any]],
        assert_getattr: Callable[..., None],
        mocker: MockerFixture,
    ) -> None:
        render_mock: MagicMock = mocker.patch.object(Line, "_render")
        shape: Line = Line(*args, **kwargs)
        assert_getattr(shape, expected)
        render_mock.assert_called_once()

    @pytest.mark.parametrize(
        "stroke",
        [
            (None),
            (Color.from_unit(0)),
        ],
    )
    def test_render(self, stroke: Color | None, mocker: MockerFixture) -> None:
        gl_color_mock: MagicMock = mocker.patch.object(gl, "color_4f")
        gl_begin_mock: MagicMock = mocker.patch.object(gl, "begin")
        gl_end_mock: MagicMock = mocker.patch.object(gl, "end")
        gl_vertex_mock: MagicMock = mocker.patch.object(gl, "vertex_2f")
        gl_lw_mock: MagicMock = mocker.patch.object(gl, "line_width")
        vertices: list[Vertex] = [(10, 20), (40, 50)]
        initial_state: Any = Line._render
        mocker.patch.object(Line, "_render")
        shape: Line = Line(10, 20, 40, 50, stroke=stroke)
        shape._render = lambda: initial_state(shape)
        shape._render()

        if stroke:
            gl_color_mock.assert_called_once_with(*shape.stroke.ratios)
            gl_begin_mock.assert_called_once_with(GL_LINE_LOOP)
            gl_lw_mock.assert_called_once_with(shape.stroke_weight)
            gl_end_mock.assert_called_once()

            for vertex, exp_args in zip(vertices, gl_vertex_mock.call_args_list):
                assert vertex == exp_args.args
        else:
            gl_color_mock.assert_not_called()
            gl_begin_mock.assert_not_called()
            gl_vertex_mock.assert_not_called()
            gl_lw_mock.assert_not_called()
            gl_end_mock.assert_not_called()

    def test_outline(self, mocker: MockerFixture) -> None:
        gl_color_mock: MagicMock = mocker.patch.object(gl, "color_4f")
        gl_begin_mock: MagicMock = mocker.patch.object(gl, "begin")
        gl_end_mock: MagicMock = mocker.patch.object(gl, "end")
        gl_vertex_mock: MagicMock = mocker.patch.object(gl, "vertex_2f")
        gl_lw_mock: MagicMock = mocker.patch.object(gl, "line_width")
        vertices: list[Vertex] = [(0, 0), (1, 0), (1, 1), (0, 1)]
        stroke: Color = 1
        stroke_weight: int = 1.0
        Line.outline(vertices, stroke=stroke, stroke_weight=stroke_weight)

        for vertex, exp_args in zip(vertices, gl_vertex_mock.call_args_list):
            assert vertex == exp_args.args

        gl_color_mock.assert_called_once_with(*Color.from_unit(stroke).ratios)
        gl_begin_mock.assert_called_once_with(GL_LINE_LOOP)
        gl_end_mock.assert_called_once()
        gl_lw_mock.assert_called_once_with(stroke_weight)


@pytest.mark.unit
class TestEllipse:
    def test_inheritance(self) -> None:
        assert issubclass(Ellipse, BaseShape)

    @pytest.mark.parametrize(
        "args, kwargs, expected",
        [
            (
                (10, 20, 40, 50),
                dict(),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    rx=(..., 40),
                    ry=(..., 50),
                    segments=(..., 50),
                    fill=(..., Color(0, 0, 0, 0)),
                    stroke=(..., None),
                    stroke_weight=(..., 1.0),
                ),
            ),
            (
                (10, 20, 40, 50),
                dict(fill=100, stroke=100, stroke_weight=5),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    rx=(..., 40),
                    ry=(..., 50),
                    segments=(..., 50),
                    fill=(..., Color.from_unit(100)),
                    stroke=(..., Color.from_unit(100)),
                    stroke_weight=(..., 5.0),
                ),
            ),
            (
                (10, 20, 40, 50),
                dict(fill=Color.from_unit(100), stroke=Color.from_unit(100)),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    rx=(..., 40),
                    ry=(..., 50),
                    segments=(..., 50),
                    fill=(..., Color.from_unit(100)),
                    stroke=(..., Color.from_unit(100)),
                    stroke_weight=(..., 1.0),
                ),
            ),
        ],
    )
    def test_init(
        self,
        args: Any,
        kwargs: Any,
        expected: dict[str, tuple[type[Any], Any]],
        assert_getattr: Callable[..., None],
        mocker: MockerFixture,
    ) -> None:
        render_mock: MagicMock = mocker.patch.object(Ellipse, "_render")
        shape: Ellipse = Ellipse(*args, **kwargs)
        assert_getattr(shape, expected)
        render_mock.assert_called_once()

    @pytest.mark.parametrize(
        "fill, stroke",
        [
            (None, Color.from_unit(0)),
            (Color.from_unit(0), None),
        ],
    )
    def test_render(
        self, fill: Color | None, stroke: Color | None, mocker: MockerFixture
    ) -> None:
        gl_color_mock: MagicMock = mocker.patch.object(gl, "color_4f")
        gl_begin_mock: MagicMock = mocker.patch.object(gl, "begin")
        gl_end_mock: MagicMock = mocker.patch.object(gl, "end")
        gl_vertex_mock: MagicMock = mocker.patch.object(gl, "vertex_2f")
        outline_mock: MagicMock = mocker.patch.object(Line, "outline")
        initial_state: Any = Ellipse._render
        mocker.patch.object(Ellipse, "_render")
        shape: Ellipse = Ellipse(10, 20, 40, 50, fill=fill, stroke=stroke)
        shape._render = lambda: initial_state(shape)
        shape._render()

        if stroke:
            outline_mock.assert_called_once()

        if fill:
            gl_color_mock.assert_called_once_with(*fill.ratios)
            gl_begin_mock.assert_called_once_with(GL_POLYGON)
            gl_end_mock.assert_called_once()
            gl_vertex_mock.call_count == shape.segments


@pytest.mark.unit
class TestCircle:
    def test_inheritance(self) -> None:
        assert issubclass(Circle, Ellipse)

    @pytest.mark.parametrize(
        "args, kwargs, expected",
        [
            (
                (10, 20, 40),
                dict(),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    rx=(..., 40),
                    ry=(..., 40),
                    segments=(..., 50),
                    fill=(..., Color(0, 0, 0, 0)),
                    stroke=(..., None),
                    stroke_weight=(..., 1.0),
                ),
            ),
            (
                (10, 20, 50),
                dict(fill=100, stroke=100, stroke_weight=5),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    rx=(..., 50),
                    ry=(..., 50),
                    segments=(..., 50),
                    fill=(..., Color.from_unit(100)),
                    stroke=(..., Color.from_unit(100)),
                    stroke_weight=(..., 5.0),
                ),
            ),
            (
                (10, 20, 40),
                dict(fill=Color.from_unit(100), stroke=Color.from_unit(100)),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    rx=(..., 40),
                    ry=(..., 40),
                    segments=(..., 50),
                    fill=(..., Color.from_unit(100)),
                    stroke=(..., Color.from_unit(100)),
                    stroke_weight=(..., 1.0),
                ),
            ),
        ],
    )
    def test_init(
        self,
        args: Any,
        kwargs: Any,
        expected: dict[str, tuple[type[Any], Any]],
        assert_getattr: Callable[..., None],
        mocker: MockerFixture,
    ) -> None:
        render_mock: MagicMock = mocker.patch.object(Circle, "_render")
        shape: Circle = Circle(*args, **kwargs)
        assert_getattr(shape, expected)
        render_mock.assert_called_once()
