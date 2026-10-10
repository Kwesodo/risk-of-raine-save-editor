from __future__ import annotations

from typing import TYPE_CHECKING, Self

from browser import document, html, timer, window

from src.data.catalog import CATALOG
from src.models.catalog import Category
from src.models.profile import MAX_COINS, ParsedProfile
from src.services import editor_service
from src.services.profile_service import generate_xml, parse_profile
from src.ui.components.cards import button
from src.ui.views.editors import RENDERERS, render_achievement_results

if TYPE_CHECKING:
    from browser import DOMEvent, DOMNode

    from src.ui.browser_types import BrowserFile, FileReadEvent

type ProfileSnapshot = tuple[int, frozenset[str], frozenset[str]]

TABS: dict[str, tuple[str, str, str]] = {
    "survivors": ("Survivors", "Your roster, organized by expansion. Select a row to edit.", "◈"),
    "loadout": ("Loadout", "Skills and skins, grouped by the expansion that introduced them.", "ϟ"),
    "artifacts": ("Artifacts", "Unlock modifiers to choose from in the game lobby.", "⬡"),
    "achievements": ("Achievements", "Item unlocks and challenges across every expansion.", "◇"),
}

SAMPLE_XML: str = """<?xml version="1.0" encoding="utf-8"?>
<UserProfile>
  <name>RiskOfRain_Tester</name>
  <coins>1000</coins>
  <achievementsList>CommandoClearGameMonsoon HuntressClearGameMonsoon AttackSpeed MoveSpeed KillEliteMonster LoopOnce</achievementsList>
  <stats>
    <unlock>Characters.Commando</unlock>
    <unlock>Characters.Huntress</unlock>
    <unlock>Skins.Commando.Alt1</unlock>
    <unlock>Skins.Huntress.Alt1</unlock>
    <unlock>Items.Hoof</unlock>
    <unlock>Items.Syringe</unlock>
    <unlock>Items.CritGlasses</unlock>
  </stats>
</UserProfile>"""


def prevent_navigation(event: DOMEvent) -> None:
    event.preventDefault()


