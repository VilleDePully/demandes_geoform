# coding=utf-8

# Imports

from uuid import uuid4
from datetime import date

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

from c2cgeoform_project.i18n import _
from c2cgeoform.ext import colander_ext, deform_ext

from c2cgeoform.models import FileData
from c2cgeoform_project.models.meta import Base

import deform, colander
from deform.widget import HiddenWidget
from c2cgeoform.ext.deform_ext import RelationSelect2Widget

# Variables

schema = 'abattage'

# Classes

# # FIXME a file upload memory store is not appropriate for production
# # See http://docs.pylonsproject.org/projects/deform/en/latest/interfaces.html#deform.interfaces.FileUploadTempStore  # noqa
# class FileUploadTempStore(dict):
#     def preview_url(self, name):
#         return None
#
# _file_upload_temp_store = FileUploadTempStore()

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

# class Photo(FileData, Base):
#     __tablename__ = 'photo'
#     __table_args__ = (
#         {"schema": schema}
#     )
#     # Setting unknown to 'preserve' is required in classes used as a
#     # FileUpload field.
#     __colanderalchemy_config__ = {
#         'title': _('Photo'),
#         'unknown': 'preserve',
#         'widget': deform_ext.FileUploadWidget(_file_upload_temp_store)
#     }
#     demande_id = Column(Integer, ForeignKey("{}.demande.id".format(schema)))

class Demande(Base):
    __tablename__ = 'demande'
    __table_args__ = (
        {"schema": schema}
    )

    __colanderalchemy_config__ = {
        'title':
        _('Demande d\'abattage d\'arbres'),
        'plural': _('Demande d\'abattage d\'arbres')
    }

    id = Column(Integer, primary_key=True, info={
        'colanderalchemy': {
            'widget': HiddenWidget()
        }})
    hash = Column(Text, unique=True, default=lambda: str(uuid4()), info={
        'colanderalchemy': {
            'widget': HiddenWidget()
        },
        'c2cgeoform': {
            'duplicate': False
        }})
    proprietaire = Column(Text, nullable=False)
    adresse = Column(Text, nullable=False)
    type_travaux_id = Column(
        Integer,
        ForeignKey('{}.type_travaux.id'.format(schema)),
        nullable=False,
        info={
            'colanderalchemy': {
                'title': _('Type de travaux'),
                'description': _('Type de travaux à entreprendre'),
                'widget': deform_ext.RelationRadioChoiceWidget(
                    Type_travaux,
                    'id',
                    'name',
                    order_by='id',
                    inline=True
                )
            }
        })
    type_arborisation_id = Column(
        Integer,
        ForeignKey('{}.type_arborisation.id'.format(schema)),
        nullable=False,
        info={
            'colanderalchemy': {
                'title': _('Type d\'arborisation'),
                'widget': RelationSelect2Widget(
                    Type_arborisation,
                    'id',
                    'name',
                    order_by='id',
                    default_value=('', _('- Select -'))
                )
            }
        })
    essence = Column(Text, nullable=False)
    diametre = Column(Numeric(5,2), nullable=False)
    hauteur = Column(Numeric(5,2), nullable=False)
    motif = Column(Text, nullable=False,
        info={
            'colanderalchemy': {
                'title': _('Motif'),
                'widget': deform.widget.TextAreaWidget(rows=3),
            }
        })
    email = Column(Text, nullable=False,
        info={
            'colanderalchemy': {
                'title':_('E-mail'),
                'validator': colander.Email()
            }
        })
    date_demande = Column(Date, info={
        'colanderalchemy': {
            'widget': HiddenWidget()
        }}, default=lambda: date.today())

    location_position = Column(
        geoalchemy2.Geometry('POINT', 4326, management=True), info={
            'colanderalchemy': {
                'title': _('Position'),
                'typ':
                colander_ext.Geometry('POINT', srid=4326, map_srid=3857),
                'widget': deform_ext.MapWidget(
                    center=[741934,5863213],
                    zoom=14,
                    fit_max_zoom=18
                )
            }}, nullable=False)

    type_travaux = relationship('Type_travaux', info={'colanderalchemy': {'exclude': True}})
    type_arborisation = relationship('Type_arborisation', info={'colanderalchemy': {'exclude': True}})

    # photos = relationship(
    #     Photo,
    #     cascade="all, delete-orphan",
    #     info={
    #         'colanderalchemy': {
    #             'title': _('Photo')
    #         }})