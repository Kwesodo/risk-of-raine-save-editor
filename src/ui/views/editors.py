from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from browser import document, html

from src.data.catalog import CATALOG
from src.models.catalog import Category, ContentPack
from src.models.profile import MAX_COINS
from src.services.editor_service import is_survivor_unlocked
from src.ui.components.cards import badge, button, inventory_status, portrait, toggle_card

if TYPE_CHECKING:
    from browser import DOMEvent, DOMNode

    from src.ui.browser_app import Editor


def achievement_handler(app: Editor, achievement_id: str) -> Callable[[DOMEvent], None]:
    def toggle(event: DOMEvent) -> None:
        app.toggle_achievement(achievement_id)

    return toggle


def inventory_group(
    pack: ContentPack,
    index: int,
    unlocked: int,
    total: int,
    *,
    available: bool = False,
) -> DOMNode:
    title_id = "pack-" + pack.id
    section = html.SECTION(
        Class="inventory-pack",
        **{"data-pack": pack.id, "aria-labelledby": title_id},
    )
    heading = html.HEADER(Class="pack-heading")
    heading.attach(html.SPAN(f"{index:02d}", Class="pack-index", **{"aria-hidden": "true"}))
    heading.attach(html.H2(pack.name, id=title_id, Class="pack-title"))
    state = "available" if available else "unlocked"
    heading.attach(html.SPAN(f"{unlocked:02d} / {total:02d} {state}", Class="pack-count"))
    section.attach(heading)
    return section


def render_survivors(app: Editor, target: DOMNode) -> None:
    profile = app.require_profile()
    toolbar = html.DIV(Class="inventory-toolbar")
    currency = html.DIV(Class="currency-control")
    label = html.LABEL("Lunar Coins", Class="field-label")
    label.attrs["for"] = "coins"
    currency.attach(label)
    row = html.DIV(Class="input-row")
    coins = html.INPUT(
        type="number",
        id="coins",
        min="0",
        max=str(MAX_COINS),
        step="1",
        value=str(profile.coins),
        inputmode="numeric",
    )
    coins.attrs["aria-describedby"] = "coin-help"
    coins.bind("input", app.input_coins)
    coins.bind("change", app.change_coins)
    row.attach(coins)
    row.attach(
        button("Set max", app.max_coins, element_id="max-coins", class_name="button secondary")
    )
    currency.attach(row)
    currency.attach(html.P("Max: 2,147,483,647", id="coin-help", Class="field-help"))
    toolbar.attach(currency)
    unlock = button(
        "Unlock everything",
        app.unlock_everything,
        element_id="unlock-all",
        class_name="button unlock-action",
    )
    unlock.title = "Unlock all catalog survivors, skills, skins, items and artifacts."
    toolbar.attach(unlock)
    target.attach(toolbar)
    groups = html.DIV(Class="inventory-groups")
    for pack_index, pack in enumerate(CATALOG.packs, start=1):
        if not pack.survivors:
            continue
        count = sum(is_survivor_unlocked(profile, survivor.id) for survivor in pack.survivors)
        section = inventory_group(pack, pack_index, count, len(pack.survivors), available=True)
        columns = html.DIV(Class="inventory-columns", **{"aria-hidden": "true"})
        for label_text in ("Survivor", "Notes", "State"):
            columns.attach(html.SPAN(label_text))
        section.attach(columns)
        for index, survivor in enumerate(pack.survivors, start=1):
            unlocked = is_survivor_unlocked(profile, survivor.id)
            default = not survivor.required_achievement

            def toggle_survivor(event: DOMEvent, survivor_id: str = survivor.id) -> None:
                app.toggle_survivor(survivor_id)

            card = button(
                "",
                toggle_survivor,
                element_id="survivor-" + survivor.id,
                class_name="survivor-row inventory-row" + (" is-unlocked" if unlocked else ""),
            )
            card.disabled = default
            card.attrs["aria-pressed"] = str(unlocked).lower()
            card.attrs["aria-label"] = survivor.name + (
                ", available by default" if default else ", unlocked" if unlocked else ", locked"
            )
            identity = html.SPAN(Class="inventory-identity")
            identity.attach(
                html.SPAN(f"{index:02d}", Class="item-number", **{"aria-hidden": "true"})
            )
            identity.attach(portrait(survivor, unlocked=unlocked))
            identity.attach(html.SPAN(survivor.name, Class="card-title"))
            card.attach(identity)
            card.attach(html.SPAN(survivor.description, Class="card-description"))
            card.attach(inventory_status(unlocked, default=default))
            section.attach(card)
        groups.attach(section)
    target.attach(groups)


