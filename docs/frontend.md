# Arquitectura Frontend MVP - Gestion de Citas

## 1. Resumen ejecutivo
Propuesta recomendada: frontend en Next.js App Router + TypeScript + Tailwind, organizado por features (`auth`, `services`, `appointments`, `admin`) sobre una base simple de capas: rutas en `app`, UI en `components`, logica de pantalla en hooks de feature, y consumo de API centralizado.

Objetivo: entregar rapido con estructura clara, sin arquitectura inflada, evitando duplicacion de logica entre paginas, componentes y servicios.

## 2. Principios de diseno frontend
- Modularidad pragmatica: dividir por features reales del negocio, no por patrones de moda.
- Separacion de responsabilidades:
	- rutas y navegacion en `app`
	- UI reusable en `components`
	- casos de uso frontend (hooks/acciones) en `features/*`
	- acceso HTTP en `services`
- Consistencia: convenciones unicas para nombres, carpetas, estado de carga/error y formularios.
- Reutilizacion sin sobreabstraccion: extraer solo cuando hay repeticion real en 2+ pantallas.
- Simplicidad de MVP: evitar stores globales innecesarios y arquitecturas enterprise.
- Cero duplicacion de flujo: una sola via para auth, una sola via para llamadas API, una sola via para manejar errores.

## 3. Arquitectura general del frontend
### Que va en `app/`
- Segmentos de rutas, layouts, `page.tsx`, `loading.tsx`, `error.tsx`.
- Server Components por defecto para shell, SEO y prefetch inicial.
- Client Components solo donde hay interaccion (formularios, filtros, acciones).

### Que va fuera de `app/`
- `features/`: logica por modulo de negocio.
- `components/`: UI compartida y de layout.
- `services/`: cliente HTTP y servicios REST.
- `lib/`: utilidades transversales (auth, fechas, env, validacion de errores).
- `types/`: contratos TS compartidos de dominio/API.

### Separacion de rutas por acceso
- Publicas: login OTP, verificacion OTP, listado de servicios.
- Cliente autenticado: disponibilidad y reserva, mis citas.
- Admin autenticado: gestion de servicios, horarios base y revision de citas.

### Como evitar mezclar layout, logica y datos
- Pagina: compone secciones y decide que hooks usar.
- Hook de feature: orquesta estado de negocio de pantalla.
- Service API: encapsula endpoint y mapeo request/response.
- Componente UI: renderiza, no decide negocio.

## 4. Estructura de carpetas del frontend
```text
src/
	app/
		(public)/
			login/page.tsx
			verify-otp/page.tsx
			services/page.tsx
			services/[serviceId]/page.tsx
		(client)/
			layout.tsx
			booking/[serviceId]/page.tsx
			my-appointments/page.tsx
		(admin)/
			layout.tsx
			admin/services/page.tsx
			admin/availability/page.tsx
			admin/appointments/page.tsx
		api/
			auth/logout/route.ts
		globals.css
		layout.tsx

	components/
		ui/
			button.tsx
			input.tsx
			select.tsx
			modal.tsx
			badge.tsx
			table.tsx
			spinner.tsx
			empty-state.tsx
			alert.tsx
		layout/
			app-shell.tsx
			topbar.tsx
			sidebar.tsx

	features/
		auth/
			components/
				request-otp-form.tsx
				verify-otp-form.tsx
			hooks/
				use-request-otp.ts
				use-verify-otp.ts
				use-session.ts
			schemas/
				request-otp.schema.ts
				verify-otp.schema.ts
		services/
			components/
				service-card.tsx
				service-list.tsx
			hooks/
				use-services.ts
			schemas/
				service.schema.ts
		availability/
			components/
				slot-picker.tsx
			hooks/
				use-service-slots.ts
		appointments/
			components/
				appointment-status-badge.tsx
				appointment-list.tsx
			hooks/
				use-book-appointment.ts
				use-my-appointments.ts
		admin/
			components/
				service-form.tsx
				availability-rule-form.tsx
				admin-appointments-table.tsx
			hooks/
				use-admin-services.ts
				use-admin-appointments.ts

	services/
		http/
			api-client.ts
			api-error.ts
		auth.service.ts
		services.service.ts
		availability.service.ts
		appointments.service.ts
		admin.service.ts

	hooks/
		use-debounce.ts
		use-pagination.ts

	lib/
		auth/
			session.ts
			permissions.ts
		env.ts
		dates.ts
		query-client.ts
		cn.ts

	types/
		auth.ts
		service.ts
		availability.ts
		appointment.ts
		api.ts

	styles/
		tokens.css
```

Notas de simplificacion:
- Se mantiene `hooks/` global solo para hooks realmente transversales.
- No se crea carpeta `store/` inicialmente para evitar estado global prematuro.

