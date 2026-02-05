# Feature Development Cycle (9 Phases: 8 Core + Phase 5.5 VERIFY)

## Objetivo

Este documento define el flujo de trabajo exacto para implementar cualquier feature. Siguiendo este ciclo se garantiza consistencia, trazabilidad y calidad.

**NUEVO:** Fase 5.5 (VERIFY) - Browser automation tests con agent-browser para validación frontend automática.

---

## Resumen Visual

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FEATURE DEVELOPMENT CYCLE (9 PHASES)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   1. INTERVIEW       2. THINK CRITICALLY    3. PLAN         4. BRANCH       │
│   ┌─────────┐       ┌─────────────┐       ┌─────────┐     ┌─────────┐     │
│   │ Preguntas│ ───► │ 11-Step     │ ───► │ Explorar │───► │ git     │     │
│   │ Decisiones│      │ Protocol    │       │ Diseñar │     │ checkout│     │
│   │ spec.md  │       │ analysis.md │       │ design.md│     │ -b      │     │
│   └─────────┘       └─────────────┘       └─────────┘     └─────────┘     │
│       │                    │                    │                │          │
│       ▼                    ▼                    ▼                ▼          │
│   📄 spec.md          📄 analysis.md       📄 design.md     🌿 branch     │
│   📄 status.md        📄 decisions.md      📄 tasks.md      📄 status.md  │
│                                                                    │        │
│                                                                    ▼        │
│   5. IMPLEMENT                                                              │
│   ┌──────────────────────────────────────────────────────────────┐          │
│   │ Código → Tests → Commits → Documentación viva                │          │
│   └──────────────────────────────────────────────────────────────┘          │
│       │                                                                      │
│       ▼                                                                      │
│   5.5 VERIFY ← NUEVO!                                                        │
│   ┌──────────────────────────────────────────────────────────────┐          │
│   │ agent-browser E2E → Screenshots → Security Filters            │          │
│   │ Auto-run si cambios tsx/jsx/css + test scripts existen        │          │
│   │ Bloquea PR si tests fallan                                    │          │
│   └──────────────────────────────────────────────────────────────┘          │
│       │                                                                      │
│       ▼                                                                      │
│   7. MERGE              6. PR (+ test results)  ◄──────────────             │
│   ┌─────────┐          ┌─────────┐                                          │
│   │ Review  │   ◄───   │ Push    │                                          │
│   │ Approve │          │ gh pr   │                                          │
│   │ Update  │          │ create  │                                          │
│   └─────────┘          └─────────┘                                          │
│       │                                                                      │
│       ▼                                                                      │
│   8. WRAP-UP                                                                 │
│   ┌─────────┐                                                                │
│   │ Context │                                                                │
│   │ Learnings│                                                               │
│   │ Cleanup │                                                                │
│   └─────────┘                                                                │
│       │                                                                      │
│       ▼                                                                      │
│   📄 status.md → 🟢 Complete                                                │
│   📄 wrap_up.md → Learnings captured                                        │
│   📄 _index.md UPDATED                                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ REGLA CRÍTICA: DOCUMENTACIÓN VIVA

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    📋 DOCUMENTATION UPDATE RULES                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   La documentación NO se actualiza "al final". Se actualiza EN TIEMPO REAL. │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ tasks.md - ACTUALIZAR EN CADA TASK                                  │   │
│   ├─────────────────────────────────────────────────────────────────────┤   │
│   │ ANTES de empezar task:    - [ ] Task 1  →  - [🟡] Task 1           │   │
│   │ DESPUÉS de completar:     - [🟡] Task 1  →  - [x] Task 1           │   │
│   │ Si hay problema:          - [🟡] Task 1  →  - [🔴] Task 1 (blocked)│   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ status.md - ACTUALIZAR EN CADA CAMBIO DE FASE                       │   │
│   ├─────────────────────────────────────────────────────────────────────┤   │
│   │ Interview completado        → Phase: Interview ✅                   │   │
│   │ Analysis completado         → Phase: Critical Analysis ✅           │   │
│   │ Plan aprobado               → Phase: Plan ✅                        │   │
│   │ Branch creado               → Phase: Branch ✅, Current: Implement  │   │
│   │ Cada 3 tasks                → Progress: 3/10 tasks                  │   │
│   │ Blocker encontrado          → Blockers: [descripción]               │   │
│   │ PR creado                   → Phase: PR, Link: [url]                │   │
│   │ Merged                      → Status: 🟢 Complete                   │   │
│   │ Wrap-Up complete            → Learnings captured                    │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ⏰ COMMIT DOCS CADA 30 MINUTOS O CADA 3 TASKS (lo que pase primero)       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Marcadores de Tasks

