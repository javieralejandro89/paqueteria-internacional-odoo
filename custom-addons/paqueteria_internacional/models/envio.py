# -*- coding: utf-8 -*-
from odoo import models, fields, api
import math

class PaqueteriaEnvio(models.Model):
    _name = 'paqueteria.envio'
    _description = 'Envío de Paquete'
    _order = 'fecha_envio_id desc, name desc'
    
    name = fields.Char(
        string='Número de Envío',
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo'
    )

    # Campo auxiliar para importar
    recepcion_importar_id = fields.Many2one(
        'paqueteria.recepcion',
        string='Importar desde Recepción',
        help='Selecciona una recepción para copiar sus datos'
    )
    
    # ========== REMITENTE (MÉXICO) ==========
    remitente_nombre = fields.Char(
        string='Remitente',
        required=True,
        help='Nombre del cliente que envía'
    )
    
    remitente_telefono = fields.Char(
        string='Teléfono Remitente',
        help='Teléfono del cliente en México'
    )
    
    tipo_cliente = fields.Selection([
        ('normal', 'Normal'),
        ('vip', 'VIP')
    ], string='Tipo de Cliente', required=True, default='normal',
       help='VIP tiene tarifa preferencial')
    
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
    
    # ========== PESOS ==========
    peso_central = fields.Float(
        string='Peso en Central (lb)',
        digits=(10, 2),
        help='Peso registrado en la central'
    )
    
    peso_etiqueta = fields.Float(
        string='Peso en Etiqueta (lb)',
        digits=(10, 2),
        help='Peso indicado en la etiqueta'
    )
    
    peso_volumen = fields.Float(
        string='Peso por Volumen (lb)',
        digits=(10, 2),
        help='Peso volumétrico calculado'
    )
    
    peso_cobrar = fields.Float(
        string='Peso a Cobrar (lb)',
        compute='_compute_peso_cobrar',
        store=True,
        digits=(10, 2),
        help='El mayor entre peso central, etiqueta y volumen'
    )
    
    # ========== COSTOS ADICIONALES ==========
    articulo_ids = fields.One2many(
        'paqueteria.envio.articulo',
        'envio_id',
        string='Artículos con Impuesto'
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
        digits=(10, 2)
    )
    
    # ========== CÁLCULOS AUTOMÁTICOS ==========
    embalaje = fields.Float(
        string='Embalaje ($)',
        compute='_compute_embalaje',
        store=True,
        digits=(10, 2),
        help='$50 por cada 10 lb o fracción'
    )
    
    tarifa_por_lb = fields.Float(
        string='Tarifa por Libra ($)',
        compute='_compute_tarifa',
        store=True,
        digits=(10, 2),
        help='Varía según tipo de cliente y provincia'
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
        help='Subtotal + Embalaje + Impuestos + Extras'
    )
    
    # ========== PAGO ==========
    forma_pago = fields.Selection([
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia')
    ], string='Forma de Pago')

    # ========== MALETA Y DISTRIBUCIÓN ==========
    maleta_distribucion_ids = fields.One2many(
        'paqueteria.envio.maleta',
        'envio_id',
        string='Distribución en Maletas',
        help='Cómo se distribuyó este envío en diferentes maletas'
    )
    
    maleta_count = fields.Integer(
        string='Maletas',
        compute='_compute_maleta_count'
    )
    
    peso_distribuido = fields.Float(
        string='Peso Distribuido (lb)',
        compute='_compute_peso_distribuido',
        digits=(10, 2),
        help='Suma de pesos distribuidos en maletas'
    )
    
    peso_pendiente = fields.Float(
        string='Peso Pendiente (lb)',
        compute='_compute_peso_distribuido',
        digits=(10, 2),
        help='Peso que falta por distribuir'
    )
    
    # ========== CONTROL ==========
    admin_id = fields.Many2one(
        'res.users',
        string='Admin que Procesó',
        default=lambda self: self.env.user,
        required=True
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
    
    fecha_envio_id = fields.Many2one(
        'paqueteria.fecha.envio',
        string='Fecha de Envío',
        #required=True,
        help='Selecciona la fecha de envío a la que pertenece'
    )
    
    # ========== MÉTODOS COMPUTADOS ==========
    
    @api.depends('peso_etiqueta', 'peso_volumen')
    def _compute_peso_cobrar(self):
        """
        Calcula el peso a cobrar como el MAYOR entre:
        - peso_etiqueta
        - peso_volumen

        NOTA: peso_central NO se incluye, es solo informativo
        """
        for record in self:
            record.peso_cobrar = max(
                record.peso_etiqueta or 0,
                record.peso_volumen or 0
            )
    @api.onchange('peso_etiqueta', 'peso_volumen')
    def _onchange_pesos(self):
        """Actualiza peso_cobrar en tiempo real mientras el usuario escribe"""
        self.peso_cobrar = max(
           self.peso_etiqueta or 0,
           self.peso_volumen or 0
        )   

    @api.depends('maleta_distribucion_ids.peso_en_maleta')
    def _compute_maleta_count(self):
        """Cuenta en cuántas maletas está distribuido"""
        for record in self:
            record.maleta_count = len(record.maleta_distribucion_ids)
    
    @api.depends('maleta_distribucion_ids.peso_en_maleta', 'peso_cobrar')
    def _compute_peso_distribuido(self):
        """Calcula peso distribuido y pendiente"""
        for record in self:
            record.peso_distribuido = sum(record.maleta_distribucion_ids.mapped('peso_en_maleta'))
            record.peso_pendiente = record.peso_cobrar - record.peso_distribuido    
    
    @api.onchange('recepcion_importar_id')
    def _onchange_recepcion_importar(self):
        """Cuando seleccionas una recepción, copia sus datos automáticamente"""
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
        """
        Calcula embalaje: $50 por cada 10 lb o fracción
        Ejemplos:
        - 6.3 lb = $50
        - 10.1 lb = $100
        - 20.1 lb = $150
        """
        for record in self:
            if record.peso_cobrar > 0:
                # math.ceil redondea hacia arriba
                record.embalaje = math.ceil(record.peso_cobrar / 10) * 50
            else:
                record.embalaje = 0.0
    
    @api.depends('tipo_cliente', 'provincia_id')
    def _compute_tarifa(self):
        """
        Calcula tarifa por libra según tipo de cliente y provincia:
        - VIP + Habana = $140
        - VIP + Resto = $170
        - Normal + Habana = $150
        - Normal + Resto = $180
        """
        for record in self:
            if not record.provincia_id:
                record.tarifa_por_lb = 0.0
                continue
            
            # Verificar si es Habana
            es_habana = record.provincia_id.name.lower() == 'la habana'
            
            if record.tipo_cliente == 'vip':
                record.tarifa_por_lb = 140.0 if es_habana else 170.0
            else:  # normal
                record.tarifa_por_lb = 150.0 if es_habana else 180.0

    @api.depends('articulo_ids.subtotal')
    def _compute_impuesto_aduanal(self):
        """Calcula el impuesto aduanal como suma de artículos"""
        for record in self:
            record.impuesto_aduanal = sum(record.articulo_ids.mapped('subtotal'))            
    
    @api.depends('peso_cobrar', 'tarifa_por_lb', 'embalaje', 
                 'impuesto_aduanal', 'costo_documentos')
    def _compute_totales(self):
        """Calcula subtotal y total a cobrar"""
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
    
    @api.model_create_multi
    def create(self, vals_list):
        """Genera número de envío automático al crear"""
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code('paqueteria.envio') or 'Nuevo'
        return super().create(vals_list)