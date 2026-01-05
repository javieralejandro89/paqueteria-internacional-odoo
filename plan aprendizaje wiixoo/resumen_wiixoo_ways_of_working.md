# Resumen: Ways of Working - Equipo de Desarrollo Wiixoo
## Metodología: Scrum Flexible (Sprints de 2 semanas)

---

## 🎯 PRINCIPIOS DE LIDERAZGO WIIXOO

### 1. Obsesión por la Personalización del Cliente
- Ir más allá de lo estándar para personalizar el camino del cliente
- Desarrollar soluciones que deleitan y superan expectativas
- Trabajar siempre con empatía, poniendo al cliente en el centro

### 2. Innovación Incansable para Líderes Inconformes
- Crear soluciones únicas y disruptivas
- Desafiar los límites y experimentar constantemente
- Fomentar creatividad y pensamiento audaz

### 3. Cuidado Mutuo y Crecimiento Colectivo
- Promover ambiente de respeto, confianza y apoyo
- Celebrar éxitos compartidos
- Apoyar desarrollo individual y levantarnos mutuamente ante desafíos

### 4. Ejecución con Visión y Propósito
- Cada línea de código orientada a generación de valor
- Mantener foco en ejecución, calidad y entrega
- Asegurar impacto significativo y medible

---

## 👥 ROLES Y RESPONSABILIDADES

### Product Owner (PO)
- **Gestión del Product Backlog** (historias de usuario, features, bugs)
- Articular la visión del producto
- Enlace con stakeholders
- Decisiones finales sobre priorización
- Participar en Sprint Review
- Disponibilidad para el equipo

### Scrum Master (SM)
- Facilitar ceremonias Scrum efectivamente
- Eliminar impedimentos
- Proteger al equipo de interrupciones
- Promover mejora continua
- Coach del equipo en prácticas ágiles
- Facilitador de transparencia

### Equipo de Desarrollo (TU ROL)
- **Entregar Incremento potencialmente desplegable cada Sprint**
- Autoorganización y multifuncionalidad
- Estimación y compromiso con el Sprint
- **Adherirse a la "Definición de Done"**
- Transparencia en Daily Scrum
- **Propiedad del código y sistemas**
- Colaboración estrecha con PO y SM

---

## 📅 FLUJO DE TRABAJO SCRUM

### Sprints
- **Duración:** 2 semanas fijas
- **Inicio/Fin:** Viernes a Viernes
- **Objetivo del Sprint:** Definido al inicio, no cambia
- **Incremento:** Potencialmente entregable y "Terminado"

---

## 🎪 CEREMONIAS SCRUM

### 1. Sprint Planning (Viernes antes del Sprint)
- **Duración:** Máximo 4 horas (2 semanas Sprint)
- **Participantes:** PO, SM, Equipo Desarrollo (Yaser, Vladimir, Yanela, equipo)
- **Agenda:**
  - Definir Objetivo del Sprint con PO
  - Seleccionar Items del Product Backlog
  - Desglosar Sprint Backlog en tareas (1-2 días)
  - Confirmar compromiso

### 2. Daily Scrum (Stand-up)
- **Duración:** 15 minutos máximo
- **Frecuencia:** 2 presenciales (Lunes y Jueves tardes) + 3 electrónicos
- **Participantes:** Equipo Desarrollo (SM facilita, PO oyente)
- **Preguntas:**
  - ¿Qué hice ayer para el Objetivo del Sprint?
  - ¿Qué haré hoy para el Objetivo del Sprint?
  - ¿Hay impedimentos?

### 3. Sprint Review (Final del Sprint)
- **Duración:** Máximo 2 horas
- **Participantes:** PO, SM, Equipo, Stakeholders
- **Agenda:**
  - Introducción del Objetivo (PO)
  - Demostración del Incremento (Equipo)
  - Feedback de stakeholders
  - Revisión del Product Backlog

### 4. Sprint Retrospective (Después de Sprint Review)
- **Duración:** Máximo 1.5 horas
- **Participantes:** Solo Equipo Scrum (Desarrollo, PO, SM)
- **Proceso:**
  - Establecer ambiente seguro
  - Recopilar datos del Sprint
  - Generar ideas de mejora
  - Decidir 1-3 acciones SMART para próximo Sprint
  - Cerrar con acuerdos

