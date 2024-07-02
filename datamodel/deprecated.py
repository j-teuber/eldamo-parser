from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from datamodel.eldamobase import EldamoBase


class DeprecatedWord(EldamoBase):
    __tablename__ = 'deprecated_word'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_word_id: Mapped[str] = mapped_column(ForeignKey('words.id'))
    second_word_id: Mapped[Optional[str]] = mapped_column(ForeignKey('words.id'))

    first_word: Mapped['Word'] = relationship(
        back_populates='deprecated_left', foreign_keys=first_word_id)
    second_word: Mapped[Optional['Word']] = relationship(
        back_populates='deprecated_right', foreign_keys=second_word_id)