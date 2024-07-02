from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from datamodel.eldamobase import EldamoBase
from datamodel.related import RelatedReferences
from datamodel.cognate import CognateReferences
from datamodel.derive import DeriveReferences
from datamodel.element import ElementReferences
from datamodel.inflect import InflectReference

class Reference(EldamoBase):
    __tablename__ = 'references'

    source: Mapped[str] = mapped_column(primary_key=True)
    parent_word_id: Mapped[str] = mapped_column(ForeignKey('words.id'))
    reference_language: Mapped[Optional[str]]
    verbum: Mapped[str]
    gloss: Mapped[Optional[str]]
    mark: Mapped[Optional[str]]

    parent_word: Mapped['Word'] = relationship(back_populates='references')

    related_left: Mapped[List[RelatedReferences]] = relationship(
        back_populates='first_reference', foreign_keys=RelatedReferences.first_ref_id)
    related_right: Mapped[List[RelatedReferences]] = relationship(
        back_populates='second_reference', foreign_keys=RelatedReferences.second_ref_id)

    cognate_left: Mapped[List[CognateReferences]] = relationship(
        back_populates='first_reference', foreign_keys=CognateReferences.first_ref_id)
    cognate_right: Mapped[List[CognateReferences]] = relationship(
        back_populates='second_reference', foreign_keys=CognateReferences.second_ref_id)

    derive_left: Mapped[List[DeriveReferences]] = relationship(
        back_populates='first_reference', foreign_keys=DeriveReferences.first_ref_id)
    derive_right: Mapped[List[DeriveReferences]] = relationship(
        back_populates='second_reference', foreign_keys=DeriveReferences.second_ref_id)

    element_left: Mapped[List[ElementReferences]] = relationship(
        back_populates='first_reference', foreign_keys=ElementReferences.first_ref_id)
    element_right: Mapped[List[ElementReferences]] = relationship(
        back_populates='second_reference', foreign_keys=ElementReferences.second_ref_id)

    inflect_left: Mapped[List[InflectReference]] = relationship(
        back_populates='first_reference', foreign_keys=InflectReference.first_ref_id)
    inflect_right: Mapped[List[InflectReference]] = relationship(
        back_populates='second_reference', foreign_keys=InflectReference.second_ref_id)

    def __repr__(self):
        return f'<{self.source}: {self.verbum} for {self.parent_word}>'
