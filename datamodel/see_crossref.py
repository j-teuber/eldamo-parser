from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from datamodel.eldamobase import EldamoBase


class SeeCrossref(EldamoBase):
    __tablename__ = 'see_crossref'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_word_id: Mapped[str] = mapped_column(ForeignKey('words.id'))
    second_word_id: Mapped[str] = mapped_column(ForeignKey('words.id'))
    type: Mapped[Optional[str]]

    first_word: Mapped['Word'] = relationship(back_populates='see_left', foreign_keys=first_word_id)
    second_word: Mapped['Word'] = relationship(back_populates='see_right', foreign_keys=second_word_id)