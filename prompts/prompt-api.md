# API Design Prompt

Actúa como arquitecto backend/API senior y ayúdame a definir los contratos de API para un MVP de gestión de citas.

Quiero una propuesta:
- clara
- consistente
- fácil de implementar
- fácil de consumir desde el frontend
- coherente con el dominio ya definido
- sin sobrecomplicar el diseño

No quiero una API enterprise exagerada ni una respuesta abstracta.

---

## Contexto del proyecto

MVP de gestión de citas para un solo negocio.

### Funcionalidades del MVP

#### Admin
- iniciar sesión por OTP
- crear servicios
- configurar disponibilidad base
- ver citas
- confirmar o cancelar citas

#### Cliente
- iniciar sesión por OTP
- ver servicios
- ver horarios disponibles
- reservar cita

---

## Reglas clave

- auth por OTP email
- luego JWT
- sin contraseñas
- bloques disponibles por servicio
- cita ocupa un bloque
- estados de cita:
  - pending_review
  - confirmed
  - cancelled

---

## Entidades del dominio

- AdminUser
- Client
- Service
- ServiceAvailabilityRule
- ServiceTimeBlock
- Appointment

---

## Lo que quiero que produzcas

### 1. Principios de diseño de la API
Explica cómo diseñarías esta API:
- consistencia
- claridad
- versionado
- manejo de errores
- simplicidad del MVP

### 2. Recursos principales
Identifica los recursos principales de la API y cómo se relacionan.

### 3. Endpoints recomendados
Propón endpoints concretos para:
- auth OTP
- servicios
- disponibilidad
- citas
- admin

### 4. Request y response shapes
Para cada endpoint importante, propone:
- método
- path
- request body
- response body
- códigos HTTP

### 5. Autenticación y autorización
Explica cómo manejarías:
- emisión de JWT
- envío del token
- protección de rutas
- rutas de cliente vs admin

### 6. Errores de API
Define un formato consistente para errores.
Incluye ejemplos.

### 7. Convenciones de naming
Define convenciones claras para:
- rutas
- campos
- enums
- timestamps
- ids

### 8. Diseño de endpoints críticos
Quiero detalle especial para:
- request OTP
- verify OTP
- list services
- list available time blocks
- create appointment
- confirm appointment
- cancel appointment

### 9. Qué evitar en esta API
Explica qué malas prácticas evitarías.

### 10. Propuesta final
Cierra con una propuesta final resumida de contratos API recomendados para este MVP.

---

## Restricciones

- no GraphQL
- no CQRS complejo
- no endpoints innecesarios
- no versionado complicado para el MVP
- no respuestas inconsistentes

---

## Resultado esperado

La respuesta debe terminar con:
1. lista final de endpoints
2. formato estándar de respuesta y error
3. convenciones API
4. cosas fuera del MVP