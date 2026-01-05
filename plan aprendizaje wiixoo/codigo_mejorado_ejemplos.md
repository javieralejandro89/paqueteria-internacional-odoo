# 💻 Código Mejorado - Ejemplos Concretos
## Transformación según Estándares Wiixoo y OCA

---

## 1. CONSTANTS.PY (NUEVO ARCHIVO)

### Crear: `models/constants.py`

```python
# Copyright 2024 Javier Alejandro Pérez <tu@email.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Constantes compartidas del módulo paquetería internacional."""

# Estados de México
ESTADOS_MEXICO = [
    ('aguascalientes', 'Aguascalientes'),
    ('baja_california', 'Baja California'),
    ('baja_california_sur', 'Baja California Sur'),
    ('campeche', 'Campeche'),
    ('cdmx', 'Ciudad de México'),
    ('chiapas', 'Chiapas'),
    ('chihuahua', 'Chihuahua'),
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
    ('queretaro', 'Querétaro'),
    ('san_luis_potosi', 'San Luis Potosí'),
    ('sinaloa', 'Sinaloa'),
    ('sonora', 'Sonora'),
    ('tabasco', 'Tabasco'),
    ('tamaulipas', 'Tamaulipas'),
    ('tlaxcala', 'Tlaxcala'),
    ('veracruz', 'Veracruz'),
    ('yucatan', 'Yucatán'),
    ('zacatecas', 'Zacatecas'),
]

# Tipos de artículo
TIPO_ARTICULO_CELULAR = 'celular'
TIPO_ARTICULO_LAPTOP = 'laptop_tablet'
TIPO_ARTICULO_OTRO = 'otro'

TIPOS_ARTICULO = [
    (TIPO_ARTICULO_CELULAR, 'Celulares'),
    (TIPO_ARTICULO_LAPTOP, 'Laptop/Tablet'),
    (TIPO_ARTICULO_OTRO, 'Otro (Precio Fijo)'),
]

# Tipos de cliente
TIPO_CLIENTE_NORMAL = 'normal'
TIPO_CLIENTE_VIP = 'vip'

TIPOS_CLIENTE = [
    (TIPO_CLIENTE_NORMAL, 'Normal'),
    (TIPO_CLIENTE_VIP, 'VIP'),
]

# Formas de pago
FORMA_PAGO_EFECTIVO = 'efectivo'
FORMA_PAGO_TRANSFERENCIA = 'transferencia'

FORMAS_PAGO = [
    (FORMA_PAGO_EFECTIVO, 'Efectivo'),
    (FORMA_PAGO_TRANSFERENCIA, 'Transferencia'),
]

# Tarifas (podrían venir de modelo configurable después)
TARIFA_EMBALAJE_POR_10LB = 50.0
PROVINCIA_HABANA = 'La Habana'
```

---

## 2. ENVIO.PY MEJORADO

### Reemplazar: `models/envio.py`

