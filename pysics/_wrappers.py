from typing import Final, TypeAlias
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