| Marcador | Significado | Cuándo usar |
|----------|-------------|-------------|
| `- [ ]` | Pendiente | Task no iniciada |
| `- [🟡]` | En progreso | ANTES de empezar la task |
| `- [x]` | Completada | DESPUÉS de completar |
| `- [🔴]` | Bloqueada | Hay un impedimento |
| `- [⏭️]` | Saltada | Decidido no hacer (con nota) |

---

## Fase 1: INTERVIEW (Especificación)

### Propósito
Capturar TODAS las decisiones técnicas y de producto ANTES de escribir código.

### Cómo Iniciar
```
"Interview me about FEAT-XXX"
/interview FEAT-XXX
```

### Proceso

1. **Claude hace preguntas estructuradas** (máx 3-4 por turno):
   - UI/UX decisions
   - Comportamiento del sistema
   - Edge cases
   - Límites y restricciones
   - Integraciones
   - **Market Validation** (Pain Level 7+? - SaaS Validator)

2. **El usuario responde con opciones claras**:
   - ✅ BIEN: "Import desde .env (DATABASE_URL format)"
   - ✅ BIEN: "Retry 3x automático + notificación"
   - ❌ MAL: "No sé, lo que tú creas"

3. **Claude actualiza spec.md** con cada decisión en formato tabla

### 📄 Documentos actualizados
- `spec.md` → Decisiones documentadas
- `status.md` → Phase: Interview ✅

---

## Fase 2: THINK CRITICALLY (Análisis Crítico) ← NUEVA

### Propósito
Análisis riguroso pre-implementación que simula una revisión de un staff engineer paranoico. Previene errores arquitectónicos costosos.

### Cómo Iniciar
```
/think-critically FEAT-XXX
```

### Proceso

1. Lee spec.md completado (output de Interview)
2. Determina profundidad de análisis (ver reglas de abreviación)
3. Ejecuta protocolo de 11 pasos (o abreviado)
4. Genera analysis.md

### Reglas de Abreviación Automática

| Condición | Pasos | Razón |
|-----------|-------|-------|
| Feature nueva + sistema nuevo | Los 11 pasos | Máximo riesgo arquitectónico |
| Feature nueva + patrones existentes | 1-2-3-5-9-11 | Riesgo medio |
| Feature pequeña/clara | 1-2-5-11 | Riesgo bajo |
| Bug fix / hotfix | Saltar completamente | Sin riesgo arquitectónico |

### Los 11 Pasos

```
 1. Clarificación del Problema    - ¿Qué estamos resolviendo exactamente?
 2. Asunciones Implícitas ⚠️      - ¿Qué asumimos que es verdad?
 3. Espacio de Diseño             - ¿Qué enfoques existen?
 4. Análisis de Trade-offs        - ¿Qué estamos intercambiando?
 5. Análisis de Fallos            - ¿Qué se romperá y cómo?
 6. Límites e Invariantes         - ¿Qué debe ser siempre verdad?
 7. Observabilidad                - ¿Cómo sabremos si funciona?
 8. Reversibilidad                - ¿Podemos deshacer esto?
 9. Revisión Adversarial 🔴       - Ataca tu propio diseño
10. Delegación IA                 - ¿Qué puede automatizar Ralph?
11. Resumen de Decisión           - Síntesis final + nivel de confianza
```

### ⚠️ Condiciones de Pausa (Ralph Loop)

El análisis PAUSA automáticamente si:
1. **Step 2:** Asunción con confianza Baja + impacto Alto → requiere validación
2. **Step 9:** Red flag crítico identificado → requiere decisión humana
3. **Step 11:** Nivel de confianza = "Bajo" → no puede proceder a Plan