```python
# Copyright 2024 Javier Alejandro Pérez <tu@email.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Gestión de envíos de paquetería internacional."""

import math
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from .constants import (
    ESTADOS_MEXICO,
    FORMAS_PAGO,
    PROVINCIA_HABANA,
    TARIFA_EMBALAJE_POR_10LB,
    TIPOS_CLIENTE,
)

_logger = logging.getLogger(__name__)


class PaqueteriaEnvio(models.Model):
    """Gestión de envíos de paquetería internacional México-Cuba.
    
    Este modelo maneja el proceso completo de envío desde la recepción
    hasta la distribución en maletas, incluyendo:
    - Cálculos automáticos de costos según tarifas
    - Distribución de pesos en múltiples maletas
    - Cálculo de impuestos aduanales
    - Control financiero de cobros
    """
    
    _name = 'paqueteria.envio'
    _description = 'Envío de Paquete'
    _order = 'fecha_envio_id desc, name desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # ========== IDENTIFICACIÓN ==========
    
    name = fields.Char(
        string='Número de Envío',
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo',
        index=True,  # ← AGREGADO
        tracking=True,  # ← AGREGADO
        help='Número de envío generado automáticamente'
    )
    
    # Campo auxiliar para importar
    recepcion_importar_id = fields.Many2one(
        'paqueteria.recepcion',
        string='Importar desde Recepción',
        help='Selecciona una recepción para copiar sus datos automáticamente'
    )
    
    # ========== REMITENTE (MÉXICO) ==========
    
    remitente_nombre = fields.Char(
        string='Remitente',
        required=True,
        index=True,  # ← AGREGADO
        tracking=True,  # ← AGREGADO
        help='Nombre del cliente que envía el paquete'
    )
    
    remitente_telefono = fields.Char(
        string='Teléfono Remitente',
        tracking=True,  # ← AGREGADO
        help='Teléfono del cliente en México'
    )
    
    tipo_cliente = fields.Selection(
        selection=TIPOS_CLIENTE,  # ← CAMBIADO: De constante
        string='Tipo de Cliente',
        required=True,
        default='normal',
        tracking=True,  # ← AGREGADO
        help='Tipo de cliente: Normal o VIP con tarifa preferencial'
    )
    
    # ========== DESTINATARIO (CUBA) ==========
    
    destinatario_nombre = fields.Char(
        string='Destinatario',
        required=True,
        index=True,  # ← AGREGADO
        tracking=True,  # ← AGREGADO
        help='Nombre de quien recibe en Cuba'
    )
    
    destinatario_telefono = fields.Char(
        string='Teléfono Destinatario',
        tracking=True,  # ← AGREGADO
        help='Teléfono del destinatario en Cuba'
    )
    
    provincia_id = fields.Many2one(
        'paqueteria.provincia',
        string='Provincia Destino',
        required=True,
        ondelete='restrict',  # ← AGREGADO
        tracking=True,  # ← AGREGADO
        help='Provincia de Cuba donde se entrega el paquete'
    )
    
    # ========== PESOS ==========
    
    peso_central = fields.Float(
        string='Peso en Central (lb)',
        digits=(10, 2),
        tracking=True,  # ← AGREGADO
        help='Peso registrado en la central (solo informativo)'
    )
    
    peso_etiqueta = fields.Float(
        string='Peso en Etiqueta (lb)',
        digits=(10, 2),
        tracking=True,  # ← AGREGADO
        help='Peso indicado en la etiqueta del paquete'
    )
    
    peso_volumen = fields.Float(
        string='Peso por Volumen (lb)',
        digits=(10, 2),
        tracking=True,  # ← AGREGADO
        help='Peso volumétrico calculado'
    )
    
    peso_cobrar = fields.Float(
        string='Peso a Cobrar (lb)',
        compute='_compute_peso_cobrar',
        store=True,
        digits=(10, 2),
        help='El mayor entre peso etiqueta y peso volumen'
    )
    
    # ========== COSTOS ADICIONALES ==========
    
    articulo_ids = fields.One2many(
        'paqueteria.envio.articulo',
        'envio_id',
        string='Artículos con Impuesto Aduanal',
        help='Lista de artículos que requieren pago de impuesto aduanal'
    )
    
    impuesto_aduanal = fields.Float(
        string='Impuesto Aduanal ($)',
        compute='_compute_impuesto_aduanal',
        store=True,
        digits=(10, 2),
        help='Suma automática de impuestos de todos los artículos'
    )
    
    costo_documentos = fields.Float(
        string='Documentos ($)',
        digits=(10, 2),
        tracking=True,  # ← AGREGADO
        help='Costo adicional por trámite de documentos si aplica'
    )
    
    # ========== CÁLCULOS AUTOMÁTICOS ==========
    
    embalaje = fields.Float(
        string='Embalaje ($)',
        compute='_compute_embalaje',
        store=True,
        digits=(10, 2),
        help=f'${TARIFA_EMBALAJE_POR_10LB} por cada 10 lb o fracción'
    )
    
    tarifa_por_lb = fields.Float(
        string='Tarifa por Libra ($)',
        compute='_compute_tarifa',
        store=True,
        digits=(10, 2),
        help='Tarifa variable según tipo de cliente y provincia destino'
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
        tracking=True,  # ← AGREGADO
        help='Subtotal + Embalaje + Impuestos + Documentos'
    )
    
    # ========== PAGO ==========
    
    forma_pago = fields.Selection(
        selection=FORMAS_PAGO,  # ← CAMBIADO: De constante
        string='Forma de Pago',
        tracking=True,  # ← AGREGADO
        help='Forma en que el cliente realizó el pago'
    )
    
    # ========== MALETA Y DISTRIBUCIÓN ==========
    
    maleta_distribucion_ids = fields.One2many(
        'paqueteria.envio.maleta',
        'envio_id',
        string='Distribución en Maletas',
        help='Distribución del peso de este envío en diferentes maletas físicas'
    )
    
    maleta_count = fields.Integer(
        string='Cantidad de Maletas',
        compute='_compute_maleta_count',
        help='Número de maletas en las que está distribuido este envío'
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
        ondelete='restrict',  # ← AGREGADO
        tracking=True,  # ← AGREGADO
        help='Administrador regional que procesó este envío'
    )
    
    estado_mexico = fields.Selection(
        selection=ESTADOS_MEXICO,  # ← CAMBIADO: De constante
        string='Estado de México',
        required=True,
        tracking=True,  # ← AGREGADO
        help='Estado de México donde opera el administrador'
    )
    
    fecha_envio_id = fields.Many2one(
        'paqueteria.fecha.envio',
        string='Fecha de Envío',
        ondelete='restrict',  # ← AGREGADO
        tracking=True,  # ← AGREGADO
        help='Fecha de envío programada para este paquete'
    )
    
    # ========== COMPUTED METHODS ==========
    
    @api.depends('peso_etiqueta', 'peso_volumen')
    def _compute_peso_cobrar(self):
        """Calcula el peso a cobrar como el máximo entre etiqueta y volumen.
        
        El peso central NO se incluye en el cálculo, es solo informativo.
        """
        for record in self:
            pesos = [
                record.peso_etiqueta or 0.0,
                record.peso_volumen or 0.0,
            ]
            record.peso_cobrar = max(pesos)
    
    @api.depends('maleta_distribucion_ids.peso_en_maleta')
    def _compute_maleta_count(self):
        """Cuenta el número de maletas en las que está distribuido."""
        for record in self:
            record.maleta_count = len(record.maleta_distribucion_ids)
    
    @api.depends('maleta_distribucion_ids.peso_en_maleta', 'peso_cobrar')
    def _compute_peso_distribuido(self):
        """Calcula peso distribuido y pendiente de distribución."""
        for record in self:
            distribuido = sum(
                record.maleta_distribucion_ids.mapped('peso_en_maleta')
            )
            record.peso_distribuido = distribuido
            record.peso_pendiente = record.peso_cobrar - distribuido
    
    @api.depends('peso_cobrar')
    def _compute_embalaje(self):
        """Calcula costo de embalaje: $50 por cada 10 lb o fracción.
        
        Ejemplos:
        - 6.3 lb = $50 (1 fracción)
        - 10.1 lb = $100 (2 fracciones)
        - 20.1 lb = $150 (3 fracciones)
        """
        for record in self:
            if record.peso_cobrar > 0:
                fracciones = math.ceil(record.peso_cobrar / 10)
                record.embalaje = fracciones * TARIFA_EMBALAJE_POR_10LB
            else:
                record.embalaje = 0.0
    
    @api.depends('tipo_cliente', 'provincia_id')
    def _compute_tarifa(self):
        """Calcula tarifa por libra según tipo de cliente y provincia.
        
        Tarifas actuales:
        - VIP + Habana: $140
        - VIP + Resto: $170
        - Normal + Habana: $150
        - Normal + Resto: $180
        
        TODO: Migrar a modelo configurable paqueteria.tarifa
        """
        for record in self:
            if not record.provincia_id:
                record.tarifa_por_lb = 0.0
                continue
            
            es_habana = record.provincia_id.name == PROVINCIA_HABANA
            
            if record.tipo_cliente == 'vip':
                record.tarifa_por_lb = 140.0 if es_habana else 170.0
            else:  # normal
                record.tarifa_por_lb = 150.0 if es_habana else 180.0
    
    @api.depends('articulo_ids.subtotal')
    def _compute_impuesto_aduanal(self):
        """Suma los impuestos aduanales de todos los artículos."""
        for record in self:
            record.impuesto_aduanal = sum(
                record.articulo_ids.mapped('subtotal')
            )
    
    @api.depends(
        'peso_cobrar',
        'tarifa_por_lb',
        'embalaje',
        'impuesto_aduanal',
        'costo_documentos',
    )
    def _compute_totales(self):
        """Calcula subtotal y total a cobrar.
        
        Fórmulas:
        - Subtotal = Peso × Tarifa
        - Total = Subtotal + Embalaje + Impuestos + Documentos
        """
        for record in self:
            record.subtotal_envio = record.peso_cobrar * record.tarifa_por_lb
            
            record.total_cobrar = (
                record.subtotal_envio
                + record.embalaje
                + (record.impuesto_aduanal or 0)
                + (record.costo_documentos or 0)
            )
    
    # ========== ONCHANGE METHODS ==========
    
    @api.onchange('recepcion_importar_id')
    def _onchange_recepcion_importar(self):
        """Importa datos automáticamente desde una recepción seleccionada."""
        if not self.recepcion_importar_id:
            return
        
        recepcion = self.recepcion_importar_id
        
        # Copiar datos del remitente
        self.remitente_nombre = recepcion.remitente_nombre
        self.remitente_telefono = recepcion.remitente_telefono
        
        # Copiar datos del destinatario
        self.destinatario_nombre = recepcion.destinatario_nombre
        self.destinatario_telefono = recepcion.destinatario_telefono
        self.provincia_id = recepcion.provincia_id
        
        # Copiar peso
        self.peso_etiqueta = recepcion.peso_etiqueta
        
        # Copiar control
        self.admin_id = recepcion.admin_id
        self.estado_mexico = recepcion.estado_mexico
        
        # Limpiar campo auxiliar
        self.recepcion_importar_id = False
        
        _logger.info(
            'Datos importados desde recepción %s para envío',
            recepcion.name
        )
    
    # ========== CRUD METHODS ==========
    
    @api.model_create_multi
    def create(self, vals_list):
        """Crea envíos generando número de secuencia automáticamente.
        
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
                
                _logger.info('Creando nuevo envío: %s', sequence)
        
        return super().create(vals_list)
    
    # ========== CONSTRAINTS ==========
    
    @api.constrains('peso_etiqueta', 'peso_volumen', 'peso_central')
    def _check_pesos_positivos(self):
        """Valida que los pesos sean mayores a cero si están definidos."""
        for record in self:
            if record.peso_etiqueta and record.peso_etiqueta <= 0:
                raise ValidationError(
                    _('El peso en etiqueta debe ser mayor a cero')
                )
            if record.peso_volumen and record.peso_volumen <= 0:
                raise ValidationError(
                    _('El peso por volumen debe ser mayor a cero')
                )
            if record.peso_central and record.peso_central <= 0:
                raise ValidationError(
                    _('El peso central debe ser mayor a cero')
                )
    
    @api.constrains('peso_cobrar')
    def _check_peso_cobrar(self):
        """Valida que haya al menos un peso definido para cobrar."""
        for record in self:
            if record.peso_cobrar <= 0:
                raise ValidationError(
                    _('Debe definir al menos el peso en etiqueta '
                      'o el peso por volumen')
                )
    
    # ========== SQL CONSTRAINTS ==========
    
    _sql_constraints = [
        (
            'peso_etiqueta_positive',
            'CHECK(peso_etiqueta IS NULL OR peso_etiqueta > 0)',
            'El peso en etiqueta debe ser positivo',
        ),
        (
            'peso_volumen_positive',
            'CHECK(peso_volumen IS NULL OR peso_volumen > 0)',
            'El peso por volumen debe ser positivo',
        ),
        (
            'total_cobrar_positive',
            'CHECK(total_cobrar >= 0)',
            'El total a cobrar debe ser positivo',
        ),
    ]
```

