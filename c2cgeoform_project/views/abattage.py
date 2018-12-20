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

from ..models.abattage import Demande, Essence

_list_field = partial(ListField, Demande)

base_schema = GeoFormSchemaNode(Demande)


@view_defaults(match_param='table=abattage')
class AbattageViews(AbstractViews):

    _model = Demande
    _base_schema = base_schema
    _id_field = 'id'

    _list_fields = [
        _list_field('id',visible=False),
        _list_field('proprietaire'),
        _list_field('parcelle'),
        _list_field('adresse'),
        _list_field('essence', 
                    renderer=lambda demande: demande.essence.name,
                    filter_column=Essence.name,
                    sort_column=Essence.name)
    ]

    def _base_query(self):
        return super()._base_query(). \
            outerjoin('essence'). \
            options(subqueryload('essence'))

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
