from __future__ import annotations

from typing import Protocol, Self


class XmlNodeList(Protocol):
    @property
    def length(self: Self) -> int: ...

    def item(self: Self, index: int) -> XmlNode | None: ...


class XmlNode(Protocol):
    @property
    def nodeType(self: Self) -> int: ...

    @property
    def nodeValue(self: Self) -> str | None: ...

    @property
    def childNodes(self: Self) -> XmlNodeList: ...

    def appendChild(self: Self, node: XmlNode) -> XmlNode: ...

    def removeChild(self: Self, node: XmlNode) -> XmlNode: ...


class XmlElement(XmlNode, Protocol):
    @property
    def tagName(self: Self) -> str: ...


class XmlDocument(Protocol):
    @property
    def documentElement(self: Self) -> XmlElement | None: ...

    def createElement(self: Self, name: str) -> XmlElement: ...

    def createTextNode(self: Self, value: str) -> XmlNode: ...

    def getElementsByTagName(self: Self, name: str) -> XmlNodeList: ...


class SerializableXmlDocument(XmlDocument, Protocol):
    def toxml(self: Self) -> str: ...
