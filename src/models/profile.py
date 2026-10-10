from dataclasses import dataclass


@dataclass
class ParsedProfile:
    file_name: str
    display_name: str
    xml_content: str
    coins: int
    unlocked_achievements: set[str]
    unlocked_items: set[str]


MAX_COINS = 2_147_483_647


def validate_coins(value: int) -> int:
    if type(value) is not int or not 0 <= value <= MAX_COINS:
        raise ValueError(f"Coins must be a whole number from 0 to {MAX_COINS}.")
    return value
