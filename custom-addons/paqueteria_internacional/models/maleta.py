# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PaqueteriaMaleta(models.Model):
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
        help='Número consecutivo de la maleta'
    )
    
    color = fields.Char(
        string='Color',
        help='Color de la maleta (ej: Azul Clara, Negra, etc.)'
    )
    
    # ========== CONTENIDO (DISTRIBUCIONES) ==========
    distribucion_ids = fields.One2many(
        'paqueteria.envio.maleta',
        'maleta_id',
        string='Distribuciones en esta Maleta',
        help='Distribuciones de envíos que están en esta maleta'
    )
    
    # Envíos únicos (computed)
    envio_ids = fields.Many2many(
        'paqueteria.envio',
        compute='_compute_envio_ids',
        string='Envíos',
        help='Envíos que tienen paquetes en esta maleta'
    )
    
    envio_count = fields.Integer(
        string='Total de Envíos',
        compute='_compute_envio_count'
    )
    
    peso_total = fields.Float(
        string='Peso Total (lb)',
        compute='_compute_peso_total',
        store=True,
        digits=(10, 2),
        help='Suma de pesos de todas las distribuciones'
    )
    
    # ========== CONTROL ==========
    fecha_creacion = fields.Date(
        string='Fecha de Creación',
        default=fields.Date.today,
        required=True
    )

    fecha_envio_id = fields.Many2one(
        'paqueteria.fecha.envio',
        string='Fecha de Envío',
        help='Fecha de envío a la que pertenece esta maleta'
    )
    
    admin_id = fields.Many2one(
        'res.users',
        string='Creado por',
        default=lambda self: self.env.user,
        required=True
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True
    )
    
    # ========== COMPUTED ==========
    
    @api.depends('distribucion_ids.envio_id')
    def _compute_envio_ids(self):
        """Obtiene los envíos únicos que tienen distribuciones en esta maleta"""
        for record in self:
            record.envio_ids = record.distribucion_ids.mapped('envio_id')
    
    @api.depends('envio_ids')
    def _compute_envio_count(self):
        """Cuenta los envíos únicos en la maleta"""
        for record in self:
            record.envio_count = len(record.envio_ids)
    
    @api.depends('distribucion_ids.peso_en_maleta')
    def _compute_peso_total(self):
        """Calcula el peso total de todas las distribuciones"""
        for record in self:
            record.peso_total = sum(record.distribucion_ids.mapped('peso_en_maleta'))