# Plan de Implementacion MVP - Gestion de Citas

## 1. Resumen ejecutivo

Estrategia recomendada: construir el MVP por vertical slices sobre una base tecnica minima estable. El objetivo es entregar valor usable en cada fase, reducir riesgo de integracion y evitar sobreingenieria.

Flujos que se deben cerrar de punta a punta:

- login OTP completo
- gestion de servicios por admin
- reserva de cita por cliente
- operacion de citas por admin

## 2. Enfoque de implementacion

Se utiliza un enfoque mixto:

- base corta por capas para habilitar estandares comunes
- ejecucion por vertical slices para entregar valor temprano

Por que este enfoque:

- minimiza bloqueos frontend/backend
- integra contratos y reglas reales desde temprano
- permite demos funcionales por fase

## 3. Fuentes de verdad transversales

Valores operativos que deben permanecer consistentes en todos los docs:

- OTP TTL: 5 minutos
- OTP max intentos por challenge: 5
- OTP cooldown por email: 60 segundos
- OTP rate limit por IP: 10 requests por 15 minutos
- OTP rate limit por email: 5 requests por hora
- JWT access token: 30 minutos
- auth frontend: cookie HttpOnly + Secure + SameSite=Lax

## 4. Roadmap por fases (0-6)

1. Fase 0: setup base
2. Fase 1: autenticacion OTP
3. Fase 2: servicios
4. Fase 3: disponibilidad
5. Fase 4: reservas
6. Fase 5: panel admin de citas
7. Fase 6: endurecimiento

## 5. Entregables por fase

### Fase 0 - Setup base

Objetivo:

- tener entorno reproducible y arquitectura inicial lista para iterar

Se implementa:

- Docker Compose para frontend, backend y PostgreSQL
- FastAPI modular: auth, services, availability, appointments
- SQLAlchemy async + Alembic
- Next.js App Router + Tailwind + cliente API
- healthchecks base y pipeline local minima

Dependencias:

- ninguna

Resultado visible:

- proyecto levanta con un comando
- endpoints de health responden

Riesgos y mitigacion:

- riesgo: entorno no reproducible
- mitigacion: .env.example, script de arranque y checklist de bootstrap

Pruebas minimas:

- smoke test de frontend/backend/db
- migracion inicial aplicada en limpio

Criterio de terminado:

- stack local estable sin pasos ambiguos
- readme de arranque validado

Evidencia de cierre:

- comando unico de levantamiento documentado
- captura de healthchecks exitosos

### Fase 1 - Autenticacion OTP

Objetivo:

- permitir login por OTP y emision de JWT para admin y cliente

Se implementa:

- POST auth/otp/request con respuesta generica
- POST auth/otp/verify con emision de JWT
- persistencia otp_challenges con hash, expiracion, intentos y single-use
- proteccion inicial de rutas por rol
- frontend: solicitar codigo, verificar codigo, inicio/cierre de sesion

Dependencias:

- fase 0

Resultado visible:

- admin y cliente pueden autenticarse sin password

Riesgos y mitigacion:

- riesgo: abuso de OTP
- mitigacion: cooldown, rate limit por email/ip, intentos maximos

Pruebas minimas:

- OTP expira a 5 minutos
- OTP no se reutiliza tras uso exitoso
- token invalido no accede a rutas privadas

Criterio de terminado:

- auth OTP funcional end-to-end
- JWT operativo en rutas protegidas

Evidencia de cierre:

- flujo manual completo request OTP -> verify OTP -> acceso protegido
- pruebas automatizadas de contrato auth

### Fase 2 - Servicios

Objetivo:

- permitir que admin publique y mantenga servicios con duracion

Se implementa:

- CRUD admin de servicios
- listado de servicios activos para cliente autenticado
- validaciones de campos: nombre, descripcion, duration_minutes, is_active
- frontend admin para alta/edicion/activacion
- frontend cliente para listado de servicios

Dependencias:

- fase 1

Resultado visible:

- catalogo de servicios usable en cliente y admin

Riesgos y mitigacion:

- riesgo: reglas de negocio difusas en duracion
- mitigacion: validaciones explicitas en API y UI

Pruebas minimas:

- solo admin modifica servicios
- cliente solo consulta activos

Criterio de terminado:

- CRUD estable y validado
- contrato API de servicios congelado

Evidencia de cierre:

- demo funcional crear/editar/desactivar servicio

### Fase 3 - Disponibilidad

Objetivo:

- generar y consultar bloques disponibles por servicio

Se implementa:

- reglas de disponibilidad por servicio (dia y rango horario)
- generador determinista de bloques futuros
- estados de bloque: available, blocked, cancelled
- endpoint de consulta de bloques por rango
- frontend cliente para visualizar agenda disponible

Dependencias:

- fase 2

Resultado visible:

- cliente ve horarios reales por servicio

Riesgos y mitigacion:

