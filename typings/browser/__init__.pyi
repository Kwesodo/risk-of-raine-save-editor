from collections.abc import Callable, Mapping, MutableMapping, Sequence
from typing import Literal, Protocol, Self, overload

from src.services.xml_types import XmlDocument
from src.ui.browser_types import BrowserFile, FileReadEvent

from . import html as html
from . import timer as timer

class _FileList(Protocol):
    @property
    def length(self: Self) -> int: ...
    def __getitem__(self: Self, index: int) -> BrowserFile: ...

class _DataTransfer(Protocol):
    files: _FileList
    dropEffect: str

class _Style(Protocol):
    display: str

class _ClassList(Protocol):
    def add(self: Self, *tokens: str) -> None: ...
    def remove(self: Self, *tokens: str) -> None: ...

class DOMNode:
    id: str
    text: str
    title: str
    value: str
    hidden: bool
    disabled: bool
    scrollTop: float
    attrs: MutableMapping[str, str]
    files: _FileList
    style: _Style
    classList: _ClassList
    def __le__(self: Self, child: DOMNode | str) -> Self: ...
    def attach(self: Self, child: DOMNode | str) -> Self: ...
    def bind(self: Self, event: str, callback: Callable[[DOMEvent], None]) -> Self: ...
    def clear(self: Self) -> None: ...
    def click(self: Self) -> None: ...
    def remove(self: Self) -> None: ...
    def focus(self: Self, options: Mapping[str, bool] | None = ...) -> None: ...

class DOMEvent:
    target: DOMNode
    dataTransfer: _DataTransfer
    returnValue: str
    def preventDefault(self: Self) -> None: ...

class _Document(DOMNode):
    body: DOMNode
    activeElement: DOMNode
    def __getitem__(self: Self, element_id: str) -> DOMNode: ...
    def __contains__(self: Self, element_id: str) -> bool: ...

class _Constructor[T](Protocol):
    def new(self: Self) -> T: ...

class _FileReader(Protocol):
    @overload
    def bind(
        self: Self, event: Literal["load"], callback: Callable[[FileReadEvent], None]
    ) -> None: ...
    @overload
    def bind(self: Self, event: Literal["error"], callback: Callable[[DOMEvent], None]) -> None: ...
    def readAsText(self: Self, file: BrowserFile) -> None: ...

class _Blob(Protocol):
    @property
    def size(self: Self) -> int: ...
    @property
    def type(self: Self) -> str: ...

class _BlobConstructor(Protocol):
    def new(self: Self, parts: Sequence[str], options: Mapping[str, str]) -> _Blob: ...

class _URL(Protocol):
    def createObjectURL(self: Self, blob: _Blob) -> str: ...
    def revokeObjectURL(self: Self, url: str) -> None: ...

class _DOMParser(Protocol):
    def parseFromString(self: Self, source: str, mime_type: str) -> XmlDocument: ...

class _XMLSerializer(Protocol):
    def serializeToString(self: Self, document: XmlDocument) -> str: ...

class _Window(Protocol):
    FileReader: _Constructor[_FileReader]
    Blob: _BlobConstructor
    URL: _URL
    DOMParser: _Constructor[_DOMParser]
    XMLSerializer: _Constructor[_XMLSerializer]
    def bind(self: Self, event: str, callback: Callable[[DOMEvent], None]) -> None: ...
    def confirm(self: Self, message: str) -> bool: ...

document: _Document
window: _Window
