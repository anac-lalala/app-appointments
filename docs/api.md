# API Contracts MVP - Gestion de Citas

Este documento define contratos REST para el MVP.

Objetivo:
- claridad
- consistencia
- implementacion simple
- consumo facil desde frontend

## 1. Principios de diseno API

- Base path: `/api/v1`
- JSON en request y response
- naming consistente en `snake_case`
- ids como `uuid`
- timestamps en ISO 8601 UTC
- versionado simple en path (`v1`)
- errores con estructura unica
- endpoints minimos para cubrir MVP

## 2. Recursos principales y relaciones

- `auth`
  - request OTP y verify OTP
- `services`
  - catalogo de servicios
- `service_time_blocks`
  - bloques disponibles por servicio
- `appointments`
  - reserva y ciclo de estados
- `admin` (scope de permisos)
  - operaciones de gestion

Relacion de negocio:
- un `service` tiene reglas de disponibilidad
- reglas generan `service_time_blocks`
- una `appointment` ocupa un bloque

## 3. Endpoints recomendados

### Auth OTP
- `POST /api/v1/auth/otp/request`
- `POST /api/v1/auth/otp/verify`
- `GET /api/v1/auth/me`

### Servicios
- `GET /api/v1/services`
- `POST /api/v1/admin/services`
- `PATCH /api/v1/admin/services/{service_id}`

### Disponibilidad
- `GET /api/v1/services/{service_id}/time-blocks`
- `PUT /api/v1/admin/services/{service_id}/availability-rules`

### Citas
- `POST /api/v1/appointments`
- `GET /api/v1/appointments/me`
- `GET /api/v1/admin/appointments`
- `PATCH /api/v1/admin/appointments/{appointment_id}/confirm`
- `PATCH /api/v1/admin/appointments/{appointment_id}/cancel`

## 4. Request/response de endpoints criticos

## 4.1 Request OTP

Metodo y path:
- `POST /api/v1/auth/otp/request`

Request:
```json
{
  "email": "client@example.com"
}
```

Response `202 Accepted`:
```json
{
  "data": {
    "message": "If the account exists, an OTP was sent"
  },
  "meta": {
    "request_id": "req_123"
  }
}
```

Errores:
- `400` payload invalido
- `429` rate limit excedido

## 4.2 Verify OTP

Metodo y path:
- `POST /api/v1/auth/otp/verify`

Request:
```json
{
  "email": "client@example.com",
  "otp_code": "123456"
}
```

Response `200 OK`:
```json
{
  "data": {
    "access_token": "jwt-token",
    "token_type": "Bearer",
    "expires_in": 1800,
    "user": {
      "id": "6fb8c2a9-9d18-4f0f-9a6d-5e9b9f8a2fcd",
      "email": "client@example.com",
      "role": "client"
    }
  },
  "meta": {
    "request_id": "req_124"
  }
}
```

Errores:
- `400` payload invalido
- `401` otp invalido o expirado
- `429` intentos maximos

## 4.3 List services

Metodo y path:
- `GET /api/v1/services`

Response `200 OK`:
```json
{
  "data": [
    {
      "id": "f6e0c8e2-f7e0-47be-8b29-f7d4bd906bc9",
      "name": "Consulta general",
      "description": "Atencion inicial",
      "duration_minutes": 30,
      "is_active": true
    }
  ],
  "meta": {
    "request_id": "req_125"
  }
}
```

## 4.4 List available time blocks

Metodo y path:
- `GET /api/v1/services/{service_id}/time-blocks?from=2026-04-01T00:00:00Z&to=2026-04-07T23:59:59Z`

Response `200 OK`:
```json
{
  "data": [
    {
      "id": "fd8f06ec-ccf0-47ef-8a71-09eaf2d79b7f",
      "service_id": "f6e0c8e2-f7e0-47be-8b29-f7d4bd906bc9",
      "start_at": "2026-04-02T15:00:00Z",
      "end_at": "2026-04-02T15:30:00Z",
      "status": "available"
    }
  ],
  "meta": {
    "request_id": "req_126"
  }
}
```

Errores:
- `400` rango invalido
- `404` service no existe

## 4.5 Create appointment

Metodo y path:
- `POST /api/v1/appointments`

Request:
```json
{
  "service_id": "f6e0c8e2-f7e0-47be-8b29-f7d4bd906bc9",
  "time_block_id": "fd8f06ec-ccf0-47ef-8a71-09eaf2d79b7f"
}
```

Response `201 Created`:
```json
{
  "data": {
    "id": "f7e8c4ac-6bb6-45a6-9a95-bbc553610f5b",
    "service_id": "f6e0c8e2-f7e0-47be-8b29-f7d4bd906bc9",
    "time_block_id": "fd8f06ec-ccf0-47ef-8a71-09eaf2d79b7f",
    "status": "pending_review",
    "created_at": "2026-04-02T14:10:22Z"
  },
  "meta": {
    "request_id": "req_127"
  }
}
```

