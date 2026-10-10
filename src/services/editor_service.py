from src.data.catalog import CATALOG
from src.models.catalog import Achievement
from src.models.profile import ParsedProfile, validate_coins


def set_coins(profile: ParsedProfile, value: int) -> None:
    profile.coins = validate_coins(value)


def toggle_achievement(profile: ParsedProfile, achievement_id: str) -> None:
    if (
        not isinstance(achievement_id, str)
        or not achievement_id
        or any(char.isspace() for char in achievement_id)
    ):
        raise ValueError("An achievement ID must be one nonempty token.")
    _set_achievement(profile, achievement_id, achievement_id not in profile.unlocked_achievements)


def _set_achievement(profile: ParsedProfile, achievement_id: str, unlocked: bool) -> None:
    unlockable = CATALOG.achievement_unlocks.get(achievement_id)
    if unlocked:
        profile.unlocked_achievements.add(achievement_id)
        if unlockable:
            profile.unlocked_items.add(unlockable)
    else:
        profile.unlocked_achievements.discard(achievement_id)
        if unlockable:
            profile.unlocked_items.discard(unlockable)


def survivor_content(survivor_id: str) -> tuple[Achievement, ...]:
    return CATALOG.survivor_content(survivor_id)


def is_survivor_unlocked(profile: ParsedProfile, survivor_id: str) -> bool:
    requirement = CATALOG.get_survivor(survivor_id).required_achievement
    return not requirement or requirement in profile.unlocked_achievements


def toggle_survivor(profile: ParsedProfile, survivor_id: str) -> None:
    survivor = CATALOG.get_survivor(survivor_id)
    requirement = survivor.required_achievement
    if not requirement:
        return
    content_ids = {item.id for item in survivor_content(survivor_id)}
    content_ids.add(requirement)
    unlocked = not is_survivor_unlocked(profile, survivor_id)
    for achievement_id in content_ids:
        _set_achievement(profile, achievement_id, unlocked)


def unlock_all(profile: ParsedProfile) -> None:
    profile.unlocked_achievements.update(CATALOG.achievement_ids)
    profile.unlocked_items.update(CATALOG.unlock_tokens)