Si todos los checks pasan → continúa automáticamente a Plan.

### Cómo analysis.md Alimenta al Plan

| Output del Análisis | Cómo lo usa Plan |
|--------------------|-----------------|
| Enfoque recomendado (Step 11) | Selecciona patrón de arquitectura |
| Mitigaciones de fallos (Step 5) | Agrega tasks de error handling |
| Invariantes (Step 6) | Se convierte en reglas de validación |
| Matriz de delegación IA (Step 10) | Decide scope de automatización |
| Requisitos de observabilidad (Step 7) | Agrega tasks de monitoreo |

### 📄 Documentos actualizados
- `analysis.md` → Resultado del análisis
- `context/decisions.md` → Decisiones clave
- `status.md` → Phase: Critical Analysis ✅

---

## Fase 3: PLAN (Diseño Técnico)

### Propósito
Diseñar la implementación ANTES de escribir código. Ahora informado por el análisis crítico.

### Cómo Iniciar
```
/plan implement FEAT-XXX
```

### Proceso

1. Claude entra en **modo plan** (solo lectura, NO edita código)
2. Lee **spec.md + analysis.md** (AMBOS son input obligatorio)
3. Exploración del codebase existente
4. Genera plan con archivos, orden, snippets
5. Usuario revisa y aprueba

### 📄 Documentos actualizados
- `design.md` → Arquitectura técnica (informada por analysis.md)
- `tasks.md` → Checklist ordenado con todas las tasks
- `status.md` → Phase: Plan ✅

---

## Fase 4: BRANCH (Preparación)

