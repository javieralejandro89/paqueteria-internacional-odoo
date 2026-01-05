# Copyright 2024 Javier Alejandro Pérez <myphoneunlockers@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Gestión de fechas de envío y estadísticas."""

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PaqueteriaFechaEnvio(models.Model):
    """Fecha de envío con estadísticas consolidadas.
    
    Este modelo agrupa envíos y maletas por fecha, calculando
    automáticamente estadísticas financieras y operativas incluyendo:
    - Total de envíos y maletas
    - Peso total transportado
    - Total cobrado separado por forma de pago
    - Provincias de destino
    """
    
    _name = 'paqueteria.fecha.envio'
    _description = 'Fecha de Envío'
    _order = 'fecha desc'
    
    # ========== IDENTIFICACIÓN ==========
    
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
        index=True,
        help='Fecha en que se realizará el envío'
    )
    
    # ========== RELACIONES ==========
    
    envio_ids = fields.One2many(
        'paqueteria.envio',
        'fecha_envio_id',
        string='Envíos',
        help='Envíos programados para esta fecha'
    )
    
    maleta_ids = fields.One2many(
        'paqueteria.maleta',
        'fecha_envio_id',
        string='Maletas',
        help='Maletas asociadas a esta fecha de envío'
    )
    
    # ========== ESTADÍSTICAS OPERATIVAS ==========
    
    total_envios = fields.Integer(
        string='Total Envíos',
        compute='_compute_totales',
        store=True,
        help='Cantidad total de envíos programados'
    )
    
    total_maletas = fields.Integer(
        string='Total Maletas',
        compute='_compute_totales',
        store=True,
        help='Cantidad total de maletas preparadas'
    )
    
    peso_total = fields.Float(
        string='Peso Total (lb)',
        compute='_compute_totales',
        store=True,
        digits=(10, 2),
        help='Suma del peso a cobrar de todos los envíos'
    )
    
    # ========== ESTADÍSTICAS FINANCIERAS ==========
    
    total_cobrado = fields.Float(
        string='Total Cobrado ($)',
        compute='_compute_totales',
        store=True,
        digits=(10, 2),
        help='Total cobrado de todos los envíos (efectivo + transferencia)'
    )
    
    total_cobrado_efectivo = fields.Float(
        string='Total Efectivo ($)',
        compute='_compute_totales_por_forma_pago',
        store=True,
        digits=(10, 2),
        help='Total cobrado en efectivo'
    )
    
    total_cobrado_transferencia = fields.Float(
        string='Total Transferencia ($)',
        compute='_compute_totales_por_forma_pago',
        store=True,
        digits=(10, 2),
        help='Total cobrado por transferencia bancaria'
    )
    
    # ========== INFORMACIÓN GEOGRÁFICA ==========
    
    provincias_destino = fields.Char(
        string='Provincias',
        compute='_compute_provincias',
        help='Provincias de destino en este envío'
    )
    
    # ========== COMPUTED METHODS ==========
    
    @api.depends('fecha')
    def _compute_name(self):
        """Genera nombre automático basado en la fecha.
        
        Formato: "Envío DD-MM-YYYY"
        Ejemplo: "Envío 08-01-2026"
        """
        for record in self:
            if record.fecha:
                record.name = record.fecha.strftime('Envío %d-%m-%Y')
            else:
                record.name = "Nuevo Envío"
    
    @api.depends(
        'envio_ids',
        'maleta_ids',
        'envio_ids.peso_cobrar',
        'envio_ids.total_cobrar',
    )
    def _compute_totales(self):
        """Calcula totales operativos y financieros generales.
        
        Calcula:
        - total_envios: Cantidad de envíos
        - total_maletas: Cantidad de maletas
        - peso_total: Suma de pesos a cobrar
        - total_cobrado: Suma total sin importar forma de pago
        """
        for record in self:
            record.total_envios = len(record.envio_ids)
            record.total_maletas = len(record.maleta_ids)
            record.peso_total = sum(record.envio_ids.mapped('peso_cobrar'))
            record.total_cobrado = sum(record.envio_ids.mapped('total_cobrar'))
            
            _logger.debug(
                'Totales calculados para %s: %d envíos, %d maletas, '
                '%.2f lb, $%.2f',
                record.name,
                record.total_envios,
                record.total_maletas,
                record.peso_total,
                record.total_cobrado,
            )
    
    @api.depends('envio_ids.total_cobrar', 'envio_ids.forma_pago')
    def _compute_totales_por_forma_pago(self):
        """Calcula totales separados por forma de pago.
        
        Separa el total cobrado en:
        - Efectivo: Suma de envíos con forma_pago = 'efectivo'
        - Transferencia: Suma de envíos con forma_pago = 'transferencia'
        
        Nota: Envíos sin forma de pago definida no se incluyen en ninguna suma.
        """
        for record in self:
            # Filtrar envíos por forma de pago
            envios_efectivo = record.envio_ids.filtered(
                lambda e: e.forma_pago == 'efectivo'
            )
            envios_transferencia = record.envio_ids.filtered(
                lambda e: e.forma_pago == 'transferencia'
            )
            
            # Sumar totales
            record.total_cobrado_efectivo = sum(
                envios_efectivo.mapped('total_cobrar')
            )
            record.total_cobrado_transferencia = sum(
                envios_transferencia.mapped('total_cobrar')
            )
            
            _logger.debug(
                'Totales por forma de pago para %s: Efectivo $%.2f, '
                'Transferencia $%.2f',
                record.name,
                record.total_cobrado_efectivo,
                record.total_cobrado_transferencia,
            )
    
    @api.depends('envio_ids.provincia_id')
    def _compute_provincias(self):
        """Lista las provincias de destino únicas.
        
        Muestra hasta 3 provincias, si hay más agrega "... (+N)"
        Ejemplo: "La Habana, Santiago de Cuba, Holguín... (+2)"
        """
        for record in self:
            provincias = record.envio_ids.mapped('provincia_id.name')
            if provincias:
                # Obtener provincias únicas
                provincias_unicas = sorted(set(provincias))
                
                if len(provincias_unicas) <= 3:
                    record.provincias_destino = ', '.join(provincias_unicas)
                else:
                    primeras_tres = ', '.join(provincias_unicas[:3])
                    restantes = len(provincias_unicas) - 3
                    record.provincias_destino = f"{primeras_tres}... (+{restantes})"
            else:
                record.provincias_destino = 'Sin envíos'