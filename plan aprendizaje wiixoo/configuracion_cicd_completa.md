# 🛠️ Configuración CI/CD y Herramientas
## Archivos de Configuración para Wiixoo

---

## 1. GITHUB ACTIONS - CI/CD

### Crear: `.github/workflows/ci.yml`

```yaml
name: CI - Paquetería Internacional

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint:
    name: Lint y Estilo de Código
    runs-on: ubuntu-latest
    steps:
      - name: Checkout código
        uses: actions/checkout@v3
      
      - name: Set up Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Cache pip
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install flake8 flake8-odoo black isort pylint
      
      - name: Flake8 (OCA Guidelines)
        run: |
          flake8 custom-addons/paqueteria_internacional/ --config=.flake8
      
      - name: Black (Formato)
        run: |
          black --check custom-addons/paqueteria_internacional/
      
      - name: isort (Imports)
        run: |
          isort --check-only custom-addons/paqueteria_internacional/
      
      - name: Pylint (Calidad)
        run: |
          pylint custom-addons/paqueteria_internacional/ --rcfile=.pylintrc || true

  test:
    name: Tests Unitarios
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: odoo_test
          POSTGRES_USER: odoo
          POSTGRES_PASSWORD: odoo
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - name: Checkout código
        uses: actions/checkout@v3
      
      - name: Set up Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Cache Odoo
        uses: actions/cache@v3
        with:
          path: |
            ~/odoo
            ~/.cache/pip
          key: ${{ runner.os }}-odoo-19-${{ hashFiles('**/requirements.txt') }}
      
      - name: Instalar dependencias del sistema
        run: |
          sudo apt-get update
          sudo apt-get install -y postgresql-client python3-dev libxml2-dev libxslt1-dev \
            libldap2-dev libsasl2-dev libssl-dev
      
      - name: Instalar Odoo 19
        run: |
          if [ ! -d ~/odoo ]; then
            git clone --depth 1 --branch 19.0 https://github.com/odoo/odoo.git ~/odoo
          fi
          pip install -r ~/odoo/requirements.txt
      
      - name: Copiar módulo a addons
        run: |
          mkdir -p ~/odoo/addons/custom
          cp -r custom-addons/paqueteria_internacional ~/odoo/addons/custom/
      
      - name: Ejecutar tests
        env:
          PGHOST: localhost
          PGPORT: 5432
          PGUSER: odoo
          PGPASSWORD: odoo
          PGDATABASE: odoo_test
        run: |
          cd ~/odoo
          python odoo-bin -c odoo.conf \
            -d odoo_test \
            --addons-path=addons,addons/custom \
            --test-enable \
            --stop-after-init \
            -i paqueteria_internacional \
            --log-level=test
      
      - name: Verificar cobertura (pytest-cov)
        run: |
          pip install pytest pytest-cov coverage
          cd custom-addons/paqueteria_internacional
          pytest tests/ \
            --cov=. \
            --cov-report=term-missing \
            --cov-report=xml \
            --cov-fail-under=85
      
      - name: Subir reporte de cobertura
        uses: codecov/codecov-action@v3
        with:
          files: ./custom-addons/paqueteria_internacional/coverage.xml
          fail_ci_if_error: true

  security:
    name: Análisis de Seguridad
    runs-on: ubuntu-latest
    steps:
      - name: Checkout código
        uses: actions/checkout@v3
      
      - name: Set up Python 3.10
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Instalar Bandit (Security)
        run: |
          pip install bandit[toml]
      
      - name: Run Bandit
        run: |
          bandit -r custom-addons/paqueteria_internacional/ -f json -o bandit-report.json || true
      
      - name: Upload Bandit report
        uses: actions/upload-artifact@v3
        with:
          name: bandit-report
          path: bandit-report.json

  build-status:
    name: Status General
    runs-on: ubuntu-latest
    needs: [lint, test, security]
    if: always()
    steps:
      - name: Check build status
        run: |
          if [ "${{ needs.lint.result }}" != "success" ] || \
             [ "${{ needs.test.result }}" != "success" ]; then
            echo "❌ Build failed"
            exit 1
          else
            echo "✅ Build successful"
          fi
```

---

## 2. PRE-COMMIT HOOKS

### Crear: `.pre-commit-config.yaml`

