from src.models.catalog import Achievement, Category, ContentPack, Survivor

SURVIVORS: tuple[Survivor, ...] = (
    Survivor(
        id="Drifter",
        name="Drifter",
        description="Scavenging brawler (Alloyed Collective DLC).",
        required_achievement="FreeDrifter",
    ),
    Survivor(
        id="DroneTech",
        name="Operator",
        description="Drone specialist (Alloyed Collective DLC).",
    ),
)

ACHIEVEMENTS: tuple[Achievement, ...] = (
    Achievement(
        id="CommandoPurge",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Commando",
        unlockable="Skins.Commando.AltSkinVulture",
    ),
    Achievement(
        id="HuntressPurge",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Huntress",
        unlockable="Skins.Huntress.AltSkinVulture",
    ),
    Achievement(
        id="Bandit2Decompile",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Bandit2",
        unlockable="Skins.Bandit2.AltSkinSolus",
    ),
    Achievement(
        id="ToolbotPurge",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Toolbot",
        unlockable="Skins.Toolbot.AltSkinVulture",
    ),
    Achievement(
        id="EngiPurge",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Engi",
        unlockable="Skins.Engi.AltSkinVulture",
    ),
    Achievement(
        id="MageDecompile",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Mage",
        unlockable="Skins.Mage.AltSkinSolus",
    ),
    Achievement(
        id="MercPurge",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Merc",
        unlockable="Skins.Merc.AltSkinVulture",
    ),
    Achievement(
        id="TreebotDecompile",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Treebot",
        unlockable="Skins.Treebot.AltSkinSolus",
    ),
    Achievement(
        id="LoaderDecompile",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Loader",
        unlockable="Skins.Loader.AltSkinSolus",
    ),
    Achievement(
        id="CrocoPurge",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Croco",
        unlockable="Skins.Croco.AltSkinVulture",
    ),
    Achievement(
        id="CaptainDecompile",
        name="Alloyed",
        description="Purge/Decompile from Alloyed Collective DLC.",
        category=Category.SKIN,
        survivor_id="Captain",
        unlockable="Skins.Captain.AltSkinSolus",
    ),
    Achievement(
        id="FreeDrifter",
        name="Drifter",
        description="Unlock Drifter",
        category=Category.SURVIVOR,
        survivor_id="Drifter",
        unlockable="Characters.Drifter",
    ),
    Achievement(
        id="DrifterJunkCubeAchievement",
        name="Drifter: Trash Compactor",
        description="As Drifter, carry 20 temporary items at once.",
        category=Category.SKILL,
        survivor_id="Drifter",
        unlockable="Skills.Drifter.JunkCube",
    ),
    Achievement(
        id="DrifterTornadoSlamAchievement",
        name="Drifter: In The Bag",
        description=(
            "\tAs Drifter, defeat a boss from the challenge of the Mountain by tossing a Shrine "
            "of the Mountain."
        ),
        category=Category.SKILL,
        survivor_id="Drifter",
        unlockable="Skills.Drifter.Tornado",
    ),
    Achievement(
        id="DrifterTinkerAchievement",
        name="Drifter: Recycling",
        description=(
            "As Drifter, claim the contents of the lost backpack in the vault of Solutional Haunt."
        ),
        category=Category.SKILL,
        survivor_id="Drifter",
        unlockable="Skills.Drifter.Tinker",
    ),
    Achievement(
        id="DrifterClearGameMonsoon",
        name="Mastery",
        description="Beat the game or obliterate on Monsoon.",
        category=Category.SKIN,
        survivor_id="Drifter",
        unlockable="Skins.Drifter.Alt1",
    ),
    Achievement(
        id="DroneTechTrickshot",
        name="Operator: That All You Got?",
        description="As Operator, kill 4 different types of monsters with a single ricochet.",
        category=Category.SKILL,
        survivor_id="DroneTech",
        unlockable="Skills.DroneTech.CommandHeadbutt",
    ),
    Achievement(
        id="DroneTechDefeatVultureBossWhileAirborne",
        name="Operator: Not So Different",
        description=(
            "As Operator, defeat the Teleporter boss on Conduit Canyon without touching the ground."
        ),
        category=Category.SKILL,
        survivor_id="DroneTech",
        unlockable="Skills.DroneTech.ShieldFormation",
    ),
    Achievement(
        id="DroneTechJuggleLemurian",
        name="Operator: That Just Happened",
        description="As Operator, keep an Elder Lemurian airborne for 10 seconds.",
        category=Category.SKILL,
        survivor_id="DroneTech",
        unlockable="Skills.DroneTech.DroneBallShootable",
    ),
    Achievement(
        id="DroneTechUniqueDrones",
        name="Operator: Putting Together a Team",
        description="As Operator, recruit 5 different drones.",
        category=Category.SKILL,
        survivor_id="DroneTech",
        unlockable="Skills.DroneTech.DroneHauler",
    ),
    Achievement(
        id="DroneTechClearGameMonsoon",
        name="Mastery",
        description="As Operator, beat the game or obliterate on Monsoon.",
        category=Category.SKIN,
        survivor_id="DroneTech",
        unlockable="Skins.DroneTech.Alt1",
    ),
    Achievement(
        id="ObtainArtifactPrestige",
        name="Trial of Prestige",
        description="Complete the Trial of Prestige.",
        category=Category.ARTIFACT,
    ),
)

EXTRA_ACHIEVEMENT_IDS: tuple[str, ...] = ()

EXTRA_UNLOCK_TOKENS: tuple[str, ...] = (
    "Characters.DroneTech",
    "Artifacts.Prestige",
)

PACK = ContentPack(
    id="alloyed_collective",
    name="Alloyed Collective",
    survivors=SURVIVORS,
    achievements=ACHIEVEMENTS,
    extra_achievement_ids=EXTRA_ACHIEVEMENT_IDS,
    extra_unlock_tokens=EXTRA_UNLOCK_TOKENS,
)
