# Quality Strategy MVP - Gestion de Citas

Este documento define una estrategia de calidad pragmatica para el MVP.

Objetivo:
- calidad suficiente para operar con confianza
- velocidad de entrega sin burocracia
- base tecnica mantenible para equipo pequeno

## 1. Principios de calidad

Calidad suficiente para este MVP significa:
- funcionalidades core confiables (auth, reserva, estados)
- errores controlados y observables
- cambios pequenos con bajo riesgo de regresion
- codigo legible y consistente

Principios operativos:
- probar mas donde el riesgo de negocio es mayor
- automatizar lo repetitivo (lint, tests, checks)
- evitar procesos pesados sin impacto real
- priorizar feedback rapido en PR

## 2. Estrategia de testing

Distribucion recomendada:
- unitarias: reglas puras de dominio (rapidas)
- integracion backend: casos de uso con DB real de test
- API tests: contratos HTTP criticos
- frontend tests: logica de componentes y flujos minimos
- smoke tests: validacion rapida post-deploy

### Unitarias

Que cubrir:
- transiciones de estado de `appointment`
- validaciones de disponibilidad
- politicas de OTP (expiracion, intentos)

Meta:
- rapidas, aisladas, sin red ni DB cuando no haga falta

### Integracion

Que cubrir:
- reserva atomica con concurrencia basica
- persistencia de snapshots en `appointments`
- invalidacion OTP al uso

Meta:
- asegurar que reglas criticas sobreviven al stack real

### API tests

Que cubrir:
- `POST /auth/otp/request`
- `POST /auth/otp/verify`
- `GET /services`
- `GET /services/{id}/time-blocks`
- `POST /appointments`
- `PATCH /admin/appointments/{id}/confirm`
- `PATCH /admin/appointments/{id}/cancel`

Meta:
- contratos estables para frontend

### Frontend tests

Que cubrir:
- formularios OTP (validaciones y estados)
- seleccion de bloque y submit de reserva
- manejo de errores API en pantallas criticas

Meta:
- evitar roturas visibles al usuario

### Smoke tests

Que cubrir en cada deploy:
- healthchecks backend/frontend
- login OTP basico en entorno de staging
- flujo corto de reserva

Meta:
- detectar fallos graves de release en minutos

## 3. Que probar primero (prioridad)

Orden recomendado:
1. auth OTP + JWT
2. reserva de cita y anti doble reserva
3. disponibilidad de bloques
4. confirmacion/cancelacion admin
5. listados principales (servicios y citas)

Justificacion:
- si falla auth o reserva, el MVP no funciona
- listados son importantes, pero menos riesgosos que auth/concurrencia

## 4. Que no sobreprobar al inicio

No invertir demasiado en:
- tests de componentes puramente visuales sin logica
- mocks excesivos de ORM/framework
- pruebas de ramas triviales de DTOs
- objetivos de cobertura global altos por dogma

Regla:
- cobertura orientada a riesgo, no a porcentaje cosmetico

## 5. Estandares de codigo minimos

Nombres y estructura:
- nombres explicitos por dominio
- una responsabilidad clara por modulo/archivo
- routers finos, logica en use cases

Manejo de errores:
- errores de dominio mapeados a HTTP consistente
- formato de error unico en API
- sin trazas sensibles en respuestas

Logging:
- logs estructurados
- incluir `request_id`
- no loggear OTP ni tokens completos

Validaciones:
- input validado en bordes (API)
- reglas de negocio validadas en capa de aplicacion
- constraints de DB para invariantes criticas

## 6. Tooling recomendado

Backend:
- formatter: `black`
- linter: `ruff`
- type checking: `mypy` (modo gradual)
- tests: `pytest` + `pytest-asyncio` + `httpx`

Frontend:
- formatter/lint: `eslint` + `prettier`
- type checking: `tsc --noEmit`
- tests: `vitest` o `jest` + `testing-library`

CI minima:
- lint frontend/backend
- type check frontend/backend
- tests criticos backend
- build frontend/backend

## 7. Criterios de Done

Una funcionalidad esta Done cuando:
1. cumple criterio funcional acordado
2. incluye validaciones y manejo de errores
3. tiene pruebas de nivel adecuado segun riesgo
4. pasa lint/type/tests en CI
5. tiene logs utiles en rutas criticas
6. no rompe contratos API existentes

## 8. Code review

Que revisar en cada PR:
- correccion funcional y riesgo de regresion
- seguridad basica (auth, autorizacion, datos sensibles)
- claridad de codigo y complejidad innecesaria
- impacto en contratos API
- cobertura de pruebas proporcional al riesgo

Como evitar reviews inutiles:
- PRs pequenos y enfocados
- checklist de autor antes de pedir review
- comentarios concretos, accionables y con contexto
- evitar debates de estilo si formatter/linter ya lo resuelve

## 9. Riesgos comunes que degradan calidad

- meter logica de negocio en routers/componentes UI
- no testear concurrencia en reservas
- acoplar frontend a detalles internos de backend
- saltarse migraciones ordenadas
- ignorar errores intermitentes en OTP/correo
- crecer el scope sin endurecer lo ya entregado

Mitigacion:
- vertical slices cerrados
- prioridad a pruebas de flujo core
- definicion de Done estricta pero liviana

## 10. Propuesta final

Estrategia concreta para este proyecto:
- base automatizada minima (lint, type check, tests)
- pruebas enfocadas en auth, reservas y estados
- PRs pequenos con checklist claro
- smoke test post-deploy obligatorio
- evitar burocracia y medir calidad por confiabilidad real

## Cierre solicitado

1. Estrategia de pruebas recomendada

- Unitarias para reglas de dominio
- Integracion para casos de uso criticos con DB
- API tests para contratos esenciales
- Frontend tests en flujos clave
- Smoke tests en cada release

2. Tooling minimo recomendado

- Backend: `black`, `ruff`, `mypy`, `pytest`
- Frontend: `eslint`, `prettier`, `tsc`, `vitest/jest`
- CI: lint + type check + tests criticos + build

3. Checklist de calidad por PR

- criterio funcional claro
- errores y validaciones cubiertos
- pruebas agregadas/actualizadas segun riesgo
- logs y seguridad basica revisados
- CI en verde

4. Que dejar simple en el MVP

- cobertura global sin target dogmatico
- QA manual pesada
- matrices de testing complejas
- procesos de aprobacion largos
- tooling enterprise de baja relacion costo/valor
