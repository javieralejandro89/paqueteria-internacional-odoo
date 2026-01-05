# Copyright 2024 Javier Alejandro Pérez <myphoneunlockers@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Gestión completa de envíos de paquetería México-Cuba."""

import logging
import math

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from .constants import ESTADOS_MEXICO, FORMAS_PAGO, TIPOS_CLIENTE

_logger = logging.getLogger(__name__)


class PaqueteriaEnvio(models.Model):
    """Envío de paquete con cálculo automático de costos.
    
    Gestiona el proceso completo de envío desde la recepción hasta
    la distribución en maletas. Calcula automáticamente:
    - Peso a cobrar (máximo entre peso etiqueta y volumétrico)
    - Embalaje ($50 por cada 10 lb o fracción)
    - Tarifas dinámicas según tipo de cliente y provincia
    - Impuestos aduanales de artículos
    - Total a cobrar consolidado
    """
    
    _name = 'paqueteria.envio'
    _description = 'Envío de Paquete'
    _order = 'fecha_envio_id desc, name desc'
    
    name = fields.Char(
        string='Número de Envío',
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo',
        index=True,
        help='Número de envío generado automáticamente (ENV-00001)'
    )

    # ========== IMPORTACIÓN DESDE RECEPCIÓN ==========

    recepcion_importar_id = fields.Many2one(
        'paqueteria.recepcion',
        string='Importar desde Recepción',
        help='Selecciona una recepción para copiar sus datos automáticamente'
    )
    
    # ========== REMITENTE (MÉXICO) ==========
    
    remitente_nombre = fields.Char(
        string='Remitente',
        required=True,
        index=True,
        help='Nombre del cliente que envía el paquete'
    )
    
    remitente_telefono = fields.Char(
        string='Teléfono Remitente',
        help='Teléfono de contacto del cliente en México'
    )
    
    tipo_cliente = fields.Selection(
        selection=TIPOS_CLIENTE,
        string='Tipo de Cliente',
        required=True,
        default='normal',
        help='VIP tiene tarifa preferencial: La Habana $140/lb, Resto $170/lb'
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
    
    # ========== PESOS ==========
    
    peso_central = fields.Float(
        string='Peso en Central (lb)',
        digits=(10, 2),
        help='Peso registrado en la central (solo informativo, no afecta cobro)'
    )
    
    peso_etiqueta = fields.Float(
        string='Peso en Etiqueta (lb)',
        digits=(10, 2),
        help='Peso indicado en la etiqueta del paquete'
    )
    
    peso_volumen = fields.Float(
        string='Peso por Volumen (lb)',
        digits=(10, 2),
        help='Peso volumétrico calculado según dimensiones'
    )
    
    peso_cobrar = fields.Float(
        string='Peso a Cobrar (lb)',
        compute='_compute_peso_cobrar',
        store=True,
        digits=(10, 2),
        help='El mayor entre peso en etiqueta y peso volumétrico'
    )
    
    # ========== COSTOS ADICIONALES ==========
    
    articulo_ids = fields.One2many(
        'paqueteria.envio.articulo',
        'envio_id',
        string='Artículos con Impuesto',
        help='Artículos que requieren pago de impuesto aduanal'
    )
    
    impuesto_aduanal = fields.Float(
        string='Impuesto Aduanal ($)',
        compute='_compute_impuesto_aduanal',
        store=True,
        digits=(10, 2),
        help='Suma automática de todos los artículos con impuesto'
    )    
    
    costo_documentos = fields.Float(
        string='Documentos ($)',
        digits=(10, 2),
        help='Costo adicional por envío de documentos (opcional)'
    )
    
    # ========== CÁLCULOS AUTOMÁTICOS ==========
    
    embalaje = fields.Float(
        string='Embalaje ($)',
        compute='_compute_embalaje',
        store=True,
        digits=(10, 2),
        help='$50 MXN por cada 10 lb o fracción'
    )
    
    tarifa_por_lb = fields.Float(
        string='Tarifa por Libra ($)',
        compute='_compute_tarifa',
        store=True,
        digits=(10, 2),
        help='Varía según tipo de cliente y provincia de destino'
    )
    
    subtotal_envio = fields.Float(
        string='Subtotal Envío ($)',
        compute='_compute_totales',
        store=True,
        digits=(10, 2),
        help='Peso a cobrar × Tarifa por lb'
    )
    
    total_cobrar = fields.Float(
        string='Total a Cobrar ($)',
        compute='_compute_totales',
        store=True,
        digits=(10, 2),
        help='Subtotal + Embalaje + Impuestos + Documentos'
    )
    
    # ========== PAGO ==========
    
    forma_pago = fields.Selection(
        selection=FORMAS_PAGO,
        string='Forma de Pago',
        help='Método de pago utilizado por el cliente'
    )

    # ========== MALETA Y DISTRIBUCIÓN ==========
    
    maleta_distribucion_ids = fields.One2many(
        'paqueteria.envio.maleta',
        'envio_id',
        string='Distribución en Maletas',
        help='Cómo se distribuyó este envío en diferentes maletas físicas'
    )
    
    maleta_count = fields.Integer(
        string='Maletas',
        compute='_compute_maleta_count',
        help='Cantidad de maletas en las que se distribuyó este envío'
    )
    
    peso_distribuido = fields.Float(
        string='Peso Distribuido (lb)',
        compute='_compute_peso_distribuido',
        digits=(10, 2),
        help='Suma de pesos ya distribuidos en maletas'
    )
    
    peso_pendiente = fields.Float(
        string='Peso Pendiente (lb)',
        compute='_compute_peso_distribuido',
        digits=(10, 2),
        help='Peso que aún falta por distribuir en maletas'
    )
    
    # ========== CONTROL ==========
    
    admin_id = fields.Many2one(
        'res.users',
        string='Admin que Procesó',
        default=lambda self: self.env.user,
        required=True,
        ondelete='restrict',
        help='Administrador que procesó este envío'
    )
    
    estado_mexico = fields.Selection(
        selection=ESTADOS_MEXICO,
        string='Estado de México',
        required=True,
        help='Estado de México donde opera el administrador'
    )
    
    fecha_envio_id = fields.Many2one(
        'paqueteria.fecha.envio',
        string='Fecha de Envío',
        ondelete='restrict',
        help='Fecha de envío programada para este paquete'
    )
    
    # ========== MÉTODOS COMPUTADOS ==========
    
    @api.depends('peso_etiqueta', 'peso_volumen')
    def _compute_peso_cobrar(self):
        """Calcula el peso a cobrar como el máximo entre pesos.
        
        El peso a cobrar es el MAYOR entre:
        - peso_etiqueta
        - peso_volumen
        
        Nota: peso_central NO se incluye, es solo informativo.
        """
        for record in self:
            record.peso_cobrar = max(
                record.peso_etiqueta or 0,
                record.peso_volumen or 0
            )

    @api.depends('maleta_distribucion_ids.peso_en_maleta')
    def _compute_maleta_count(self):
        """Cuenta en cuántas maletas está distribuido el envío."""
        for record in self:
            record.maleta_count = len(record.maleta_distribucion_ids)
    
    @api.depends('maleta_distribucion_ids.peso_en_maleta', 'peso_cobrar')
    def _compute_peso_distribuido(self):
        """Calcula peso distribuido y peso pendiente por distribuir."""
        for record in self:
            record.peso_distribuido = sum(
                record.maleta_distribucion_ids.mapped('peso_en_maleta')
            )
            record.peso_pendiente = record.peso_cobrar - record.peso_distribuido
    
    @api.onchange('recepcion_importar_id')
    def _onchange_recepcion_importar(self):
        """Importa datos automáticamente desde una recepción seleccionada.
        
        Copia todos los datos relevantes:
        - Remitente y destinatario
        - Provincia de destino
        - Peso en etiqueta
        - Administrador y estado
        """
        if self.recepcion_importar_id:
            recepcion = self.recepcion_importar_id
            
            # Copiar todos los datos
            self.remitente_nombre = recepcion.remitente_nombre
            self.remitente_telefono = recepcion.remitente_telefono
            self.destinatario_nombre = recepcion.destinatario_nombre
            self.destinatario_telefono = recepcion.destinatario_telefono
            self.provincia_id = recepcion.provincia_id.id
            self.peso_etiqueta = recepcion.peso_etiqueta
            self.admin_id = recepcion.admin_id.id
            self.estado_mexico = recepcion.estado_mexico
            
            # Limpiar el campo auxiliar
            self.recepcion_importar_id = False
    
    @api.depends('peso_cobrar')
    def _compute_embalaje(self):
        """Calcula embalaje: $50 por cada 10 lb o fracción.
        
        Ejemplos:
        - 6.3 lb → $50
        - 10.1 lb → $100
        - 20.1 lb → $150
        """
        for record in self:
            if record.peso_cobrar > 0:
                # math.ceil redondea hacia arriba
                record.embalaje = math.ceil(record.peso_cobrar / 10) * 50
            else:
                record.embalaje = 0.0
    
    @api.depends('tipo_cliente', 'provincia_id')
    def _compute_tarifa(self):
        """Calcula tarifa por libra según tipo de cliente y provincia.
        
        Tarifas:
        - VIP + La Habana: $140/lb
        - VIP + Resto: $170/lb
        - Normal + La Habana: $150/lb
        - Normal + Resto: $180/lb
        """
        for record in self:
            if not record.provincia_id:
                record.tarifa_por_lb = 0.0
                continue
            
            # Verificar si es La Habana
            es_habana = record.provincia_id.name.lower() == 'la habana'
            
            if record.tipo_cliente == 'vip':
                record.tarifa_por_lb = 140.0 if es_habana else 170.0
            else:  # normal
                record.tarifa_por_lb = 150.0 if es_habana else 180.0

    @api.depends('articulo_ids.subtotal')
    def _compute_impuesto_aduanal(self):
        """Calcula el impuesto aduanal total sumando todos los artículos."""
        for record in self:
            record.impuesto_aduanal = sum(
                record.articulo_ids.mapped('subtotal')
            )
    
    @api.depends(
        'peso_cobrar',
        'tarifa_por_lb',
        'embalaje',
        'impuesto_aduanal',
        'costo_documentos'
    )
    def _compute_totales(self):
        """Calcula subtotal y total a cobrar del envío.
        
        Subtotal: Peso × Tarifa
        Total: Subtotal + Embalaje + Impuestos + Documentos
        """
        for record in self:
            # Subtotal = Peso × Tarifa
            record.subtotal_envio = record.peso_cobrar * record.tarifa_por_lb
            
            # Total = Subtotal + Embalaje + Extras
            record.total_cobrar = (
                record.subtotal_envio +
                record.embalaje +
                (record.impuesto_aduanal or 0) +
                (record.costo_documentos or 0)
            )
    
    # ========== CRUD METHODS ==========
    
    @api.model_create_multi
    def create(self, vals_list):
        """Crea envíos generando número de secuencia automático.
        
        Args:
            vals_list: Lista de diccionarios con valores para crear
            
        Returns:
            Recordset de envíos creados
            
        Raises:
            ValidationError: Si no se puede generar número de envío
        """
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                sequence = self.env['ir.sequence'].next_by_code(
                    'paqueteria.envio'
                )
                if not sequence:
                    raise ValidationError(
                        _('No se pudo generar el número de envío. '
                          'Verifique que la secuencia esté configurada.')
                    )
                vals['name'] = sequence
                
                _logger.info(
                    'Creando envío %s para %s → %s',
                    sequence,
                    vals.get('remitente_nombre'),
                    vals.get('destinatario_nombre')
                )
        
        return super().create(vals_list)