from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from datamodel.eldamobase import EldamoBase


class InflectReference(EldamoBase):
    __tablename__ = 'inflect_reference'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_ref_id: Mapped[str] = mapped_column(ForeignKey('references.source'))
    second_ref_id: Mapped[Optional[str]] = mapped_column(ForeignKey('references.source'))
    text: Mapped[Optional[str]]
    form: Mapped[Optional[str]]
    variant: Mapped[Optional[str]]

    first_reference: Mapped['Reference'] = relationship(back_populates='inflect_left', foreign_keys=first_ref_id)
    second_reference: Mapped['Reference'] = relationship(back_populates='inflect_right', foreign_keys=second_ref_id)
