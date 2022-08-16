from typing import Any, Callable
import pytest
from OpenGL.GL import *
from pysics._wrappers import _GLWrapper


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
            begin=glBegin,
            end=glEnd,
            vertex_2f=glVertex2f,
        )

        for attr_name, exp_value in attr_mapping.items():
            assert getattr(_GLWrapper, attr_name) == exp_value
