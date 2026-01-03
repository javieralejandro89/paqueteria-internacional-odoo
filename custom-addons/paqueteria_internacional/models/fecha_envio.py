# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PaqueteriaFechaEnvio(models.Model):
    _name = 'paqueteria.fecha.envio'
    _description = 'Fecha de Envío'
    _order = 'fecha desc'
    
    name = fields.Char(
        string='Nombre',
        compute='_compute_name',
        store=True,
        help='Nombre generado automáticamente (ej: Envío 08-01-2026)'
    )
    
    fecha = fields.Date(
        string='Fecha de Envío',
        required=True,
        default=fields.Date.today,
        help='Fecha en que se realizará el envío'
    )
    
    # ========== RELACIONES ==========
    envio_ids = fields.One2many(
        'paqueteria.envio',
        'fecha_envio_id',
        string='Envíos'
    )
    
    maleta_ids = fields.One2many(
        'paqueteria.maleta',
        'fecha_envio_id',
        string='Maletas'
    )
    
    # ========== ESTADÍSTICAS ==========
    total_envios = fields.Integer(
        string='Total Envíos',
        compute='_compute_totales',
        store=True
    )
    
    total_maletas = fields.Integer(
        string='Total Maletas',
        compute='_compute_totales',
        store=True
    )
    
    peso_total = fields.Float(
        string='Peso Total (lb)',
        compute='_compute_totales',
        store=True,
        digits=(10, 2)
    )
    
    total_cobrado = fields.Float(
        string='Total Cobrado ($)',
        compute='_compute_totales',
        store=True,
        digits=(10, 2)
    )
    
    provincias_destino = fields.Char(
        string='Provincias',
        compute='_compute_provincias',
        help='Provincias de destino en este envío'
    )
    
    # ========== COMPUTED ==========
    
    @api.depends('fecha')
    def _compute_name(self):
        """Genera nombre automático basado en fecha"""
        for record in self:
            if record.fecha:
                record.name = f"Envío {record.fecha.strftime('%d-%m-%Y')}"
            else:
                record.name = "Nuevo Envío"
    
    @api.depends('envio_ids', 'maleta_ids', 'envio_ids.peso_cobrar', 'envio_ids.total_cobrar')
    def _compute_totales(self):
        """Calcula totales de envíos, maletas, peso y dinero"""
        for record in self:
            record.total_envios = len(record.envio_ids)
            record.total_maletas = len(record.maleta_ids)
            record.peso_total = sum(record.envio_ids.mapped('peso_cobrar'))
            record.total_cobrado = sum(record.envio_ids.mapped('total_cobrar'))
    
    @api.depends('envio_ids.provincia_id')
    def _compute_provincias(self):
        """Lista las provincias de destino"""
        for record in self:
            provincias = record.envio_ids.mapped('provincia_id.name')
            if provincias:
                # Contar provincias únicas
                provincias_unicas = list(set(provincias))
                if len(provincias_unicas) <= 3:
                    record.provincias_destino = ', '.join(provincias_unicas)
                else:
                    record.provincias_destino = f"{', '.join(provincias_unicas[:3])}... (+{len(provincias_unicas)-3})"
            else:
                record.provincias_destino = 'Sin envíos'