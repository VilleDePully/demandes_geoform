# coding=utf-8

# Imports

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    Text,
    Boolean,
    Date,
    Table,
    Numeric,
    ForeignKey)
from sqlalchemy.orm import relationship

import geoalchemy2

from deform.widget import HiddenWidget


from c2cgeoform_project.i18n import _
from c2cgeoform.ext import colander_ext, deform_ext

from c2cgeoform_project.models.meta import Base
from c2cgeoform.ext.deform_ext import RelationSelectWidget
# Variables

schema = 'abattage'

# Classes

class Type_travaux(Base):
    __tablename__ = 'type_travaux'
    __table_args__ = (
        {"schema": schema}
    )

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

class Type_arborisation(Base):
    __tablename__ = 'type_arborisation'
    __table_args__ = (
        {"schema": schema}
    )

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

class Demande(Base):
    __tablename__ = 'demande'
    __table_args__ = (
        {"schema": schema}
    )

    id = Column(Integer, primary_key=True, info={
        'colanderalchemy': {
            'widget': HiddenWidget()
        }})

    proprietaire = Column(Text, nullable=False)
    adresse = Column(Text, nullable=False)
    type_travaux_id = Column(Integer, ForeignKey('{}.type_travaux.id'.format(schema)), nullable=False)
    type_arborisation_id = Column(Integer, ForeignKey('{}.type_arborisation.id'.format(schema)), nullable=False)
    essence = Column(Text, nullable=False)
    diametre = Column(Numeric(5,2), nullable=False)
    hauteur = Column(Numeric(5,2), nullable=False)
    motif = Column(Text, nullable=False)
    date_demande = Column(Date)

    location_position = Column(
        geoalchemy2.Geometry('POINT', 4326, management=True), info={
            'colanderalchemy': {
                'title': _('Position'),
                'typ':
                colander_ext.Geometry('POINT', srid=4326, map_srid=3857),
                'widget': deform_ext.MapWidget()
            }})

    type_travaux = relationship('Type_travaux', info={'colanderalchemy': {'exclude': True}})
    type_arborisation = relationship('Type_arborisation', info={'colanderalchemy': {'exclude': True}})

