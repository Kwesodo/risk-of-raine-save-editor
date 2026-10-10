from typing import Protocol


class BrowserFile(Protocol):
    name: str
    size: int


class TextReaderResult(Protocol):
    result: str


class FileReadEvent(Protocol):
    target: TextReaderResult
