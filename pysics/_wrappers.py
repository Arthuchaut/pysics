from typing import Final, TypeAlias
from OpenGL.GL import *


class _GLWrapper:
    viewport: Final[TypeAlias] = glViewport
    matrix_mode: Final[TypeAlias] = glMatrixMode
    load_identity: Final[TypeAlias] = glLoadIdentity
    ortho: Final[TypeAlias] = glOrtho
    clear: Final[TypeAlias] = glClear
    clear_color: Final[TypeAlias] = glClearColor
    color_3f: Final[TypeAlias] = glColor3f
    color_4f: Final[TypeAlias] = glColor4f
    point_size: Final[TypeAlias] = glPointSize
    line_width: Final[TypeAlias] = glLineWidth
    begin: Final[TypeAlias] = glBegin
    end: Final[TypeAlias] = glEnd
    flush: Final[TypeAlias] = glFlush
    vertex_2f: Final[TypeAlias] = glVertex2f
    enable: Final[TypeAlias] = glEnable
    blend_func: Final[TypeAlias] = glBlendFunc
