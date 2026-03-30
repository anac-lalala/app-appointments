# Database Design MVP - Gestion de Citas

Este documento traduce el dominio del MVP a un esquema relacional en PostgreSQL, con foco en integridad, simplicidad y control de concurrencia para evitar reservas duplicadas.

## 1. Principios de modelado

- Modelado normalizado pragmático: 3FN en entidades core, sin descomposición excesiva.
- Integridad en DB primero: constraints y FKs para sostener reglas críticas.
- Estado explícito: enums/checks en bloques y citas para transiciones claras.
- Concurrencia defendida en dos capas: lock transaccional + constraint única parcial.
- Compatibilidad Alembic: tipos simples, índices explícitos, migraciones incrementales.
- Alcance MVP: single business, sin multi-tenant ni permisos complejos.

## 2. Tablas principales

Tipos recomendados base:
- PK: `uuid`
- Fechas: `timestamptz`
- Duraciones: `integer` (minutos)
- Estados: `text` + `check constraint` (simple para MVP)

### 2.1 `admin_users`

Propósito:
- Usuarios internos con capacidad de administrar servicios y citas.

Columnas:
- `id uuid primary key`
- `email text not null`
- `full_name text not null`
- `is_active boolean not null default true`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### 2.2 `clients`

Propósito:
- Usuarios clientes autenticados por OTP.

Columnas:
- `id uuid primary key`
- `email text not null`
- `full_name text null`
- `phone text null`
- `is_active boolean not null default true`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### 2.3 `services`

Propósito:
- Catálogo de servicios reservables.

Columnas:
- `id uuid primary key`
- `name text not null`
- `description text null`
- `duration_minutes integer not null`
- `is_active boolean not null default true`
- `created_by_admin_id uuid not null`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### 2.4 `service_availability_rules`

Propósito:
- Reglas base semanales desde las que se generan bloques.

Columnas:
- `id uuid primary key`
- `service_id uuid not null`
- `weekday smallint not null` (0-6)
- `start_time time not null`
- `end_time time not null`
- `is_active boolean not null default true`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### 2.5 `service_time_blocks`

Propósito:
- Bloques concretos reservables para un servicio.

Columnas:
- `id uuid primary key`
- `service_id uuid not null`
- `start_at timestamptz not null`
- `end_at timestamptz not null`
- `status text not null default 'available'`
- `generated_from_rule_id uuid null`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

Estados válidos de bloque:
- `available`
- `blocked`
- `cancelled`

### 2.6 `appointments`

Propósito:
- Reserva realizada por cliente sobre un bloque.

Columnas:
- `id uuid primary key`
- `client_id uuid not null`
- `service_id uuid not null`
- `service_time_block_id uuid not null`
- `status text not null default 'pending_review'`
- `client_name_snapshot text not null`
- `client_email_snapshot text not null`
- `client_phone_snapshot text null`
- `confirmed_at timestamptz null`
- `cancelled_at timestamptz null`
- `cancel_reason text null`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

Estados válidos de cita:
- `pending_review`
- `confirmed`
- `cancelled`

## 3. Relaciones y foreign keys

- `services.created_by_admin_id -> admin_users.id`
- `service_availability_rules.service_id -> services.id`
- `service_time_blocks.service_id -> services.id`
- `service_time_blocks.generated_from_rule_id -> service_availability_rules.id`
- `appointments.client_id -> clients.id`
- `appointments.service_id -> services.id`
- `appointments.service_time_block_id -> service_time_blocks.id`

Cardinalidades:
- un `service` tiene muchas `service_availability_rules`
- un `service` tiene muchos `service_time_blocks`
- un `client` tiene muchas `appointments`
- un `service_time_block` puede tener como máximo una cita activa

## 4. Constraints e integridad

### Unique constraints

- `admin_users(email)`
- `clients(email)`
- `service_time_blocks(service_id, start_at, end_at)` para evitar duplicados de bloque

### Check constraints

- `services.duration_minutes > 0`
- `service_availability_rules.weekday between 0 and 6`
- `service_availability_rules.start_time < end_time`
- `service_time_blocks.start_at < end_at`
- `service_time_blocks.status in ('available','blocked','cancelled')`
- `appointments.status in ('pending_review','confirmed','cancelled')`
- `appointments.confirmed_at is null or appointments.status = 'confirmed'`
- `appointments.cancelled_at is null or appointments.status = 'cancelled'`

### Foreign keys

- todas con `on update restrict`
- para MVP, preferir `on delete restrict` en tablas core para no romper histórico

### Integridad cita-bloque

