from sqlalchemy import Column, Integer, ForeignKey, String
from app import db


class Pokemon_Move_Association(db.Model):
    __tablename__ = "pokemon_move_association"
    id = Column(Integer, primary_key=True)
    move_id = Column(ForeignKey("move.id"))
    pokemon_id = Column(ForeignKey("pokemon.id"))
    learn_method = Column(String)
    level_learned = Column(Integer)