## 5. Organizacion por features o modulos
- `auth`:
	- Request OTP, verify OTP, session actual, logout.
	- Validaciones y formularios de acceso.
- `services`:
	- Listado publico de servicios.
	- Detalle basico de servicio (duracion, descripcion).
- `availability`:
	- Consulta de bloques disponibles por servicio/fecha.
	- Seleccion de slot reservable.
- `appointments`:
	- Reserva de cita y listado de citas del cliente.
	- Render de estados `pending_review`, `confirmed`, `cancelled`.
- `admin`:
	- CRUD basico de servicios, reglas de disponibilidad, confirmacion/cancelacion.

Regla de ownership:
- Cada feature contiene su UI + hooks de negocio de pantalla.
- Ninguna feature llama `fetch` directo: siempre usa `services/`.

## 6. Diseno de componentes
- Presentacionales (`components/ui`, `features/*/components`): reciben props y callbacks, sin HTTP.
- Formularios: componentes dedicados por caso (`request-otp-form`, `service-form`) + schema unico.
- Layout: shell, topbar, sidebar y wrappers de seccion.
- Especificos de feature: tablas/cards/pickers de cada modulo.

Como evitar componentes gigantes:
- Maximo 150-200 lineas por componente de pantalla; dividir en secciones.
- Extraer subcomponentes solo cuando mejora legibilidad o reuso.
- Mover logica de mutaciones/fetch a hooks de feature.

Como evitar duplicacion de UI:
- Catalogo base de `ui/` para controles repetidos (button/input/table/badge).
- Estados estandar: `LoadingState`, `EmptyState`, `ErrorState`.

## 7. Manejo de autenticacion OTP + JWT en frontend
Recomendacion para este MVP:
- Access token en cookie `httpOnly`, `secure`, `sameSite=lax`.
- Refresh token opcional fuera del MVP (si la sesion puede ser corta).
- Evitar `localStorage` para tokens.

Flujo:
1. `POST /auth/otp/request` (email).
2. `POST /auth/otp/verify` (email + otp).
3. Backend setea cookie de sesion JWT.
4. Frontend consulta `GET /auth/me` para hidratar sesion.

Proteccion de rutas:
- `middleware.ts` valida presencia de cookie para segmentos `(client)` y `(admin)`.
- Distincion admin/cliente por claim `role` en JWT y validacion en middleware + guard de servidor.

Server vs Client Components para auth:
- Server Components para leer sesion inicial y decidir redirect temprano.
- Client Components solo para formularios OTP y acciones de logout.

Logout y expiracion:
- Logout via `POST /api/auth/logout` (route handler) para limpiar cookie.
- En 401 global, invalidar cache de sesion y redirigir a `/login`.

## 8. Manejo de estado y datos
Estado local (componente):
- Inputs, modales, seleccion temporal de fecha/slot, toggles UI.

Estado centralizado (servidor/cache):
- Sesion actual, servicios, slots, citas.

Libreria recomendada:
- Si: TanStack Query (vale la pena para este MVP).
	- Evita duplicar fetch, cachea respuestas, facilita invalidaciones tras mutaciones.
	- Reduce boilerplate de loading/error y reintentos.
- No: Zustand/Redux al inicio (no hay estado cliente complejo que lo justifique).

Regla practica:
- Estado remoto en Query.
- Estado efimero de UI en componente.

## 9. Comunicacion con el backend
Estandar unico de consumo REST:
- `services/http/api-client.ts` centraliza `fetch`, headers, parseo y manejo de errores.
- Un archivo service por dominio (`auth.service.ts`, `appointments.service.ts`, etc.).

Tipos request/response:
- Definidos en `types/*`.
- Cada service tipa entrada/salida explicitamente.

Errores API:
- `ApiError` unico con `status`, `code`, `message`, `details`.
- Adaptador para mostrar mensajes de negocio consistentes en UI.

Normalizacion de respuestas:
- Mantener shape de backend cuando sea estable.
- Normalizar solo fechas/enums y estructuras que la UI consume repetidamente.

Como evitar fetch distinto en cada pagina:
- Todas las paginas llaman hooks de feature.
- Todos los hooks llaman `services/*`.
- Ninguna pagina usa `fetch` crudo.

## 10. Flujo de una operacion clave
### Login OTP
1. `app/(public)/login/page.tsx` renderiza `RequestOtpForm`.
2. `RequestOtpForm` usa `useRequestOtp`.
3. `useRequestOtp` ejecuta `authService.requestOtp`.
4. Exito: navegar a `/verify-otp` con email.

### Consulta de servicios
1. `app/(public)/services/page.tsx` usa `useServices`.
2. `useServices` llama `servicesService.list` con Query.
3. `ServiceList` renderiza cards y estados loading/error/empty.

