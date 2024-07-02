from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from datamodel.eldamobase import EldamoBase


class CognateWords(EldamoBase):
    __tablename__ = 'cognate_words'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_word_id: Mapped[str] = mapped_column(ForeignKey('words.id'))
    second_word_id: Mapped[str] = mapped_column(ForeignKey('words.id'))
    mark: Mapped[Optional[str]]
    text: Mapped[Optional[str]]

    first_word: Mapped['Word'] = relationship(back_populates='cognate_left', foreign_keys=first_word_id)
    second_word: Mapped['Word'] = relationship(back_populates='cognate_right', foreign_keys=second_word_id)


class CognateReferences(EldamoBase):
    __tablename__ = 'cognate_references'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_ref_id: Mapped[str] = mapped_column(ForeignKey('references.source'))
    second_ref_id: Mapped[str] = mapped_column(ForeignKey('references.source'))
    mark: Mapped[Optional[str]]
    text: Mapped[Optional[str]]

    first_reference: Mapped['Reference'] = relationship(back_populates='cognate_left', foreign_keys=first_ref_id)
    second_reference: Mapped['Reference'] = relationship(back_populates='cognate_right', foreign_keys=second_ref_id)
