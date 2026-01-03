# -*- coding: utf-8 -*-
{
    'name': 'Paquetería Internacional',
    'version': '19.0.1.0.0',
    'category': 'Operations/Inventory',
    'summary': 'Sistema de envío de paquetes México-Cuba',
    'description': """
        Sistema de Paquetería Internacional
        ===================================
        
        Gestión completa de envíos internacionales:
        * Recepciones de paquetes por admins regionales
        * Control de envíos y destinatarios
        * Gestión de paquetes con fotografías
        * Distribución multi-maleta con pesos personalizados
        * Control financiero (cobros y pagos)
        * Estadísticas y reportes
    """,
    'author': 'Javier Alejandro Pérez',
    'website': 'https://github.com/javieralejandro89',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        # Seguridad
        'security/ir.model.access.csv',
        
        # Datos iniciales
        'data/provincia_data.xml',
        'data/recepcion_sequence.xml',
        'data/envio_sequence.xml',
        
        # Vistas
        'views/fecha_envio_views.xml',
        'views/articulo_views.xml',
        'views/recepcion_views.xml',
        'views/envio_views.xml',
        'views/maleta_views.xml',
        'views/provincia_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}