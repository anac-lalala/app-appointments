# Database Design Prompt

Actúa como arquitecto de datos/backend senior y ayúdame a traducir el modelo de dominio de un MVP de gestión de citas a un diseño relacional en PostgreSQL.

Quiero una propuesta:
- clara
- normalizada sin exceso
- consistente con el dominio
- segura frente a reservas duplicadas
- fácil de migrar con Alembic
- realista para un MVP

---

## Contexto del proyecto

MVP de gestión de citas para un solo negocio.

### Entidades del dominio
- AdminUser
- Client
- Service
- ServiceAvailabilityRule
- ServiceTimeBlock
- Appointment

### Reglas clave
- cada servicio tiene duración
- la disponibilidad depende del servicio
- los bloques se generan a partir de reglas
- un bloque puede estar available, blocked o cancelled
- una cita ocupa un bloque
- estados de cita:
  - pending_review
  - confirmed
  - cancelled
- la cita guarda snapshot histórico del cliente:
  - client_name_snapshot
  - client_email_snapshot
  - client_phone_snapshot

### Auth
- OTP por correo
- JWT
- sin contraseñas

---

## Stack
- PostgreSQL
- SQLAlchemy async
- Alembic
- psycopg v3
- asyncpg

---

## Lo que quiero que produzcas

### 1. Principios de modelado
Explica cómo modelarías esta base de datos para el MVP.

### 2. Tablas principales
Propón las tablas principales con:
- nombre
- propósito
- columnas
- tipos sugeridos
- claves primarias

### 3. Relaciones
Explica las relaciones entre tablas y sus foreign keys.

### 4. Constraints e integridad
Quiero recomendaciones concretas para:
- unique constraints
- check constraints
- foreign keys
- integridad de citas y bloques

### 5. Concurrencia al reservar
Explica cómo evitar doble reserva del mismo bloque.
Quiero opciones concretas y recomendación.

### 6. Tablas para OTP/auth
Propón las tablas o estructuras necesarias para:
- OTP requests / codes
- expiración
- single-use
- trazabilidad mínima

### 7. Índices
Dime qué índices pondrías desde el inicio y por qué.

### 8. Campos auditables y timestamps
Define qué timestamps o campos auditables sí conviene tener.

### 9. Cosas que no modelar todavía
Qué cosas no incluirías aún en la base.

### 10. Propuesta final
Cierra con un esquema relacional recomendado para este MVP.

---

## Restricciones

- no modelado multiempresa todavía
- no tablas de permisos complejas
- no event sourcing
- no sobrecomplicar auditoría
- no optimizar prematuramente para escalas que aún no existen

---

## Resultado esperado

La respuesta debe terminar con:
1. tablas finales recomendadas
2. relaciones y constraints
3. estrategia de concurrencia para reservas
4. cosas fuera del MVP