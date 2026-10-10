from src.models.catalog import Achievement, Category, ContentPack, Survivor

SURVIVORS: tuple[Survivor, ...] = (
    Survivor(
        id="Railgunner",
        name="Railgunner",
        description="Long-range sniper (SotV DLC).",
    ),
    Survivor(
        id="VoidSurvivor",
        name="Void Fiend",
        description="Corrupted survivor (SotV DLC).",
        required_achievement="CompleteVoidEnding",
    ),
)

ACHIEVEMENTS: tuple[Achievement, ...] = (
    Achievement(
        id="RailgunnerConsecutiveWeakPoints",
        name="Railgunner: Marksman",
        description="Fire 30 consecutive sniper shots without missing a Weak Point.",
        category=Category.SKILL,
        survivor_id="Railgunner",
        unlockable="Skills.Railgunner.SecondaryAlt1",
    ),
    Achievement(
        id="RailgunnerDealMassiveDamage",
        name="Railgunner: Annihilator",
        description="Deal 1,000,000 damage in one shot.",
        category=Category.SKILL,
        survivor_id="Railgunner",
        unlockable="Skills.Railgunner.UtilityAlt1",
    ),
    Achievement(
        id="RailgunnerAirborneMultiKill",
        name="Railgunner: Trickshot",
        description="Get 3 kills with a single Supercharge shot while airborne.",
        category=Category.SKILL,
        survivor_id="Railgunner",
        unlockable="Skills.Railgunner.SpecialAlt1",
    ),
    Achievement(
        id="RailgunnerClearGameMonsoon",
        name="Mastery",
        description="Beat the game or obliterate on Monsoon.",
        category=Category.SKIN,
        survivor_id="Railgunner",
        unlockable="Skins.RailGunner.Alt1",
    ),
    Achievement(
        id="CompleteVoidEnding",
        name="Dragged Below",
        description="Unlock Void Fiend",
        category=Category.SURVIVOR,
        survivor_id="VoidSurvivor",
        unlockable="Characters.VoidSurvivor",
    ),
    Achievement(
        id="VoidSurvivorClearGameMonsoon",
        name="Mastery",
        description="Beat the game or obliterate on Monsoon.",
        category=Category.SKIN,
        survivor_id="VoidSurvivor",
        unlockable="Skins.VoidSurvivor.Alt1",
    ),
)

EXTRA_ACHIEVEMENT_IDS: tuple[str, ...] = ()

EXTRA_UNLOCK_TOKENS: tuple[str, ...] = (
    "Characters.Railgunner",
    "Items.DroneWeapons",
    "Items.PrimarySkillShuriken",
    "Items.FreeChest",
    "Items.MoveSpeedOnKill",
    "Items.ImmuneToDebuff",
    "Items.VoidBear",
    "Items.VoidMegaCrabItem",
    "Items.VoidCoin",
    "Items.VoidMan",
    "Items.MissileVoid",
    "Items.ChainLightningVoid",
    "Items.VoidCritGlasses",
    "Items.VoidBackpack",
    "Items.VoidBleedOnHit",
    "Items.VoidTripleJump",
    "Items.VoidBarnacle",
    "Skins.Railgunner.Alt1",
)

PACK = ContentPack(
    id="survivors_of_the_void",
    name="Survivors of the Void",
    survivors=SURVIVORS,
    achievements=ACHIEVEMENTS,
    extra_achievement_ids=EXTRA_ACHIEVEMENT_IDS,
    extra_unlock_tokens=EXTRA_UNLOCK_TOKENS,
)