### ⚠️ REGLA CRÍTICA
```
╔═══════════════════════════════════════════════════════════════════════════╗
║  NUNCA EMPEZAR A CODEAR SIN CREAR LA RAMA PRIMERO                        ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

### Proceso
```bash
git checkout main
git pull
git checkout -b feature/XXX-nombre-descriptivo
```

### Convención de Nombres
```
feature/001-auth           ✅ (número + descripción)
feature/002-db-connection  ✅
feat-001                   ❌ (muy corto)
nueva-feature              ❌ (no descriptivo)
```

### 📄 Documentos actualizados
- `status.md` → Phase: Branch ✅, Branch: feature/XXX-nombre

---

## Fase 5: IMPLEMENT (Desarrollo)

### Propósito
Implementar siguiendo el plan, con documentación viva.

### ⚠️ FLUJO OBLIGATORIO POR CADA TASK

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         POR CADA TASK                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   1. ANTES DE EMPEZAR                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ □ Actualizar tasks.md:  - [ ] Task N  →  - [🟡] Task N             │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│   2. IMPLEMENTAR                                                            │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ □ Escribir código                                                   │   │
│   │ □ Escribir tests (si aplica)                                        │   │
│   │ □ Verificar que funciona                                            │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│   3. DESPUÉS DE COMPLETAR                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ □ Actualizar tasks.md:  - [🟡] Task N  →  - [x] Task N             │   │
│   │ □ git add [archivos de esta task]                                   │   │
│   │ □ git commit -m "FEAT-XXX: Complete Task N - descripción"          │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│                              ▼                                              │
│   4. CHECKPOINT (cada 30 min o 3 tasks)                                     │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ □ Actualizar status.md: Progress: X/Y tasks                         │   │
│   │ □ git push (backup remoto)                                          │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Orden de Implementación Típico
1. Utilidades/helpers primero
2. Modelos de datos
3. Lógica de negocio / servicios
4. API endpoints / UI
5. Integración con sistema existente
6. Tests

### 📄 Documentos actualizados (CONTINUAMENTE)
- `tasks.md` → Marcadores actualizados por cada task
- `status.md` → Progress actualizado cada 3 tasks

---

## Fase 5.5: VERIFY (Browser Automation Tests) ← NUEVO

### Propósito
Validar automáticamente cambios frontend mediante browser automation antes de crear PR. Usa agent-browser (Anthropic CLI) para E2E testing.

### ¿Cuándo se ejecuta?
**Automático** cuando Ralph Loop detecta:
1. ✅ Cambios en archivos frontend (tsx/jsx/css/scss)
2. ✅ Scripts de test existen en `docs/features/FEAT-XXX/tests/`

Si NO hay cambios frontend o NO hay scripts → **SKIP** (no bloquea)

### Cómo Configurar Tests (Una vez por feature)

**1. Copiar templates:**
```bash
cp -r docs/features/_template/tests docs/features/FEAT-XXX/tests
```

**2. Configurar test-config.json:**
```json
{
  "feature_id": "FEAT-XXX",
  "base_url": "http://localhost:3000",
  "test_user": {
    "email": "feat-xxx-test@example.com",
    "password": "test-feat-xxx-password"
  }
}
```

**3. Personalizar e2e-flow.sh:**
```bash
# Cambiar URLs, selectores, assertions para tu feature
vim docs/features/FEAT-XXX/tests/e2e-flow.sh
```

### Ejecución Automática (Ralph Loop)

```bash
./ralph-feature.sh FEAT-XXX  # o .ps1 en PowerShell
```

Cuando llega a Phase 5.5:
```
[FEAT-XXX] 12:34:56 [INFO] Executing Verify phase (Phase 5.5)
[FEAT-XXX] 12:34:56 [INFO] Frontend changes detected
[FEAT-XXX] 12:34:57 [INFO] Running E2E flow tests...
[FEAT-XXX] 12:35:10 [SUCCESS] E2E tests passed
[FEAT-XXX] 12:35:11 [INFO] Running security filters...
[FEAT-XXX] 12:35:12 [SUCCESS] No secrets detected
[FEAT-XXX] 12:35:12 [SUCCESS] VERIFY phase complete
```

### Qué hace Phase 5.5

1. **Detecta cambios frontend** (git diff últimos 5 commits)
2. **Crea test results directory**
3. **Ejecuta e2e-flow.sh** (test principal)
4. **Ejecuta e2e-smoke.sh** (opcional, no bloquea)
5. **Captura screenshots** en cada paso + failures
6. **Ejecuta security filters** (redacta secrets antes de commit)
7. **Genera test-report.md**
8. **Bloquea PR si tests fallan** ❌

### Test Results Structure

```
docs/features/FEAT-XXX/test-results/
├── screenshots/
│   ├── step-01-login-page.png
│   ├── step-02-feature-page.png
│   └── step-03-item-created.png
├── videos/                              (opcional)
├── console-logs.txt                     (filtrado)
├── network-logs.json                    (filtrado)
└── test-report.md
```

### Security Filters (Automático)

Antes de commit, todos los test results pasan por security filters:
- **Detecta:** API keys, tokens, passwords, AWS credentials, private keys, DB URLs
- **Redacta:** Reemplaza con `[REDACTED-API-KEY]`, `[REDACTED-TOKEN]`, etc.
- **Pre-commit hook:** Bloquea commit si secrets detectados después de filtrado

```bash
# Instalado automáticamente en setup
bash .memory-system/scripts/install-git-hooks.sh
```

### Manual Testing (Sin Ralph Loop)

```bash
# Ejecutar tests manualmente
cd docs/features/FEAT-XXX/tests
bash e2e-flow.sh

# Filtrar secrets
bash ../../../.memory-system/scripts/security-filters.sh filter-all \
  ../test-results/

# Commit (con pre-commit hook activo)
git add test-results/
git commit -m "FEAT-XXX: Add test results"
```

### Troubleshooting

**Tests fallan pero UI funciona manualmente:**
- Verificar que localhost:3000 esté corriendo
- Revisar selectores en e2e-flow.sh (pueden haber cambiado)
- Checkear console-logs.txt para errores JS

**Pre-commit hook bloquea commit:**
```bash
# Ver qué secrets detectó
bash .memory-system/scripts/security-filters.sh scan \
  docs/features/FEAT-XXX/test-results/console-logs.txt

# Filtrar y reintentar
bash .memory-system/scripts/security-filters.sh filter-all \
  docs/features/FEAT-XXX/test-results/
