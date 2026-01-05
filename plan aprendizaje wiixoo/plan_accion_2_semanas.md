# 📅 PLAN DE ACCIÓN - 2 SEMANAS
## Transformación Completa del Módulo según Estándares Wiixoo

---

## 🎯 OBJETIVO

Transformar el módulo `paqueteria_internacional` de un **4.4/10** a un **9/10** en 2 semanas, cumpliendo con los estándares de producción de Wiixoo.

---

## 📊 MÉTRICAS DE ÉXITO

| Métrica | Antes | Meta | Crítico |
|---------|-------|------|---------|
| **Tests Coverage** | 0% | 85%+ | ✅ SÍ |
| **OCA Compliance** | 40% | 95%+ | ✅ SÍ |
| **Documentación** | 20% | 90%+ | ✅ SÍ |
| **CI/CD** | 0% | 100% | ✅ SÍ |
| **Seguridad** | 50% | 85%+ | ⚠️ Importante |
| **Performance** | 60% | 80%+ | ⚠️ Importante |

---

## 📅 SEMANA 1: FUNDAMENTOS CRÍTICOS

### DÍA 1 (Lunes) - Setup CI/CD ⏱️ 6-8 horas

#### Mañana (4 horas)
- [ ] **Crear estructura de archivos de configuración**
  ```bash
  mkdir -p .github/workflows
  touch .github/workflows/ci.yml
  touch .pre-commit-config.yaml
  touch .flake8
  touch .pylintrc
  touch pyproject.toml
  touch .bandit.yml
  touch requirements-dev.txt
  touch Makefile
  touch setup_dev.sh
  ```

- [ ] **Copiar configuraciones** (del archivo `configuracion_cicd_completa.md`)
  - Copiar contenido de `.github/workflows/ci.yml`
  - Copiar contenido de `.pre-commit-config.yaml`
  - Copiar contenido de `.flake8`
  - Copiar contenido de `.pylintrc`
  - Copiar contenido de `pyproject.toml`
  - Copiar contenido de `.bandit.yml`
  - Copiar contenido de `requirements-dev.txt`
  - Copiar contenido de `Makefile`
  - Copiar contenido de `setup_dev.sh`

- [ ] **Ejecutar setup inicial**
  ```bash
  chmod +x setup_dev.sh
  ./setup_dev.sh
  ```

#### Tarde (2-3 horas)
- [ ] **Primera ejecución de herramientas**
  ```bash
  source .venv/bin/activate
  make lint   # Ver todos los errores
  ```

- [ ] **Crear lista de errores** en un archivo `ERRORES.md`
  - Categorizar por tipo (imports, docstrings, etc.)
  - Priorizar por severidad

#### Noche (1 hora) - OPCIONAL
- [ ] **Leer documentación OCA**
  - https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst
  - https://github.com/OCA/maintainer-tools

**✅ Entregable Día 1:** CI/CD configurado, lista de errores documentada

---

### DÍA 2 (Martes) - Limpieza de Código ⏱️ 6-8 horas

#### Mañana (4 horas)
- [ ] **Eliminar `# -*- coding: utf-8 -*-`**
  - En TODOS los archivos `.py`
  - Usar VS Code: Find & Replace en todos los archivos

- [ ] **Agregar Copyright Headers**
  ```python
  # Copyright 2024 Javier Alejandro Pérez <tu@email.com>
  # License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
  ```
  - Agregar al inicio de CADA archivo `.py`

- [ ] **Formatear código automáticamente**
  ```bash
  make format
  # Esto ejecuta black + isort automáticamente
  ```

#### Tarde (3 horas)
- [ ] **Crear `constants.py`**
  - Copiar código del archivo `codigo_mejorado_ejemplos.md`
  - Mover `ESTADOS_MEXICO` desde `recepcion.py` y `envio.py`
  - Mover `TIPOS_ARTICULO`, `TIPOS_CLIENTE`, `FORMAS_PAGO`

- [ ] **Actualizar imports en modelos**
  ```python
  # En recepcion.py y envio.py
  from .constants import ESTADOS_MEXICO, TIPOS_CLIENTE, FORMAS_PAGO
  ```

- [ ] **Ejecutar tests**
  ```bash
  make lint
  # Debería tener ~70% menos errores
  ```

