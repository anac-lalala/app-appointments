# Frontend Architecture Prompt

Actúa como arquitecto frontend senior especializado en Next.js App Router, Tailwind CSS y diseño de aplicaciones web mantenibles.

Quiero que me ayudes a definir la arquitectura frontend de un MVP de gestión de citas, priorizando:

- simplicidad
- claridad
- mantenibilidad
- modularidad
- consistencia
- plazo corto de desarrollo
- buenas prácticas reales
- evitar repeticiones innecesarias
- evitar sobreingeniería

No quiero una respuesta genérica ni una arquitectura demasiado enterprise.

---

## 1. Contexto del proyecto

Estoy construyendo un MVP pequeño y real de gestión de citas para un solo negocio.

### Objetivo del sistema
Permitir que un negocio publique servicios y que clientes autenticados puedan consultar horarios disponibles y reservar citas.

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

## 2. Reglas de negocio

- El MVP es para un solo negocio
- Existe un solo usuario administrador interno
- Los clientes deben autenticarse
- La autenticación será por OTP enviado por correo
- Después de validar OTP, el sistema usa JWT
- Cada servicio tiene una duración definida
- La disponibilidad se define por servicio
- Los bloques de tiempo se generan a partir de reglas de disponibilidad
- Un bloque puede estar:
  - available
  - blocked
  - cancelled
- Una cita ocupa un bloque de tiempo
- La ocupación real del bloque se expresa por la existencia de una cita activa
- Una cita puede estar en estado:
  - pending_review
  - confirmed
  - cancelled

---

## 3. Modelo de dominio ya definido

Las entidades principales ya definidas en el dominio son:

- AdminUser
- Client
- Service
- ServiceAvailabilityRule
- ServiceTimeBlock
- Appointment

Relaciones clave:
- Service define reglas de disponibilidad
- Service genera bloques reservables
- Client reserva citas
- Appointment pertenece a un Service
- Appointment ocupa un ServiceTimeBlock

Usa este dominio como base conceptual.
No quiero que rediseñes el dominio desde cero.
Quiero que el frontend sea consistente con este modelo.

---

## 4. Stack frontend obligatorio

- Next.js con App Router
- Tailwind CSS
- TypeScript
- consumo de API REST del backend FastAPI
- autenticación con OTP + JWT

---

## 5. Decisiones ya tomadas que debes respetar

- El frontend debe ser entendible y fácil de mantener
- No quiero una arquitectura frontend sobrecomplicada
- No quiero exceso de capas ni carpetas vacías
- No quiero repetir la misma responsabilidad en múltiples lugares
- No quiero duplicar lógica entre páginas, hooks, services y components
- Quiero coherencia en nombres, estructura y flujo
- Quiero separar claramente:
  - rutas
  - componentes UI
  - lógica de negocio del frontend
  - acceso a API
  - manejo de sesión/auth
  - validación de formularios
- Quiero que la respuesta evite repeticiones innecesarias entre secciones
- Si propones algo una vez, luego reutilízalo en vez de volver a explicarlo completo

---

## 6. Lo que quiero que produzcas

Quiero que propongas una arquitectura frontend clara y concreta, estructurando tu respuesta así:

### 1. Resumen ejecutivo
Dame una propuesta breve de arquitectura frontend recomendada para este MVP.

### 2. Principios de diseño frontend
Explica qué principios aplicarías en este proyecto:
- modularidad
- separación de responsabilidades
- consistencia
- reutilización sin abstracción excesiva
- simplicidad del MVP
- evitar duplicación de lógica
- evitar repetición de estructuras innecesarias

### 3. Arquitectura general del frontend
Explícame cómo organizarías el frontend usando Next.js App Router.
Quiero que expliques:
- qué va en `app/`
- qué va fuera de `app/`
- cómo separar rutas públicas, rutas autenticadas de cliente y rutas de administrador
- cómo evitar mezclar layout, lógica y acceso a datos

### 4. Estructura de carpetas del frontend
Dame una estructura de carpetas concreta, realista y coherente.
Debe incluir, si aplica:
- app
- components
- features
- lib
- services
- hooks
- types
- styles

Quiero una propuesta aterrizada y sin redundancias.
Si decides no usar alguna carpeta, explícalo brevemente.

