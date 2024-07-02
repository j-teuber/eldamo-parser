from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from datamodel.eldamobase import EldamoBase


class SemanticCategories(EldamoBase):
    __tablename__ = 'semantic_categories'

    id: Mapped[str] = mapped_column(primary_key=True)
    parent_category_id: Mapped[str] = mapped_column(ForeignKey('semantic_groups.id'))
    lable: Mapped[str]
    number: Mapped[str]

    parent_category: Mapped['SemanticGroups'] = relationship(back_populates='subcategories')


class SemanticGroups(EldamoBase):
    __tablename__ = 'semantic_groups'

    id: Mapped[str] = mapped_column(primary_key=True)
    label: Mapped[str]
    number: Mapped[str]

    subcategories: Mapped[List['SemanticCategories']] = relationship(back_populates='parent_category')