Errores:
- `400` payload invalido
- `401` no autenticado
- `404` service o block no existe
- `409` bloque no disponible

## 4.6 Confirm appointment (admin)

Metodo y path:
- `PATCH /api/v1/admin/appointments/{appointment_id}/confirm`

Request:
```json
{}
```

Response `200 OK`:
```json
{
  "data": {
    "id": "f7e8c4ac-6bb6-45a6-9a95-bbc553610f5b",
    "status": "confirmed",
    "updated_at": "2026-04-02T14:15:00Z"
  },
  "meta": {
    "request_id": "req_128"
  }
}
```

Errores:
- `401` no autenticado
- `403` sin rol admin
- `404` cita no existe
- `409` transicion invalida

## 4.7 Cancel appointment (admin)

Metodo y path:
- `PATCH /api/v1/admin/appointments/{appointment_id}/cancel`

Request:
```json
{
  "reason": "client_no_show"
}
```

Response `200 OK`:
```json
{
  "data": {
    "id": "f7e8c4ac-6bb6-45a6-9a95-bbc553610f5b",
    "status": "cancelled",
    "updated_at": "2026-04-02T14:20:00Z"
  },
  "meta": {
    "request_id": "req_129"
  }
}
```

Errores:
- `401` no autenticado
- `403` sin rol admin
- `404` cita no existe
- `409` transicion invalida

## 5. Autenticacion y autorizacion

Flujo:
1. `request OTP`
2. `verify OTP`
3. backend emite JWT access token

Envio del token:
- `Authorization: Bearer <token>`

Proteccion de rutas:
- rutas cliente: cualquier usuario autenticado con `role=client`
- rutas admin: solo `role=admin`

Claims JWT minimos:
- `sub` (user id)
- `role` (`client` o `admin`)
- `iat`
- `exp`

## 6. Formato estandar de errores

Contrato:
```json
{
  "error": {
    "code": "TIME_BLOCK_UNAVAILABLE",
    "message": "Selected time block is no longer available",
    "details": {
      "time_block_id": "fd8f06ec-ccf0-47ef-8a71-09eaf2d79b7f"
    }
  },
  "meta": {
    "request_id": "req_130"
  }
}
```

Reglas:
- `code`: estable y orientado a negocio
- `message`: claro para frontend
- `details`: opcional
- `meta.request_id`: obligatorio para trazabilidad

## 7. Convenciones de naming

- rutas: plural y `kebab-case` cuando aplique
- campos JSON: `snake_case`
- enums: `snake_case` en minuscula
- timestamps: `*_at` en UTC ISO 8601
- ids: `uuid`

Estados de cita permitidos:
- `pending_review`
- `confirmed`
- `cancelled`

## 8. Que evitar en esta API

- endpoints duplicados para la misma accion
- respuestas distintas para errores equivalentes
- mezclar logica de admin y cliente en una ruta ambigua
- exponer detalles internos de DB
- versionado multiple prematuro (`v1`, `v2`, `internal`) en MVP

## 9. Propuesta final resumida

API REST simple en `/api/v1`, auth OTP + JWT, recursos minimos (`auth`, `services`, `time-blocks`, `appointments`) y separacion clara de permisos admin/cliente.

El contrato se mantiene consistente con:
- wrapper de respuesta `data + meta`
- wrapper de error `error + meta`
- convenciones unicas de naming y estados

## Cierre solicitado

1. Lista final de endpoints

- `POST /api/v1/auth/otp/request`
- `POST /api/v1/auth/otp/verify`
- `GET /api/v1/auth/me`
- `GET /api/v1/services`
- `POST /api/v1/admin/services`
- `PATCH /api/v1/admin/services/{service_id}`
- `PUT /api/v1/admin/services/{service_id}/availability-rules`
- `GET /api/v1/services/{service_id}/time-blocks`
- `POST /api/v1/appointments`
- `GET /api/v1/appointments/me`
- `GET /api/v1/admin/appointments`
- `PATCH /api/v1/admin/appointments/{appointment_id}/confirm`
- `PATCH /api/v1/admin/appointments/{appointment_id}/cancel`

2. Formato estandar de respuesta y error

Respuesta exitosa:
```json
{
  "data": {},
  "meta": {
    "request_id": "req_001"
  }
}
```

Respuesta de error:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  },
  "meta": {
    "request_id": "req_001"
  }
}
```

3. Convenciones API

- base path `/api/v1`
- JSON y `snake_case`
- ids `uuid`
- timestamps ISO 8601 UTC
- enums `snake_case`
- estados de cita: `pending_review`, `confirmed`, `cancelled`

4. Cosas fuera del MVP

- refresh tokens rotativos
- GraphQL
- CQRS/event bus
- paginacion compleja y filtros avanzados
- notificaciones omnicanal
- auditoria enterprise