#### Noche (1 hora) - COMMIT
- [ ] **Hacer primer commit**
  ```bash
  git add .
  git commit -m "refactor: aplicar OCA guidelines y formateo automático

  - Eliminar # -*- coding: utf-8 -*-
  - Agregar copyright headers
  - Formatear con black + isort
  - Crear constants.py para valores compartidos
  - Reducir duplicación de código"
  
  git push origin develop
  ```

**✅ Entregable Día 2:** Código limpio, OCA compliance >70%

---

### DÍA 3 (Miércoles) - Docstrings ⏱️ 6-8 horas

#### Mañana (4 horas)
- [ ] **Agregar docstrings a clases**
  ```python
  class PaqueteriaEnvio(models.Model):
      """Gestión de envíos de paquetería internacional México-Cuba.
      
      Este modelo maneja el proceso completo de envío desde la recepción
      hasta la distribución en maletas, incluyendo:
      - Cálculos automáticos de costos según tarifas
      - Distribución de pesos en múltiples maletas
      - Cálculo de impuestos aduanales
      - Control financiero de cobros
      """
  ```
  - Revisar CADA modelo y agregar docstring descriptivo

#### Tarde (3 horas)
- [ ] **Agregar docstrings a métodos**
  ```python
  def _compute_peso_cobrar(self):
      """Calcula el peso a cobrar como el máximo entre etiqueta y volumen.
      
      El peso central NO se incluye en el cálculo, es solo informativo.
      """
  ```
  - Todos los `@api.depends`, `@api.constrains`, `@api.onchange`
  - Todos los métodos públicos
  - Métodos complejos con ejemplos

#### Noche (1 hora) - VERIFICAR
- [ ] **Ejecutar pylint**
  ```bash
  make lint
  # Verificar que no haya warnings de docstrings faltantes
  ```

**✅ Entregable Día 3:** Docstrings completos, OCA compliance >85%

---

### DÍA 4 (Jueves) - Setup Tests ⏱️ 6-8 horas

#### Mañana (4 horas)
- [ ] **Crear estructura de tests**
  ```bash
  mkdir -p custom-addons/paqueteria_internacional/tests
  cd custom-addons/paqueteria_internacional/tests
  touch __init__.py
  touch common.py
  touch test_provincia.py
  touch test_articulo.py
  touch test_recepcion.py
  touch test_envio.py
  touch test_envio_articulo.py
  touch test_maleta.py
  touch test_fecha_envio.py
  ```

- [ ] **Copiar `common.py`**
  - Del archivo `codigo_mejorado_ejemplos.md`
  - Setup con datos de prueba

- [ ] **Copiar `tests/__init__.py`**
  - Importar todos los módulos de test

#### Tarde (3 horas)
- [ ] **Escribir primeros tests básicos**
  - `test_provincia.py`: Crear, leer, actualizar
  - `test_articulo.py`: Crear artículos de cada tipo
  - Tests sencillos para validar setup

- [ ] **Ejecutar tests**
  ```bash
  make test
  # Verificar que pasen aunque sean pocos
  ```

#### Noche (1 hora) - COMMIT
- [ ] **Commit de tests básicos**
  ```bash
  git add .
  git commit -m "test: agregar estructura de tests y casos básicos

  - Crear common.py con setup compartido
  - Tests básicos para provincia y artículo
  - Configurar pytest y coverage"
  
  git push origin develop
  ```

**✅ Entregable Día 4:** Estructura de tests funcionando, ~20% coverage

---

### DÍA 5 (Viernes) - Tests Core ⏱️ 8 horas

#### Mañana (4 horas)
- [ ] **Tests de Envío (Crítico)**
  - Copiar `test_envio.py` del archivo `codigo_mejorado_ejemplos.md`
  - Verificar TODOS los tests:
    - `test_01_create_envio_secuencia`
    - `test_02_compute_peso_cobrar_etiqueta_mayor`
    - `test_03_compute_peso_cobrar_volumen_mayor`
    - `test_04_compute_embalaje_una_fraccion`
    - `test_05_compute_embalaje_dos_fracciones`
    - `test_06_compute_tarifa_normal_habana`
    - `test_07_compute_tarifa_normal_resto`
    - `test_08_compute_tarifa_vip_habana`
    - `test_09_compute_tarifa_vip_resto`
    - `test_10_compute_totales_basico`
    - `test_11_compute_totales_con_documentos`
    - `test_12_constraint_peso_etiqueta_negativo`
    - `test_13_constraint_peso_volumen_negativo`
    - `test_14_constraint_sin_peso`
    - `test_15_onchange_importar_recepcion`

