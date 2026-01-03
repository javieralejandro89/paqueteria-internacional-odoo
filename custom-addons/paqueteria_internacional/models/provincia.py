# -*- coding: utf-8 -*-
from odoo import models, fields

class PaqueteriaProvincia(models.Model):
    _name = 'paqueteria.provincia'
    _description = 'Provincia de Cuba'
    _order = 'name'
    
    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre de la provincia'
    )
    
    code = fields.Char(
        string='Código',
        size=3,
        help='Código de la provincia (opcional)'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Si está inactivo, no aparecerá en las opciones'
    )