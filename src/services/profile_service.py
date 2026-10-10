from __future__ import annotations

import sys
from typing import Self, cast

from src.models.profile import ParsedProfile, validate_coins
from src.services.xml_types import SerializableXmlDocument, XmlDocument, XmlElement, XmlNode


class _XmlDocument:
    def __init__(self: Self, xml_content: str) -> None:
        if not isinstance(xml_content, str) or not xml_content.strip():
            raise ValueError("The profile must contain XML text.")
        if "<!DOCTYPE" in xml_content or "<!ENTITY" in xml_content:
            raise ValueError("XML entity declarations and DTDs are not supported.")
        self.browser = sys.platform == "brython"
        self.document: XmlDocument
        if self.browser:
            from browser import window

            self.document = cast(
                XmlDocument,
                window.DOMParser.new().parseFromString(xml_content, "application/xml"),
            )
            if self.document.getElementsByTagName("parsererror").length:
                raise ValueError("Invalid XML profile.")
        else:
            from xml.dom import minidom
            from xml.parsers.expat import ExpatError

            try:
                self.document = cast(XmlDocument, minidom.parseString(xml_content))
            except (ExpatError, ValueError) as error:
                raise ValueError("Invalid XML profile.") from error
        root = self.document.documentElement
        if root is None or root.tagName != "UserProfile":
            raise ValueError("Expected a Risk of Rain 2 UserProfile XML document.")
        self.root: XmlElement = root

    def serialize(self: Self) -> str:
        if self.browser:
            from browser import window

            return cast(str, window.XMLSerializer.new().serializeToString(self.document))
        return cast(SerializableXmlDocument, self.document).toxml()

    def ensure_child(self: Self, parent: XmlNode, name: str) -> XmlElement:
        child = _first_child(parent, name)
        if child is None:
            child = self.document.createElement(name)
            parent.appendChild(child)
        return child

    def set_text(self: Self, node: XmlNode, value: str) -> None:
        for child in _children(node):
            node.removeChild(child)
        node.appendChild(self.document.createTextNode(value))


def _children(node: XmlNode) -> list[XmlNode]:
    nodes = node.childNodes
    return [child for index in range(nodes.length) if (child := nodes.item(index)) is not None]


def _element_children(node: XmlNode, name: str) -> list[XmlElement]:
    elements = (cast(XmlElement, child) for child in _children(node) if child.nodeType == 1)
    return [element for element in elements if element.tagName == name]


def _first_child(node: XmlNode, name: str) -> XmlElement | None:
    children = _element_children(node, name)
    return children[0] if children else None


def _text(node: XmlNode | None) -> str:
    if node is None:
        return ""
    return "".join(
        (child.nodeValue or "") if child.nodeType in (3, 4) else _text(child)
        for child in _children(node)
        if child.nodeType in (1, 3, 4)
    )


def parse_profile(xml_content: str, file_name: str) -> ParsedProfile:
    xml = _XmlDocument(xml_content)
    coins_node = _first_child(xml.root, "coins")
    coins_text = _text(coins_node).strip() if coins_node is not None else "0"
    if not coins_text or any(char not in "0123456789" for char in coins_text):
        raise ValueError("The profile contains an invalid coin amount.")
    try:
        coins = validate_coins(int(coins_text))
    except ValueError as error:
        raise ValueError("The profile contains an invalid coin amount.") from error
    stats = _first_child(xml.root, "stats")
    unlocks: set[str] = set()
    if stats is not None:
        unlocks = {
            _text(node).strip()
            for node in _element_children(stats, "unlock")
            if _text(node).strip()
        }
    return ParsedProfile(
        file_name=file_name,
        display_name=_text(_first_child(xml.root, "name")) or "Unknown Profile",
        xml_content=xml_content,
        coins=coins,
        unlocked_achievements=set(_text(_first_child(xml.root, "achievementsList")).split()),
        unlocked_items=unlocks,
    )


def generate_xml(profile: ParsedProfile) -> str:
    validate_coins(profile.coins)
    xml = _XmlDocument(profile.xml_content)
    xml.set_text(xml.ensure_child(xml.root, "coins"), str(profile.coins))
    xml.set_text(
        xml.ensure_child(xml.root, "achievementsList"),
        " ".join(sorted(profile.unlocked_achievements)),
    )

    stats = xml.ensure_child(xml.root, "stats")
    present: set[str] = set()
    for node in _element_children(stats, "unlock"):
        unlock_id = _text(node).strip()
        if unlock_id in profile.unlocked_items and unlock_id not in present:
            present.add(unlock_id)
        else:
            stats.removeChild(node)
    for unlock_id in sorted(profile.unlocked_items - present):
        node = xml.document.createElement("unlock")
        xml.set_text(node, unlock_id)
        stats.appendChild(node)
    return xml.serialize()