class Editor:
    def __init__(self: Self) -> None:
        self.profile: ParsedProfile | None = None
        self.saved_state: ProfileSnapshot | None = None
        self.active_tab = "survivors"
        self.search = ""
        self.pending_coins = False
        self.read_token = 0
        self.root: DOMNode = document["app"]
        document["profile-file"].bind("change", self.file_selected)
        document["dismiss-notice"].bind("click", self.dismiss_notice)
        window.bind("beforeunload", self.before_unload)
        document.bind("dragover", prevent_navigation)
        document.bind("drop", prevent_navigation)
        self.render_landing()

    def require_profile(self: Self) -> ParsedProfile:
        if self.profile is None:
            raise RuntimeError("No profile is loaded.")
        return self.profile

    def snapshot(self: Self) -> ProfileSnapshot | None:
        if self.profile is None:
            return None
        return (
            self.profile.coins,
            frozenset(self.profile.unlocked_achievements),
            frozenset(self.profile.unlocked_items),
        )

    @property
    def dirty(self: Self) -> bool:
        return self.pending_coins or self.snapshot() != self.saved_state

    def notify(self: Self, message: str, *, error: bool = False) -> None:
        notice = document["notice"]
        notice.attrs["class"] = "notice" + (" notice-error" if error else "")
        notice.hidden = False
        document["notice-message"].text = "" if error else message
        document["error-message"].text = message if error else ""

    def dismiss_notice(self: Self, event: DOMEvent | None = None) -> None:
        document["notice"].hidden = True
        document["notice-message"].text = ""
        document["error-message"].text = ""

    def confirm_discard(self: Self) -> bool:
        return not self.dirty or window.confirm(
            "You have unsaved changes. Continue without downloading them?"
        )

    def before_unload(self: Self, event: DOMEvent) -> None:
        if self.dirty:
            event.preventDefault()
            event.returnValue = ""

    def pick_file(self: Self, event: DOMEvent | None = None) -> None:
        document["profile-file"].click()

    def file_selected(self: Self, event: DOMEvent) -> None:
        if event.target.files.length:
            self.read_file(event.target.files[0])
        event.target.value = ""

    def read_file(self: Self, file: BrowserFile) -> None:
        if not file.name.lower().endswith(".xml"):
            self.notify("Please choose a .xml Risk of Rain 2 profile.", error=True)
            return
        if file.size > 1024 * 1024:
            self.notify(
                "The file is too large. Choose an XML profile no larger than 1 MB.", error=True
            )
            return
        if not self.confirm_discard():
            return
        self.read_token += 1
        token = self.read_token
        reader = window.FileReader.new()

        def loaded(event: FileReadEvent) -> None:
            if token == self.read_token:
                self.load_profile(event.target.result, file.name)

        def failed(event: DOMEvent) -> None:
            if token == self.read_token:
                self.notify("The file could not be read. Please choose it again.", error=True)

        reader.bind("load", loaded)
        reader.bind("error", failed)
        reader.readAsText(file)

    def drop_file(self: Self, event: DOMEvent) -> None:
        event.preventDefault()
        document["drop-zone"].classList.remove("is-dragging")
        if event.dataTransfer.files.length:
            self.read_file(event.dataTransfer.files[0])

    def drag_over(self: Self, event: DOMEvent) -> None:
        event.preventDefault()
        event.dataTransfer.dropEffect = "copy"
        document["drop-zone"].classList.add("is-dragging")

    def drag_leave(self: Self, event: DOMEvent) -> None:
        document["drop-zone"].classList.remove("is-dragging")

    def load_sample(self: Self, event: DOMEvent | None = None) -> None:
        if self.confirm_discard():
            self.read_token += 1
            self.load_profile(SAMPLE_XML, "sample_profile.xml")

    def load_profile(self: Self, xml_content: str, file_name: str) -> None:
        try:
            profile = parse_profile(xml_content, file_name)
        except (ValueError, TypeError) as error:
            self.notify(str(error), error=True)
            return
        self.profile = profile
        self.pending_coins = False
        self.saved_state = self.snapshot()
        self.active_tab = "survivors"
        self.search = ""
        self.render_editor()
        self.notify("Profile loaded. Your original file stays unchanged until you replace it.")

    def close_profile(self: Self, event: DOMEvent | None = None) -> None:
        if self.confirm_discard():
            self.read_token += 1
            self.profile = None
            self.pending_coins = False
            self.saved_state = None
            self.dismiss_notice()
            self.render_landing()

    def save_profile(self: Self, event: DOMEvent | None = None) -> None:
        if self.profile is None:
            return
        if self.pending_coins:
            self.notify("Enter a valid coin amount before downloading the profile.", error=True)
            return
        try:
            xml_content = generate_xml(self.profile)
            blob = window.Blob.new([xml_content], {"type": "application/xml;charset=utf-8"})
            url = window.URL.createObjectURL(blob)
            link = html.A(href=url, download=self.profile.file_name)
            link.style.display = "none"
            document.body.attach(link)
            link.click()
            link.remove()

            def release_url() -> None:
                window.URL.revokeObjectURL(url)

            timer.set_timeout(release_url, 10000)
        except Exception as error:
            self.notify("Could not prepare the download: " + str(error), error=True)
            return
        self.saved_state = self.snapshot()
        self.update_save_state()
        self.notify("XML download started. Replace the original profile when you are ready.")

    def input_coins(self: Self, event: DOMEvent) -> None:
        try:
            text = event.target.value.strip()
            if not text or not text.isdecimal():
                raise ValueError("Invalid coin amount.")
            editor_service.set_coins(self.require_profile(), int(text))
        except ValueError:
            self.pending_coins = True
        else:
            self.pending_coins = False
        self.update_save_state()

    def change_coins(self: Self, event: DOMEvent) -> None:
        try:
            text = event.target.value.strip()
            if not text or not text.isdecimal():
                raise ValueError("Enter a whole number from 0 to 2,147,483,647.")
            editor_service.set_coins(self.require_profile(), int(text))
        except ValueError as error:
            event.target.value = str(self.require_profile().coins)
            self.pending_coins = False
            self.update_save_state()
            self.notify(str(error), error=True)
            return
        self.pending_coins = False
        self.update_save_state()

    def max_coins(self: Self, event: DOMEvent | None = None) -> None:
        editor_service.set_coins(self.require_profile(), MAX_COINS)
        self.pending_coins = False
        document["coins"].value = str(MAX_COINS)
        self.update_save_state()

    def unlock_everything(self: Self, event: DOMEvent | None = None) -> None:
        editor_service.unlock_all(self.require_profile())
        self.refresh_content()
        self.notify("All catalog survivors, skills, skins, items and artifacts are unlocked.")

    def toggle_survivor(self: Self, survivor_id: str) -> None:
        editor_service.toggle_survivor(self.require_profile(), survivor_id)
        self.refresh_content()

    def toggle_achievement(self: Self, achievement_id: str) -> None:
        editor_service.toggle_achievement(self.require_profile(), achievement_id)
        self.refresh_content()

    def search_achievements(self: Self, event: DOMEvent) -> None:
        self.search = event.target.value
        render_achievement_results(self)

    def update_save_state(self: Self) -> None:
        state = document["save-state"]
        state.text = "Unsaved changes" if self.dirty else "No unsaved changes"
        state.attrs["class"] = "save-state" + (" is-dirty" if self.dirty else "")

    def select_tab(self: Self, tab: str) -> None:
        self.active_tab = tab
        for key in TABS:
            nav = document["tab-" + key]
            nav.attrs["class"] = "nav-button" + (" active" if key == tab else "")
            nav.attrs["aria-current"] = "page" if key == tab else "false"
        title, description, _ = TABS[tab]
        document["view-title"].text = title
        document["view-description"].text = description
        document["editor-main"].scrollTop = 0
        self.refresh_content()

    def refresh_content(self: Self) -> None:
        focused_id = document.activeElement.id
        target = document["editor-content"]
        target.clear()
        RENDERERS[self.active_tab](self, target)
        self.update_progress()
        self.update_save_state()
        if focused_id and focused_id in document:
            document[focused_id].focus({"preventScroll": True})

    def update_progress(self: Self) -> None:
        profile = self.require_profile()
        survivors = sum(
            editor_service.is_survivor_unlocked(profile, survivor.id)
            for survivor in CATALOG.survivors
        )
        metrics = [("survivors", survivors, len(CATALOG.survivors))]
        for key, categories in (
            ("loadout", {Category.SKILL, Category.SKIN}),
            ("artifacts", {Category.ARTIFACT}),
            ("achievements", {Category.ITEM, Category.CHALLENGE}),
        ):
            items = [item for item in CATALOG.achievements if item.category in categories]
            unlocked = sum(item.id in profile.unlocked_achievements for item in items)
            metrics.append((key, unlocked, len(items)))
        for key, count, total in metrics:
            document["nav-count-" + key].text = f"{count} / {total}"
            document["tab-" + key].title = f"{TABS[key][0]}: {count} of {total} unlocked"

    def render_landing(self: Self) -> None:
        self.root.clear()
        self.root.attrs["class"] = "landing"
        header = html.HEADER(Class="landing-header")
        header.attach(self.brand())
        status = html.DIV(Class="header-status")
        status.attach(html.SPAN(Class="status-dot", **{"aria-hidden": "true"}))
        status.attach(html.SPAN("LOCAL SAVE EDITOR"))
        header.attach(status)
        self.root.attach(header)
        main = html.MAIN(id="editor-main", Class="welcome", tabindex="-1")
        story = html.SECTION(Class="welcome-story")
        story.attach(html.P("PROFILE & UNLOCKS", Class="eyebrow"))
        title = html.H1("Risk of Rain 2 ")
        title.attach(html.SPAN("Save Editor", Class="hero-emphasis"))
        story.attach(title)
        story.attach(
            html.P(
                "Get your profile ready for another drop on Petrichor V. "
                "Unlock survivors, alternate skills, skins and artifacts, "
                "adjust your Lunar Coins, and download your updated save.",
                Class="welcome-description",
            )
        )
        facts = html.DIV(Class="landing-facts")
        for value, label in (
            (str(len(CATALOG.survivors)), "Survivors"),
            (str(len(CATALOG.packs) - 1), "Expansions"),
            ("100%", "Local editing"),
        ):
            fact = html.DIV(Class="landing-fact")
            fact.attach(html.SPAN(value, Class="metric-value"))
            fact.attach(html.SPAN(label, Class="metric-label"))
            facts.attach(fact)
        main.attach(story)
        import_panel = html.SECTION(Class="import-panel", **{"aria-label": "Open a profile"})
        panel_topline = html.DIV(Class="panel-topline")
        panel_topline.attach(html.SPAN("01 / OPEN PROFILE", Class="section-code"))
        panel_topline.attach(html.SPAN("XML SAVE FILE", Class="eyebrow"))
        import_panel.attach(panel_topline)
        drop = html.DIV(id="drop-zone", Class="drop-zone")
        drop.bind("dragover", self.drag_over)
        drop.bind("dragleave", self.drag_leave)
        drop.bind("drop", self.drop_file)
        drop.attach(html.SPAN("↥", Class="upload-symbol", **{"aria-hidden": "true"}))
        drop.attach(html.H2("Open your survivor profile"))
        drop.attach(html.P("Drop your XML profile here or browse your files.", Class="muted-text"))
        drop.attach(
            button(
                "Choose profile",
                self.pick_file,
                element_id="choose-profile",
                class_name="button primary",
            )
        )
        drop.attach(html.P("XML files · up to 1 MB", Class="field-help"))
        import_panel.attach(drop)
        utilities = html.DIV(Class="import-utilities")
        sample_row = html.P(Class="sample-row")
        sample_row.attach("Just exploring? ")
        sample_row.attach(
            button(
                "Try a sample profile →",
                self.load_sample,
                element_id="load-sample",
                class_name="text-button",
            )
        )
        utilities.attach(sample_row)
        location = html.DIV(Class="save-location")
        help_button = html.BUTTON(
            "Where do I find my save?",
            type="button",
            id="show-save-location",
            Class="save-location-trigger text-button",
            popovertarget="save-location-help",
            **{"aria-haspopup": "dialog"},
        )
        help_button.attach(html.SPAN("↗", Class="help-arrow", **{"aria-hidden": "true"}))
        location.attach(help_button)
        help_popover = html.DIV(
            id="save-location-help",
            Class="save-location-popover",
            popover="auto",
            role="dialog",
            **{"aria-labelledby": "save-location-title"},
        )
        help_heading = html.DIV(Class="save-location-heading")
        help_heading.attach(html.H2("Where do I find my save?", id="save-location-title"))
        help_heading.attach(
            html.BUTTON(
                "×",
                type="button",
                id="close-save-location",
                Class="close-help",
                popovertarget="save-location-help",
                popovertargetaction="hide",
                autofocus=True,
                **{"aria-label": "Close save location help"},
            )
        )
        help_popover.attach(help_heading)
        help_popover.attach(html.P("In your Steam folder, open:"))
        help_popover.attach(
            html.CODE(r"userdata\[Steam ID]\632360\remote\UserProfiles", Class="save-location-path")
        )
        help_popover.attach(
            html.P("Choose the XML file for your profile. Keep a backup before replacing it.")
        )
        location.attach(help_popover)
        utilities.attach(location)
        import_panel.attach(utilities)
        import_panel.attach(facts)
        main.attach(import_panel)
        workflow = html.DIV(Class="workflow-strip")
        for index, (title, description) in enumerate(
            (
                ("Open a profile", "Choose an XML save from your Steam folder."),
                ("Edit your inventory", "Manage survivors, loadouts and unlocks by expansion."),
                ("Download your save", "Export the XML and replace your original profile."),
            ),
            start=1,
        ):
            step = html.DIV(Class="workflow-step")
            step.attach(html.SPAN(f"0{index}", Class="step-number"))
            copy = html.DIV()
            copy.attach(html.SPAN(title, Class="step-title"))
            copy.attach(html.P(description, Class="step-description"))
            step.attach(copy)
            workflow.attach(step)
        main.attach(workflow)
        self.root.attach(main)
        footer = html.FOOTER(Class="landing-footer")
        footer.attach(html.SPAN("Your save stays on your device. Nothing is uploaded."))
        footer.attach(html.SPAN("UNOFFICIAL COMMUNITY TOOL"))
        self.root.attach(footer)

    def brand(self: Self) -> DOMNode:
        brand = html.DIV(Class="brand")
        brand.attach(html.SPAN("ϟ", Class="brand-mark", **{"aria-hidden": "true"}))
        text = html.SPAN(Class="brand-text")
        text.attach(html.SPAN("RoR2", Class="brand-game"))
        text.attach(html.SPAN("Save Editor", Class="brand-name"))
        brand.attach(text)
        return brand

    def render_editor(self: Self) -> None:
        profile = self.require_profile()
        self.root.clear()
        self.root.attrs["class"] = "editor-shell"
        topbar = html.HEADER(Class="editor-topbar")
        topbar_inner = html.DIV(Class="editor-topbar-inner")
        topbar_inner.attach(self.brand())
        identity = html.DIV(Class="profile-identity")
        identity.attach(
            html.P(profile.display_name, Class="profile-name", title=profile.display_name)
        )
        identity.attach(html.P(profile.file_name, Class="profile-file", title=profile.file_name))
        topbar_inner.attach(identity)
        actions = html.DIV(Class="file-actions")
        actions.attach(
            button(
                "Open another", self.pick_file, element_id="open-profile", class_name="text-button"
            )
        )
        actions.attach(
            button(
                "Close file",
                self.close_profile,
                element_id="close-profile",
                class_name="text-button close-button",
            )
        )
        topbar_inner.attach(actions)
        topbar.attach(topbar_inner)
        self.root.attach(topbar)
        nav = html.NAV(Class="editor-nav")
        nav.attrs["aria-label"] = "Profile sections"
        nav_inner = html.DIV(Class="editor-nav-inner")
        for key, (title, _, icon) in TABS.items():

            def select(event: DOMEvent, tab: str = key) -> None:
                self.select_tab(tab)

            item = button(
                "",
                select,
                element_id="tab-" + key,
                class_name="nav-button",
            )
            item.attach(html.SPAN(icon, Class="nav-icon", **{"aria-hidden": "true"}))
            item.attach(html.SPAN(title, Class="nav-title"))
            item.attach(html.SPAN(id="nav-count-" + key, Class="nav-count"))
            nav_inner.attach(item)
        nav.attach(nav_inner)
        self.root.attach(nav)
        main = html.MAIN(id="editor-main", Class="editor-main", tabindex="-1")
        inner = html.DIV(Class="editor-inner")
        top = html.HEADER(Class="view-header")
        heading = html.DIV(Class="view-heading")
        heading.attach(html.P("PROFILE INVENTORY", Class="eyebrow"))
        heading.attach(html.H1(id="view-title"))
        heading.attach(html.P(id="view-description", Class="muted-text"))
        top.attach(heading)
        session = html.DIV(Class="session-badge")
        session.attach(html.SPAN(Class="status-dot", **{"aria-hidden": "true"}))
        session.attach(html.SPAN("LOCAL SESSION"))
        top.attach(session)
        inner.attach(top)
        inner.attach(html.DIV(id="editor-content"))
        main.attach(inner)
        self.root.attach(main)
        download = html.DIV(
            Class="download-dock", role="region", **{"aria-label": "Download edited profile"}
        )
        save_state = html.P(id="save-state", Class="save-state")
        save_state.attrs["aria-live"] = "polite"
        download.attach(save_state)
        download.attach(
            button(
                "↓  Download XML",
                self.save_profile,
                element_id="save-profile",
                class_name="button save-button",
            )
        )
        self.root.attach(download)
        self.select_tab(self.active_tab)


def start() -> Editor:
    return Editor()
