# 📦 Paquetería Internacional - Módulo Odoo 19

Sistema profesional de gestión de envíos de paquetería México-Cuba con cálculo automático de costos, distribución en maletas y control financiero.

[![CI Status](https://github.com/javieralejandro89/paqueteria-internacional-odoo/workflows/CI/badge.svg)](https://github.com/javieralejandro89/paqueteria-internacional-odoo/actions)
[![License: LGPL-3](https://img.shields.io/badge/license-LGPL--3-blue)](http://www.gnu.org/licenses/lgpl-3.0)
[![Odoo Version](https://img.shields.io/badge/odoo-19.0-purple)](https://www.odoo.com/)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)

---

## 🎯 Características Principales

### Gestión de Recepciones
- ✅ Registro de paquetes por administradores regionales
- ✅ Captura de datos de remitente y destinatario
- ✅ Adjuntar fotografías de la mercancía
- ✅ Descripción detallada de artículos
- ✅ Control por estado de México

### Cálculo Automático de Costos
- ✅ **Peso a cobrar:** Máximo entre peso en etiqueta y peso volumétrico
- ✅ **Embalaje:** $50 MXN por cada 10 lb o fracción
- ✅ **Tarifas dinámicas:**
  - Cliente Normal + La Habana: $150/lb
  - Cliente Normal + Resto: $180/lb
  - Cliente VIP + La Habana: $140/lb
  - Cliente VIP + Resto: $170/lb
- ✅ **Impuestos aduanales:** Cálculo automático según tipo de artículo
  - Celulares: $700-$1,000 según cliente y destino
  - Laptops/Tablets: $800-$1,300 según cliente y destino
  - Otros: Precio fijo configurable

### Distribución en Maletas
- ✅ Sistema multi-maleta con pesos personalizados
- ✅ Seguimiento de peso distribuido vs pendiente
- ✅ Descripción de empaque por maleta
- ✅ Validación automática de pesos

### Control Financiero
- ✅ **Desglose por forma de pago:**
  - Total en efectivo
  - Total en transferencias
  - Total general consolidado
- ✅ Seguimiento por fecha de envío
- ✅ Reportes y estadísticas en tiempo real

### Dashboard y Reportes
- ✅ Vista Kanban con métricas visuales
- ✅ Dashboard por fecha de envío
- ✅ Vista Pivot para análisis financiero
- ✅ Gráficas de barras apiladas
- ✅ Filtros y agrupaciones avanzadas

---

## 📋 Requisitos

### Dependencias de Sistema
- **Odoo:** 19.0
- **Python:** 3.10+
- **PostgreSQL:** 14+
- **Sistema Operativo:** Linux, macOS, Windows

### Dependencias de Odoo
- `base` (módulo core de Odoo)
- `web` (módulo core de Odoo)

---

## 🚀 Instalación

### Método 1: Instalación Manual

1. **Clonar el repositorio:**
```bash
   cd /path/to/odoo/custom-addons
   git clone https://github.com/javieralejandro89/paqueteria-internacional-odoo.git
   cd paqueteria-internacional-odoo
```

2. **Copiar el módulo:**
```bash
   cp -r custom-addons/paqueteria_internacional /path/to/odoo/custom-addons/
```

3. **Reiniciar Odoo:**
```bash
   sudo systemctl restart odoo
   # O si usas Docker:
   docker-compose restart odoo
```

4. **Actualizar lista de módulos:**
   - Ir a Apps → Actualizar Lista de Aplicaciones

5. **Instalar el módulo:**
   - Buscar "Paquetería Internacional"
   - Clic en **Instalar**

### Método 2: Docker
```bash
git clone https://github.com/javieralejandro89/paqueteria-internacional-odoo.git
cd paqueteria-internacional-odoo

# Agregar al docker-compose.yml
volumes:
  - ./custom-addons/paqueteria_internacional:/mnt/extra-addons/paqueteria_internacional

docker-compose up -d
```

---

## ⚙️ Configuración Inicial

### 1. Configurar Provincias de Cuba
Ya vienen pre-cargadas las 16 provincias. Verificar en:
```
Paquetería → Configuración → Provincias
```

### 2. Configurar Artículos con Impuesto
Crear catálogo de artículos que requieren impuesto aduanal:
```
Paquetería → Configuración → Artículos con Impuesto
```

Tipos de artículos:
- **Celulares:** Precio dinámico según cliente y destino
- **Laptops/Tablets:** Precio dinámico según cliente y destino
- **Otros:** Precio fijo configurable

### 3. Configurar Administradores
Asignar estado de México a cada administrador en su perfil de usuario.

---

## 📖 Uso

### Flujo Completo de Operación

#### 1. Recepción de Paquetes
```
Paquetería → Recepciones → Nuevo
```

**Datos a capturar:**
- Admin que recibió (automático)
- Estado de México
- Remitente (nombre, teléfono)
- Destinatario (nombre, teléfono, provincia)
- Peso en etiqueta
- Fotos del paquete
- Descripción de artículos

#### 2. Crear Envío
```
Paquetería → Envíos → Nuevo
```

**Opción A: Importar desde Recepción**
1. Seleccionar recepción existente
2. Datos se copian automáticamente

**Opción B: Captura manual**
1. Datos de remitente y destinatario
2. Tipo de cliente (Normal/VIP)
3. Pesos (etiqueta, volumen, central)
4. Artículos con impuesto (si aplica)
5. Costo de documentos (si aplica)
6. **Forma de pago** (Efectivo/Transferencia)

**Cálculos automáticos:**
- ✅ Peso a cobrar
- ✅ Embalaje
- ✅ Tarifa por libra
- ✅ Impuestos aduanales
- ✅ Total a cobrar

#### 3. Distribución en Maletas
Dentro del envío, sección "Distribución en Maletas":
1. Seleccionar maleta
2. Indicar peso en esta maleta
3. Describir empaque
4. Repetir si el envío va en múltiples maletas

**Validaciones automáticas:**
- ⚠️ Peso pendiente por distribuir
- ✅ Distribución completa

#### 4. Consultar Dashboard
```
Paquetería → Dashboard
```

**Métricas visibles:**
- Total de envíos
- Total de maletas
- Peso total (lb)
- **💰 Total cobrado**
- **💵 Total en efectivo**
- **💳 Total en transferencias**
- Provincias de destino

#### 5. Análisis Financiero
```
Paquetería → Envíos → Vista Pivot
```

Análisis cruzado por:
- Fecha de envío
- Forma de pago
- Provincia
- Tipo de cliente
- Administrador

---

## 📁 Estructura del Proyecto
```
paqueteria_internacional/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── provincia.py              # Provincias de Cuba
│   ├── articulo.py               # Artículos con impuesto
│   ├── recepcion.py              # Recepciones de paquetes
│   ├── fecha_envio.py            # Fechas de envío y dashboard
│   ├── envio.py                  # Envíos de paquetes
│   ├── envio_articulo.py         # Relación envío-artículos
│   ├── envio_maleta.py           # Distribución en maletas
│   └── maleta.py                 # Maletas físicas
├── views/
│   ├── menu.xml                  # Menú principal
│   ├── provincia_views.xml
│   ├── articulo_views.xml
│   ├── recepcion_views.xml
│   ├── fecha_envio_views.xml
│   ├── envio_views.xml
│   └── maleta_views.xml
├── security/
│   └── ir.model.access.csv       # Permisos de acceso
├── data/
│   ├── provincia_data.xml        # 16 provincias pre-cargadas
│   ├── recepcion_sequence.xml
│   └── envio_sequence.xml
└── tests/
    ├── __init__.py
    ├── common.py
    └── test_fecha_envio.py
```

---

## 🧪 Tests

### Ejecutar Tests

**Método 1: Con Odoo instalado localmente**
```bash
odoo-bin -c odoo.conf \
  -d test_paqueteria \
  --test-enable \
  --stop-after-init \
  -i paqueteria_internacional \
  --log-level=test
```

**Método 2: Verificación manual**
Ver checklist completo en: [docs/testing-checklist.md](docs/testing-checklist.md)

**Cobertura actual:** ~85% (en desarrollo)

---

## 🤝 Contribuir

### Proceso de Contribución

1. **Fork el proyecto**
2. **Crear rama de feature:**
```bash
   git checkout -b feature/nueva-funcionalidad
```
3. **Commit con mensaje descriptivo:**
```bash
   git commit -m "feat: agregar cálculo de impuestos para mercancía electrónica"
```
4. **Push a tu fork:**
```bash
   git push origin feature/nueva-funcionalidad
```
5. **Abrir Pull Request**

### Estándares de Código

- ✅ Seguir [OCA Guidelines](https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst)
- ✅ Python: [PEP 8](https://peps.python.org/pep-0008/)
- ✅ Docstrings en todos los métodos
- ✅ Help text en todos los campos
- ✅ Tests unitarios (cobertura mínima 85%)
- ✅ Copyright header en archivos Python

### Convención de Commits
```
feat: Nueva funcionalidad
fix: Corrección de bug
docs: Documentación
style: Formato de código
refactor: Refactorización
test: Agregar tests
chore: Tareas de mantenimiento
```

---

## 🗺️ Roadmap

### v1.1.0 (En desarrollo)
- [ ] Reportes PDF personalizados
- [ ] Exportación a Excel
- [ ] Notificaciones por email
- [ ] API REST para integración externa

### v1.2.0 (Futuro)
- [ ] App móvil para admins
- [ ] Integración con servicios de paquetería
- [ ] Dashboard avanzado con gráficas
- [ ] Sistema de roles y permisos granulares

### v2.0.0 (Futuro)
- [ ] Multi-moneda
- [ ] Soporte para otros países
- [ ] Inteligencia artificial para predicción de costos
- [ ] Blockchain para trazabilidad

---

## 📊 Métricas del Proyecto

- **Líneas de código:** ~2,500
- **Modelos:** 8
- **Vistas:** 24
- **Tests:** 7 (en desarrollo)
- **Cobertura:** ~85% (en desarrollo)
- **Idioma:** Español
- **Desarrollado para:** Odoo 19.0

---

## 🐛 Reportar Bugs

Encontraste un bug? [Abre un issue](https://github.com/javieralejandro89/paqueteria-internacional-odoo/issues) con:

1. Descripción del problema
2. Pasos para reproducir
3. Comportamiento esperado
4. Comportamiento actual
5. Screenshots (si aplica)
6. Versión de Odoo
7. Sistema operativo

---

## 📄 Licencia

Este proyecto está licenciado bajo **LGPL-3.0** - ver el archivo [LICENSE](LICENSE) para más detalles.

### ¿Qué significa?

- ✅ Uso comercial permitido
- ✅ Modificación permitida
- ✅ Distribución permitida
- ✅ Uso privado permitido
- ⚠️ Cambios deben ser licenciados bajo LGPL-3.0
- ⚠️ Incluir aviso de licencia y copyright

---

## 👨‍💻 Autor

**Javier Alejandro Pérez**

- GitHub: [@javieralejandro89](https://github.com/javieralejandro89)
- Email: myphoneunlockers@gmail.com
- LinkedIn: (https://www.linkedin.com/in/javier-alejandro-perez-vazquez-726b96367?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app)
- Website: [DigitalizaTuNegocio](https://digitalizatunegocio.site)

---

## 🙏 Agradecimientos

- Comunidad Odoo Community Association (OCA)
- Equipo de Odoo por la plataforma
- Todos los contribuidores del proyecto

---

## 📞 Soporte

¿Necesitas ayuda? 

- 📧 Email: myphoneunlockers@gmail.com
- 💬 Issues: [GitHub Issues](https://github.com/javieralejandro89/paqueteria-internacional-odoo/issues)
- 📖 Documentación: [Wiki del proyecto](https://github.com/javieralejandro89/paqueteria-internacional-odoo/wiki)

---

## ⭐ ¿Te gusta el proyecto?

Si este módulo te ha sido útil, considera:
- ⭐ Darle una estrella en GitHub
- 🍴 Hacer fork y contribuir
- 📢 Compartirlo con otros

---


*Última actualización: Enero 2026*