```yaml
# Pre-commit hooks para Paquetería Internacional
# Instalar: pip install pre-commit
# Activar: pre-commit install
# Ejecutar manual: pre-commit run --all-files

repos:
  # Hooks básicos
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
        name: Eliminar espacios al final
      - id: end-of-file-fixer
        name: Fix final de archivo
      - id: check-yaml
        name: Validar YAML
      - id: check-xml
        name: Validar XML
      - id: check-added-large-files
        name: Verificar archivos grandes
        args: ['--maxkb=500']
      - id: check-merge-conflict
        name: Detectar conflictos de merge
      - id: mixed-line-ending
        name: Fix line endings
        args: ['--fix=lf']
      - id: check-case-conflict
        name: Verificar case conflicts
      - id: check-json
        name: Validar JSON

  # Black - Formateador de código
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        name: Black (formato Python)
        language_version: python3.10
        args: ['--line-length=88']

  # isort - Ordenar imports
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        name: isort (ordenar imports)
        args: ['--profile', 'black', '--line-length=88']

  # Flake8 - Linter con OCA
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        name: Flake8 (OCA guidelines)
        additional_dependencies: 
          - flake8-odoo
          - flake8-bugbear
          - flake8-comprehensions
        args: ['--config=.flake8']

  # Pylint - Análisis estático
  - repo: https://github.com/PyCQA/pylint
    rev: v3.0.3
    hooks:
      - id: pylint
        name: Pylint (calidad código)
        args: ['--rcfile=.pylintrc', '--score=no']
        files: ^custom-addons/.*\.py$

  # Bandit - Seguridad
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        name: Bandit (seguridad)
        args: ['-c', '.bandit.yml']
        files: ^custom-addons/.*\.py$

  # Prettier - XML, JSON
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        name: Prettier (XML, JSON)
        types_or: [xml, json]
        args: ['--print-width=100', '--tab-width=4']

# Configuración global
default_language_version:
  python: python3.10

fail_fast: false
```

---

## 3. FLAKE8 CONFIGURATION

### Crear: `.flake8`

```ini
[flake8]
# OCA Guidelines compatible
max-line-length = 88
max-complexity = 16

# Ignorar errores específicos
extend-ignore = 
    # E203: whitespace before ':' (conflicto con black)
    E203,
    # W503: line break before binary operator (conflicto con black)
    W503,
    # E501: line too long (manejado por black)
    E501,
    # E722: do not use bare except (pylint lo maneja)
    E722,

# Excluir directorios
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    build,
    dist,
    *.egg-info,
    .tox,
    .pytest_cache,
    migrations,

# OCA específico
per-file-ignores =
    __init__.py:F401,F403
    tests/*.py:D100,D101,D102,D103

# Plugins OCA
enable-extensions = 
    flake8-odoo

# OCA-specific
odoo-addons-path = custom-addons

select =
    # Pycodestyle errors
    E,
    # Pycodestyle warnings  
    W,
    # Pyflakes
    F,
    # Complexity
    C90,
    # OCA checks
    N8,
```

---

## 4. PYLINT CONFIGURATION

### Crear: `.pylintrc`

```ini
[MASTER]
# Odoo addons path
init-hook='import sys; sys.path.append("custom-addons")'

# Extensiones de archivos a analizar
extension-pkg-whitelist=
    lxml,
    odoo

# No cargar plugins por defecto
load-plugins=
    pylint.extensions.docparams,
    pylint.extensions.docstyle,

# Paralelización
jobs=4

[MESSAGES CONTROL]
# Deshabilitar mensajes específicos
disable=
    # Informational
    locally-disabled,
    file-ignored,
    suppressed-message,
    # Conflictos con Black
    line-too-long,
    bad-continuation,
    # Odoo específico
    missing-module-docstring,
    consider-using-f-string,
    # Too restrictive
    too-few-public-methods,
    too-many-instance-attributes,
    too-many-arguments,
    too-many-locals,
    too-many-branches,
    too-many-statements,

[REPORTS]
output-format=colorized
score=yes

[BASIC]
# Convenciones de nombres Odoo
good-names=i,j,k,ex,Run,_,id,cr,uid

# Docstrings
docstring-min-length=10
no-docstring-rgx=^_

[FORMAT]
max-line-length=88
indent-string='    '

[VARIABLES]
# Variables dummy permitidas
dummy-variables-rgx=_.*|dummy

[DESIGN]
max-args=10
max-locals=25
max-returns=6
max-branches=15
max-statements=60
max-parents=7
max-attributes=10
min-public-methods=0
max-public-methods=25
```

---

## 5. BLACK CONFIGURATION

### Crear: `pyproject.toml`

