from typing import Any, Callable
import pytest
from glfw.GLFW import *
from OpenGL.GL import *
from pysics._wrappers import _GLWrapper, _GLFWWrapper


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


@pytest.mark.unit
class TestGLFWWrapper:
    def test_attrs(self) -> None:
        attr_mapping: dict[str, Callable[..., Any]] = dict(
            init=glfwInit,
            create_window=glfwCreateWindow,
            get_frame_buffer_size=glfwGetFramebufferSize,
            make_context_current=glfwMakeContextCurrent,
            swap_buffers=glfwSwapBuffers,
            window_should_close=glfwWindowShouldClose,
            poll_events=glfwPollEvents,
            terminate=glfwTerminate,
        )

        for attr_name, exp_value in attr_mapping.items():
            assert getattr(_GLFWWrapper, attr_name) == exp_value
