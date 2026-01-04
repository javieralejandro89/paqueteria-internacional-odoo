# Copyright 2024 Javier Alejandro Pérez <myphoneunlockers@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

"""Tests para modelo de Fecha de Envío."""

from odoo.tests import tagged

from .common import PaqueteriaCommon


@tagged('post_install', '-at_install')
class TestPaqueteriaFechaEnvio(PaqueteriaCommon):
    """Tests para el modelo paqueteria.fecha.envio."""
    
    def setUp(self):
        """Setup ejecutado antes de cada test."""
        super().setUp()
        
        # Crear fecha de envío
        self.fecha_envio = self.FechaEnvio.create({
            'fecha': '2026-01-15',
        })
    
    def test_01_compute_name(self):
        """Test generación automática de nombre basado en fecha."""
        self.assertEqual(
            self.fecha_envio.name,
            'Envío 15-01-2026'
        )
    
    def test_02_totales_sin_envios(self):
        """Test totales cuando no hay envíos."""
        self.assertEqual(self.fecha_envio.total_envios, 0)
        self.assertEqual(self.fecha_envio.total_maletas, 0)
        self.assertEqual(self.fecha_envio.peso_total, 0.0)
        self.assertEqual(self.fecha_envio.total_cobrado, 0.0)
        self.assertEqual(self.fecha_envio.total_cobrado_efectivo, 0.0)
        self.assertEqual(self.fecha_envio.total_cobrado_transferencia, 0.0)
    
    def test_03_totales_con_envios_efectivo(self):
        """Test totales con envíos pagados en efectivo."""
        # Crear 2 envíos en efectivo
        envio1 = self.Envio.create({
            'remitente_nombre': 'Cliente 1',
            'destinatario_nombre': 'Destino 1',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            'forma_pago': 'efectivo',
        })
        
        envio2 = self.Envio.create({
            'remitente_nombre': 'Cliente 2',
            'destinatario_nombre': 'Destino 2',
            'provincia_id': self.provincia_santiago.id,
            'peso_etiqueta': 20.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            'forma_pago': 'efectivo',
        })
        
        # Verificar totales
        self.assertEqual(self.fecha_envio.total_envios, 2)
        
        # Total efectivo = suma de ambos envíos
        total_esperado_efectivo = envio1.total_cobrar + envio2.total_cobrar
        self.assertEqual(
            self.fecha_envio.total_cobrado_efectivo,
            total_esperado_efectivo
        )
        
        # Total transferencia = 0
        self.assertEqual(self.fecha_envio.total_cobrado_transferencia, 0.0)
        
        # Total general = solo efectivo
        self.assertEqual(
            self.fecha_envio.total_cobrado,
            total_esperado_efectivo
        )
    
    def test_04_totales_con_envios_transferencia(self):
        """Test totales con envíos pagados por transferencia."""
        # Crear 2 envíos por transferencia
        envio1 = self.Envio.create({
            'remitente_nombre': 'Cliente 1',
            'destinatario_nombre': 'Destino 1',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 15.0,
            'tipo_cliente': 'vip',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            'forma_pago': 'transferencia',
        })
        
        envio2 = self.Envio.create({
            'remitente_nombre': 'Cliente 2',
            'destinatario_nombre': 'Destino 2',
            'provincia_id': self.provincia_santiago.id,
            'peso_etiqueta': 25.0,
            'tipo_cliente': 'vip',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            'forma_pago': 'transferencia',
        })
        
        # Verificar totales
        total_esperado_transferencia = (
            envio1.total_cobrar + envio2.total_cobrar
        )
        
        self.assertEqual(
            self.fecha_envio.total_cobrado_transferencia,
            total_esperado_transferencia
        )
        
        # Total efectivo = 0
        self.assertEqual(self.fecha_envio.total_cobrado_efectivo, 0.0)
        
        # Total general = solo transferencia
        self.assertEqual(
            self.fecha_envio.total_cobrado,
            total_esperado_transferencia
        )
    
    def test_05_totales_mixtos_efectivo_y_transferencia(self):
        """Test totales con envíos mixtos (efectivo + transferencia)."""
        # Crear 2 envíos en efectivo
        envio_efectivo_1 = self.Envio.create({
            'remitente_nombre': 'Cliente Efectivo 1',
            'destinatario_nombre': 'Destino 1',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            'forma_pago': 'efectivo',
        })
        
        envio_efectivo_2 = self.Envio.create({
            'remitente_nombre': 'Cliente Efectivo 2',
            'destinatario_nombre': 'Destino 2',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 15.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            'forma_pago': 'efectivo',
        })
        
        # Crear 2 envíos por transferencia
        envio_trans_1 = self.Envio.create({
            'remitente_nombre': 'Cliente Transferencia 1',
            'destinatario_nombre': 'Destino 3',
            'provincia_id': self.provincia_santiago.id,
            'peso_etiqueta': 20.0,
            'tipo_cliente': 'vip',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            'forma_pago': 'transferencia',
        })
        
        envio_trans_2 = self.Envio.create({
            'remitente_nombre': 'Cliente Transferencia 2',
            'destinatario_nombre': 'Destino 4',
            'provincia_id': self.provincia_santiago.id,
            'peso_etiqueta': 25.0,
            'tipo_cliente': 'vip',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            'forma_pago': 'transferencia',
        })
        
        # Calcular totales esperados
        total_esperado_efectivo = (
            envio_efectivo_1.total_cobrar + 
            envio_efectivo_2.total_cobrar
        )
        
        total_esperado_transferencia = (
            envio_trans_1.total_cobrar + 
            envio_trans_2.total_cobrar
        )
        
        total_esperado_general = (
            total_esperado_efectivo + 
            total_esperado_transferencia
        )
        
        # Verificar totales
        self.assertEqual(self.fecha_envio.total_envios, 4)
        
        self.assertEqual(
            self.fecha_envio.total_cobrado_efectivo,
            total_esperado_efectivo
        )
        
        self.assertEqual(
            self.fecha_envio.total_cobrado_transferencia,
            total_esperado_transferencia
        )
        
        self.assertEqual(
            self.fecha_envio.total_cobrado,
            total_esperado_general
        )
        
        # Verificar que la suma cuadre
        self.assertEqual(
            self.fecha_envio.total_cobrado,
            (self.fecha_envio.total_cobrado_efectivo + 
             self.fecha_envio.total_cobrado_transferencia)
        )
    
    def test_06_envios_sin_forma_pago(self):
        """Test que envíos sin forma de pago no se cuentan en ningún total."""
        # Crear envío con forma de pago
        envio_con_pago = self.Envio.create({
            'remitente_nombre': 'Cliente 1',
            'destinatario_nombre': 'Destino 1',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            'forma_pago': 'efectivo',
        })
        
        # Crear envío SIN forma de pago
        envio_sin_pago = self.Envio.create({
            'remitente_nombre': 'Cliente 2',
            'destinatario_nombre': 'Destino 2',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 20.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            # forma_pago NO definida
        })
        
        # Total efectivo solo cuenta el primero
        self.assertEqual(
            self.fecha_envio.total_cobrado_efectivo,
            envio_con_pago.total_cobrar
        )
        
        # Total transferencia = 0
        self.assertEqual(self.fecha_envio.total_cobrado_transferencia, 0.0)
        
        # Total general cuenta AMBOS
        self.assertEqual(
            self.fecha_envio.total_cobrado,
            envio_con_pago.total_cobrar + envio_sin_pago.total_cobrar
        )
        
        # Verificar que hay diferencia (envío sin forma de pago)
        diferencia = (
            self.fecha_envio.total_cobrado - 
            self.fecha_envio.total_cobrado_efectivo - 
            self.fecha_envio.total_cobrado_transferencia
        )
        self.assertEqual(diferencia, envio_sin_pago.total_cobrar)
    
    def test_07_actualiza_totales_al_cambiar_forma_pago(self):
        """Test que los totales se recalculan al cambiar forma de pago."""
        # Crear envío en efectivo
        envio = self.Envio.create({
            'remitente_nombre': 'Cliente',
            'destinatario_nombre': 'Destino',
            'provincia_id': self.provincia_habana.id,
            'peso_etiqueta': 10.0,
            'tipo_cliente': 'normal',
            'estado_mexico': 'cdmx',
            'fecha_envio_id': self.fecha_envio.id,
            'forma_pago': 'efectivo',
        })
        
        # Verificar inicial
        total_inicial = envio.total_cobrar
        self.assertEqual(
            self.fecha_envio.total_cobrado_efectivo,
            total_inicial
        )
        self.assertEqual(
            self.fecha_envio.total_cobrado_transferencia,
            0.0
        )
        
        # Cambiar a transferencia
        envio.write({'forma_pago': 'transferencia'})
        
        # Verificar que cambió
        self.assertEqual(self.fecha_envio.total_cobrado_efectivo, 0.0)
        self.assertEqual(
            self.fecha_envio.total_cobrado_transferencia,
            total_inicial
        )