def render_loadout(app: Editor, target: DOMNode) -> None:
    profile = app.require_profile()
    groups = html.DIV(Class="inventory-groups")
    for pack_index, pack in enumerate(CATALOG.packs, start=1):
        content = [
            item for item in pack.achievements if item.category in {Category.SKILL, Category.SKIN}
        ]
        if not content:
            continue
        count = sum(item.id in profile.unlocked_achievements for item in content)
        section = inventory_group(pack, pack_index, count, len(content))
        for survivor in CATALOG.survivors:
            items = [item for item in content if item.survivor_id == survivor.id]
            if not items:
                continue
            row = html.DIV(Class="loadout-row")
            identity = html.DIV(Class="loadout-identity")
            unlocked = is_survivor_unlocked(profile, survivor.id)
            identity.attach(portrait(survivor, unlocked=unlocked))
            details = html.DIV()
            details.attach(html.H3(survivor.name))
            count = sum(item.id in profile.unlocked_achievements for item in items)
            details.attach(
                html.SPAN(f"{count:02d} / {len(items):02d} unlocked", Class="loadout-count")
            )
            if not unlocked:
                details.attach(badge("Survivor locked", "muted"))
            identity.attach(details)
            row.attach(identity)
            slots = html.DIV(Class="loadout-slots")
            for category, label in ((Category.SKILL, "Skills"), (Category.SKIN, "Skins")):
                choices = [item for item in items if item.category == category]
                if not choices:
                    continue
                group = html.DIV(Class="slot-group")
                group.attach(html.SPAN(label, Class="slot-label"))
                options = html.DIV(Class="slot-options")
                for item in choices:
                    options.attach(
                        toggle_card(
                            item,
                            item.id in profile.unlocked_achievements,
                            achievement_handler(app, item.id),
                            compact=True,
                        )
                    )
                group.attach(options)
                slots.attach(group)
            row.attach(slots)
            section.attach(row)
        groups.attach(section)
    target.attach(groups)


def render_achievement_packs(
    app: Editor,
    target: DOMNode,
    categories: set[Category],
    *,
    query: str = "",
) -> int:
    profile = app.require_profile()
    total = 0
    for pack_index, pack in enumerate(CATALOG.packs, start=1):
        items = [
            item
            for item in pack.achievements
            if item.category in categories
            and (
                not query
                or any(query in value.lower() for value in (item.name, item.description, item.id))
            )
        ]
        if not items:
            continue
        count = sum(item.id in profile.unlocked_achievements for item in items)
        section = inventory_group(pack, pack_index, count, len(items))
        for item in items:
            section.attach(
                toggle_card(
                    item,
                    item.id in profile.unlocked_achievements,
                    achievement_handler(app, item.id),
                    artifact=item.category == Category.ARTIFACT,
                )
            )
        target.attach(section)
        total += len(items)
    return total


def render_artifacts(app: Editor, target: DOMNode) -> None:
    groups = html.DIV(Class="inventory-groups")
    render_achievement_packs(app, groups, {Category.ARTIFACT})
    target.attach(groups)


def render_achievements(app: Editor, target: DOMNode) -> None:
    controls = html.DIV(Class="search-controls")
    field = html.DIV(Class="search-field")
    label = html.LABEL("Search achievements", Class="field-label")
    label.attrs["for"] = "achievement-search"
    field.attach(label)
    search = html.INPUT(
        id="achievement-search",
        type="search",
        value=app.search,
        placeholder="Search by name, description or ID…",
        autocomplete="off",
    )
    search.attrs["aria-controls"] = "achievement-results"
    search.bind("input", app.search_achievements)
    field.attach(search)
    controls.attach(field)
    summary = html.DIV(Class="search-summary")
    summary.attach(html.SPAN("RESULTS", Class="eyebrow"))
    counter = html.P(id="achievement-count", Class="field-help")
    counter.attrs["aria-live"] = "polite"
    summary.attach(counter)
    controls.attach(summary)
    target.attach(controls)
    target.attach(html.DIV(id="achievement-results", Class="inventory-groups achievement-list"))
    render_achievement_results(app)


def render_achievement_results(app: Editor) -> None:
    target = document["achievement-results"]
    target.clear()
    query = app.search.strip().lower()
    count = render_achievement_packs(app, target, {Category.ITEM, Category.CHALLENGE}, query=query)
    count_label = "matches" if query else "achievements"
    document["achievement-count"].text = f"{count:02d} {count_label}"
    if not count:
        target.attach(html.P("No achievements match your search.", Class="empty-state"))


RENDERERS: dict[str, Callable[[Editor, DOMNode], None]] = {
    "survivors": render_survivors,
    "loadout": render_loadout,
    "artifacts": render_artifacts,
    "achievements": render_achievements,
}
