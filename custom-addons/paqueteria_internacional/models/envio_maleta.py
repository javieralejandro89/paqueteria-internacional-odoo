# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PaqueteriaEnvioMaleta(models.Model):
    _name = 'paqueteria.envio.maleta'
    _description = 'Distribución de Envío en Maletas'
    _order = 'maleta_id, id'
    
    envio_id = fields.Many2one(
        'paqueteria.envio',
        string='Envío',
        required=True,
        ondelete='cascade'
    )
    
    maleta_id = fields.Many2one(
        'paqueteria.maleta',
        string='Maleta',
        required=True,
        ondelete='restrict'
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
        help='Cómo se empacó en esta maleta (ej: 2 bolsas azules, 1 nylon transparente)'
    )
    
    # Campos relacionales para vistas
    remitente_nombre = fields.Char(
        related='envio_id.remitente_nombre',
        string='Remitente',
        store=True
    )
    
    provincia_id = fields.Many2one(
        related='envio_id.provincia_id',
        string='Provincia',
        store=True
    )
    
    peso_total_envio = fields.Float(
        related='envio_id.peso_cobrar',
        string='Peso Total del Envío',
        store=True
    )
    
    @api.constrains('peso_en_maleta', 'envio_id')
    def _check_peso_valido(self):
        """Valida que la suma de pesos en maletas no exceda el peso total del envío"""
        for record in self:
            if record.peso_en_maleta <= 0:
                raise ValidationError('El peso debe ser mayor a 0')
            
            total_distribuido = sum(record.envio_id.maleta_distribucion_ids.mapped('peso_en_maleta'))
            if total_distribuido > record.peso_total_envio:
                raise ValidationError(
                    f'La suma de pesos en maletas ({total_distribuido} lb) '
                    f'excede el peso total del envío ({record.peso_total_envio} lb)'
                )