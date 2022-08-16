from flask import render_template, url_for
from pokeapi import get_link, get_pokemon, get_first_gen_pokedex
from utils import get_abilities, get_moves, get_stats

from app import app


@app.route("/", methods=["GET"])
def index():
    return "Hello world"


@app.route("/home", methods=["GET"])
def home():
    return render_template("base.html")


@app.route("/pokedex", methods=["GET"])
def pokedex():
    pokedex_data = get_first_gen_pokedex()
    if "err" in pokedex_data.keys():
        return render_template("error.html", error=pokemon_data["err"])
    pokemon_data = [
        get_link(pokemon_link["url"]) for pokemon_link in pokedex_data["results"]
    ]
    pokemon_dict = [
        {
            "name": pokemon["name"].capitalize(),
            "sprites": pokemon["sprites"],
            "href": url_for("pokemon", pokemon_name=pokemon["name"]),
        }
        for pokemon in pokemon_data
    ]
    return render_template("pokedex.html", pokemon_dict=pokemon_dict)


@app.route("/pokemon/<pokemon_name>", methods=["GET"])
def pokemon(pokemon_name):
    pokemon_data = get_pokemon(pokemon_name)
    if "err" in pokemon_data.keys():
        return render_template("error.html", error=pokemon_data["err"])
    height = pokemon_data["height"]
    weight = pokemon_data["weight"]
    pokedex_number = pokemon_data["id"]
    abilities = get_abilities(pokemon_data)
    stats = get_stats(pokemon_data)
    types = [
        type_dict["type"]["name"].capitalize() for type_dict in pokemon_data["types"]
    ]
    sprites = pokemon_data["sprites"]
    moves = get_moves(pokemon_data)
    level_up_moves = sorted(
        [move for move in moves if "level-up" in move.get("learn_method")],
        key=lambda m: m.get("level_learned_at"),
    )
    tm_moves = [move for move in moves if "machine" in move.get("learn_method")]
    tutor_moves = [move for move in moves if "tutor" in move.get("learn_method")]
    egg_moves = [move for move in moves if "egg" in move.get("learn_method")]
    # base_expereince = pokemon_data["base_expereince"]
    return render_template(
        "pokemon.html",
        pokemon_data=pokemon_data,
        pokedex_number=pokedex_number,
        height=height,
        weight=weight,
        abilities=abilities,
        stats=stats,
        sprites=sprites,
        level_up_moves=level_up_moves,
        tm_moves=tm_moves,
        tutor_moves=tutor_moves,
        egg_moves=egg_moves,
        types=types,
    )
