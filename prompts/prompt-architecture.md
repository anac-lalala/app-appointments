Quiero que actúes como arquitecto de software senior y me propongas una arquitectura clara, entendible y realista para un MVP de gestión de citas, priorizando buenas prácticas, modularidad, mantenibilidad y un plazo corto de desarrollo.

## Objetivo del proyecto
Necesito construir un MVP pequeño pero útil de una plataforma web de gestión de citas que resuelva un problema real: permitir a un negocio administrar servicios y recibir reservas de clientes en horarios disponibles.

El objetivo no es hacer una plataforma compleja desde el inicio, sino construir un sistema pequeño, bien diseñado y con base sólida para crecer después.

## Alcance funcional del MVP
El MVP debe permitir:

### Administrador
- iniciar sesión
- crear servicios
- configurar duración del servicio
- definir horarios base del servicio
- visualizar citas
- confirmar o cancelar citas

### Cliente
- iniciar sesión
- consultar servicios disponibles
- consultar horarios disponibles de un servicio
- reservar una cita

## Reglas del negocio
- Es un MVP inicialmente para un solo negocio
- Existe un solo usuario administrador interno
- Los clientes deben autenticarse
- La autenticación será sin contraseña, usando OTP por correo
- Cada servicio tiene una duración definida
- La disponibilidad se define por servicio
- Los bloques de tiempo se generan a partir de reglas de disponibilidad
- Un bloque puede estar disponible, bloqueado o cancelado
- Una cita ocupa un bloque de tiempo
- La ocupación real del bloque se expresa por la existencia de una cita activa
- Una cita puede estar en estado pending_review, confirmed o cancelled
- El sistema debe guardar snapshot histórico básico del cliente en la cita:
  - nombre
  - correo
  - teléfono

## Contexto adicional: UML de dominio ya definido
Ya existe un UML de clases de dominio para el MVP y debe tomarse como referencia base del diseño arquitectónico.

Las entidades principales ya definidas son:
- AdminUser
- Client
- Service
- ServiceAvailabilityRule
- ServiceTimeBlock
- Appointment

Relaciones clave del dominio:
- Service define reglas de disponibilidad
- Service genera bloques de tiempo reservables
- Client reserva citas
- Appointment pertenece a un Service
- Appointment ocupa un ServiceTimeBlock
- ServiceTimeBlock puede originarse desde una ServiceAvailabilityRule

Reglas importantes del modelo:
- cada servicio tiene duración definida
- la disponibilidad depende del servicio
- los bloques se generan a partir de reglas de disponibilidad
- un bloque puede estar available, blocked o cancelled
- la ocupación real del bloque se expresa por la existencia de una cita activa
- una cita puede estar en estado pending_review, confirmed o cancelled
- Appointment guarda snapshot histórico básico del cliente:
  - client_name_snapshot
  - client_email_snapshot
  - client_phone_snapshot

Quiero que uses este UML como base del dominio y que la arquitectura propuesta sea consistente con él.
No quiero que rediseñes el dominio desde cero, sino que lo uses como referencia para:
- organizar módulos
- definir capas
- proponer estructura del repositorio
- explicar flujo entre componentes
- decidir qué patrones sí y no aplicar

## Stack tecnológico obligatorio
- Frontend: Next.js (App Router) + Tailwind CSS
- Backend: Python con FastAPI (async, buenas prácticas)
- Base de datos: PostgreSQL
- Autenticación: Membership con OTP por correo, sin contraseña
- Infraestructura: Dockerizado para desarrollo y producción

## Lo que quiero de la respuesta
Quiero una propuesta de arquitectura enfocada en que el proyecto sea:
- entendible
- realista
- mantenible
- modular
- implementable en corto plazo
- alineado con buenas prácticas
- sin sobreingeniería