- cita siempre referencia bloque existente
- el bloque puede existir aunque la cita se cancele (histórico)
- no se borra cita física en MVP, solo cambio de estado

## 5. Concurrencia al reservar

Opciones:

1. Solo lock transaccional (`SELECT ... FOR UPDATE` en `service_time_blocks`)
- bueno, pero insuficiente ante paths alternos o bugs de app

2. Solo unique parcial en `appointments`
- robusto a nivel DB, pero puede devolver colisiones tardías sin flujo claro

3. Recomendado: lock + unique parcial
- lock para flujo limpio
- constraint para garantía final de integridad

Recomendación concreta:
- en `BookAppointment`, abrir transacción
- lock del bloque por `id`
- verificar bloque elegible
- insertar cita
- sostener garantía final con índice único parcial:

```sql
create unique index uq_active_appointment_per_block
on appointments (service_time_block_id)
where status in ('pending_review', 'confirmed');
```

Si hay colisión, mapear a `409 Conflict`.

## 6. Tablas para OTP/auth

### 6.1 `otp_challenges`

Propósito:
- Gestión de OTP con expiración, intentos y single-use.

Columnas:
- `id uuid primary key`
- `email text not null`
- `otp_hash text not null`
- `expires_at timestamptz not null`
- `attempt_count integer not null default 0`
- `max_attempts integer not null default 5`
- `used_at timestamptz null`
- `requested_ip_hash text null`
- `created_at timestamptz not null default now()`

Checks:
- `attempt_count >= 0`
- `max_attempts > 0`

Reglas:
- OTP nunca en texto plano
- challenge usado o expirado no puede verificarse
- al emitir nuevo OTP para email, invalidar challenges activos previos

### 6.2 Tabla de sesiones JWT (opcional MVP)

Para MVP mínimo, no obligatoria.

Si quieres trazabilidad extra sin complejidad alta:
- `auth_sessions(id uuid, user_id uuid, role text, issued_at, expires_at, revoked_at null, jti text unique)`

## 7. Índices recomendados desde inicio

- `idx_services_is_active` en `services(is_active)` para listados públicos
- `idx_rules_service_weekday` en `service_availability_rules(service_id, weekday)`
- `idx_blocks_service_start` en `service_time_blocks(service_id, start_at)`
- `idx_blocks_status_start` en `service_time_blocks(status, start_at)`
- `idx_appointments_client_created` en `appointments(client_id, created_at desc)`
- `idx_appointments_status_created` en `appointments(status, created_at desc)` para panel admin
- `idx_otp_email_created` en `otp_challenges(email, created_at desc)`
- índice único parcial de cita activa por bloque (sección concurrencia)

## 8. Campos auditables y timestamps

Mínimos recomendados:
- `created_at` y `updated_at` en todas las tablas core
- `confirmed_at` y `cancelled_at` en `appointments`
- `used_at` en `otp_challenges`

Audit básico opcional de bajo costo:
- `created_by_admin_id` en `services`
- `updated_by_admin_id` en acciones admin críticas (si aplica)

No agregar todavía:
- tabla de auditoría genérica para cada cambio de columna

## 9. Qué no modelar todavía

- multiempresa / tenant_id en todas las tablas
- RBAC complejo (roles y permisos granulares)
- event sourcing
- soft-delete universal en todas las tablas
- versionado de reglas de disponibilidad
- sistema avanzado de notificaciones/pipeline de eventos

## 10. Propuesta final

Esquema recomendado para este MVP:
- `admin_users`
- `clients`
- `services`
- `service_availability_rules`
- `service_time_blocks`
- `appointments`
- `otp_challenges`

Con este diseño se logra:
- consistencia con el dominio
- control fuerte contra doble reserva
- migraciones simples con Alembic
- complejidad ajustada al MVP

## Cierre solicitado

1. Tablas finales recomendadas

- `admin_users`
- `clients`
- `services`
- `service_availability_rules`
- `service_time_blocks`
- `appointments`
- `otp_challenges`

2. Relaciones y constraints

- FKs entre servicios-reglas-bloques-citas y usuarios
- unique en emails y en `(service_id, start_at, end_at)` de bloques
- checks de estados, rangos y coherencia de timestamps
- `on delete restrict` para proteger histórico

3. Estrategia de concurrencia para reservas

- transacción + `SELECT ... FOR UPDATE` del bloque
- índice único parcial para cita activa por bloque
- mapeo de colisión a `409 Conflict`

4. Cosas fuera del MVP

- multiempresa
- permisos avanzados
- event sourcing
- auditoría enterprise
- optimizaciones prematuras de escala
