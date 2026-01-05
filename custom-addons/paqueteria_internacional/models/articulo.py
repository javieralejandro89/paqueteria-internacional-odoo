# Copyright 2024 Javier Alejandro Pérez <myphoneunlockers@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Catálogo de artículos con impuesto aduanal."""

from odoo import fields, models
from .constants import TIPOS_ARTICULO


class PaqueteriaArticulo(models.Model):
    """Artículos que requieren pago de impuesto aduanal.
    
    Define el catálogo de artículos con sus respectivos costos
    aduanales. Los artículos tipo 'celular' y 'laptop_tablet' tienen
    precios dinámicos calculados según tipo de cliente y provincia.
    Los de tipo 'otro' tienen precio fijo configurable.
    """
    
    _name = 'paqueteria.articulo'
    _description = 'Artículo con Impuesto Aduanal'
    _order = 'tipo_articulo, name asc'
    
    name = fields.Char(
        string='Artículo',
        required=True,
        help='Nombre del artículo (ej: iPhone 15, Laptop Dell, Mando PS5)'
    )
    
    tipo_articulo = fields.Selection(
        selection=TIPOS_ARTICULO,
        string='Tipo de Artículo',
        required=True,
        default='otro',
        help='El tipo determina cómo se calcula el precio: '
             'Celulares y Laptops usan precios dinámicos según cliente y destino, '
             'Otros usan el precio fijo definido en costo_aduanal'
    )
    
    costo_aduanal = fields.Float(
        string='Costo Aduanal Fijo ($)',
        digits=(10, 2),
        help='Solo para artículos tipo "Otro". '
             'Celulares y Laptops calculan precio automáticamente'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Si está inactivo, no aparecerá en las opciones al crear envíos'
    )