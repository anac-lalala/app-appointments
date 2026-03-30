# Documentacion de Citas App

Este README es el punto de entrada de la documentacion del MVP.
Sirve para saber que cubre cada documento, por donde leer primero y como mantener coherencia entre archivos.

## 1. Resumen del proyecto

- Producto: MVP de gestion de citas para un solo negocio.
- Arquitectura: monolito modular.
- Frontend: Next.js App Router + TypeScript + Tailwind.
- Backend: FastAPI async + SQLAlchemy async + Alembic.
- Base de datos: PostgreSQL.
- Auth: OTP por correo + JWT.
- Infra: Docker Compose para desarrollo y despliegue simple con contenedores.

## 2. Limites del alcance

Dentro del MVP:
- Login OTP para cliente y admin.
- Gestion de servicios por admin.
- Reglas de disponibilidad y bloques horarios.
- Reserva con proteccion de concurrencia.
- Operacion admin de citas (confirmar/cancelar).
- Endurecimiento y salida a produccion.

Fuera del MVP:
- Multi-negocio o multi-tenant.
- RBAC avanzado.
- Pagos y facturacion.
- Integraciones externas complejas.
- App movil nativa.

## 3. Mapa de documentacion

- [docs/architecture.md](docs/architecture.md)
  - Arquitectura de alto nivel, limites por modulo y capas.
- [docs/backend.md](docs/backend.md)
  - Convenciones de implementacion backend y responsabilidades por modulo.
- [docs/frontend.md](docs/frontend.md)
  - Estructura frontend, rutas y patrones de integracion.
- [docs/api.md](docs/api.md)
  - Contratos API, endpoints y formato de respuestas/errores.
- [docs/database.md](docs/database.md)
  - Esquema relacional, constraints y estrategia de concurrencia.
- [docs/security.md](docs/security.md)
  - Controles de seguridad y guardrails de auth.
- [docs/devops.md](docs/devops.md)
  - Entornos, despliegue y base operativa.
- [docs/implementacion.md](docs/implementacion.md)
  - Roadmap por fases 0-6, entregables y criterios de cierre.
- [docs/quailty.md](docs/quailty.md)
  - Estandares de calidad y criterios de testing/release.

## 4. Fuente de verdad por tema

- Contratos y codigos API: [docs/api.md](docs/api.md)
- Controles de seguridad y auth: [docs/security.md](docs/security.md)
- Constraints de DB y locks: [docs/database.md](docs/database.md)
- Orden de fases y entregables: [docs/implementacion.md](docs/implementacion.md)
- Limites de arquitectura y capas: [docs/architecture.md](docs/architecture.md)

Regla:
- No redefinir el mismo tema en varios archivos.
- Enlazar a la fuente de verdad en lugar de duplicar detalle.

## 5. Invariantes transversales

Estos valores deben mantenerse identicos en toda la documentacion:

- OTP TTL: 5 minutos.
- Max intentos OTP por challenge: 5.
- Cooldown OTP por email: 60 segundos.
- Rate limit OTP por IP: 10 requests por 15 minutos.
- Rate limit OTP por email: 5 requests por hora.
- JWT access token TTL: 30 minutos.
- Storage de auth en frontend: cookie HttpOnly + Secure + SameSite=Lax.

Si cambia un valor, actualizar todas las secciones afectadas en el mismo cambio.

## 6. Orden de lectura recomendado

Para PM o stakeholders de producto:
1. [docs/architecture.md](docs/architecture.md)
2. [docs/implementacion.md](docs/implementacion.md)
3. [docs/api.md](docs/api.md)

Para backend:
1. [docs/architecture.md](docs/architecture.md)
2. [docs/backend.md](docs/backend.md)
3. [docs/database.md](docs/database.md)
4. [docs/api.md](docs/api.md)
5. [docs/security.md](docs/security.md)
6. [docs/implementacion.md](docs/implementacion.md)

Para frontend:
1. [docs/architecture.md](docs/architecture.md)
2. [docs/frontend.md](docs/frontend.md)
3. [docs/api.md](docs/api.md)
4. [docs/security.md](docs/security.md)
5. [docs/implementacion.md](docs/implementacion.md)

Para DevOps y release:
1. [docs/devops.md](docs/devops.md)
2. [docs/security.md](docs/security.md)
3. [docs/implementacion.md](docs/implementacion.md)

Para onboarding:
1. [README.md](README.md)
2. [docs/architecture.md](docs/architecture.md)
3. [docs/implementacion.md](docs/implementacion.md)
4. Track por rol.

## 7. Politica de actualizacion

Cuando cambies documentacion:
1. Actualizar primero el archivo fuente de verdad.
2. Actualizar archivos relacionados solo con referencias e impacto.
3. Mantener fases alineadas con [docs/implementacion.md](docs/implementacion.md).
4. Mantener valores de auth/seguridad alineados con [docs/security.md](docs/security.md) y [docs/api.md](docs/api.md).
5. Evitar secciones nuevas que dupliquen ownership existente.

## 8. Checklist minimo por feature

Antes de cerrar una feature:
- Cambios API reflejados en [docs/api.md](docs/api.md).
- Impacto de seguridad reflejado en [docs/security.md](docs/security.md).
- Impacto de DB reflejado en [docs/database.md](docs/database.md).
- Impacto por fases reflejado en [docs/implementacion.md](docs/implementacion.md).
- Cambios de limites de arquitectura reflejados en [docs/architecture.md](docs/architecture.md).

Esto mantiene la documentacion coherente, facil de navegar y util para personas y flujos de IA.