---

## 3. EJEMPLO DE TESTS COMPLETOS

### Crear: `tests/__init__.py`

```python
# Copyright 2024 Javier Alejandro Pérez <tu@email.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from . import test_provincia
from . import test_articulo
from . import test_recepcion
from . import test_envio
from . import test_envio_articulo
from . import test_maleta
from . import test_fecha_envio
```

### Crear: `tests/common.py`

```python
# Copyright 2024 Javier Alejandro Pérez <tu@email.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Clase base para tests de paquetería internacional."""

from odoo.tests.common import TransactionCase


class PaqueteriaCommon(TransactionCase):
    """Clase base con setup común para todos los tests."""
    
    @classmethod
    def setUpClass(cls):
        """Setup ejecutado una vez antes de todos los tests."""
        super().setUpClass()
        
        # Modelos
        cls.Provincia = cls.env['paqueteria.provincia']
        cls.Articulo = cls.env['paqueteria.articulo']
        cls.Recepcion = cls.env['paqueteria.recepcion']
        cls.Envio = cls.env['paqueteria.envio']
        cls.EnvioArticulo = cls.env['paqueteria.envio.articulo']
        cls.Maleta = cls.env['paqueteria.maleta']
        cls.FechaEnvio = cls.env['paqueteria.fecha.envio']
        
        # Datos de prueba: Provincia
        cls.provincia_habana = cls.Provincia.create({
            'name': 'La Habana',
            'code': 'LH',
        })
        
        cls.provincia_santiago = cls.Provincia.create({
            'name': 'Santiago de Cuba',
            'code': 'SC',
        })
        
        # Datos de prueba: Artículo
        cls.articulo_celular = cls.Articulo.create({
            'name': 'iPhone 15 Pro',
            'tipo_articulo': 'celular',
        })
        
        cls.articulo_laptop = cls.Articulo.create({
            'name': 'Laptop Dell XPS',
            'tipo_articulo': 'laptop_tablet',
        })
        
        cls.articulo_otro = cls.Articulo.create({
            'name': 'Perfume Chanel',
            'tipo_articulo': 'otro',
            'costo_aduanal': 200.0,
        })
```

