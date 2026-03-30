# Backend Architecture MVP - Gestion de Citas

Este documento define la arquitectura backend y decisiones tecnicas de implementacion.

Los contratos HTTP (endpoints, request/response, errores y convenciones de API) viven en `api.md`.

## 1. Alcance de este documento

Incluye:
- arquitectura backend
- organizacion por modulos
- decisiones de persistencia y concurrencia
- autenticacion OTP/JWT a nivel tecnico
- estrategia de pruebas

No incluye:
- detalle de contratos REST
- payloads endpoint por endpoint

## 2. Stack tecnico recomendado

- FastAPI 0.115+
- SQLAlchemy 2 async
- PostgreSQL
- Alembic
- Pydantic v2 + pydantic-settings
- python-jose (o PyJWT)
- aiosmtplib
- pytest + pytest-asyncio + httpx

Decision de simplicidad MVP:
- runtime DB con SQLAlchemy async + asyncpg
- evitar complejidad de librerias duplicadas para la misma responsabilidad

## 3. Principios de arquitectura

- Monolito modular, no microservicios.
- Logica de negocio en casos de uso, no en routers.
- Dominio desacoplado de HTTP y ORM.
- Infraestructura intercambiable solo donde aporta valor (repositorios, email, JWT).
- Evitar sobre-ingenieria: sin CQRS, sin event bus, sin capas vacias.

## 4. Modulos de dominio

- `auth`
  - request OTP
  - verify OTP
  - emision JWT
- `clients`
  - perfil minimo del cliente autenticado
- `services`
  - CRUD de servicios (admin)
  - reglas base de disponibilidad
- `appointments`
  - reserva de cita
  - confirmacion/cancelacion admin

## 5. Capas por modulo

- `api`
  - routers y schemas HTTP
- `application`
  - casos de uso
  - puertos (interfaces)
- `domain`
  - entidades, enums y reglas
- `infrastructure`
  - repositorios SQLAlchemy
  - SMTP
  - JWT service

Reglas de separacion:
- router no contiene reglas de negocio
- caso de uso no depende de FastAPI
- dominio no depende de SQLAlchemy

## 6. Estructura sugerida

```text
backend/
  app/
    main.py
    config/
      settings.py
      security.py
    db/
      session.py
      base.py
      models/
    modules/
      auth/
        api/
        application/
        domain/
        infrastructure/
      clients/
        api/
        application/
        domain/
        infrastructure/
      services/
        api/
        application/
        domain/
        infrastructure/
      appointments/
        api/
        application/
        domain/
        infrastructure/
    shared/
      errors.py
      enums.py
      ids.py
  alembic/
    versions/
  tests/
    unit/
    integration/
    api/
```

## 7. Persistencia y concurrencia

- Sesion por request con `async_sessionmaker`.
- Casos write con transaccion explicita (`session.begin()`).
- Reserva de bloque con lock pesimista (`SELECT ... FOR UPDATE`).
- Constraint para evitar doble reserva activa por bloque (defensa final en DB).

Recomendacion:
- devolver conflicto de negocio cuando hay colision de reserva

## 8. Autenticacion OTP + JWT (tecnico)

Lineamientos:
- OTP de 6 digitos
- hash de OTP, nunca valor plano
- expiracion corta (5-10 min)
- single-use estricto
- intentos maximos por challenge
- rate limiting por email e IP

JWT:
- claims minimos: `sub`, `role`, `iat`, `exp`
- expiracion corta para access token
- refresh token fuera del alcance inicial

## 9. Testing prioritario

Prioridad de pruebas:
1. Integracion de auth OTP (request + verify)
2. Integracion de reserva concurrente
3. Integracion de transiciones de cita
4. API tests de endpoints criticos

Evitar al inicio:
- testear boilerplate en exceso
- mocks profundos de ORM sin valor

## 10. Riesgos a evitar

- logica de negocio en controllers
- no controlar concurrencia en reservas
- no invalidar OTP al usarse
- respuestas inconsistentes entre endpoints
- abstracciones prematuras sin necesidad real

## 11. Referencias de documentacion

- Contratos API: `api.md`
- Diseno de base de datos: `database.md`
- Operacion e infraestructura: `devops.md`
- Vision integral del sistema: `architecture.md`
- Arquitectura frontend: `frontend.md`
- Plan de ejecucion: `implementacion.md`
