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

class Essence(Base):
    __tablename__ = 'essence'
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
    parcelle = Column(Integer, nullable=False)
    adresse = Column(Text, nullable=False)
    #essence_id = Column(Integer, ForeignKey('{}.essence.id'.format(schema)), nullable=False)
    essence_id = Column(Integer, ForeignKey('{}.essence.id'.format(schema)), nullable=False, info={
        'colanderalchemy': {
            'title': 'Essence',
            'widget': RelationSelectWidget(
                Essence,
                'id',
                'name',
                order_by='name',
                default_value=('', _('- Select -'))
            )
        }})
    location_position = Column(
        geoalchemy2.Geometry('POINT', 4326, management=True), info={
            'colanderalchemy': {
                'title': _('Position'),
                'typ':
                colander_ext.Geometry('POINT', srid=4326, map_srid=3857),
                'widget': deform_ext.MapWidget()
            }})

    essence = relationship('Essence', info={'colanderalchemy': {'exclude': True}})

