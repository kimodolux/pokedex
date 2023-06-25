from flask import render_template, request, Response
from utils import get_stats, get_latest_group
import re
import requests
from app import app, db

from models.pokemon import Pokemon
from models.move import Move
from models.ability import Ability
from models.pokemon_move_association import Pokemon_Move_Association


@app.route("/", methods=["GET"])
def home():
    return render_template("pokedex.html")


@app.route("/pokemon", methods=["GET"])
def list_pokemon():
    results = db.session.execute(db.select(Pokemon).limit(100).offset(151)).scalars()
    pokemon_list: list[Pokemon] = results.all()
    return render_template("pokemon_list.html", pokemon_list=pokemon_list)

@app.route("/gen1", methods=["GET"])
def list_gen1_pokemon():
    results = db.session.execute(db.select(Pokemon).limit(151)).scalars()
    pokemon_list: list[Pokemon] = results.all()
    return render_template("pokemon_list.html", pokemon_list=pokemon_list)


@app.route("/gen2", methods=["GET"])
def list_gen2_pokemon():
    results = db.session.execute(db.select(Pokemon).limit(100).offset(151)).scalars()
    pokemon_list: list[Pokemon] = results.all()
    return render_template("pokemon_list.html", pokemon_list=pokemon_list)


@app.route("/gen3", methods=["GET"])
def list_gen3_pokemon():
    results = db.session.execute(db.select(Pokemon).limit(135).offset(251)).scalars()
    pokemon_list: list[Pokemon] = results.all()
    return render_template("pokemon_list.html", pokemon_list=pokemon_list)

@app.route("/gen4", methods=["GET"])
def list_gen4_pokemon():
    results = db.session.execute(db.select(Pokemon).limit(107).offset(386)).scalars()
    pokemon_list: list[Pokemon] = results.all()
    return render_template("pokemon_list.html", pokemon_list=pokemon_list)


@app.route("/pokemon/<id>")
def pokemon_detail(id):
    pokemon: Pokemon = db.first_or_404(db.select(Pokemon).filter_by(id=id))
    types = [pokemon.type_1.capitalize()]
    if pokemon.type_2:
        types.append(pokemon.type_2.capitalize())
    stats = get_stats(
        [
            {"name": "hp", "stat": pokemon.hp_stat},
            {"name": "attack", "stat": pokemon.attack_stat},
            {"name": "defence", "stat": pokemon.defence_stat},
            {"name": "special-attack", "stat": pokemon.special_attack_stat},
            {"name": "special-defence", "stat": pokemon.special_defence_stat},
            {"name": "speed", "stat": pokemon.speed_stat},
        ]
    )
    ability_1 = db.session.execute(
        db.select(Ability).filter_by(id=pokemon.ability_id_1)
    ).scalar_one()
    ability_2 = (
        db.session.execute(
            db.select(Ability).filter_by(id=pokemon.ability_id_2)
        ).scalar_one()
        if pokemon.ability_id_2
        else None
    )

    abilities: list[Ability] = [ability_1]
    if ability_2:
        abilities.append(ability_2)

    move_tuples = db.session.execute(
        db.select(Move, Pokemon_Move_Association)
        .join(Pokemon_Move_Association)
        .where(
            Move.id == Pokemon_Move_Association.move_id
        )
        .where(
            id == Pokemon_Move_Association.pokemon_id
        )
    ).all()

    moves = []
    for tuple in move_tuples:
        move = tuple[0]
        move.learn_method = tuple[1].learn_method
        print(move.learn_method)
        move.level_learned = tuple[1].level_learned
        if move.short_effect:
            move.short_effect = move.short_effect if not "$effect_chance" in move.short_effect else move.short_effect.replace("$effect_chance", str(move.effect_chance)) 
        if move.long_effect:
            move.long_effect = move.long_effect if not "$effect_chance" in move.long_effect else move.long_effect.replace("$effect_chance", str(move.effect_chance)) 
        moves.append(move)
    
    level_up_moves = sorted(
        [move for move in moves if "level-up" in move.learn_method],
        key=lambda m: m.level_learned,
    )
    tm_moves = [move for move in moves if "machine" in move.learn_method]
    tutor_moves = [move for move in moves if "tutor" in move.learn_method]
    egg_moves = [move for move in moves if "egg" in move.learn_method]
    return render_template(
        "pokemon_detail.html",
        id=pokemon.id,
        name=pokemon.pokemon_name.capitalize(),
        height=pokemon.pokemon_height,
        weight=pokemon.pokemon_weight,
        sprite=pokemon.sprite,
        types=types,
        stats=stats,
        abilities=abilities,
        level_up_moves=level_up_moves,
        tm_moves=tm_moves,
        tutor_moves=tutor_moves,
        egg_moves=egg_moves,
    )


