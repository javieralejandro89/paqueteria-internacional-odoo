# Copyright 2024 Javier Alejandro Pérez <myphoneunlockers@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Gestión de provincias de Cuba."""

from odoo import fields, models


class PaqueteriaProvincia(models.Model):
    """Provincias de Cuba para destinos de envío.
    
    Catálogo de las 16 provincias de Cuba utilizadas para
    determinar tarifas y destinos de los envíos.
    """
    
    _name = 'paqueteria.provincia'
    _description = 'Provincia de Cuba'
    _order = 'name'
    
    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre de la provincia cubana'
    )
    
    code = fields.Char(
        string='Código',
        size=3,
        help='Código de dos letras de la provincia (opcional)'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Si está inactivo, no aparecerá en las opciones de destino'
    )