# Copyright 2024 Javier Alejandro Pérez <myphoneunlockers@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Distribución de envíos en maletas físicas."""

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PaqueteriaEnvioMaleta(models.Model):
    """Distribución de peso de un envío en una maleta específica.
    
    Modelo de relación Many2many entre envíos y maletas que permite
    distribuir el peso de un envío en múltiples maletas. Incluye
    validaciones para asegurar que la suma de pesos distribuidos
    no exceda el peso total del envío.
    """
    
    _name = 'paqueteria.envio.maleta'
    _description = 'Distribución de Envío en Maletas'
    _order = 'maleta_id, id'
    
    envio_id = fields.Many2one(
        'paqueteria.envio',
        string='Envío',
        required=True,
        ondelete='cascade',
        help='Envío que se está distribuyendo en maletas'
    )
    
    maleta_id = fields.Many2one(
        'paqueteria.maleta',
        string='Maleta',
        required=True,
        ondelete='restrict',
        help='Maleta física donde se guarda parte o todo el envío'
    )
    
    peso_en_maleta = fields.Float(
        string='Peso en esta Maleta (lb)',
        required=True,
        digits=(10, 2),
        help='Peso del paquete que se guardó en esta maleta específica'
    )
    
    descripcion_empaque = fields.Char(
        string='Descripción del Empaque',
        required=True,
        help='Cómo se empacó en esta maleta (ej: 2 bolsas azules, 1 nylon transparente, 1 caja negra)'
    )
    
    # ========== CAMPOS RELACIONALES PARA VISTAS ==========
    
    remitente_nombre = fields.Char(
        related='envio_id.remitente_nombre',
        string='Remitente',
        store=True,
        help='Nombre del remitente del envío (para búsquedas)'
    )
    
    provincia_id = fields.Many2one(
        related='envio_id.provincia_id',
        string='Provincia',
        store=True,
        help='Provincia de destino del envío (para filtros)'
    )
    
    peso_total_envio = fields.Float(
        related='envio_id.peso_cobrar',
        string='Peso Total del Envío',
        store=True,
        help='Peso total a cobrar del envío (para validación)'
    )
    
    # ========== CONSTRAINTS ==========
    
    @api.constrains('peso_en_maleta', 'envio_id')
    def _check_peso_valido(self):
        """Valida que la distribución de pesos sea coherente.
        
        Verifica:
        1. El peso en maleta sea mayor a 0
        2. La suma de pesos distribuidos no exceda el peso total del envío
        
        Raises:
            ValidationError: Si el peso es <= 0 o si la suma excede el total
        """
        for record in self:
            if record.peso_en_maleta <= 0:
                raise ValidationError('El peso debe ser mayor a 0')
            
            total_distribuido = sum(
                record.envio_id.maleta_distribucion_ids.mapped('peso_en_maleta')
            )
            
            if total_distribuido > record.peso_total_envio:
                raise ValidationError(
                    f'La suma de pesos en maletas ({total_distribuido} lb) '
                    f'excede el peso total del envío ({record.peso_total_envio} lb)'
                )