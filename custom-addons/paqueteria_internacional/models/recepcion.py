# Copyright 2024 Javier Alejandro Pérez <myphoneunlockers@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Gestión de recepciones de paquetes por administradores regionales."""

import logging

from odoo import _, api, fields, models
from .constants import ESTADOS_MEXICO
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaqueteriaRecepcion(models.Model):
    """Recepción de paquetes por administrador regional.
    
    Los administradores regionales registran aquí los paquetes que
    reciben de los clientes, capturando fotografías y descripción
    de la mercancía. Posteriormente estos datos pueden ser importados
    automáticamente al crear un envío.
    """
    
    _name = 'paqueteria.recepcion'
    _description = 'Recepción de Paquete por Admin Regional'
    _order = 'fecha_recepcion desc, id desc'
    
    name = fields.Char(
        string='Número de Recepción',
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo',
        index=True,
        help='Número de recepción generado automáticamente (REC-00001)'
    )
    
    # ========== ADMIN QUE REGISTRÓ ==========
    
    admin_id = fields.Many2one(
        'res.users',
        string='Admin que Recibió',
        default=lambda self: self.env.user,
        required=True,
        ondelete='restrict',
        help='Administrador regional que recibió el paquete del cliente'
    )
    
    estado_mexico = fields.Selection(
        selection=ESTADOS_MEXICO,
        string='Estado de México',
        required=True,
        help='Estado de México donde opera el administrador'
    )
    
    fecha_recepcion = fields.Date(
        string='Fecha de Recepción',
        default=fields.Date.today,
        required=True,
        index=True,
        help='Fecha en que el admin recibió el paquete del cliente'
    )
    
    # ========== REMITENTE (MÉXICO) ==========
    
    remitente_nombre = fields.Char(
        string='Cliente Remitente',
        required=True,
        index=True,
        help='Nombre del cliente que envía el paquete'
    )
    
    remitente_telefono = fields.Char(
        string='Teléfono Remitente',
        help='Teléfono de contacto del cliente en México'
    )
    
    # ========== DESTINATARIO (CUBA) ==========
    
    destinatario_nombre = fields.Char(
        string='Destinatario',
        required=True,
        index=True,
        help='Nombre de quien recibe el paquete en Cuba'
    )
    
    destinatario_telefono = fields.Char(
        string='Teléfono Destinatario',
        help='Teléfono de contacto del destinatario en Cuba'
    )
    
    provincia_id = fields.Many2one(
        'paqueteria.provincia',
        string='Provincia Destino',
        required=True,
        ondelete='restrict',
        help='Provincia de Cuba donde se entregará el paquete'
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
        help='Fotografías de la mercancía recibida para evidencia'
    )
    
    fotos_count = fields.Integer(
        string='Total Fotos',
        compute='_compute_fotos_count',
        help='Cantidad de fotografías adjuntas'
    )
    
    descripcion_articulos = fields.Text(
        string='Descripción de Artículos',
        required=True,
        help='Lista detallada de todos los artículos contenidos en el paquete'
    )
    
    # ========== COMPUTED METHODS ==========
    
    @api.depends('fotos_ids')
    def _compute_fotos_count(self):
        """Cuenta las fotografías adjuntas a la recepción."""
        for record in self:
            record.fotos_count = len(record.fotos_ids)
    
    # ========== CRUD METHODS ==========
    
    @api.model_create_multi
    def create(self, vals_list):
        """Crea recepciones generando número de secuencia automático.
        
        Args:
            vals_list: Lista de diccionarios con valores para crear
            
        Returns:
            Recordset de recepciones creadas
            
        Raises:
            ValidationError: Si no se puede generar número de recepción
        """
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                sequence = self.env['ir.sequence'].next_by_code(
                    'paqueteria.recepcion'
                )
                if not sequence:
                    raise ValidationError(
                        _('No se pudo generar el número de recepción. '
                          'Verifique que la secuencia esté configurada.')
                    )
                vals['name'] = sequence
                
                _logger.info(
                    'Creando recepción %s por admin %s',
                    sequence,
                    vals.get('admin_id')
                )
        
        return super().create(vals_list)
    
    # ========== ACTION METHODS ==========
    
    def action_ver_fotos(self):
        """Abre ventana para ver las fotografías adjuntas.
        
        Returns:
            dict: Acción para abrir ventana de attachments
        """
        self.ensure_one()
        return {
            'name': f'Fotos - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'ir.attachment',
            'view_mode': 'kanban,list,form',
            'domain': [('id', 'in', self.fotos_ids.ids)],
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
            },
        }
    
    # ========== CONSTRAINTS ==========
    
    @api.constrains('peso_etiqueta')
    def _check_peso_positivo(self):
        """Valida que el peso sea mayor a cero."""
        for record in self:
            if record.peso_etiqueta <= 0:
                raise ValidationError(
                    _('El peso debe ser mayor a cero')
                )
    
    _sql_constraints = [
        (
            'peso_etiqueta_positive',
            'CHECK(peso_etiqueta > 0)',
            'El peso en etiqueta debe ser positivo',
        ),
    ]