git add docs/features/FEAT-XXX/test-results/
git commit -m "FEAT-XXX: Add filtered test results"
```

**Quiero skip Phase 5.5:**
- No crear `docs/features/FEAT-XXX/tests/` directory
- Ralph Loop detectará y saltará automáticamente

### 📄 Documentos actualizados
- `test-results/test-report.md` → Test results
- `test-results/screenshots/` → Visual evidence
- `status.md` → Phase: Verify ✅

---

## Fase 6: PR (Pull Request)

### Proceso

```bash
# 1. Verificar estado
git status
git diff --stat --no-pager

# 2. Asegurar todo commiteado (incluyendo test results si Phase 5.5 corrió)
git add .
git commit -m "FEAT-XXX: Final adjustments"

# 3. Push
git push -u origin feature/XXX-nombre

# 4. Crear PR (Ralph Loop incluye test results automáticamente)
gh pr create --title "FEAT-XXX: Nombre Descriptivo" --body "..." --base main
```

### PR Body Incluye Test Results (Automático)

Si Phase 5.5 (VERIFY) corrió, el PR automáticamente incluye:

```markdown
## Test Results

# Test Report: FEAT-XXX
**Status:** ✅ PASSED
**Date:** 2025-02-03

## Screenshots
- step-01-login-page.png
- step-02-feature-page.png
- step-03-item-created.png

## Console Logs (filtered)
[Secrets redacted]
```

### 📄 Documentos actualizados
- `status.md` → Phase: PR ✅, PR: #123 [url]
- `_index.md` → Status: 🔵 In Review

---

## Fase 7: MERGE (Cierre)

### Proceso

1. **Review** del PR
2. **Aprobar y Merge** en GitHub
3. **Actualizar documentación final**
4. **Limpiar**:
   ```bash
   git checkout main
   git pull
   git branch -d feature/XXX-nombre
   ```

### 📄 Documentos actualizados
- `status.md` → Status: 🟢 Complete, Merged: [date]
- `_index.md` → Status: 🟢 Complete

---

## Fase 8: WRAP-UP (Cierre de Contexto) ← NUEVA

### Propósito
Capturar aprendizajes, cerrar contexto, y documentar decisiones para futuras sesiones.

### Proceso

1. Revisar todas las decisiones tomadas durante implementación
2. Documentar lo que funcionó y lo que no
3. Registrar deuda técnica creada
4. Actualizar context files para futuras features

### 📄 Documentos actualizados
- `context/wrap_up.md` → Aprendizajes capturados
- `context/decisions.md` → Decisiones finales consolidadas
- `status.md` → Phase: Wrap-Up ✅
- `_index.md` → 🟢 Complete

---

## Ralph Loop (Ejecución Autónoma)

### Flujo Completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  RALPH LOOP - 9 FASES AUTÓNOMAS                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Iter 1: INTERVIEW          → spec.md            → INTERVIEW_COMPLETE       │
│  Iter 2: THINK CRITICALLY   → analysis.md        → ANALYSIS_COMPLETE        │
│           ⚠️ Pausa si: Low conf + High impact / Red flag / Low confidence    │
│  Iter 3: PLAN               → design.md + tasks  → PLAN_COMPLETE            │
│  Iter 4: BRANCH             → feature/XXX-name   → BRANCH_COMPLETE          │
│  Iter 5-N: IMPLEMENT        → código + tests     → IMPLEMENT_PROGRESS       │
│           ...hasta que todas las tasks estén ✅   → IMPLEMENT_COMPLETE       │
│  Iter N+1: VERIFY           → browser E2E tests  → VERIFY_COMPLETE          │
│           ⚠️ Auto-skip si: No frontend changes o no test scripts            │
│           ⚠️ Bloquea si: Tests fallan                                        │
│  Iter N+2: PR               → push + gh pr       → PR_COMPLETE              │
│  Iter N+3: MERGE            → espera aprobación  → MERGE_COMPLETE           │
│  Iter N+4: WRAP-UP          → wrap_up.md         → FEATURE_COMPLETE         │
│                                                                              │
│  ✅ LOOP TERMINADO                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Estructura de Archivos por Feature

```
docs/features/FEAT-XXX/
├── spec.md                ← Phase 1: Interview
├── analysis.md            ← Phase 2: Think Critically
├── design.md              ← Phase 3: Plan
├── tasks.md               ← Phase 3: Plan
├── tests.md               ← Phase 5: Implement
├── status.md              ← Updated each phase
├── tests/                 ← Phase 5.5: VERIFY (NEW!)
│   ├── helpers.sh         │   Reusable test functions
│   ├── e2e-flow.sh        │   Main E2E test
│   ├── e2e-smoke.sh       │   Quick smoke tests
│   └── test-config.json   │   Test configuration
├── test-results/          ← Generated by Phase 5.5 (NEW!)
│   ├── screenshots/       │   Visual evidence
│   ├── videos/            │   (optional)
│   ├── console-logs.txt   │   Filtered
│   ├── network-logs.json  │   Filtered
│   └── test-report.md     │   Test summary
└── context/
    ├── session_log.md
    ├── decisions.md       ← Enriched by Think Critically
    ├── blockers.md
    └── wrap_up.md         ← Phase 8: Wrap-Up
