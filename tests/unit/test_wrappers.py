from typing import Any, Callable
import pytest
from OpenGL.GL import *
from pysics._wrappers import gl


@pytest.mark.unit
class TestGLWrapper:
    def test_attrs(self) -> None:
        attr_mapping: dict[str, Callable[..., Any]] = dict(
            viewport=glViewport,
            matrix_mode=glMatrixMode,
            load_identity=glLoadIdentity,
            ortho=glOrtho,
            clear=glClear,
            color_3f=glColor3f,
            color_4f=glColor4f,
            point_size=glPointSize,
            line_width=glLineWidth,
            begin=glBegin,
            end=glEnd,
            flush=glFlush,
            vertex_2f=glVertex2f,
            enable=glEnable,
            blend_func=glBlendFunc,
        )

        for attr_name, exp_value in attr_mapping.items():
            assert getattr(gl, attr_name) == exp_value
