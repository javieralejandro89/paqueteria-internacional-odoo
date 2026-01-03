# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PaqueteriaEnvioArticulo(models.Model):
    _name = 'paqueteria.envio.articulo'
    _description = 'Artículos con Impuesto en Envío'
    _order = 'id'
    
    envio_id = fields.Many2one(
        'paqueteria.envio',
        string='Envío',
        required=True,
        ondelete='cascade'
    )
    
    articulo_id = fields.Many2one(
        'paqueteria.articulo',
        string='Artículo',
        required=True,
        domain=[('active', '=', True)]
    )
    
    tipo_articulo = fields.Selection(
        related='articulo_id.tipo_articulo',
        string='Tipo',
        store=True
    )
    
    cantidad = fields.Integer(
        string='Cantidad',
        required=True,
        default=1
    )
    
    costo_unitario = fields.Float(
        string='Costo Unitario ($)',
        compute='_compute_costo_unitario',
        store=True,
        digits=(10, 2)
    )
    
    subtotal = fields.Float(
        string='Subtotal ($)',
        compute='_compute_subtotal',
        store=True,
        digits=(10, 2)
    )
    
    # Campos relacionales para cálculo
    tipo_cliente = fields.Selection(related='envio_id.tipo_cliente', store=True)
    provincia_id = fields.Many2one(related='envio_id.provincia_id', store=True)
    
    @api.depends('articulo_id', 'tipo_cliente', 'provincia_id')
    def _compute_costo_unitario(self):
        """
        Calcula el costo unitario según tipo de artículo, cliente y destino
        
        CELULARES:
          Normal Habana: $800
          Normal Resto: $1000
          VIP Habana: $700
          VIP Resto: $900
        
        LAPTOPS/TABLETS:
          Normal Habana: $1000
          Normal Resto: $1300
          VIP Habana: $800
          VIP Resto: $1100
        
        OTROS:
          Precio fijo del catálogo
        """
        for record in self:
            if not record.articulo_id:
                record.costo_unitario = 0
                continue
            
            tipo = record.tipo_articulo
            es_habana = record.provincia_id.name == 'La Habana' if record.provincia_id else False
            es_vip = record.tipo_cliente == 'vip'
            
            # CELULARES
            if tipo == 'celular':
                if es_vip:
                    # VIP: Habana $700, Resto $900
                    record.costo_unitario = 700 if es_habana else 900
                else:
                    # Normal: Habana $800, Resto $1000
                    record.costo_unitario = 800 if es_habana else 1000
            
            # LAPTOPS/TABLETS
            elif tipo == 'laptop_tablet':
                if es_vip:
                    # VIP: Habana $800, Resto $1100
                    record.costo_unitario = 800 if es_habana else 1100
                else:
                    # Normal: Habana $1000, Resto $1300
                    record.costo_unitario = 1000 if es_habana else 1300
            
            # OTROS (precio fijo)
            else:
                record.costo_unitario = record.articulo_id.costo_aduanal or 0
    
    @api.depends('cantidad', 'costo_unitario')
    def _compute_subtotal(self):
        """Calcula el subtotal (cantidad × costo)"""
        for record in self:
            record.subtotal = record.cantidad * record.costo_unitario