```

---

## Checklist Rápido

```
□ INTERVIEW
  □ Preguntas hechas
  □ Decisiones en spec.md
  □ Market Validation (Pain Level 7+)
  □ status.md → Phase: Interview ✅

□ THINK CRITICALLY                    ← NUEVO
  □ Profundidad determinada
  □ Protocolo ejecutado
  □ analysis.md generado
  □ Sin red flags críticos
  □ Confidence level ≥ Medium
  □ status.md → Phase: Critical Analysis ✅

□ PLAN
  □ spec.md + analysis.md leídos (AMBOS)
  □ Codebase explorado
  □ design.md creado
  □ tasks.md con checklist
  □ status.md → Phase: Plan ✅

□ BRANCH
  □ git checkout -b feature/XXX
  □ status.md → Branch creado

□ IMPLEMENT
  □ Por cada task:
    □ Marcar 🟡 antes
    □ Implementar
    □ Marcar ✅ después
    □ Commit
  □ Push cada 30 min
  □ status.md actualizado

□ VERIFY                              ← NUEVO
  □ Tests configurados (si frontend feature)
  □ e2e-flow.sh personalizado
  □ test-config.json completado
  □ Browser tests ejecutados
  □ Security filters aplicados
  □ test-report.md generado
  □ status.md → Verify ✅

□ PR
  □ Todo commiteado (+ test results)
  □ gh pr create (incluye test report)
  □ status.md → PR link

□ MERGE
  □ Review aprobado
  □ Merged
  □ status.md → 🟢 Complete
  □ _index.md actualizado
  □ Rama local borrada

□ WRAP-UP                             ← NUEVO
  □ Learnings capturados
  □ Deuda técnica documentada
  □ context/wrap_up.md completado
  □ status.md → Wrap-Up ✅
```

---

## Anti-Patterns

| ❌ Anti-Pattern | ✅ Correcto |
|----------------|-------------|
| Codear sin interview | Interview primero |
| Planear sin análisis crítico | Think Critically antes de Plan |
| Codear sin rama | Rama antes de código |
| Codear sin plan | Plan primero |
| Actualizar docs al final | Docs en tiempo real |
| Commits gigantes | Commit por task |
| Ignorar tests | Tests obligatorios |
| No capturar learnings | Wrap-Up al final |
| Ignorar red flags del análisis | Resolver antes de implementar |
| Proceder con confianza baja | Validar asunciones primero |

---

## Flujo Completo End-to-End

```bash
# Phase 0: Setup (una vez por proyecto)
/project-interview
/saas-validate project      # Gate: Pain Level 7+?
/architecture
/mvp

# Per-Feature Cycle (manual o via Ralph)
/interview FEAT-001-auth
/think-critically FEAT-001-auth    # 11-step protocol → analysis.md
/plan implement FEAT-001-auth      # Lee spec.md + analysis.md
git checkout -b feature/001-auth
# Implement (via Ralph o manual)
# VERIFY (automático si frontend changes)  ← NUEVO
/git pr
# Review + merge
/wrap-up FEAT-001-auth

# O completamente autónomo (9 fases):
./ralph-feature.sh FEAT-001-auth  # Ejecuta las 9 fases autónomamente
# o PowerShell:
.\ralph-feature.ps1 FEAT-001-auth
```

---

*Última actualización: {date}*
