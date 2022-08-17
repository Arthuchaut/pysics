from abc import ABC
from typing import Any, Callable
from unittest.mock import MagicMock
import pytest
from pytest_mock import MockerFixture
from pysics.types import Color, Vertex
from pysics._wrappers import _GLWrapper, GL_QUADS
from pysics.shapes import BaseShape, Rect


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
            ((10, 20), dict(), dict(x=(..., 10), y=(..., 20), fill=(..., None))),
            (
                (10, 20),
                dict(fill=255),
                dict(x=(..., 10), y=(..., 20), fill=(..., Color.from_unit(255))),
            ),
            (
                (10, 20),
                dict(fill=Color.from_unit(0)),
                dict(x=(..., 10), y=(..., 20), fill=(..., Color.from_unit(0))),
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
                    fill=(..., None),
                ),
            ),
            (
                (10, 20, 50, 60),
                dict(fill=255),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    width=(..., 50),
                    height=(..., 60),
                    fill=(..., Color.from_unit(255)),
                ),
            ),
            (
                (10, 20, 50, 60),
                dict(fill=Color.from_unit(0)),
                dict(
                    x=(..., 10),
                    y=(..., 20),
                    width=(..., 50),
                    height=(..., 60),
                    fill=(..., Color.from_unit(0)),
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
        "bg",
        [
            (None),
            (Color.from_unit(150)),
        ],
    )
    def test_render(self, bg: Color | None, mocker: MockerFixture) -> None:
        gl_color_mock: MagicMock = mocker.patch.object(_GLWrapper, "color_4f")
        gl_begin_mock: MagicMock = mocker.patch.object(_GLWrapper, "begin")
        gl_end_mock: MagicMock = mocker.patch.object(_GLWrapper, "end")
        draw_vertices_mock: MagicMock = mocker.patch.object(Rect, "_draw_vertices")
        vertices: list[Vertex] = [(10, 20), (50, 20), (50, 70), (10, 70)]
        initial_state: Any = Rect._render
        mocker.patch.object(Rect, "_render")
        shape: Rect = Rect(10, 20, 40, 50, fill=bg)
        shape._render = lambda: initial_state(shape)
        shape._render()
        gl_begin_mock.assert_called_once_with(GL_QUADS)
        gl_end_mock.assert_called_once()
        draw_vertices_mock.call_count == 4

        if bg:
            gl_color_mock.assert_called_once_with(*bg.ratios)
        else:
            gl_color_mock.assert_not_called()

    def test_draw_vertices(self, mocker: MockerFixture) -> None:
        mocker.patch.object(Rect, "_render")
        gl_vertex_mock: MagicMock = mocker.patch.object(_GLWrapper, "vertex_2f")
        shape: Rect = Rect(10, 20, 40, 50)
        vertices: list[Vertex] = [(10, 20), (50, 20), (50, 70), (10, 70)]
        shape._draw_vertices(vertices)

        for vertex, exp_args in zip(vertices, gl_vertex_mock.call_args_list):
            assert vertex == exp_args.args
