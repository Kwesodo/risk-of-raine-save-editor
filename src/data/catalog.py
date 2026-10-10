from typing import Self

from src.data import (
    alloyed_collective,
    base_game,
    hallowed_concepts,
    seekers_of_the_storm,
    survivors_of_the_void,
)
from src.data.catalog_validation import index_by_id, validate_references
from src.models.catalog import Achievement, Category, ContentPack, Survivor


class GameCatalog:
    def __init__(self: Self, packs: tuple[ContentPack, ...]) -> None:
        self.packs = tuple(packs)
        self._packs_by_id = index_by_id(self.packs, "content pack")
        self._survivors_by_id = index_by_id((*pack.survivors for pack in self.packs), "survivor")
        self._achievements_by_id = index_by_id(
            (*pack.achievements for pack in self.packs), "achievement"
        )
        validate_references(self._survivors_by_id, self._achievements_by_id)
        self.survivors = tuple(self._survivors_by_id.values())
        self.achievements = tuple(self._achievements_by_id.values())
        self._achievement_unlocks: frozendict[str, str] = frozendict(
            (achievement.id, achievement.unlockable)
            for achievement in self.achievements
            if achievement.unlockable
        )
        self.achievement_ids = tuple(
            dict.fromkeys(
                [achievement.id for achievement in self.achievements]
                + [*pack.extra_achievement_ids for pack in self.packs]
            )
        )
        self.unlock_tokens = tuple(
            dict.fromkeys(
                list(self.achievement_unlocks.values())
                + [*pack.extra_unlock_tokens for pack in self.packs]
            )
        )
        self._content_by_survivor = self._index_loadouts()

    def _index_loadouts(self: Self) -> frozendict[str, tuple[Achievement, ...]]:
        content: dict[str, list[Achievement]] = {survivor.id: [] for survivor in self.survivors}
        for achievement in self.achievements:
            if (
                achievement.category in {Category.SKILL, Category.SKIN}
                and achievement.survivor_id is not None
            ):
                content[achievement.survivor_id].append(achievement)
        return frozendict((survivor_id, tuple(entries)) for survivor_id, entries in content.items())

    @property
    def achievement_unlocks(self: Self) -> frozendict[str, str]:
        return self._achievement_unlocks

    def get_pack(self: Self, pack_id: str) -> ContentPack:
        if pack_id not in self._packs_by_id:
            raise ValueError(f"Unknown content pack: {pack_id}")
        return self._packs_by_id[pack_id]

    def get_survivor(self: Self, survivor_id: str) -> Survivor:
        if survivor_id not in self._survivors_by_id:
            raise ValueError(f"Unknown survivor: {survivor_id}")
        return self._survivors_by_id[survivor_id]

    def get_achievement(self: Self, achievement_id: str) -> Achievement:
        if achievement_id not in self._achievements_by_id:
            raise ValueError(f"Unknown achievement: {achievement_id}")
        return self._achievements_by_id[achievement_id]

    def survivor_content(self: Self, survivor_id: str) -> tuple[Achievement, ...]:
        self.get_survivor(survivor_id)
        return self._content_by_survivor[survivor_id]


CATALOG = GameCatalog(
    (
        base_game.PACK,
        survivors_of_the_void.PACK,
        seekers_of_the_storm.PACK,
        alloyed_collective.PACK,
        hallowed_concepts.PACK,
    )
)