```toml
[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  # Directorios a excluir
  \.git
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
  | migrations
)/
'''

[tool.isort]
profile = "black"
line_length = 88
known_odoo = ["odoo"]
known_third_party = ["lxml", "werkzeug", "dateutil"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "ODOO", "FIRSTPARTY", "LOCALFOLDER"]
default_section = "THIRDPARTY"
skip_glob = ["**/migrations/*", "**/__pycache__/*"]

[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-ra -q --strict-markers --cov-report=term-missing"

[tool.coverage.run]
source = ["."]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__pycache__/*",
    "*/static/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
fail_under = 85

[tool.bandit]
exclude_dirs = ["/tests/", "/migrations/"]
skips = ["B101", "B601"]  # B101: assert_used, B601: paramiko
```

---

## 6. BANDIT CONFIGURATION (SEGURIDAD)

### Crear: `.bandit.yml`

```yaml
# Configuración de Bandit para análisis de seguridad

tests:
  - B201  # flask_debug_true
  - B301  # pickle
  - B302  # marshal
  - B303  # md5
  - B304  # ciphers
  - B305  # cipher_modes
  - B306  # mktemp_q
  - B307  # eval
  - B308  # mark_safe
  - B309  # httpsconnection
  - B310  # urllib_urlopen
  - B311  # random
  - B312  # telnetlib
  - B313  # xml_bad_cElementTree
  - B314  # xml_bad_ElementTree
  - B315  # xml_bad_expatreader
  - B316  # xml_bad_expatbuilder
  - B317  # xml_bad_sax
  - B318  # xml_bad_minidom
  - B319  # xml_bad_pulldom
  - B320  # xml_bad_etree
  - B321  # ftplib
  - B323  # unverified_context
  - B324  # hashlib_new_insecure_functions
  - B325  # tempnam
  - B401  # import_telnetlib
  - B402  # import_ftplib
  - B403  # import_pickle
  - B404  # import_subprocess
  - B405  # import_xml_etree
  - B406  # import_xml_sax
  - B407  # import_xml_expat
  - B408  # import_xml_minidom
  - B409  # import_xml_pulldom
  - B410  # import_lxml
  - B411  # import_xmlrpclib
  - B412  # import_httpoxy
  - B413  # import_pycrypto
  - B501  # request_with_no_cert_validation
  - B502  # ssl_with_bad_version
  - B503  # ssl_with_bad_defaults
  - B504  # ssl_with_no_version
  - B505  # weak_cryptographic_key
  - B506  # yaml_load
  - B507  # ssh_no_host_key_verification
  - B601  # paramiko_calls
  - B602  # subprocess_popen_with_shell_equals_true
  - B603  # subprocess_without_shell_equals_true
  - B604  # any_other_function_with_shell_equals_true
  - B605  # start_process_with_a_shell
  - B606  # start_process_with_no_shell
  - B607  # start_process_with_partial_path
  - B608  # hardcoded_sql_expressions
  - B609  # linux_commands_wildcard_injection
  - B610  # django_extra_used
  - B611  # django_rawsql_used
  - B701  # jinja2_autoescape_false
  - B702  # use_of_mako_templates
  - B703  # django_mark_safe

exclude_dirs:
  - /tests/
  - /migrations/
  - /.venv/
  - /venv/
  - __pycache__

skips:
  # B101: Test assert_used - común en tests
  # B601: Paramiko - usado en Odoo
```

---

## 7. GITIGNORE COMPLETO

### Actualizar: `.gitignore`

```gitignore
# ========== Python ==========
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg
*.egg-info/
dist/
build/
*.whl

# ========== Virtual Environments ==========
venv/
.venv/
ENV/
env/
.env

# ========== IDEs ==========
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# ========== Odoo ==========
filestore/
sessions/
*.log
odoo.conf
odoo-server.conf

# ========== Testing ==========
.pytest_cache/
.coverage
htmlcov/
coverage.xml
*.cover
.tox/

# ========== CI/CD ==========
.mypy_cache/
.ruff_cache/
bandit-report.json

# ========== Temporales ==========
*.tmp
*.bak
*.swp
.cache/

# ========== OS ==========
Thumbs.db
Desktop.ini
.Trashes
```

---

## 8. DEPENDENCIAS DEL PROYECTO

### Crear: `requirements-dev.txt`

```txt
# Herramientas de desarrollo

# Linting
flake8==7.0.0
flake8-odoo==1.6.0
flake8-bugbear==23.12.2
flake8-comprehensions==3.14.0
pylint==3.0.3

# Formatting
black==23.12.1
isort==5.13.2

# Testing
pytest==7.4.3
pytest-cov==4.1.0
coverage==7.4.0

# Security
bandit==1.7.6

# Pre-commit
pre-commit==3.6.0

# Debugging
ipdb==0.13.13
pdbpp==0.10.3

# Documentation
Sphinx==7.2.6
sphinx-rtd-theme==2.0.0
```

---

## 9. SCRIPT DE INSTALACIÓN

### Crear: `setup_dev.sh`

