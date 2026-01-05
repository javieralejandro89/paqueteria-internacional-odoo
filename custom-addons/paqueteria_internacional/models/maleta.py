# Copyright 2024 Javier Alejandro Pérez <myphoneunlockers@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Gestión de maletas físicas para transporte."""

from odoo import api, fields, models


class PaqueteriaMaleta(models.Model):
    """Maletas físicas utilizadas para el transporte de envíos.
    
    Cada maleta puede contener distribuciones de múltiples envíos.
    El sistema lleva control del peso total y cantidad de envíos
    que contiene cada maleta.
    """
    
    _name = 'paqueteria.maleta'
    _description = 'Maleta de Envíos'
    _order = 'numero asc'
    
    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre completo de la maleta (ej: Maleta #1 Azul Clara)'
    )
    
    numero = fields.Integer(
        string='Número',
        required=True,
        help='Número consecutivo de la maleta para identificación'
    )
    
    color = fields.Char(
        string='Color',
        help='Color de la maleta para identificación visual (ej: Azul Clara, Negra)'
    )
    
    # ========== CONTENIDO (DISTRIBUCIONES) ==========
    
    distribucion_ids = fields.One2many(
        'paqueteria.envio.maleta',
        'maleta_id',
        string='Distribuciones en esta Maleta',
        help='Distribuciones de pesos de envíos que están en esta maleta'
    )
    
    envio_ids = fields.Many2many(
        'paqueteria.envio',
        compute='_compute_envio_ids',
        string='Envíos',
        help='Envíos únicos que tienen distribuciones en esta maleta'
    )
    
    envio_count = fields.Integer(
        string='Total de Envíos',
        compute='_compute_envio_count',
        help='Cantidad de envíos diferentes en esta maleta'
    )
    
    peso_total = fields.Float(
        string='Peso Total (lb)',
        compute='_compute_peso_total',
        store=True,
        digits=(10, 2),
        help='Suma de pesos de todas las distribuciones en esta maleta'
    )
    
    # ========== CONTROL ==========
    
    fecha_creacion = fields.Date(
        string='Fecha de Creación',
        default=fields.Date.today,
        required=True,
        help='Fecha en que se creó el registro de la maleta'
    )

    fecha_envio_id = fields.Many2one(
        'paqueteria.fecha.envio',
        string='Fecha de Envío',
        ondelete='restrict',
        help='Fecha de envío programada para esta maleta'
    )
    
    admin_id = fields.Many2one(
        'res.users',
        string='Creado por',
        default=lambda self: self.env.user,
        required=True,
        ondelete='restrict',
        help='Usuario que creó el registro de la maleta'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Si está inactivo, no aparecerá en las opciones de distribución'
    )
    
    # ========== COMPUTED METHODS ==========
    
    @api.depends('distribucion_ids.envio_id')
    def _compute_envio_ids(self):
        """Obtiene los envíos únicos que tienen distribuciones en esta maleta."""
        for record in self:
            record.envio_ids = record.distribucion_ids.mapped('envio_id')
    
    @api.depends('envio_ids')
    def _compute_envio_count(self):
        """Cuenta los envíos únicos en la maleta."""
        for record in self:
            record.envio_count = len(record.envio_ids)
    
    @api.depends('distribucion_ids.peso_en_maleta')
    def _compute_peso_total(self):
        """Calcula el peso total sumando todas las distribuciones."""
        for record in self:
            record.peso_total = sum(
                record.distribucion_ids.mapped('peso_en_maleta')
            )