# Copyright 2024 Javier Alejandro Pérez <myphoneunlockers@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Relación entre envíos y artículos con impuesto aduanal."""

from odoo import api, fields, models


class PaqueteriaEnvioArticulo(models.Model):
    """Artículos con impuesto aduanal en un envío específico.
    
    Línea de detalle que relaciona un envío con los artículos que
    contiene y que requieren pago de impuesto aduanal. Calcula
    automáticamente el costo según el tipo de artículo, cliente
    y provincia de destino.
    """
    
    _name = 'paqueteria.envio.articulo'
    _description = 'Artículos con Impuesto en Envío'
    _order = 'id'
    
    envio_id = fields.Many2one(
        'paqueteria.envio',
        string='Envío',
        required=True,
        ondelete='cascade',
        help='Envío al que pertenece este artículo'
    )
    
    articulo_id = fields.Many2one(
        'paqueteria.articulo',
        string='Artículo',
        required=True,
        domain=[('active', '=', True)],
        help='Artículo del catálogo que requiere impuesto aduanal'
    )
    
    tipo_articulo = fields.Selection(
        related='articulo_id.tipo_articulo',
        string='Tipo',
        store=True,
        help='Tipo de artículo (determina cálculo de precio)'
    )
    
    cantidad = fields.Integer(
        string='Cantidad',
        required=True,
        default=1,
        help='Cantidad de unidades de este artículo'
    )
    
    costo_unitario = fields.Float(
        string='Costo Unitario ($)',
        compute='_compute_costo_unitario',
        store=True,
        digits=(10, 2),
        help='Costo de impuesto aduanal por unidad calculado automáticamente'
    )
    
    subtotal = fields.Float(
        string='Subtotal ($)',
        compute='_compute_subtotal',
        store=True,
        digits=(10, 2),
        help='Total de impuesto: cantidad × costo unitario'
    )
    
    # ========== CAMPOS RELACIONALES PARA CÁLCULO ==========
    
    tipo_cliente = fields.Selection(
        related='envio_id.tipo_cliente',
        store=True,
        help='Tipo de cliente del envío (afecta tarifa)'
    )
    
    provincia_id = fields.Many2one(
        related='envio_id.provincia_id',
        store=True,
        help='Provincia de destino del envío (afecta tarifa)'
    )
    
    # ========== COMPUTED METHODS ==========
    
    @api.depends('articulo_id', 'tipo_cliente', 'provincia_id')
    def _compute_costo_unitario(self):
        """Calcula el costo unitario según tipo de artículo, cliente y destino.
        
        Tarifas de impuesto aduanal:
        
        CELULARES:
          - Normal + Habana: $800
          - Normal + Resto: $1,000
          - VIP + Habana: $700
          - VIP + Resto: $900
        
        LAPTOPS/TABLETS:
          - Normal + Habana: $1,000
          - Normal + Resto: $1,300
          - VIP + Habana: $800
          - VIP + Resto: $1,100
        
        OTROS:
          - Precio fijo del catálogo (articulo.costo_aduanal)
        """
        for record in self:
            if not record.articulo_id:
                record.costo_unitario = 0
                continue
            
            tipo = record.tipo_articulo
            es_habana = (
                record.provincia_id.name == 'La Habana' 
                if record.provincia_id else False
            )
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
        """Calcula el subtotal: cantidad × costo unitario."""
        for record in self:
            record.subtotal = record.cantidad * record.costo_unitario