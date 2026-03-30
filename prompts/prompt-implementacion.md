# Implementation Plan Prompt

Actúa como technical lead senior y ayúdame a definir un plan de implementación realista para un MVP de gestión de citas.

Quiero un plan enfocado en:
- construir algo funcional en corto plazo
- mantener buenas prácticas
- evitar sobreingeniería
- priorizar entregables reales
- reducir riesgo técnico
- permitir aprendizaje progresivo mientras construyo

No quiero un roadmap abstracto. Quiero una propuesta concreta y ejecutable.

---

## Contexto del proyecto

Estoy construyendo un MVP pequeño de gestión de citas para un solo negocio.

### Funcionalidades del MVP

#### Administrador
- iniciar sesión por OTP email
- crear servicios
- configurar duración del servicio
- definir horarios base del servicio
- visualizar citas
- confirmar o cancelar citas

#### Cliente
- iniciar sesión por OTP email
- consultar servicios disponibles
- consultar horarios disponibles de un servicio
- reservar una cita

---

## Reglas de negocio

- un solo negocio
- un solo admin interno
- clientes autenticados
- autenticación OTP por email, sin contraseña
- después del OTP se emiten JWT
- cada servicio tiene duración definida
- la disponibilidad depende del servicio
- los bloques se generan a partir de reglas de disponibilidad
- un bloque puede estar available, blocked o cancelled
- una cita ocupa un bloque
- una cita puede estar pending_review, confirmed o cancelled
- Appointment guarda snapshot histórico básico del cliente:
  - client_name_snapshot
  - client_email_snapshot
  - client_phone_snapshot

---

## Stack principal

### Frontend
- Next.js App Router
- Tailwind CSS
- TypeScript

### Backend
- FastAPI
- SQLAlchemy async
- Alembic
- PostgreSQL
- OTP por correo
- JWT

### Infraestructura
- Docker para desarrollo y producción

---

## Arquitectura ya decidida

- monolito modular
- backend y frontend separados por responsabilidades
- dominio ya definido
- se busca aplicar SOLID de forma práctica
- se busca modularidad y claridad
- no se busca microservicios ni complejidad excesiva

---

## Lo que quiero que produzcas

### 1. Resumen ejecutivo
Dame una propuesta breve de estrategia de implementación para este MVP.

### 2. Estrategia general de construcción
Explica cómo conviene implementar este sistema:
- por capas
- por features
- por vertical slices
- por entregables funcionales
- qué enfoque recomiendas y por qué

### 3. Orden recomendado de implementación
Dame el orden ideal para construir el MVP.
Quiero saber qué se debería implementar primero, segundo, tercero, etc.

### 4. Fases del proyecto
Divide el proyecto en fases pequeñas y realistas.
Por ejemplo:
- setup base
- auth
- servicios
- disponibilidad
- reservas
- panel admin
- endurecimiento

### 5. Entregables por fase
Para cada fase quiero:
- objetivo
- qué se implementa
- dependencias
- resultado visible
- criterio de terminado

### 6. Vertical slices recomendados
Quiero que me propongas slices funcionales reales.
Por ejemplo:
- login OTP completo
- crear servicio completo
- reservar cita completa

### 7. Qué construir primero en backend y frontend
Explícame cómo coordinar backend y frontend para avanzar sin bloqueo.

### 8. Backlog técnico inicial
Dame un backlog inicial bien estructurado:
- épicas
- historias técnicas
- tareas
- orden sugerido

### 9. Riesgos de implementación
Dime qué puede retrasar o complicar este MVP y cómo reducir esos riesgos.

### 10. Qué dejar fuera del MVP
Quiero una lista clara de cosas que no deberían entrar todavía.

### 11. Propuesta final de plan
Cierra con un plan final resumido y ejecutable.

### 12. Formato obligatorio por fase
Cada fase debe usar exactamente esta estructura:
- objetivo
- se implementa
- dependencias
- resultado visible
- riesgos y mitigacion
- pruebas minimas
- criterio de terminado
- evidencia de cierre

La fase 0 a 6 es obligatoria. No omitir ninguna.

### 13. Coherencia tecnica obligatoria
Usa estos valores en toda la respuesta sin contradicciones:
- OTP TTL: 5 minutos
- OTP max intentos por challenge: 5
- OTP cooldown por email: 60 segundos
- OTP rate limit por IP: 10 requests por 15 minutos
- OTP rate limit por email: 5 requests por hora
- JWT access token: 30 minutos
- frontend auth: cookie HttpOnly + Secure + SameSite=Lax

---

## Restricciones importantes

- no microservicios
- no roadmap inflado
- no tareas demasiado abstractas
- no sobreingeniería
- no intentar construir todo al mismo tiempo
- no omitir pruebas minimas por fase
- no omitir riesgos por fase
- no proponer dependencias circulares entre fases

---

## Resultado esperado

La respuesta debe terminar con:
1. roadmap por fases
2. backlog inicial priorizado
3. primeros 3 slices funcionales recomendados
4. lista de cosas fuera del MVP

Adicionalmente:
5. una tabla de control que muestre fase, dependencia y estado de validacion de coherencia