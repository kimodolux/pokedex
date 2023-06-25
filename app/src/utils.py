from pokeapi import get_link


def get_abilities(pokemon_data):
    abilities_links = pokemon_data["abilities"]
    abilities_dict = [
        get_link(ability["ability"]["url"]) for ability in abilities_links
    ]
    abilities = []
    for ability in abilities_dict:
        effects = ability.get("effect_entries")
        for effect in effects:
            if effect["language"]["name"] == "en":
                en_effect = effect

        abilities.append(
            {
                "name": ability.get("name").capitalize(),
                "effect": en_effect["short_effect"],
            }
        )
    return abilities


def get_latest_group(groups):
    latest_group = {
        "version_group": {
            "name": "",
            "url": "https://pokeapi.co/api/v2/version-group/0/",
        }
    }
    for group in groups:
        if (
            group["version_group"]["url"][-3:-1]
            > latest_group["version_group"]["url"][-3:-1]
        ):
            latest_group = group
    return latest_group


def get_moves(pokemon_data):
    moves_links = pokemon_data["moves"]
    moves_dict = [
        {
            "move": get_link(move["move"]["url"]),
            "version_group_details": move["version_group_details"],
        }
        for move in moves_links
    ]
    moves = []
    for move in moves_dict:
        move_info = move["move"]
        version_group_details = move["version_group_details"]
        effects = move_info.get("effect_entries")
        for effect in effects:
            if effect["language"]["name"] == "en":
                en_effect = effect
        latest_group = get_latest_group(version_group_details)
        effect = en_effect.get("short_effect")
        effect_chance = move_info.get("effect_chance")
        print(move)
        print("  ")
        moves.append(
            {
                "name": move_info.get("name").capitalize(),
                "class": move_info.get("damage_class"),
                "pp": move_info.get("pp"),
                "power": move_info.get("power"),
                "accuracy": move_info.get("accuracy"),
                "type": move_info.get("type").get("name"),
                "effect": effect
                if not "$effect_chance" in effect
                else effect.replace("$effect_chance", str(effect_chance)),
                "effect_chance": move_info.get("effect_chance"),
                "learn_method": latest_group.get("move_learn_method").get("name"),
                "level_learned_at": latest_group.get("level_learned_at"),
            }
        )
    return moves


def get_stat_bar_color(stat_value):
    if stat_value > 150:
        return "#00ff00"
    percent = stat_value / 150
    percent_diff = 1 - percent
    red = min(255, percent_diff * 255)
    green = min(255, percent * 255)

    return f"rgb({red}, {green}, 0)"


def shorten_stat_names(stat_name):
    if stat_name == "special-attack":
        return "Sp. Attack"
    if stat_name == "special-defense":
        return "Sp. Defense"
    return stat_name


def get_stats(pokemon_stats):
    base_stats = []
    for stat in pokemon_stats:
        base_stats.append(
            {
                "name": shorten_stat_names(stat["name"]).capitalize(),
                "value": stat["stat"],
                "color": get_stat_bar_color(stat["stat"]),
                "percentage_of_max": int(stat["stat"] / 255 * 100),
            }
        )

    return base_stats
