from src.models.catalog import Achievement, Category, ContentPack, Survivor

SURVIVORS: tuple[Survivor, ...] = (
    Survivor(
        id="Enforcer2",
        name="Enforcer",
        description=(
            "The Enforcer is a bastion of defensive and offensive capabilities using his "
            "impenetrable shield and ample firepower."
        ),
        dlc="Hallowed Concepts",
    ),
    Survivor(
        id="Acolyte",
        name="Acolyte",
        description=(
            "The Acolyte is a close-range whirlwind of death, conducting sacrifices to unleash "
            "the Anima Harvester that is bound to her. Balance shall be restored to Petrichor "
            "V."
        ),
        required_achievement="ChampRushRitualCompleted",
        dlc="Hallowed Concepts",
    ),
)

ACHIEVEMENTS: tuple[Achievement, ...] = (
    Achievement(
        id="Enforcer2BlockXTeleporter",
        name="Enforcer: Safe and Sound",
        description=(
            "As Enforcer, block the attacks of 12 enemies during a single teleporter event."
        ),
        category=Category.SKILL,
        survivor_id="Enforcer2",
        unlockable="Skills.Enforcer2.RageGas",
    ),
    Achievement(
        id="Enforcer2ParryVagrant",
        name="Enforcer: +PARRY",
        description="As Enforcer, parry a Wandering Vagrant's supernova.",
        category=Category.SKILL,
        survivor_id="Enforcer2",
        unlockable="Skills.Enforcer2.KineticCharge",
    ),
    Achievement(
        id="Enforcer2RepeatedlyDamageMagmaWorm",
        name="Enforcer: Burning Lead",
        description="As Enforcer, shoot a Magma Worm 24 times in 12 seconds.",
        category=Category.SKILL,
        survivor_id="Enforcer2",
        unlockable="Skills.Enforcer2.ClusterGrenade",
    ),
    Achievement(
        id="Enforcer2TankTitanLaser",
        name="Enforcer: Indomitable",
        description="As Enforcer, survive an entire Stone Titan's laser without blocking.",
        category=Category.SKILL,
        survivor_id="Enforcer2",
        unlockable="Skills.Enforcer2.ShieldLeap",
    ),
    Achievement(
        id="Enforcer2ClearChampRush",
        name="Enforcer: Dying to Meet You",
        description="As Enforcer, complete Soulbound Threshold before the 4th Teleporter event.",
        category=Category.SKIN,
        survivor_id="Enforcer2",
        unlockable="Skins.Enforcer2.AltSkinLynx",
    ),
    Achievement(
        id="Enforcer2ClearGameMonsoon",
        name="Enforcer: Mastery",
        description="As Enforcer, beat the game or obliterate on Monsoon.",
        category=Category.SKIN,
        survivor_id="Enforcer2",
        unlockable="Skins.Enforcer2.Alt1",
    ),
    Achievement(
        id="ChampRushRitualCompleted",
        name="A Broken Ritual",
        description="Revive the survivor within Soulbound Threshold.",
        category=Category.SURVIVOR,
        survivor_id="Acolyte",
        unlockable="Characters.Acolyte",
    ),
    Achievement(
        id="AcolyteJuggleLemurian",
        name="Acolyte: Not Even Close",
        description="As Acolyte, keep an Elder Lemurian airborne for 11 seconds.",
        category=Category.SKILL,
        survivor_id="Acolyte",
        unlockable="Skills.Acolyte.Javelin",
    ),
    Achievement(
        id="AcolyteReaperMultiKill",
        name="Acolyte: Bloodbath",
        description=(
            "As Acolyte, kill 15 enemies within one transformation into the Anima Harvester."
        ),
        category=Category.SKILL,
        survivor_id="Acolyte",
        unlockable="Skills.Acolyte.SoulJar",
    ),
    Achievement(
        id="AcolyteUniqueSacrifices",
        name="Acolyte: Hit List",
        description=(
            "As Acolyte, land a killing blow with Sacrifice on 20 different types of monsters "
            "in a single run."
        ),
        category=Category.SKILL,
        survivor_id="Acolyte",
        unlockable="Skills.Acolyte.Backpack",
    ),
    Achievement(
        id="AcolyteClearGameMonsoon",
        name="Acolyte: Mastery",
        description="As Acolyte, beat the game or obliterate on Monsoon.",
        category=Category.SKIN,
        survivor_id="Acolyte",
        unlockable="Skins.Acolyte.Alt1",
    ),
    Achievement(
        id="AcolyteClearUltima",
        name="Acolyte: Memento Mori",
        description="As Acolyte, defeat what lies beyond the door of Soulbound Threshold.",
        category=Category.SKIN,
        survivor_id="Acolyte",
        unlockable="Skins.Acolyte.AltSkinHallow",
    ),
    Achievement(
        id="CommandoClearChampRush",
        name="Commando: Dying to Meet You",
        description="As Commando, complete Soulbound Threshold before the 4th Teleporter event.",
        category=Category.SKIN,
        survivor_id="Commando",
        unlockable="Skins.Commando.AltSkinLynx",
    ),
    Achievement(
        id="HuntressClearChampRush",
        name="Huntress: Dying to Meet You",
        description="As Huntress, complete Soulbound Threshold before the 4th Teleporter event.",
        category=Category.SKIN,
        survivor_id="Huntress",
        unlockable="Skins.Huntress.AltSkinLynx",
    ),
    Achievement(
        id="Bandit2ClearUltima",
        name="Bandit: Memento Mori",
        description="As Bandit, defeat what lies beyond the door of Soulbound Threshold.",
        category=Category.SKIN,
        survivor_id="Bandit2",
        unlockable="Skins.Bandit2.AltSkinHallow",
    ),
    Achievement(
        id="ToolbotClearGameHexes",
        name="MUL-T: Against All Odds",
        description="As MUL-T, complete a run while holding 10 Hexes.",
        category=Category.SKIN,
        survivor_id="Toolbot",
        unlockable="Skins.Toolbot.AltSkinFungal",
    ),
    Achievement(
        id="EngiClearUltima",
        name="Engineer: Memento Mori",
        description="As Engineer, defeat what lies beyond the door of Soulbound Threshold.",
        category=Category.SKIN,
        survivor_id="Engi",
        unlockable="Skins.Engi.AltSkinHallow",
    ),
    Achievement(
        id="MageClearUltima",
        name="Artificer: Memento Mori",
        description="As Artificer, defeat what lies beyond the door of Soulbound Threshold.",
        category=Category.SKIN,
        survivor_id="Mage",
        unlockable="Skins.Mage.AltSkinHallow",
    ),
    Achievement(
        id="MercClearGameHexes",
        name="Mercenary: Against All Odds",
        description="As Mercenary, complete a run while holding 10 Hexes.",
        category=Category.SKIN,
        survivor_id="Merc",
        unlockable="Skins.Merc.AltSkinFungal",
    ),
    Achievement(
        id="TreebotClearUltima",
        name="REX: Memento Mori",
        description="As REX, defeat what lies beyond the door of Soulbound Threshold.",
        category=Category.SKIN,
        survivor_id="Treebot",
        unlockable="Skins.Treebot.AltSkinHallow",
    ),
    Achievement(
        id="LoaderClearGameHexes",
        name="Loader: Against All Odds",
        description="As Loader, complete a run while holding 10 Hexes.",
        category=Category.SKIN,
        survivor_id="Loader",
        unlockable="Skins.Loader.AltSkinFungal",
    ),
    Achievement(
        id="CrocoClearChampRush",
        name="Acrid: Dying to Meet You",
        description="As Acrid, complete Soulbound Threshold before the 4th Teleporter event.",
        category=Category.SKIN,
        survivor_id="Croco",
        unlockable="Skins.Croco.AltSkinLynx",
    ),
    Achievement(
        id="CaptainClearUltima",
        name="Captain: Memento Mori",
        description="As Captain, defeat what lies beyond the door of Soulbound Threshold.",
        category=Category.SKIN,
        survivor_id="Captain",
        unlockable="Skins.Captain.AltSkinHallow",
    ),
    Achievement(
        id="RailgunnerClearGameHexes",
        name="Railgunner: Against All Odds",
        description="As Railgunner, complete a run while holding 10 Hexes.",
        category=Category.SKIN,
        survivor_id="Railgunner",
        unlockable="Skins.RailGunner.AltSkinFungal",
    ),
    Achievement(
        id="VoidSurvivorClearGameHexes",
        name="「V??oid Fiend』: Against All Odds",
        description="As 「V??oid Fiend』, complete a run while holding 10 Hexes.",
        category=Category.SKIN,
        survivor_id="VoidSurvivor",
        unlockable="Skins.VoidSurvivor.AltSkinFungal",
    ),
    Achievement(
        id="SeekerClearChampRush",
        name="Seeker: Dying to Meet You",
        description="As Seeker, complete Soulbound Threshold before the 4th Teleporter event.",
        category=Category.SKIN,
        survivor_id="Seeker",
        unlockable="Skins.Seeker.AltSkinLynx",
    ),
    Achievement(
        id="ChefClearChampRush",
        name="CHEF: Dying to Meet You",
        description="As CHEF, complete Soulbound Threshold before the 4th Teleporter event.",
        category=Category.SKIN,
        survivor_id="Chef",
        unlockable="Skins.Chef.AltSkinLynx",
    ),
    Achievement(
        id="FalseSonClearGameHexes",
        name="False Son: Against All Odds",
        description="As False Son, complete a run while holding 10 Hexes.",
        category=Category.SKIN,
        survivor_id="FalseSon",
        unlockable="Skins.FalseSon.AltSkinFungal",
    ),
)

EXTRA_ACHIEVEMENT_IDS: tuple[str, ...] = ()

EXTRA_UNLOCK_TOKENS: tuple[str, ...] = ()

PACK = ContentPack(
    id="hallowed_concepts",
    name="Hallowed Concepts",
    survivors=SURVIVORS,
    achievements=ACHIEVEMENTS,
    extra_achievement_ids=EXTRA_ACHIEVEMENT_IDS,
    extra_unlock_tokens=EXTRA_UNLOCK_TOKENS,
)
