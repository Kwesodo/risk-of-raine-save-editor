from typing import Protocol, Self

from . import DOMNode

class _ElementConstructor(Protocol):
    def __call__(
        self: Self,
        content: DOMNode | str = ...,
        /,
        **attributes: str | int | float | bool,
    ) -> DOMNode: ...

A: _ElementConstructor
BUTTON: _ElementConstructor
CODE: _ElementConstructor
DIV: _ElementConstructor
FOOTER: _ElementConstructor
H1: _ElementConstructor
H2: _ElementConstructor
H3: _ElementConstructor
HEADER: _ElementConstructor
INPUT: _ElementConstructor
LABEL: _ElementConstructor
MAIN: _ElementConstructor
NAV: _ElementConstructor
P: _ElementConstructor
SECTION: _ElementConstructor
SPAN: _ElementConstructor