### Crear: `tests/test_envio.py`

```python
# Copyright 2024 Javier Alejandro Pérez <tu@email.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Tests para modelo de Envío."""

from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import PaqueteriaCommon


@tagged('post_install', '-at_install')
class TestPaqueteriaEnvio(PaqueteriaCommon):
    """Tests para el modelo paqueteria.envio."""
    
    def test_01_create_envio_secuencia(self):
        """Test que se genera secuencia automática al crear envío."""
        envio = self.Envio.create({
            'remitente_nombre': 'Juan Pérez',
            'destinatario_nombre': 'María García',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
        })
        
        self.assertTrue(envio.name)
        self.assertNotEqual(envio.name, 'Nuevo')
        self.assertTrue(envio.name.startswith('ENV-'))
    
    def test_02_compute_peso_cobrar_etiqueta_mayor(self):
        """Test peso a cobrar cuando etiqueta es mayor que volumen."""
        envio = self.Envio.create({
            'remitente_nombre': 'Test',
            'destinatario_nombre': 'Test',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 15.0,
            'peso_volumen': 10.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
        })
        
        self.assertEqual(envio.peso_cobrar, 15.0)
    
    def test_03_compute_peso_cobrar_volumen_mayor(self):
        """Test peso a cobrar cuando volumen es mayor que etiqueta."""
        envio = self.Envio.create({
            'remitente_nombre': 'Test',
            'destinatario_nombre': 'Test',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.0,
            'peso_volumen': 15.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
        })
        
        self.assertEqual(envio.peso_cobrar, 15.0)
    
    def test_04_compute_embalaje_una_fraccion(self):
        """Test cálculo de embalaje para menos de 10 lb."""
        envio = self.Envio.create({
            'remitente_nombre': 'Test',
            'destinatario_nombre': 'Test',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 6.3,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
        })
        
        self.assertEqual(envio.embalaje, 50.0)
    
    def test_05_compute_embalaje_dos_fracciones(self):
        """Test cálculo de embalaje para 10.1 lb."""
        envio = self.Envio.create({
            'remitente_nombre': 'Test',
            'destinatario_nombre': 'Test',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.1,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
        })
        
        self.assertEqual(envio.embalaje, 100.0)
    
    def test_06_compute_tarifa_normal_habana(self):
        """Test tarifa para cliente normal en La Habana."""
        envio = self.Envio.create({
            'remitente_nombre': 'Test',
            'destinatario_nombre': 'Test',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
        })
        
        self.assertEqual(envio.tarifa_por_lb, 150.0)
    
    def test_07_compute_tarifa_normal_resto(self):
        """Test tarifa para cliente normal fuera de La Habana."""
        envio = self.Envio.create({
            'remitente_nombre': 'Test',
            'destinatario_nombre': 'Test',
            'provincia_id': self.provincia_santiago.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
        })
        
        self.assertEqual(envio.tarifa_por_lb, 180.0)
    
    def test_08_compute_tarifa_vip_habana(self):
        """Test tarifa para cliente VIP en La Habana."""
        envio = self.Envio.create({
            'remitente_nombre': 'Test',
            'destinatario_nombre': 'Test',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'vip',
            'estado_mexico': 'cdmx',
        })
        
        self.assertEqual(envio.tarifa_por_lb, 140.0)
    
    def test_09_compute_tarifa_vip_resto(self):
        """Test tarifa para cliente VIP fuera de La Habana."""
        envio = self.Envio.create({
            'remitente_nombre': 'Test',
            'destinatario_nombre': 'Test',
            'provincia_id': self.provincia_santiago.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'vip',
            'estado_mexico': 'cdmx',
        })
        
        self.assertEqual(envio.tarifa_por_lb, 170.0)
    
    def test_10_compute_totales_basico(self):
        """Test cálculo de totales sin extras."""
        envio = self.Envio.create({
            'remitente_nombre': 'Test',
            'destinatario_nombre': 'Test',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
        })
        
        # Subtotal = 10 lb × 150 = 1500
        self.assertEqual(envio.subtotal_envio, 1500.0)
        
        # Total = 1500 + 50 (embalaje) = 1550
        self.assertEqual(envio.total_cobrar, 1550.0)
    
    def test_11_compute_totales_con_documentos(self):
        """Test cálculo de totales con costo de documentos."""
        envio = self.Envio.create({
            'remitente_nombre': 'Test',
            'destinatario_nombre': 'Test',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
            'costo_documentos': 500.0,
        })
        
        # Total = 1500 + 50 + 500 = 2050
        self.assertEqual(envio.total_cobrar, 2050.0)
    
    def test_12_constraint_peso_etiqueta_negativo(self):
        """Test que no permite peso etiqueta negativo."""
        with self.assertRaises(ValidationError):
            self.Envio.create({
                'remitente_nombre': 'Test',
                'destinatario_nombre': 'Test',
                'provincia_id': self.provincia_habana.id,
                'peso_etiqueta': -5.0,
                'tipo_cliente': 'normal',
                'estado_mexico': 'cdmx',
            })
    
    def test_13_constraint_peso_volumen_negativo(self):
        """Test que no permite peso volumen negativo."""
        with self.assertRaises(ValidationError):
            self.Envio.create({
                'remitente_nombre': 'Test',
                'destinatario_nombre': 'Test',
                'provincia_id': self.provincia_habana.id,
                'peso_volumen': -5.0,
                'tipo_cliente': 'normal',
                'estado_mexico': 'cdmx',
            })
    
    def test_14_constraint_sin_peso(self):
        """Test que requiere al menos un peso definido."""
        with self.assertRaises(ValidationError):
            self.Envio.create({
                'remitente_nombre': 'Test',
                'destinatario_nombre': 'Test',
                'provincia_id': self.provincia_habana.id,
                'tipo_cliente': 'normal',
                'estado_mexico': 'cdmx',
            })
    
    def test_15_onchange_importar_recepcion(self):
        """Test importación de datos desde recepción."""
        # Crear recepción
        recepcion = self.Recepcion.create({
            'remitente_nombre': 'Carlos López',
            'remitente_telefono': '55-1234-5678',
            'destinatario_nombre': 'Ana Martínez',
            'destinatario_telefono': '53-9876-5432',
            'provincia_id': self.provincia_santiago.id,
            'peso_etiqueta': 15.0,
            'estado_mexico': 'jalisco',
            'descripcion_articulos': 'Test',
        })
        
        # Crear envío y simular onchange
        envio = self.Envio.new({
            'tipo_cliente': 'normal',
        })
        envio.recepcion_importar_id = recepcion
        envio._onchange_recepcion_importar()
        
        # Verificar datos copiados
        self.assertEqual(envio.remitente_nombre, 'Carlos López')
        self.assertEqual(envio.remitente_telefono, '55-1234-5678')
        self.assertEqual(envio.destinatario_nombre, 'Ana Martínez')
        self.assertEqual(envio.destinatario_telefono, '53-9876-5432')
        self.assertEqual(envio.provincia_id, self.provincia_santiago)
        self.assertEqual(envio.peso_etiqueta, 15.0)
        self.assertEqual(envio.estado_mexico, 'jalisco')
```

Continúa...