### 5. Organización por features o módulos
Quiero que expliques cómo organizarías el frontend por módulos o features, por ejemplo:
- auth
- services
- appointments
- admin

Y qué debe vivir dentro de cada uno.

### 6. Diseño de componentes
Explícame cómo separarías:
- componentes presentacionales
- componentes de formulario
- componentes de layout
- componentes específicos por feature

También quiero que expliques cómo evitarías:
- componentes gigantes
- duplicación de UI
- lógica dispersa en muchos componentes

### 7. Manejo de autenticación OTP + JWT en frontend
Propón una forma limpia de manejar:
- request de OTP
- verificación de OTP
- almacenamiento de sesión
- protección de rutas
- distinción entre admin y cliente si aplica
- logout
- expiración de sesión

Quiero que expliques si recomiendas:
- cookies httpOnly
- tokens en memoria
- localStorage
- middleware
- server components vs client components para auth

Justifica tu recomendación para este MVP.

### 8. Manejo de estado y datos
Quiero que me digas claramente:
- qué estado local debe quedarse en componentes
- qué estado debe centralizarse
- si recomiendas o no librerías extra de estado global
- cómo manejar fetch, cache, loading y error states
- cómo evitar duplicar llamadas al backend

Si propones librerías como TanStack Query o Zustand, justifica si realmente valen la pena en este MVP.
Si no las recomiendas, explícalo con claridad.

### 9. Comunicación con el backend
Propón una forma consistente de consumir la API.
Quiero que expliques:
- cómo organizar clients o services HTTP
- dónde definir tipos de request/response
- cómo manejar errores de API
- cómo normalizar respuestas
- cómo evitar que cada página haga fetch de forma distinta

### 10. Flujo de una operación clave
Explica paso a paso cómo debería fluir en frontend:
- login OTP
- consulta de servicios
- consulta de disponibilidad
- reserva de cita
- confirmación/cancelación desde admin

Quiero ver cómo interactúan:
- page
- components
- hooks
- services API
- auth/session
- UI states

### 11. Formularios y validación
Explica cómo manejarías formularios en este MVP:
- login OTP
- creación de servicio
- configuración de horarios
- reserva de cita

Quiero que expliques:
- si recomiendas React Hook Form o no
- cómo validar sin duplicar reglas innecesariamente
- cómo mantener formularios claros y mantenibles

### 12. Patrones recomendados
Indica qué patrones sí usarías y cuáles no.
Por ejemplo:
- feature-based structure
- container/presentational
- custom hooks
- service layer
- view models
- global store
- atomic design

Y explica por qué.

### 13. Buenas prácticas clave
Dame una lista de buenas prácticas específicas para este frontend.
No generales, sino aterrizadas a:
- Next.js App Router
- Tailwind
- auth OTP + JWT
- consumo de API
- modularidad
- evitar duplicaciones

### 14. Riesgos y errores comunes
Explica qué errores debo evitar en este frontend, por ejemplo:
- repetir lógica entre páginas
- poner fetch directamente en muchos componentes
- crear hooks innecesarios
- abstraer demasiado pronto
- mezclar UI con lógica de negocio
- usar demasiados client components sin necesidad
- desordenar la estructura del proyecto

### 15. Propuesta final recomendada
Cierra con una propuesta final concreta de arquitectura frontend para ejecutar este MVP.

---

## 7. Restricciones importantes

- No quiero una arquitectura inflada
- No quiero patrones por moda
- No quiero repetir explicaciones ya dadas en secciones anteriores
- No quiero que propongas demasiadas librerías si no son realmente necesarias
- No quiero duplicación de lógica entre módulos
- No quiero estructuras de carpetas redundantes
- Quiero que todo sea entendible y construible en poco tiempo

---

## 8. Enfoque esperado

Quiero una respuesta:
- clara
- coherente
- concreta
- orientada a implementación
- sin repeticiones innecesarias
- con decisiones justificadas
- práctica para aprender buenas prácticas reales mientras construyo

Si detectas que alguna decisión frontend puede simplificarse más para este MVP, debes decirlo claramente.

---

## 9. Resultado esperado

La respuesta debe terminar con:

1. arquitectura frontend final recomendada
2. estructura de carpetas frontend
3. decisiones clave de auth/session
4. lista de cosas que quedan fuera del MVP