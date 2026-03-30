# Quality Strategy Prompt

Actúa como engineer manager / staff engineer y ayúdame a definir una estrategia de calidad realista para un MVP de gestión de citas.

Quiero una propuesta:
- práctica
- liviana
- mantenible
- útil para un equipo pequeño
- enfocada en calidad real, no en burocracia

---

## Contexto del proyecto

MVP de gestión de citas con:
- frontend en Next.js
- backend en FastAPI
- PostgreSQL
- auth por OTP + JWT
- Docker

Objetivo: construir rápido, pero con buena base técnica.

---

## Lo que quiero que produzcas

### 1. Principios de calidad
Qué significa “calidad suficiente” para este MVP.

### 2. Estrategia de testing
Qué tipos de pruebas sí harías:
- unitarias
- integración
- API
- frontend
- smoke tests

### 3. Qué probar primero
Quiero prioridad de pruebas:
- auth OTP
- reserva de cita
- disponibilidad
- confirmación/cancelación
- etc.

### 4. Qué no sobreprobar
Dónde no vale la pena invertir demasiado al inicio.

### 5. Estándares de código
Convenciones mínimas para mantener calidad:
- nombres
- estructura
- manejo de errores
- logging
- validaciones

### 6. Tooling recomendado
Qué herramientas de calidad sí usarías:
- formatter
- linter
- type checking
- test runner
- CI mínima

### 7. Criterios de Done
Cómo definir cuándo una funcionalidad está realmente terminada.

### 8. Code review
Qué revisar en PRs y cómo evitar reviews inútiles.

### 9. Riesgos comunes
Errores típicos que degradan calidad en un MVP como este.

### 10. Propuesta final
Cierra con una estrategia de calidad concreta para este proyecto.

---

## Restricciones

- no procesos pesados
- no métricas vacías
- no coverage dogmático
- no QA burocrático
- sí enfoque pragmático

---

## Resultado esperado

La respuesta debe terminar con:
1. estrategia de pruebas recomendada
2. tooling mínimo recomendado
3. checklist de calidad por PR
4. qué dejar simple en el MVP