- riesgo: inconsistencias por timezone
- mitigacion: timezone de negocio unica y UTC en persistencia

Pruebas minimas:

- no superposicion de bloques
- respeto estricto de duration_minutes

Criterio de terminado:

- bloques consistentes y consultables por rango

Evidencia de cierre:

- caso de prueba semanal con bloques esperados

### Fase 4 - Reservas

Objetivo:

- permitir reservar una cita sobre un bloque available sin doble reserva

Se implementa:

- endpoint atomico de reserva con transaccion y lock
- creacion de appointment con snapshots de cliente:
  - client_name_snapshot
  - client_email_snapshot
  - client_phone_snapshot
- estado inicial: pending_review
- actualizacion del bloque reservado a estado no disponible
- frontend cliente de confirmacion de reserva

Dependencias:

- fase 3

Resultado visible:

- reserva persistida y bloque ocupado

Riesgos y mitigacion:

- riesgo: doble reserva en concurrencia
- mitigacion: lock pesimista o constraint unico transaccional

Pruebas minimas:

- prueba concurrente de doble intento sobre mismo bloque
- persistencia correcta de snapshots

Criterio de terminado:

- no hay doble reserva bajo concurrencia basica
- flujo E2E de reserva completo

Evidencia de cierre:

- test concurrente exitoso + demo funcional de reserva

### Fase 5 - Panel admin de citas

Objetivo:

- dar control operativo al admin para confirmar o cancelar citas

Se implementa:

- listado admin de citas por fecha y estado
- acciones: confirmar y cancelar
- regla consistente de impacto en bloque al cancelar
- historial minimo de cambios de estado
- frontend admin con bandeja de pendientes

Dependencias:

- fase 4

Resultado visible:

- admin opera ciclo minimo de citas

Riesgos y mitigacion:

- riesgo: transiciones de estado inconsistentes
- mitigacion: maquina de estados explicita y validada en backend

Pruebas minimas:

- solo pending_review pasa a confirmed o cancelled
- usuario sin rol admin recibe 403

Criterio de terminado:

- transiciones validas y auditables

Evidencia de cierre:

- prueba E2E admin revisar -> confirmar/cancelar

### Fase 6 - Endurecimiento

Objetivo:

- reducir riesgo operativo de produccion sin ampliar alcance funcional

Se implementa:

- formato de error API uniforme
- logs estructurados con request_id
- pruebas criticas: auth OTP, disponibilidad, reserva atomica, transiciones admin
- hardening basico: CORS restringido, headers de seguridad, limites OTP
- dockerfile de produccion y checklist de despliegue

Dependencias:

- fases 0-5

Resultado visible:

- MVP desplegable con riesgo tecnico controlado

Riesgos y mitigacion:

- riesgo: incidentes por configuracion insegura
- mitigacion: checklist de release y validaciones previas a deploy

Pruebas minimas:

- smoke deploy + health ready
- suite minima de regresion de flujos criticos

Criterio de terminado:

- checklist de release aprobado
- pruebas criticas en verde

Evidencia de cierre:

- acta de release con resultados de smoke y regresion

## 6. Vertical slices recomendados

1. Slice A - Login OTP completo
2. Slice B - Crear servicio completo
3. Slice C - Reservar cita completa
4. Slice D - Operacion admin de citas

## 7. Coordinacion backend y frontend

Regla operativa por slice:

1. backend define contrato minimo y ejemplos
2. frontend arranca con mock corto y migra rapido a API real
3. cierre conjunto con prueba E2E del slice en Docker

Controles para evitar bloqueo:

- congelar contrato por slice
- no abrir mas de un slice critico en paralelo
- definition of done compartida entre frontend/backend

## 8. Backlog inicial priorizado

1. Epica 1: fundaciones tecnicas
2. Epica 2: autenticacion OTP/JWT
3. Epica 3: gestion de servicios
4. Epica 4: disponibilidad y bloques
5. Epica 5: reserva de citas
6. Epica 6: operacion admin y hardening

## 9. Riesgos principales y mitigacion

1. complejidad de disponibilidad y timezone
2. doble reserva por concurrencia
3. abuso de OTP
4. desalineacion frontend/backend
5. crecimiento de alcance en panel admin

Mitigacion transversal:

- contratos congelados por slice
- pruebas de concurrencia tempranas
- limites de OTP desde fase 1
- demo y cierre formal por fase

## 10. Fuera del MVP

- multi-negocio o multi-sucursal
- RBAC avanzado
- pagos online y facturacion
- notificaciones multicanal complejas
- integraciones externas avanzadas
- reporteria avanzada
- app movil nativa

## 11. Cierre ejecutivo

Plan de ejecucion recomendado:

1. roadmap por fases 0-6
2. backlog inicial priorizado por epicas
3. primeros 3 slices: login OTP, crear servicio, reservar cita
4. exclusion explicita de alcance no MVP