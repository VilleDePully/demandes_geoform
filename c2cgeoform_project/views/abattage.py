from pyramid.view import view_config
from pyramid.view import view_defaults
from functools import partial

from sqlalchemy.orm import subqueryload

import colander

from c2cgeoform.schema import (
    GeoFormSchemaNode,
    GeoFormManyToManySchemaNode,
    manytomany_validator,
)
from c2cgeoform.ext.deform_ext import RelationCheckBoxListWidget
from c2cgeoform.views.abstract_views import AbstractViews, ListField

from ..models.abattage import Demande, Type_arborisation, Type_travaux

_list_field = partial(ListField, Demande)

base_schema = GeoFormSchemaNode(Demande)


@view_defaults(match_param='table=abattage')
class AbattageViews(AbstractViews):

    _model = Demande
    _base_schema = base_schema
    _id_field = 'id'

    _list_fields = [
        _list_field('id', visible=False),
        _list_field('proprietaire'),
        _list_field('adresse'),
        _list_field('type_travaux',
                    renderer=lambda demande: demande.type_travaux.name,
                    filter_column=Type_travaux.name,
                    sort_column=Type_travaux.name),
        _list_field('type_arborisation',
                    renderer=lambda demande: demande.type_arborisation.name,
                    filter_column=Type_arborisation.name,
                    sort_column=Type_arborisation.name),
        _list_field('essence'),
        _list_field('diametre'),
        _list_field('hauteur'),
        _list_field('motif'),
        _list_field('date_demande', visible=False)
    ]

    @view_config(route_name='c2cgeoform_index',
                 renderer='../templates/index.jinja2')
    def index(self):
        return super().index()

    @view_config(route_name='c2cgeoform_grid',
                 renderer='json')
    def grid(self):
        return super().grid()

    @view_config(route_name='c2cgeoform_item',
                 request_method='GET',
                 renderer='../templates/edit.jinja2')
    def edit(self):
        return super().edit()

    @view_config(route_name='c2cgeoform_item_duplicate',
                 request_method='GET',
                 renderer='../templates/edit.jinja2')
    def duplicate(self):
        return super().duplicate()

    @view_config(route_name='c2cgeoform_item',
                 request_method='DELETE',
                 renderer='json')
    def delete(self):
        return super().delete()

    @view_config(route_name='c2cgeoform_item',
                 request_method='POST',
                 renderer='../templates/edit.jinja2')
    def save(self):
        return super().save()