### Consulta de disponibilidad
1. `app/(client)/booking/[serviceId]/page.tsx` usa `useServiceSlots`.
2. Hook consulta `availabilityService.listSlots(serviceId, date)`.
3. `SlotPicker` muestra bloques `available` y bloquea `blocked/cancelled`.

### Reserva de cita
1. Usuario selecciona slot en `SlotPicker`.
2. `useBookAppointment` ejecuta mutacion `appointmentsService.book`.
3. On success: invalidar queries de slots y citas, mostrar confirmacion.

### Confirmacion/cancelacion desde admin
1. `app/(admin)/admin/appointments/page.tsx` usa `useAdminAppointments`.
2. Tabla ejecuta acciones confirmar/cancelar.
3. Mutacion en `adminService.confirmAppointment/cancelAppointment`.
4. Invalidacion de lista admin y detalle de cita.

## 11. Formularios y validacion
Recomendacion:
- Si usar React Hook Form + Zod.

Por que si:
- Reduce rerenders y boilerplate.
- Mantiene reglas en schemas reusables por formulario.
- Facilita errores por campo y validacion de tipos con TypeScript.

Aplicacion en MVP:
- Login OTP: `request-otp.schema.ts`, `verify-otp.schema.ts`.
- Crear servicio: schema con nombre, duracion y estado.
- Configurar horarios: schema para reglas por dia/franja.
- Reserva de cita: schema simple con `serviceId` y `timeBlockId`.

Regla anti-duplicacion:
- Un schema por formulario.
- No repetir validacion en componente y hook; el componente valida, el hook solo ejecuta caso de uso.

## 12. Patrones recomendados
Patrones que si:
- Feature-based structure: claridad de ownership y escalado controlado.
- Service layer: consistencia de API y manejo de errores.
- Custom hooks de feature: concentran logica de pantalla.
- Container/presentational ligero: util para separar logica de render.

Patrones que no (por ahora):
- Global store grande (Redux/Zustand): costo mayor que beneficio en MVP.
- Atomic design completo: sobreestructura para alcance actual.
- View models formales por pantalla: puede esperar hasta que haya complejidad real.

## 13. Buenas practicas clave
- App Router: Server Components por defecto, Client Components solo para interaccion.
- Tailwind: tokens en `styles/tokens.css` y componentes UI consistentes.
- Auth OTP + JWT: cookie httpOnly, sin token en localStorage.
- API REST: cliente HTTP unico, `ApiError` unico, invalidaciones controladas.
- Modularidad: feature con boundaries claros y naming consistente.
- Evitar duplicaciones: no `fetch` en paginas, no hooks wrappers vacios, no schemas repetidos.
- DX: tipos compartidos por dominio, convencion de archivos estable, lints desde inicio.

## 14. Riesgos y errores comunes
- Repetir llamadas API en pagina, hook y componente al mismo tiempo.
- Crear hooks que solo delegan una linea y no agregan valor.
- Mezclar permisos/roles de auth en componentes UI sueltos.
- Sobreusar Client Components y perder ventajas de App Router.
- Duplicar validaciones entre frontend y frontend (schema + regex suelto).
- Crear demasiadas carpetas vacias para "futuro".
- Modelar estado global demasiado pronto.

## 15. Propuesta final recomendada
Implementar un frontend modular por features en Next.js App Router, con:
- rutas claras por segmento `(public)`, `(client)`, `(admin)`
- auth OTP+JWT via cookies httpOnly y middleware de proteccion
- consumo API consistente en service layer centralizado
- estado remoto con TanStack Query y estado UI local en componentes
- formularios con React Hook Form + Zod

Esta propuesta prioriza entrega rapida, mantenibilidad y coherencia, sin patrones inflados.

## Cierre solicitado
1. arquitectura frontend final recomendada
	 - Next.js App Router + Tailwind + TypeScript, arquitectura por features, service layer unico, auth por cookie httpOnly, Query para datos remotos.
2. estructura de carpetas frontend
	 - Definida en la seccion 4, con `src/app`, `src/components`, `src/features`, `src/services`, `src/lib`, `src/types`, `src/styles`.
3. decisiones clave de auth/session
	 - OTP request/verify, JWT en cookie httpOnly, middleware para rutas protegidas, control de rol admin/cliente, logout server-side.
4. lista de cosas que quedan fuera del MVP
	 - Refresh token avanzado y rotacion compleja.
	 - Multi-tenant (solo un negocio).
	 - Notificaciones push/sms.
	 - Auditoria avanzada y panel analitico.
	 - i18n completo.
	 - Offline mode y sincronizacion avanzada.
