from typing import Final, TypeAlias
from glfw.GLFW import *
from OpenGL.GL import *


class _GLWrapper:
    viewport: Final[TypeAlias] = glViewport
    matrix_mode: Final[TypeAlias] = glMatrixMode
    load_identity: Final[TypeAlias] = glLoadIdentity
    ortho: Final[TypeAlias] = glOrtho
    clear: Final[TypeAlias] = glClear
    color_3f: Final[TypeAlias] = glColor3f
    color_4f: Final[TypeAlias] = glColor4f
    begin: Final[TypeAlias] = glBegin
    end: Final[TypeAlias] = glEnd
    vertex_2f: Final[TypeAlias] = glVertex2f


class _GLFWWrapper:
    init: Final[TypeAlias] = glfwInit
    create_window: Final[TypeAlias] = glfwCreateWindow
    get_frame_buffer_size: Final[TypeAlias] = glfwGetFramebufferSize
    make_context_current: Final[TypeAlias] = glfwMakeContextCurrent
    swap_buffers: Final[TypeAlias] = glfwSwapBuffers
    window_should_close: Final[TypeAlias] = glfwWindowShouldClose
    poll_events: Final[TypeAlias] = glfwPollEvents
    terminate: Final[TypeAlias] = glfwTerminate
