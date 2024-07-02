from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from datamodel.eldamobase import EldamoBase


class CombineWords(EldamoBase):
    __tablename__ = 'combine_words'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_word_id: Mapped[str] = mapped_column(ForeignKey('words.id'))
    second_word_id: Mapped[str] = mapped_column(ForeignKey('words.id'))

    first_word: Mapped['Word'] = relationship(back_populates='combine_left', foreign_keys=first_word_id)
    second_word: Mapped['Word'] = relationship(back_populates='combine_right', foreign_keys=second_word_id)