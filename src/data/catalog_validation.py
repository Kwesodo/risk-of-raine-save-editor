from collections.abc import Iterable, Mapping

from src.models.catalog import Achievement, Category, ContentPack, Survivor


def index_by_id[Entry: (ContentPack, Survivor, Achievement)](
    entries: Iterable[Entry], kind: str
) -> frozendict[str, Entry]:
    index: dict[str, Entry] = {}
    for entry in entries:
        if entry.id in index:
            raise ValueError(f"Duplicate {kind}: {entry.id}")
        index[entry.id] = entry
    return frozendict(index)


def validate_references(
    survivors: Mapping[str, Survivor], achievements: Mapping[str, Achievement]
) -> None:
    for achievement in achievements.values():
        if not isinstance(achievement.category, Category):
            raise ValueError(f"Invalid achievement category: {achievement.id}")
        if achievement.survivor_id is not None and achievement.survivor_id not in survivors:
            raise ValueError(f"Unknown achievement survivor: {achievement.survivor_id}")
        if achievement.category in {Category.SKILL, Category.SKIN} and not achievement.survivor_id:
            raise ValueError(f"Missing achievement survivor: {achievement.id}")

    for survivor in survivors.values():
        if not survivor.required_achievement:
            continue
        requirement = achievements.get(survivor.required_achievement)
        if requirement is None:
            raise ValueError(f"Unknown survivor achievement: {survivor.required_achievement}")
        if requirement.survivor_id != survivor.id:
            raise ValueError(
                f"Incorrect survivor achievement owner: {survivor.required_achievement}"
            )
        if not requirement.unlockable:
            raise ValueError(f"Missing survivor unlock token: {survivor.required_achievement}")