## Instrucciones importantes
1. No propongas microservicios. Debe ser un monolito modular.
2. No sobrediseñes con patrones innecesarios.
3. Aplica SOLID de forma razonable y práctica, no dogmática.
4. Prioriza separación clara de responsabilidades.
5. Explica las decisiones arquitectónicas de forma sencilla.
6. Si propones capas, módulos o patrones, justifica por qué sí aportan valor para este MVP.
7. No mezcles dominio con detalles de frameworks más de lo necesario.
8. La arquitectura debe dejar camino para crecer en el futuro, pero sin agregar complejidad innecesaria hoy.
9. No cambies arbitrariamente las entidades del UML; trabaja sobre ellas.
10. Si propones ajustes al UML, deben ser mínimos y claramente justificados.

## Quiero que estructures tu respuesta así

### 1. Visión general de la arquitectura
Explícame la arquitectura general propuesta para frontend, backend, base de datos, autenticación e infraestructura.

### 2. Principios arquitectónicos
Explica qué principios seguirías en este proyecto:
- modularidad
- separación de capas
- responsabilidad única
- dependencia de abstracciones
- simplicidad del MVP

### 3. Estructura del backend
Propón una estructura clara para FastAPI como monolito modular.
Quiero que expliques:
- capas recomendadas
- módulos del dominio
- dónde van entidades, casos de uso, repositorios, esquemas, endpoints e infraestructura
- qué conviene abstraer y qué no

### 4. Estructura del frontend
Propón una estructura clara para Next.js App Router.
Quiero que expliques:
- organización por rutas
- separación entre UI, lógica, hooks, servicios y componentes
- cómo manejar autenticación OTP
- cómo conectar con la API

### 5. Modelo de dominio del MVP
Resume las entidades principales:
- AdminUser
- Client
- Service
- ServiceAvailabilityRule
- ServiceTimeBlock
- Appointment

Y explica cómo deberían vivir conceptualmente dentro de la arquitectura.

### 6. Flujo de comunicación entre componentes
Explica claramente cómo fluye una operación típica, por ejemplo:
- el cliente inicia sesión por OTP
- consulta servicios
- consulta horarios disponibles
- reserva una cita
- el administrador luego la confirma

Quiero ver el flujo entre:
- frontend
- endpoints
- casos de uso
- dominio
- repositorios
- base de datos
- servicio de correo OTP

### 7. Estructura del repositorio
Propón una estructura de carpetas realista para el repositorio completo, incluyendo:
- frontend
- backend
- docker
- configuración
- scripts
- documentación

Dame una estructura concreta, no solo conceptual.

### 8. Patrones recomendados
Indica qué patrones sí recomendarías para este MVP y cuáles no.
Por ejemplo:
- modular monolith
- repository
- use case / application service
- DTOs
- dependency injection
- domain services
- policy objects

Y explica por qué.

### 9. Buenas prácticas clave
Dame una lista de buenas prácticas específicas para este proyecto.
No generales, sino aterrizadas a este stack y este MVP.

### 10. Riesgos y errores comunes
Explícame qué errores de arquitectura debería evitar en este proyecto.
Por ejemplo:
- sobrediseño
- mezclar ORM con dominio
- meter demasiadas abstracciones
- acoplar frontend directamente a detalles internos del backend
- diseñar primero para escala que aún no existe

### 11. Versión recomendada de arquitectura final
Cierra con una propuesta concreta y resumida de arquitectura recomendada para este MVP, como si fuera la decisión final a ejecutar.

## Importante
Quiero una respuesta clara, pedagógica y orientada a implementación real.
No quiero una respuesta académica abstracta ni una arquitectura enterprise exagerada.
Quiero algo que pueda construir de forma limpia en poco tiempo, aprendiendo buenas prácticas reales.

Al final, incluye una propuesta concreta de estructura de carpetas para backend y frontend lista para iniciar el proyecto.

A continuación incluyo el PlantUML actual del dominio. Úsalo como referencia contextual del modelo, no como algo que deba rehacerse desde cero.

@startuml
hide methods
skinparam classAttributeIconSize 0
skinparam linetype ortho

