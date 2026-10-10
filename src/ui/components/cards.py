from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from browser import html

from src.models.catalog import Achievement, Survivor

if TYPE_CHECKING:
    from browser import DOMEvent, DOMNode


def button(
    label: str,
    callback: Callable[[DOMEvent], None],
    *,
    element_id: str | None = None,
    class_name: str = "button",
) -> DOMNode:
    node = html.BUTTON(label, type="button", Class=class_name)
    if element_id:
        node.id = element_id
    node.bind("click", callback)
    return node


def portrait(survivor: Survivor, *, unlocked: bool = True) -> DOMNode:
    initials = "".join(word[0] for word in survivor.name.split()[:2])
    frame = html.SPAN(
        initials,
        Class="portrait" + ("" if unlocked else " portrait-locked"),
    )
    frame.attrs["aria-hidden"] = "true"
    return frame


def badge(label: str, class_name: str = "") -> DOMNode:
    return html.SPAN(label, Class="badge " + class_name)


def card_state(unlocked: bool, *, default: bool = False) -> DOMNode:
    label = "Always available" if default else "Unlocked" if unlocked else "Locked"
    state = html.SPAN(Class="card-state" + (" is-available" if unlocked else ""))
    indicator = html.SPAN(Class="state-indicator")
    indicator.attrs["aria-hidden"] = "true"
    state.attach(indicator)
    state.attach(label)
    return state


def inventory_status(unlocked: bool, *, default: bool = False) -> DOMNode:
    status = html.SPAN(Class="inventory-status")
    status.attach(card_state(unlocked, default=default))
    status.attach(html.SPAN(Class="toggle-switch", **{"aria-hidden": "true"}))
    return status


def toggle_card(
    item: Achievement,
    unlocked: bool,
    callback: Callable[[DOMEvent], None],
    *,
    compact: bool = False,
    artifact: bool = False,
) -> DOMNode:
    name = item.name
    if compact and ":" in name:
        name = name.split(":", 1)[1].strip()
    class_name = "toggle-card compact-card" if compact else "inventory-row toggle-card"
    if artifact:
        class_name += " artifact-row"
    if unlocked:
        class_name += " is-unlocked"
    node = button(
        "",
        callback,
        element_id="achievement-" + item.id,
        class_name=class_name,
    )
    node.attrs["aria-pressed"] = str(unlocked).lower()
    node.attrs["aria-label"] = item.name + (", unlocked" if unlocked else ", locked")
    node.title = item.description
    marker = html.SPAN("✓" if unlocked else "+", Class="toggle-marker")
    marker.attrs["aria-hidden"] = "true"
    node.attach(marker)
    details = html.SPAN(Class="toggle-details")
    details.attach(html.SPAN(name, Class="card-title"))
    if not compact:
        details.attach(html.SPAN(item.description, Class="card-description"))
    else:
        details.attach(html.SPAN("Unlocked" if unlocked else "Locked", Class="compact-status"))
    node.attach(details)
    if not compact:
        node.attach(inventory_status(unlocked))
    return node
