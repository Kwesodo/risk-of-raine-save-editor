from dataclasses import dataclass
from enum import StrEnum


class Category(StrEnum):
    ITEM = "Item"
    CHALLENGE = "Challenge"
    ARTIFACT = "Artifact"
    SURVIVOR = "Survivor"
    SKILL = "Skill"
    SKIN = "Skin Unlock"


@dataclass(frozen=True)
class Survivor:
    id: str
    name: str
    description: str
    required_achievement: str | None = None
    dlc: str | None = None


@dataclass(frozen=True)
class Achievement:
    id: str
    name: str
    description: str
    category: Category
    survivor_id: str | None = None
    unlockable: str | None = None


@dataclass(frozen=True)
class ContentPack:
    id: str
    name: str
    survivors: tuple[Survivor, ...] = ()
    achievements: tuple[Achievement, ...] = ()
    extra_achievement_ids: tuple[str, ...] = ()
    extra_unlock_tokens: tuple[str, ...] = ()
