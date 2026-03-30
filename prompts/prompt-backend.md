# Backend Architecture Prompt

Actúa como arquitecto backend senior especializado en Python, FastAPI y monolitos modulares.

Quiero que me ayudes a definir la arquitectura backend de un MVP de gestión de citas, priorizando:

- simplicidad
- buenas prácticas
- modularidad
- mantenibilidad
- plazo corto de desarrollo
- código entendible
- base sólida para crecer después

No quiero sobreingeniería ni arquitectura enterprise innecesaria.

---

## 1. Contexto del proyecto

Estoy construyendo un MVP pequeño pero real de gestión de citas para un solo negocio.

### Objetivo del sistema
Permitir que un negocio publique servicios y que clientes autenticados puedan ver horarios disponibles y reservar citas.

### Funcionalidades del MVP

#### Administrador
- iniciar sesión
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

## 2. Reglas de negocio

- El MVP es para un solo negocio
- Existe un solo usuario administrador interno
- Los clientes deben autenticarse
- La autenticación será por OTP enviado por correo, sin contraseña
- Después de validar el OTP, el sistema emitirá JWT para autenticación
- Cada servicio tiene una duración definida
- La disponibilidad se define por servicio
- Los bloques de tiempo se generan a partir de reglas de disponibilidad
- Un bloque puede estar en estado:
  - available
  - blocked
  - cancelled
- Una cita ocupa un bloque de tiempo
- La ocupación real del bloque se expresa por la existencia de una cita activa
- Una cita puede estar en estado:
  - pending_review
  - confirmed
  - cancelled
- Appointment guarda snapshot histórico básico del cliente:
  - client_name_snapshot
  - client_email_snapshot
  - client_phone_snapshot

---

## 3. Modelo de dominio ya definido

Las entidades principales del dominio son:

- AdminUser
- Client
- Service
- ServiceAvailabilityRule
- ServiceTimeBlock
- Appointment

Relaciones principales:
- Service define reglas de disponibilidad
- Service genera bloques de tiempo reservables
- Client reserva citas
- Appointment pertenece a un Service
- Appointment ocupa un ServiceTimeBlock
- ServiceTimeBlock puede originarse desde una ServiceAvailabilityRule

Usa este dominio como base. No quiero que rediseñes el modelo desde cero.

---

## 4. Stack técnico propuesto a revisar

Evalúa este stack y clasifícalo en:
- recomendado para el MVP
- opcional / depende del alcance
- innecesario por ahora
- reemplazo sugerido si aplica

### Posible stack técnico

| Componente         | Tecnología                              | Versión   |
|--------------------|-----------------------------------------|-----------|
| Framework          | FastAPI                                 | 0.115+    |
| Servidor ASGI      | Uvicorn + Gunicorn (producción)         | latest    |
| ORM async          | SQLAlchemy 2.x (async mode)             | 2.0+      |
| Migraciones        | Alembic                                 | 1.14+     |
| Driver PostgreSQL  | asyncpg (runtime async) + psycopg v3    | latest    |
| Validación         | Pydantic v2                             | 2.x       |
| Settings           | pydantic-settings                       | 2.x       |
| JWT                | python-jose[cryptography]               | 3.3+      |
| Email async        | aiosmtplib                              | 3.x       |
| Rate limiting      | slowapi                                 | 0.1.9     |
| Tests              | pytest + pytest-asyncio + httpx         | latest    |

### Importante
Revisa críticamente este stack.
No asumas que todo debe entrar.
Quiero que me digas qué sí tiene sentido para este MVP backend y qué no.

### Aclaraciones ya definidas
- No se usarán contraseñas
- La autenticación será OTP por correo
- Después de validar OTP se emitirán JWT
- El sistema sí enviará correos reales para OTP
- Se usará psycopg v3 como parte del stack técnico

---

## 5. Lo que quiero que produzcas

Quiero que me propongas una arquitectura backend clara y concreta, estructurando la respuesta así:

### 1. Resumen ejecutivo
Dame una propuesta breve de arquitectura backend recomendada para este MVP.

### 2. Evaluación del stack técnico
Analiza cada herramienta del stack propuesto y clasifícala como:
- recomendada
- opcional
- no necesaria por ahora
- alternativa mejor si aplica