### 5. Backlog Refinement (Continuo)
- **Tiempo dedicado:** ~10% capacidad del equipo por Sprint
- **Frecuencia:** 1-2 sesiones semanales de 1-1.5 horas
- **Participantes:** PO y Equipo Desarrollo
- **Objetivo:** 
  - PBIs claros y listos para futuros Sprints
  - Descomponer elementos grandes
  - Estimar esfuerzo (Story Points)

---

## ✅ DEFINICIÓN DE "DONE" (DOD)

### Criterios Mínimos:
1. ✅ Código cumple estándares de estilo Wiixoo
2. ✅ Pruebas unitarias escritas y pasadas
3. ✅ Pruebas de integración escritas y pasadas
4. ✅ **Code Review** aprobado por al menos otro miembro
5. ✅ Código integrado en rama principal (main)
6. ✅ Pruebas de regresión automáticas pasadas
7. ✅ Funcionalidad probada en staging/QA
8. ✅ Documentación técnica actualizada (APIs, config)
9. ✅ Cumple criterios de aceptación del PO
10. ✅ Desplegado a entorno de prueba (staging)

---

## 🛠️ PRÁCTICAS DE DESARROLLO Y CALIDAD

### Control de Versiones
- **Sistema:** Git (GitHub)
- **Estrategia:** Git Flow simplificado / Trunk-Based Development
- **Ramas:**
  - `main/master`: Siempre desplegable y estable
  - `feature/nombre-historia`: Cortas, eliminadas después de merge
  - `hotfix/nombre-problema`: Solo para urgencias en producción
- **Commits:** Claros, descriptivos, vinculados a IDs de tareas

### Integración Continua (CI)
- **Herramienta:** GitHub Actions
- **Frecuencia:** Integración al menos 1 vez/día
- **Pipeline automático:**
  - Construcción del proyecto
  - Pruebas unitarias e integración
  - Análisis de calidad (linter, análisis estático, pre-commit, SonarQube)
- **Fallo CI:** Prioridad máxima - resolver inmediatamente

### Despliegue Continuo (CD)
- **Herramienta:** GitHub Actions
- **Entornos:**
  - Desarrollo (local)
  - QA/Staging (replica producción)
  - Producción
- **Liberaciones:** Decisión del PO, cadencia frecuente

### Pruebas

#### Pruebas Unitarias
- Responsabilidad de cada desarrollador
- **Cobertura mínima: 85%**
- Ejecución automática en CI

#### Pruebas de Integración
- Verificar interacción entre componentes
- Automatizadas en CI/CD

#### Pruebas End-to-End (E2E)
- Herramientas: Cypress, Selenium, Playwright
- Simular flujos completos de usuario
- En QA/Staging

#### UAT (User Acceptance Testing)
- Responsabilidad: PO y stakeholders
- En cada Sprint Review o staging

### Code Reviews
- **Obligatorio:** Todo código antes de merge a main
- **Herramienta:** Pull Requests en GitHub
- **Revisores:** Al menos otro desarrollador
- **Foco:** Funcionalidad, estilo, rendimiento, seguridad, legibilidad, DOD
- **Actitud:** Comunicación constructiva y aprendizaje mutuo

### Gestión de Errores y Bugs
- Registro obligatorio en herramienta de gestión (Jira)
- Descripción clara, pasos reproducir, impacto
- Priorización en Product Backlog por PO
- Críticos: atención inmediata

### Documentación Técnica
- APIs, configuraciones, arquitecturas significativas
- Actualizada como parte de DOD
- Comentarios en código para lógica compleja
- README para módulos/proyectos

---

## 💬 COMUNICACIÓN Y COLABORACIÓN

### Herramientas
- **Gestión proyectos:** Odoo Project Management / Jira
- **Comunicación:** Slack, Microsoft Teams, correo
- **Código y repos:** GitHub
- **Documentación:** Confluence, Google Docs

### Principios
- **Transparencia:** Tableros actualizados en tiempo real
- **Métricas compartidas:** Velocity, Burndown Charts, Lead Time
- **Comunicación proactiva:** Impedimentos, retrasos, cambios
- **Cultura de preguntas:** No hay preguntas "tontas"