```bash
#!/bin/bash
# Script de instalación de entorno de desarrollo

set -e

echo "🚀 Configurando entorno de desarrollo..."

# Colores
GREEN='\033[0.32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python 3.10+
python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo -e "${RED}❌ Se requiere Python 3.10 o superior${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python ${python_version} detectado${NC}"

# Crear virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creando virtual environment..."
    python3 -m venv .venv
    echo -e "${GREEN}✅ Virtual environment creado${NC}"
fi

# Activar virtual environment
source .venv/bin/activate

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias de desarrollo
echo "📦 Instalando dependencias de desarrollo..."
pip install -r requirements-dev.txt

# Instalar pre-commit hooks
echo "🎣 Instalando pre-commit hooks..."
pre-commit install

# Ejecutar pre-commit en todos los archivos (primera vez)
echo "🔍 Ejecutando pre-commit en todos los archivos..."
pre-commit run --all-files || true

echo ""
echo -e "${GREEN}✅ Entorno de desarrollo configurado exitosamente!${NC}"
echo ""
echo "📝 Próximos pasos:"
echo "  1. Activar virtual environment: source .venv/bin/activate"
echo "  2. Ejecutar tests: pytest tests/"
echo "  3. Verificar código: flake8 custom-addons/"
echo "  4. Formatear código: black custom-addons/"
echo ""
```

### Hacer ejecutable:

```bash
chmod +x setup_dev.sh
```

---

## 10. MAKEFILE PARA COMANDOS COMUNES

### Crear: `Makefile`

```makefile
.PHONY: help install test lint format clean

help:
	@echo "📚 Comandos disponibles:"
	@echo ""
	@echo "  make install   - Instalar entorno de desarrollo"
	@echo "  make test      - Ejecutar tests"
	@echo "  make lint      - Verificar código (flake8, pylint)"
	@echo "  make format    - Formatear código (black, isort)"
	@echo "  make clean     - Limpiar archivos temporales"
	@echo "  make pre-commit - Ejecutar pre-commit en todos los archivos"
	@echo "  make coverage  - Generar reporte de cobertura"

install:
	@echo "🚀 Instalando entorno de desarrollo..."
	bash setup_dev.sh

test:
	@echo "🧪 Ejecutando tests..."
	pytest tests/ -v --cov=custom-addons/paqueteria_internacional --cov-report=term-missing

lint:
	@echo "🔍 Verificando código..."
	flake8 custom-addons/paqueteria_internacional/
	pylint custom-addons/paqueteria_internacional/

format:
	@echo "✨ Formateando código..."
	black custom-addons/paqueteria_internacional/
	isort custom-addons/paqueteria_internacional/

clean:
	@echo "🧹 Limpiando archivos temporales..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov/ .mypy_cache/

pre-commit:
	@echo "🎣 Ejecutando pre-commit..."
	pre-commit run --all-files

coverage:
	@echo "📊 Generando reporte de cobertura..."
	pytest tests/ --cov=custom-addons/paqueteria_internacional --cov-report=html
	@echo "Reporte generado en: htmlcov/index.html"
```

---

## 🚀 INSTRUCCIONES DE USO

### Configuración Inicial

```bash
# 1. Clonar el repositorio
git clone https://github.com/javieralejandro89/paqueteria-internacional-odoo.git
cd paqueteria-internacional-odoo

# 2. Instalar entorno de desarrollo
make install
# O manual:
bash setup_dev.sh

# 3. Activar virtual environment
source .venv/bin/activate
```

### Workflow Diario

```bash
# Antes de hacer commit
make format    # Formatear código
make lint      # Verificar estilo
make test      # Ejecutar tests

# O simplemente hacer commit (pre-commit se ejecuta automáticamente)
git add .
git commit -m "feat: agregar validación de peso"
```

### Comandos Útiles

```bash
# Ver todos los comandos
make help

# Solo tests
make test

# Solo linting
make lint

# Limpiar archivos temporales
make clean

# Ver cobertura en HTML
make coverage
```

---

## ✅ CHECKLIST DE INTEGRACIÓN

- [ ] Crear todos los archivos de configuración
- [ ] Ejecutar `make install`
- [ ] Verificar que pre-commit funcione: `pre-commit run --all-files`
- [ ] Corregir errores de flake8
- [ ] Formatear código con black
- [ ] Escribir tests (mínimo 85% cobertura)
- [ ] Verificar que CI pase: push a GitHub
- [ ] Configurar branch protection en GitHub
- [ ] Activar status checks requeridos

---

¡Con esto tendrás un pipeline CI/CD completo y profesional según estándares de Wiixoo! 🚀