Justifica cada decisión brevemente.

### 3. Principios de diseño backend
Explica qué principios aplicarías:
- modularidad
- separación de capas
- SOLID práctico
- bajo acoplamiento
- alta cohesión
- simplicidad del MVP

### 4. Arquitectura del backend
Propón una arquitectura de monolito modular en FastAPI.
Quiero que expliques:
- capas
- módulos
- dependencias entre capas
- qué responsabilidades vive en cada capa

### 5. Estructura de carpetas del backend
Dame una estructura de carpetas concreta y realista para el backend.
Debe incluir, si aplica:
- api
- application
- domain
- infrastructure
- db
- config
- tests

No la dejes genérica. Quiero una propuesta aterrizada.

### 6. Módulos del dominio/backend
Quiero que propongas módulos claros como:
- auth
- clients
- services
- appointments

Y expliques qué vive dentro de cada uno.

### 7. Diseño de capas dentro de cada módulo
Explícame cómo organizar dentro de cada módulo:
- entidades
- casos de uso
- repositorios
- esquemas
- endpoints
- persistencia

### 8. Flujo de una operación clave
Explica paso a paso cómo debería fluir:
- request de OTP por email
- validación de OTP
- emisión de JWT
- consulta de disponibilidad
- creación de cita
- confirmación de cita

Quiero ver el flujo entre:
- endpoint
- schema/request
- use case
- dominio
- repositorio
- base de datos
- servicio de email

### 9. Persistencia y base de datos
Dime cómo manejarías:
- SQLAlchemy async
- Alembic
- sessions
- transacciones
- concurrencia básica al reservar un bloque
- snapshots históricos en Appointment

### 10. Autenticación OTP + JWT
Propón una forma limpia de implementar autenticación por OTP email con JWT.
Quiero que expliques:
- flujo recomendado
- tablas o entidades necesarias
- vencimiento del OTP
- invalidación o single-use del OTP
- rate limiting
- seguridad mínima razonable
- emisión y expiración de access token
- si recomiendas refresh token o no para este MVP

### 11. Qué abstraer y qué no
Quiero que me digas claramente:
- qué abstraerías desde el principio
- qué no abstraería todavía
- qué cosas sería mejor dejar simples en este MVP

### 12. Patrones recomendados
Indica qué patrones sí usarías y cuáles no.
Por ejemplo:
- repository
- use case / application service
- dependency injection
- domain service
- policy object
- unit of work
- event bus
- CQRS

Y explica por qué.

### 13. Testing strategy
Propón una estrategia de pruebas realista para el MVP:
- unit tests
- integration tests
- API tests
- qué probar primero
- qué no hace falta sobreprobar al inicio

### 14. Riesgos y errores comunes
Explica qué errores debo evitar en este backend, por ejemplo:
- poner toda la lógica en los routers
- abstraer demasiado pronto
- mezclar ORM y dominio sin criterio
- diseñar un sistema de auth más complejo de lo que el MVP necesita
- usar demasiadas capas vacías
- complicar innecesariamente el envío y validación de OTP

### 15. Propuesta final recomendada
Cierra con una propuesta final concreta de backend para ejecutar este MVP, como si fuera la decisión técnica recomendada.

---

## 6. Restricciones importantes

- No microservicios
- No arquitectura enterprise exagerada
- No sobreingeniería
- No quiero patrones puestos por moda
- Todo debe ser entendible por una persona que quiere aprender buenas prácticas reales mientras construye
- El diseño debe ser implementable en corto plazo
- La autenticación debe ser OTP + JWT, sin contraseñas

---

## 7. Enfoque esperado

Quiero una respuesta:
- clara
- pedagógica
- práctica
- orientada a implementación real
- con criterio técnico
- honesta sobre qué sí vale la pena y qué no en este MVP

Si detectas elementos del stack que sobran o complican innecesariamente el proyecto, debes decirlo claramente.

---

## 8. Resultado esperado

La respuesta debe terminar con:

1. stack final recomendado
2. estructura de carpetas backend
3. decisiones arquitectónicas clave
4. lista de cosas que quedan fuera del MVP