### Prácticas
- **Pair Programming / Mob Programming** para tareas complejas
- **Sesiones de Intercambio de Conocimiento**
- **Feedback Constructivo** (Code Reviews, Retrospectivas)
- **Resolución de Conflictos** profesional y constructiva

---

## 🏗️ ARQUITECTURA Y DISEÑO

### Principios
1. **Modularidad y Desacoplamiento**
2. **Escalabilidad** (horizontal/vertical)
3. **Resiliencia y Fiabilidad**
4. **Seguridad por Diseño**
5. **Mantenibilidad y Extensibilidad**
6. **Microservicios** (cuando apropiado)
7. **Elección Tecnológica Pragmática**

### Proceso de Diseño
- Refinamiento continuo en Backlog Refinement
- Sesiones de diseño técnico para funcionalidades complejas
- Diagramas de alto nivel
- "Just Enough" Design (evitar sobre-ingeniería)
- Revisiones de diseño por pares

### Gestión Deuda Técnica
- Registro en Product Backlog con prioridad
- Sprints ocasionales dedicados a calidad
- CI/CD y DOD previenen acumulación

### Monitoreo y Observabilidad
- Métricas de rendimiento, errores, latencia
- Logs centralizados
- Alertas para eventos críticos

---

## 🔒 SEGURIDAD Y COMPLIANCE

### Mejores Prácticas Seguridad
- Análisis de amenazas y modelado
- **Codificación segura** (OWASP Top 10)
- Validación de entradas (prevenir SQL injection, XSS, CSRF)
- **Gestión de credenciales:** NO en código fuente
  - Usar gestores de secretos (HashiCorp Vault, AWS Secrets Manager)
- Control de acceso granular (RBAC, ABAC)
- Auditorías de seguridad (SAST, DAST)
- Pruebas de penetración periódicas
- Actualización de dependencias
- Cifrado datos (en tránsito HTTPS/TLS, en reposo)
- Capacitación continua en seguridad

### Compliance (si aplica)
- Identificar normativas (GDPR, CCPA, HIPAA, ISO 27001, PCI DSS)
- Políticas de privacidad de datos
- Trazabilidad y auditoría
- Gestión de registros (logs)
- Colaboración con legal/compliance

---

## 📊 ELEMENTOS DE TRABAJO EN JIRA

### 1. Épica (Epic)
- Gran cuerpo de trabajo (múltiples Sprints)
- Objetivo de negocio significativo
- Ejemplo: "Implementar Módulo E-commerce B2B en Odoo"

### 2. Historia (User Story)
- Unidad centrada en el usuario
- Completable en 1 Sprint
- Formato: "Como [usuario], quiero [funcionalidad], para que [beneficio]"
- Principio INVEST
- Estimada en Story Points

### 3. Tarea (Task)
- Trabajo técnico/administrativo
- Parte de Historia o independiente
- Estimada en horas/días
- Ejemplo: "Configurar permisos usuario B2B"

### 4. Error (Bug)
- Problema/fallo en software
- Incluye: pasos reproducir, esperado vs actual
- Priorizado por impacto/urgencia

---

## 📈 ESTADOS EN JIRA

1. **Backlog** - Inicial, no refinado
2. **Definido** - Refinado, criterios aceptación claros
3. **En Desarrollo** - Trabajo activo
4. **En Revisión** - Code Review
5. **En Pruebas** - QA/Testing
6. **Terminado** - Cumple DOD, desplegado a staging
7. **Bloqueado** - Impedimentos técnicos/externos

---

## 🎯 ESTIMACIÓN: PUNTOS DE ESFUERZO (FIBONACCI)

| Puntos | Complejidad | Tiempo Estimado | Descripción |
|--------|-------------|-----------------|-------------|
| 1 | Trivial | < 2 horas | Cambio muy simple |
| 2 | Muy Baja | 2-4 horas | Tarea pequeña |
| 3 | Baja | 4-8 horas | Tarea sencilla |
| 5 | Media | 1-2 días | Complejidad moderada |
| 8 | Alta | 2-3 días | Compleja, requiere investigación |
| 13 | Muy Alta | 3-5 días | Muy compleja, considerar dividir |
| 21+ | Extrema | > 5 días | DEBE dividirse |

