# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PaqueteriaRecepcion(models.Model):
    _name = 'paqueteria.recepcion'
    _description = 'Recepción de Paquete por Admin Regional'
    _order = 'fecha_recepcion desc, id desc'
    
    name = fields.Char(
        string='Número de Recepción',
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo'
    )
    
    # ========== ADMIN QUE REGISTRÓ ==========
    admin_id = fields.Many2one(
        'res.users',
        string='Admin que Recibió',
        default=lambda self: self.env.user,
        required=True,
        help='Admin regional que recibió el paquete del cliente'
    )
    
    estado_mexico = fields.Selection([
        ('aguascalientes', 'Aguascalientes'),
        ('baja_california', 'Baja California'),
        ('baja_california_sur', 'Baja California Sur'),
        ('monterrey', 'Monterrey'),
        ('campeche', 'Campeche'),
        ('chiapas', 'Chiapas'),
        ('chihuahua', 'Chihuahua'),
        ('cdmx', 'Ciudad de México'),
        ('coahuila', 'Coahuila'),
        ('colima', 'Colima'),
        ('durango', 'Durango'),
        ('estado_mexico', 'Estado de México'),
        ('guanajuato', 'Guanajuato'),
        ('guerrero', 'Guerrero'),
        ('hidalgo', 'Hidalgo'),
        ('jalisco', 'Jalisco'),
        ('michoacan', 'Michoacán'),
        ('morelos', 'Morelos'),
        ('nayarit', 'Nayarit'),
        ('nuevo_leon', 'Nuevo León'),
        ('oaxaca', 'Oaxaca'),
        ('puebla', 'Puebla'),
        ('puerto_vallarta', 'Puerto Vallarta'),
        ('queretaro', 'Querétaro'),
        ('cancun', 'Cancún'),
        ('san_luis_potosi', 'San Luis Potosí'),
        ('saltillo', 'Saltillo'),
        ('sinaloa', 'Sinaloa'),
        ('sonora', 'Sonora'),
        ('tabasco', 'Tabasco'),
        ('tamaulipas', 'Tamaulipas'),
        ('texcoco', 'Texcoco'),
        ('tijuana', 'Tijuana'),
        ('toluca', 'Toluca'),
        ('tlaxcala', 'Tlaxcala'),
        ('veracruz', 'Veracruz'),
        ('yucatan', 'Yucatán'),
        ('zacatecas', 'Zacatecas'),
    ], string='Estado de México', required=True,
       help='Estado de México donde opera el admin')
    
    fecha_recepcion = fields.Date(
        string='Fecha de Recepción',
        default=fields.Date.today,
        required=True,
        help='Fecha en que el admin recibió el paquete'
    )
    
    # ========== REMITENTE (MÉXICO) ==========
    remitente_nombre = fields.Char(
        string='Cliente Remitente',
        required=True,
        help='Nombre del cliente que envía el paquete'
    )
    
    remitente_telefono = fields.Char(
        string='Teléfono Remitente',
        help='Teléfono del cliente en México'
    )
    
    # ========== DESTINATARIO (CUBA) ==========
    destinatario_nombre = fields.Char(
        string='Destinatario',
        required=True,
        help='Nombre de quien recibe en Cuba'
    )
    
    destinatario_telefono = fields.Char(
        string='Teléfono Destinatario',
        help='Teléfono del destinatario en Cuba'
    )
    
    provincia_id = fields.Many2one(
        'paqueteria.provincia',
        string='Provincia Destino',
        required=True,
        help='Provincia de Cuba donde se entrega'
    )
    
    # ========== PESO ==========
    peso_etiqueta = fields.Float(
        string='Peso en Etiqueta (lb)',
        digits=(10, 2),
        required=True,
        help='Peso que el admin pesó y cobró al cliente'
    )
    
    # ========== CONTENIDO ==========
    fotos_ids = fields.Many2many(
        'ir.attachment',
        'recepcion_attachment_rel',
        'recepcion_id',
        'attachment_id',
        string='Fotos del Paquete',
        help='Fotos de la mercancía recibida'
    )
    
    fotos_count = fields.Integer(
        string='Total Fotos',
        compute='_compute_fotos_count'
    )
    
    descripcion_articulos = fields.Text(
        string='Descripción de Artículos',
        required=True,
        help='Lista detallada de artículos en el paquete'
    )
    
    # ========== COMPUTED ==========
    
    @api.depends('fotos_ids')
    def _compute_fotos_count(self):
        """Cuenta las fotos adjuntas"""
        for record in self:
            record.fotos_count = len(record.fotos_ids)
    
    @api.model_create_multi
    def create(self, vals_list):
        """Genera número de recepción automático"""
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('paqueteria.recepcion') or 'Nuevo'
        return super().create(vals_list)
    
    def action_ver_fotos(self):
        """Acción para ver fotos en ventana aparte"""
        self.ensure_one()
        return {
            'name': f'Fotos - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'ir.attachment',
            'view_mode': 'kanban,list,form',
            'domain': [('id', 'in', self.fotos_ids.ids)],
            'context': {'default_res_model': self._name, 'default_res_id': self.id}
        }