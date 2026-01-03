# -*- coding: utf-8 -*-
from odoo import models, fields

class PaqueteriaArticulo(models.Model):
    _name = 'paqueteria.articulo'
    _description = 'Artículo con Impuesto Aduanal'
    _order = 'tipo_articulo, name asc'
    
    name = fields.Char(
        string='Artículo',
        required=True,
        help='Nombre del artículo (ej: iPhone 15, Laptop Dell, Mando PS5)'
    )
    
    tipo_articulo = fields.Selection([
        ('celular', 'Celulares'),
        ('laptop_tablet', 'Laptop/Tablet'),
        ('otro', 'Otro (Precio Fijo)'),
    ], string='Tipo de Artículo',
       required=True,
       default='otro',
       help='El tipo determina cómo se calcula el precio')
    
    costo_aduanal = fields.Float(
        string='Costo Aduanal Fijo ($)',
        digits=(10, 2),
        help='Solo para artículos tipo "Otro". Celulares y Laptops usan precios dinámicos.'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True
    )