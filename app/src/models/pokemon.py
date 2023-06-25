from sqlalchemy import Column, Integer, String, BLOB, ForeignKey
from app import db


class Pokemon(db.Model):
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True)
    pokemon_name = Column(String(30), nullable=False, unique=True)
    pokemon_height = Column(Integer, nullable=False)
    pokemon_weight = Column(Integer, nullable=False)
    type_1 = Column(String, nullable=False)
    type_2 = Column(String)
    ability_id_1 = Column(ForeignKey("ability.id"))
    ability_id_2 = Column(ForeignKey("ability.id"))
    sprite = Column(String)
    hp_stat = Column(Integer, nullable=False)
    attack_stat = Column(Integer, nullable=False)
    defence_stat = Column(Integer, nullable=False)
    special_attack_stat = Column(Integer, nullable=False)
    special_defence_stat = Column(Integer, nullable=False)
    speed_stat = Column(Integer, nullable=False)