#### Tarde (4 horas)
- [ ] **Tests de Envío Artículo**
  - Tests de cálculo de costos celulares
  - Tests de cálculo de costos laptops
  - Tests de artículos tipo "otro"
  - Tests de cantidades

- [ ] **Ejecutar y verificar cobertura**
  ```bash
  make coverage
  # Meta: >60% después de hoy
  ```

**✅ Entregable Día 5:** Tests de lógica core, ~60-70% coverage

---

## 📅 SEMANA 2: COMPLETAR Y PULIR

### DÍA 6 (Lunes) - Tests Restantes ⏱️ 8 horas

#### Mañana (4 horas)
- [ ] **Tests de Recepción**
  - Crear recepción con fotos
  - Importar datos a envío
  - Validaciones de campos requeridos

- [ ] **Tests de Maleta**
  - Crear maleta
  - Distribuir envíos
  - Calcular peso total
  - Validar límites

#### Tarde (4 horas)
- [ ] **Tests de Fecha Envío**
  - Crear fecha envío
  - Asociar envíos y maletas
  - Calcular estadísticas
  - Dashboard

- [ ] **Verificar cobertura**
  ```bash
  make coverage
  # Meta: >85%
  ```

**✅ Entregable Día 6:** Coverage >85%, todos los modelos testeados

---

### DÍA 7 (Martes) - README y Docs ⏱️ 6 horas

#### Mañana (3 horas)
- [ ] **README.md Completo**
  ```markdown
  # Paquetería Internacional - Módulo Odoo
  
  ## Descripción
  [Descripción detallada del módulo]
  
  ## Características
  - ✅ Gestión de recepciones por admin regional
  - ✅ Cálculo automático de costos
  - ✅ Sistema de distribución en maletas
  - ✅ Dashboard con estadísticas
  
  ## Requisitos
  - Odoo 19.0
  - Python 3.10+
  - PostgreSQL 14+
  
  ## Instalación
  [Pasos detallados]
  
  ## Configuración
  [Configuración inicial]
  
  ## Uso
  [Ejemplos de uso]
  
  ## Tests
  [Cómo ejecutar tests]
  
  ## Contribuir
  [Guía de contribución]
  
  ## Licencia
  LGPL-3.0
  
  ## Autor
  Javier Alejandro Pérez
  ```

#### Tarde (3 horas)
- [ ] **CHANGELOG.md**
  ```markdown
  # Changelog
  
  ## [1.0.0] - 2026-01-XX
  ### Added
  - Gestión de recepciones regionales
  - Cálculo automático de costos
  - Sistema de distribución en maletas
  - Dashboard con estadísticas
  
  ### Changed
  - Aplicar OCA guidelines
  - Mejorar estructura de código
  
  ### Fixed
  - Validaciones de peso
  - Cálculo de tarifas
  ```

- [ ] **CONTRIBUTING.md**
  ```markdown
  # Guía de Contribución
  
  ## Código de Conducta
  ## Cómo Contribuir
  ## Estándares de Código
  ## Proceso de Pull Request
  ## Tests
  ## Documentación
  ```

**✅ Entregable Día 7:** Documentación completa

---

### DÍA 8 (Miércoles) - Refactoring ⏱️ 6-8 horas

#### Mañana (4 horas)
- [ ] **Mejorar `envio.py`**
  - Copiar código mejorado de `codigo_mejorado_ejemplos.md`
  - Agregar `tracking=True` en campos
  - Agregar `_inherit = ['mail.thread', 'mail.activity.mixin']`
  - Agregar constraints SQL
  - Mejorar docstrings
  - Agregar logging

#### Tarde (3 horas)
- [ ] **Eliminar código duplicado**
  - Eliminar `@api.onchange` redundante en `envio.py`
  - Usar constants.py en todos los modelos
  - Refactorizar métodos repetidos

- [ ] **Ejecutar tests**
  ```bash
  make test
  # Asegurar que NADA se rompió
  ```

**✅ Entregable Día 8:** Código refactorizado, tests pasando

---

### DÍA 9 (Jueves) - Seguridad ⏱️ 6 horas

#### Mañana (3 horas)
- [ ] **Crear grupos de seguridad**
  ```xml
  <!-- security/security.xml -->
  <record id="group_paqueteria_admin" model="res.groups">
      <field name="name">Paquetería / Administrador</field>
      <field name="category_id" ref="base.module_category_operations"/>
  </record>
  
  <record id="group_paqueteria_user" model="res.groups">
      <field name="name">Paquetería / Usuario</field>
      <field name="category_id" ref="base.module_category_operations"/>
      <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
  </record>
  ```