@app.route("/abilities", methods=["GET"])
def list_abilities():
    results = db.session.execute(db.select(Ability).limit(10)).scalars()
    abilities: list[Ability] = results.all()
    return render_template("abilities.html", abilities=abilities)


@app.route("/moves", methods=["GET"])
def list_moves():
    results = db.session.execute(db.select(Move).limit(10)).scalars()
    moves: list[Move] = results.all()
    return render_template("moves.html", moves=moves)


@app.route("/api/createcontext", methods=["GET"])
def create_context():
    with app.app_context():
        db.create_all()
    return Response(status=200)


@app.route("/api/create_pokemon", methods=["POST"])
def pokemon_create():
    content = request.json.get("data")

    types = content.get("types")
    type_1 = types[0].get("type").get("name")
    type_2 = None
    if len(types) > 1:
        type_2 = types[1].get("type").get("name")

    abilities = content.get("abilities")
    ability_id_1 = None
    ability_id_2 = None
    for ability in abilities:
        if ability.get("slot") == 1:
            ability_id_1 = int(
                re.findall("[0-9]+", ability.get("ability").get("url"))[1]
            )

        if ability.get("slot") == 2:
            ability_id_2 = int(
                re.findall("[0-9]+", ability.get("ability").get("url"))[1]
            )

    stats = content.get("stats")
    pokemon = Pokemon(
        id=content.get("id"),
        pokemon_name=content.get("name"),
        pokemon_height=content.get("height"),
        pokemon_weight=content.get("weight"),
        type_1=type_1,
        type_2=type_2,
        ability_id_1=ability_id_1,
        ability_id_2=ability_id_2,
        sprite=content.get("sprites").get("front_default"),
        hp_stat=stats[0].get("base_stat"),
        attack_stat=stats[1].get("base_stat"),
        defence_stat=stats[2].get("base_stat"),
        special_attack_stat=stats[3].get("base_stat"),
        special_defence_stat=stats[4].get("base_stat"),
        speed_stat=stats[5].get("base_stat"),
    )
    db.session.add(pokemon)
    db.session.commit()
    
    moves = content.get("moves")
    if moves:
        for move in moves:
            move_id = int(re.findall("[0-9]+", move["move"]["url"])[1])
            version_group_details = move["version_group_details"]
            latest_group = get_latest_group(version_group_details)
            learn_method = latest_group.get("move_learn_method").get("name")
            level_learned = latest_group.get("level_learned_at")

            association = Pokemon_Move_Association(
                move_id=move_id,
                pokemon_id=content.get("id"),
                learn_method=learn_method,
                level_learned=level_learned,
            )
            db.session.add(association)
            db.session.commit()
    return Response(status=201)


@app.route("/api/create_move", methods=["POST"])
def move_create():
    content = request.json.get("data")
    effects = content.get("effect_entries")
    en_effect = None
    if effects:
        for effect in effects:
            if effect["language"]["name"] == "en":
                en_effect = effect
    flavour_text_entries = content.get("flavour_text_entries")
    en_flavour_text = None
    if flavour_text_entries:
        for ft_entry in flavour_text_entries:
            if ft_entry["language"]["name"] == "en":
                en_flavour_text = ft_entry

    short_effect = None
    long_effect = None
    if en_effect:
        short_effect = en_effect.get("short_effect")
        long_effect = en_effect.get("effect")

    move = Move(
        id=content.get("id"),
        move_name=content.get("name"),
        move_class=content.get("damage_class").get("name"),
        pp=content.get("pp"),
        power=content.get("power"),
        priority=content.get("priority"),
        accuracy=content.get("accuracy"),
        type=content.get("type").get("name"),
        short_effect=short_effect,
        long_effect=long_effect,
        flavour_text=en_flavour_text,
        effect_chance=content.get("effect_chance"),
    )
    db.session.add(move)
    db.session.commit()
    return Response(status=201)


@app.route("/api/create_ability", methods=["POST"])
def ability_create():
    content = request.json.get("data")
    effects = content.get("effect_entries")
    en_effect = None
    if effects:
        for effect in effects:
            if effect["language"]["name"] == "en":
                en_effect = effect

    short_effect = None
    long_effect = None
    if en_effect:
        short_effect = en_effect.get("short_effect")
        long_effect = en_effect.get("effect")

    flavour_text_entries = content.get("flavour_text_entries")
    en_flavour_text = None
    if flavour_text_entries:
        for ft_entry in flavour_text_entries:
            if ft_entry["language"]["name"] == "en":
                en_flavour_text = ft_entry
    ability = Ability(
        id=content.get("id"),
        ability_name=content.get("name"),
        flavour_text_entry=en_flavour_text,
        short_effect=short_effect,
        long_effect=long_effect,
    )
    db.session.add(ability)
    db.session.commit()
    return Response(status=201)
