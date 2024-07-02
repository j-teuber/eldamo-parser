from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from datamodel.cognate import CognateWords
from datamodel.eldamobase import EldamoBase
from datamodel.notes import Note
from datamodel.reference import Reference
from datamodel.related import RelatedWords
from datamodel.combine import CombineWords
from datamodel.deprecated import DeprecatedWord
from datamodel.derive import DeriveWords
from datamodel.element import ElementWords
from datamodel.see_crossref import SeeCrossref


class Word(EldamoBase):
    __tablename__ = 'words'

    id: Mapped[str] = mapped_column(primary_key=True)
    language: Mapped[str]
    verbum: Mapped[str]
    sort_key: Mapped[str]
    page_id: Mapped[str]
    part_of_speech: Mapped[str]
    gloss: Mapped[Optional[str]]
    stem_form: Mapped[Optional[str]]
    mark: Mapped[Optional[str]]
    tengwar_hints: Mapped[Optional[str]]
    semantic_category: Mapped[Optional[str]]  # = mapped_column(ForeignKey('semantic_categories.id'))
    neo_gloss: Mapped[Optional[str]]
    neo_version: Mapped[Optional[str]]
    neo_creator: Mapped[Optional[str]]
    vetted_by: Mapped[Optional[str]]

    parent_word_id: Mapped[Optional[str]] = mapped_column(ForeignKey('words.id'))

    references: Mapped[List['Reference']] = relationship(
        back_populates='parent_word', cascade='all, delete, delete-orphan'
    )
    child_words: Mapped[List['Word']] = relationship(
        back_populates='parent_word', cascade='none'
    )
    parent_word: Mapped['Word'] = relationship(back_populates='child_words', remote_side=id)

    notes: Mapped[List[Note]] = relationship(back_populates='word')

    related_left: Mapped[List['RelatedWords']] = relationship(
        back_populates='first_word', foreign_keys=RelatedWords.first_word_id)
    related_right: Mapped[List['RelatedWords']] = relationship(
        back_populates='second_word', foreign_keys=RelatedWords.second_word_id)

    combine_left: Mapped[List['CombineWords']] = relationship(
        back_populates='first_word', foreign_keys=CombineWords.first_word_id)
    combine_right: Mapped[List['CombineWords']] = relationship(
        back_populates='second_word', foreign_keys=CombineWords.second_word_id)

    cognate_left: Mapped[List['CognateWords']] = relationship(
        back_populates='first_word', foreign_keys=CognateWords.first_word_id)
    cognate_right: Mapped[List['CognateWords']] = relationship(
        back_populates='second_word', foreign_keys=CognateWords.second_word_id)

    deprecated_left: Mapped[List['DeprecatedWord']] = relationship(
        back_populates='first_word', foreign_keys=DeprecatedWord.first_word_id)
    deprecated_right: Mapped[List['DeprecatedWord']] = relationship(
        back_populates='second_word', foreign_keys=DeprecatedWord.second_word_id)

    derive_left: Mapped[List[DeriveWords]] = relationship(
        back_populates='first_word', foreign_keys=DeriveWords.first_word_id)
    derive_right: Mapped[List[DeriveWords]] = relationship(
        back_populates='second_word', foreign_keys=DeriveWords.second_word_id)

    element_left: Mapped[List[ElementWords]] = relationship(
        back_populates='first_word', foreign_keys=ElementWords.first_word_id)
    element_right: Mapped[List[ElementWords]] = relationship(
        back_populates='second_word', foreign_keys=ElementWords.second_word_id)

    see_left: Mapped[List[SeeCrossref]] = relationship(
        back_populates='first_word', foreign_keys=SeeCrossref.first_word_id)
    see_right: Mapped[List[SeeCrossref]] = relationship(
        back_populates='second_word', foreign_keys=SeeCrossref.second_word_id)

    def __repr__(self):
        return f'<{self.id}>'