---

## 📚 GUÍAS DE ESTILO DE CÓDIGO

### Para Proyectos Odoo
- **Referencia:** OCA (Odoo Community Association)
- **Documentación:**
  - https://www.odoo.com/documentation/17.0/es/contributing/development/coding_guidelines.html
  - https://www.odoo.com/documentation/17.0/es/contributing/development/git_guidelines.html
- **Herramientas:** flake8 con plugins Odoo, pre-commit

### Para Proyectos Python Generales
- **Referencia:** PEP 8
- **Documentación:** https://peps.python.org/pep-0008/
- **Herramientas:** flake8, black (formateador), isort (importaciones)

### Cumplimiento
- Revisiones de código
- Automatización en CI/CD
- Capacitación continua

---

## 🎓 MEJORA CONTINUA (KAIZEN)

### Retrospectivas de Sprint
- Identificar: qué funcionó, qué no, qué empezar/parar/continuar
- Acciones SMART para próximo Sprint

### Métricas y Monitoreo
- Velocity, Lead Time, Cycle Time, tasa defectos
- Identificar cuellos de botella

### Aprendizaje y Desarrollo
- Sesiones internas de conocimiento
- Conferencias, cursos, certificaciones
- Experimentación con nuevas tecnologías
- Lectura y estudio autónomo

### Análisis Post-Mortem
- Ante incidentes importantes
- Comprender causas raíz
- Aprender para evitar recurrencias

---

## 📋 PROPUESTAS DE SOLUCIÓN (ANEXO C)

### Elementos Clave:
1. **Introducción** - Descripción breve del cliente
2. **Situación Actual** - Procesos del cliente, problemas identificados
3. **Objetivos** - General y específicos
4. **Propuesta de Solución** - Requisitos funcionales, módulos Odoo, personalizaciones
5. **Descripción de Arquitectura** - Interrelación e integración
6. **Cronograma** - Fases, actividades, duración
7. **Últimas Consideraciones** - Resumen y aspectos relevantes

### Importante:
- Al entregar al cliente: **NO** incluir detalles funcionales específicos ni integración
- Alternativa: Presentación de diapositivas con elementos fundamentales

---

## 🎯 PUNTOS CLAVE PARA TU ONBOARDING

### Prioridades Inmediatas:
1. ✅ Entender la **Definición de Done** - es tu guía diaria
2. ✅ Familiarizarte con las **ceremonias** (Daily, Sprint Planning, etc.)
3. ✅ Configurar tu entorno con **herramientas de CI/CD** (GitHub Actions)
4. ✅ Revisar las **guías de estilo de código** (OCA para Odoo, PEP 8 para Python)
5. ✅ Entender el flujo de **branching** y **Pull Requests**
6. ✅ Conocer cómo usar **Jira** (o la herramienta de gestión que usen)
7. ✅ Participar activamente en **Code Reviews**
8. ✅ Abrazar la cultura de **mejora continua**

### Expectativas del Rol:
- **Autoorganización**: Decidir cómo abordar tu trabajo
- **Multifuncionalidad**: Tener skills en desarrollo, pruebas, DevOps
- **Propiedad del código**: Responsabilidad completa
- **Transparencia**: Comunicar progreso e impedimentos
- **Colaboración**: Trabajar estrechamente con PO, SM y equipo
- **Calidad**: Adherirse siempre a DOD

---

## 💡 CONSEJOS DE INTEGRACIÓN

1. **Primera semana**: Observa y aprende las dinámicas del equipo
2. **Haz preguntas**: La cultura fomenta preguntas sin miedo
3. **Participa en Retrospectivas**: Tu feedback es valioso desde el día 1
4. **Code Reviews**: Aprende del código existente antes de escribir
5. **Pair Programming**: Solicítalo para aprender más rápido
6. **Documenta**: Ayuda a futuros miembros del equipo
7. **Comunica impedimentos**: No te quedes atascado en silencio

---

¡Bienvenido al equipo Wiixoo! 🚀