title UML de clases de dominio - MVP simplificado de gestión de citas

class AdminUser {
  +id: UUID
  +name: string
  +email: string
  +password_hash: string
  +is_active: boolean
  +created_at: datetime
  +updated_at: datetime
}

class Client {
  +id: UUID
  +name: string
  +email: string
  +phone: string
  +password_hash: string
  +is_active: boolean
  +created_at: datetime
  +updated_at: datetime
}

enum ConfirmationMode {
  automatic
  manual
}

class Service {
  +id: UUID
  +name: string
  +description: string
  +duration_minutes: int
  +confirmation_mode: ConfirmationMode
  +is_active: boolean
  +created_at: datetime
  +updated_at: datetime
}

class ServiceAvailabilityRule {
  +id: UUID
  +service_id: UUID
  +day_of_week: int
  +start_time: time
  +end_time: time
  +is_active: boolean
  +created_at: datetime
  +updated_at: datetime
}

enum TimeBlockStatus {
  available
  blocked
  cancelled
}

class ServiceTimeBlock {
  +id: UUID
  +service_id: UUID
  +availability_rule_id: UUID
  +start_at: datetime
  +end_at: datetime
  +status: TimeBlockStatus
  +created_at: datetime
  +updated_at: datetime
}

enum AppointmentStatus {
  pending_review
  confirmed
  cancelled
}

class Appointment {
  +id: UUID
  +client_id: UUID
  +service_id: UUID
  +service_time_block_id: UUID
  +status: AppointmentStatus
  +client_name_snapshot: string
  +client_email_snapshot: string
  +client_phone_snapshot: string
  +created_at: datetime
  +confirmed_at: datetime
  +cancelled_at: datetime
  +updated_at: datetime
}

' =========================
' AGREGACIONES
' =========================
Service o-- "0..*" ServiceAvailabilityRule : define >
Service o-- "0..*" ServiceTimeBlock : ofrece >

' =========================
' ASOCIACIONES
' =========================
Client "1" -- "0..*" Appointment : reserva >
Appointment "0..*" --> "1" Service : pertenece a >
Appointment "0..*" --> "1" ServiceTimeBlock : ocupa >
ServiceTimeBlock "0..1" --> "0..1" ServiceAvailabilityRule : se genera desde >

' =========================
' DEPENDENCIAS
' =========================
Service ..> ConfirmationMode : usa
ServiceTimeBlock ..> TimeBlockStatus : usa
Appointment ..> AppointmentStatus : usa

' =========================
' NOTAS
' =========================
note right of AdminUser
Usuario interno único del MVP.

Responsable de:
- crear servicios
- configurar disponibilidad
- ver citas
- confirmar o cancelar citas
end note

note right of Client
Cliente autenticado que:
- consulta servicios
- consulta horarios disponibles
- reserva citas
end note

note right of Service
Entidad central del agendamiento.

Define:
- duración
- modo de confirmación
- estado activo
end note

note right of ServiceAvailabilityRule
Regla base de horario.

Ejemplo:
- lunes 09:00 a 12:00
- lunes 14:00 a 18:00
end note

note right of ServiceTimeBlock
Unidad concreta reservable.

status representa solo disponibilidad operativa:
- available
- blocked
- cancelled

La ocupación real se expresa
por la existencia de Appointment.
end note

note right of Appointment
Entidad transaccional principal.

Guarda snapshot básico del cliente
para preservar la información histórica
aunque el cliente actualice su perfil luego.
end note

note bottom of Appointment
Una cita activa ocupa un solo bloque.
Para el MVP, una cita activa puede ser:
- pending_review
- confirmed
end note

note bottom of Service
Aunque el MVP es para un solo negocio,
la estructura puede crecer luego
agregando Business sin romper el modelo base.
end note
@enduml

Si detectas inconsistencias menores, señálalas, pero mantén el enfoque en proponer una arquitectura práctica para implementar este MVP.