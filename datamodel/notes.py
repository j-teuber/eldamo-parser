from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from datamodel.eldamobase import EldamoBase


class Note(EldamoBase):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[str] = mapped_column(ForeignKey('words.id'))
    text: Mapped[str]

    word: Mapped['Word'] = relationship(back_populates='notes')

    def __repr__(self):
        return f'<note for {self.word.id}: {self.text[:30]}...>'