- [ ] **Actualizar `ir.model.access.csv`**
  - Separar permisos admin vs usuario
  - Restringir delete solo a admins

#### Tarde (3 horas)
- [ ] **Agregar validaciones de seguridad**
  ```python
  @api.constrains('estado_mexico')
  def _check_admin_region(self):
      """Validar que admin solo opere en su región asignada"""
      # Implementar validación
  ```

- [ ] **Sanitizar inputs**
  - Validar teléfonos
  - Validar pesos
  - Prevenir SQL injection en búsquedas

**✅ Entregable Día 9:** Seguridad mejorada, grupos configurados

---

### DÍA 10 (Viernes) - Optimizaciones ⏱️ 6 horas

#### Mañana (3 horas)
- [ ] **Agregar índices faltantes**
  ```python
  name = fields.Char(..., index=True)
  remitente_nombre = fields.Char(..., index=True)
  destinatario_nombre = fields.Char(..., index=True)
  ```

- [ ] **Optimizar búsquedas**
  - Agregar `search_fields` a modelos
  - Configurar paginación en listas

#### Tarde (3 horas)
- [ ] **Performance testing**
  - Crear dataset grande (100+ envíos)
  - Medir tiempos de carga
  - Optimizar queries lentas

- [ ] **Cache de cálculos**
  - Verificar uso de `store=True`
  - Optimizar métodos compute

**✅ Entregable Día 10:** Performance optimizado, índices agregados

---

### DÍA 11-12 (Lunes-Martes) - BUFFER Y AJUSTES FINALES ⏱️ 12 horas

- [ ] **Corregir fallos de CI**
  - Revisar GitHub Actions
  - Corregir tests que fallen
  - Ajustar configuraciones

- [ ] **Revisión completa**
  - Code review manual
  - Verificar TODOS los checklists
  - Corregir últimos detalles

- [ ] **Documentación final**
  - Screenshots para README
  - Diagramas de flujo
  - Video demo (opcional)

**✅ Entregable Final:** Módulo 100% listo para Wiixoo

---

## 📝 CHECKLISTS DIARIOS

### Checklist Inicio del Día
- [ ] Activar virtual environment: `source .venv/bin/activate`
- [ ] Pull últimos cambios: `git pull origin develop`
- [ ] Revisar tasks del día
- [ ] Estimar tiempo realista

### Checklist Fin del Día
- [ ] Ejecutar tests: `make test`
- [ ] Ejecutar linter: `make lint`
- [ ] Commit de progreso: `git commit -m "..."`
- [ ] Push a GitHub: `git push origin develop`
- [ ] Actualizar este documento con progreso
- [ ] Planificar mañana

---

## 🎯 HITOS CLAVE

| Día | Hito | Métrica |
|-----|------|---------|
| 1 | CI/CD Setup | Pipeline funcionando |
| 2 | Código Limpio | OCA compliance >70% |
| 3 | Documentado | Docstrings completos |
| 5 | Tests Core | Coverage >60% |
| 6 | Tests Completos | Coverage >85% |
| 7 | Documentación | README completo |
| 10 | Optimizado | Performance OK |
| 12 | LISTO | Todo funcional |

---

## ⚠️ RIESGOS Y MITIGACIÓN

### Riesgo 1: Tests toman más tiempo
**Mitigación:** Priorizar tests críticos (envío, cálculos)

### Riesgo 2: CI falla en GitHub
**Mitigación:** Probar local primero con `make test`

### Riesgo 3: Refactoring rompe funcionalidad
**Mitigación:** Tests antes y después, commits pequeños

---

## 💡 TIPS DE PRODUCTIVIDAD

1. **Usa el Makefile:** `make test`, `make lint`, `make format`
2. **Commits frecuentes:** Cada 1-2 horas
3. **Tests primero:** TDD cuando sea posible
4. **Pide ayuda:** Usa GitHub Issues si te atoras
5. **Breaks:** Pomodoro (25 min trabajo, 5 min break)

---

## 🏆 RECOMPENSAS

- ✅ Día 5: Celebra >60% coverage
- ✅ Día 7: README completo = pausa extra
- ✅ Día 10: >85% coverage = objetivo cumplido
- ✅ Día 12: MÓDULO LISTO = ¡Listo para Wiixoo! 🎉

---

¡VAMOS A TRANSFORMAR ESTE MÓDULO! 💪🚀
