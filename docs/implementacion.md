# Plan de Implementacion MVP - Gestion de Citas

Este documento sirve para dos objetivos:

1. empezar el proyecto sin bloqueos tecnicos
2. entender que se construye primero, por que y como validar avance

La idea es evitar un roadmap abstracto. Cada fase tiene un resultado visible y un criterio claro de cierre.

## 1. Entender el sistema: que es y por que esta diseno

### Que sistema estamos construyendo

MVP para un solo negocio de citas con dos actores:

- administrador: crea servicios, define disponibilidad, confirma/cancela citas
- cliente: inicia sesion por OTP, ve servicios y horarios, reserva cita

### Por que esta arquitectura

Se usa monolito modular porque:

- permite entregar rapido sin complejidad de microservicios
- mantiene limites claros entre dominios (auth, services, availability, appointments)
- facilita evolucion futura sin rehacer todo

Stack base:

- frontend: Next.js App Router + TypeScript + Tailwind
- backend: FastAPI async + SQLAlchemy async + Alembic
- base de datos: PostgreSQL
- auth: OTP por email + JWT
- infraestructura: Docker Compose para desarrollo

## 2. Requisitos previos

### Opcion A - Con Docker (recomendada)

- Docker instalado y corriendo
- Docker Compose v2
- Git

### Opcion B - Sin Docker

- Python 3.11+
- PostgreSQL 14+
- Node.js 18+
- npm o pnpm
- Git

Verificar herramientas:

```bash
docker --version
docker compose version
python --version
node --version
npm --version
```

## 3. Arranque del proyecto

### Opcion A - Arranque con Docker (recomendada)

Paso 1 - Crear archivo de entorno:

```bash
cp .env.example .env
```

Si no existe `.env.example`, crear `.env` manualmente con este minimo:

```env
# Database
POSTGRES_DB=citas
POSTGRES_USER=citas
POSTGRES_PASSWORD=devpass
DATABASE_URL=postgresql+asyncpg://citas:devpass@db:5432/citas

# JWT
JWT_SECRET_KEY=change-this-in-prod
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=30

# OTP
OTP_TTL_SECONDS=300
OTP_MAX_ATTEMPTS=5
OTP_REQUEST_RATE_LIMIT_PER_IP=10/15m
OTP_REQUEST_RATE_LIMIT_PER_EMAIL=5/h

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=app-password
SMTP_FROM_EMAIL=your-email@example.com

# CORS
CORS_ALLOWED_ORIGINS=["http://localhost:3000"]
```

Paso 2 - Levantar servicios:

```bash
docker compose up -d
```

Paso 3 - Ejecutar migraciones:

```bash
docker compose exec backend alembic upgrade head
```

Paso 4 - Verificar salud basica:

```bash
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready
```

### Opcion B - Arranque sin Docker

Paso 1 - Backend:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Paso 2 - Frontend:

```bash
npm install
npm run dev
```

Paso 3 - Validar:

- frontend en `http://localhost:3000`
- backend en `http://localhost:8000`

## 4. Invariantes tecnicos (no negociables)

Estos valores deben ser iguales en codigo, API, seguridad y docs:

- OTP TTL: 5 minutos
- OTP max intentos por challenge: 5
- OTP cooldown por email: 60 segundos
- OTP rate limit por IP: 10 requests por 15 minutos
- OTP rate limit por email: 5 requests por hora
- JWT access token: 30 minutos
- storage de auth frontend: cookie HttpOnly + Secure + SameSite=Lax

## 5. Estrategia de implementacion

Se construye por vertical slices sobre una base corta por capas.

Por que:

- muestra valor funcional pronto
- reduce bloqueos entre frontend y backend
- detecta problemas reales (auth, concurrencia, estados) antes

Regla de coordinacion por slice:

1. backend congela contrato minimo
2. frontend implementa contra contrato (mock corto)
3. integracion y prueba E2E del slice

## 6. Roadmap por fases (que se hace y por que)

### Fase 0.0 - Scaffold del repositorio

Que se hace:

- crear estructura base de directorios del backend y frontend
- agregar archivos mínimos para que el stack sea reconocido (package.json, pyproject.toml, main.py, etc.)
- configurar docker-compose.yml con servicios básicos (postgres, backend, frontend)
- crear .env.example con variables mínimas

Por que se hace:

- establece la forma del proyecto antes de levantar contenedores o instalar dependencias
- clarifica dónde va cada cosa siguiendo la arquitectura modular

Entregable visible:

- estructura de directorios lista y reconocible
- docker-compose.yml operativo (aunque servicios backend/frontend aún estén vacíos)
- .env.example con variables de control

Criterio de cierre:

- `docker compose up` puede levantar postgres + nginx/proxy sin errores
- directorios `backend/app/main.py` y `frontend/package.json` existen y son válidos
- `docker compose ps` muestra 3 servicios "up"

Checklist de scaffold:

**Backend**:
- [ ] `backend/pyproject.toml` con dependencias base (fastapi, sqlalchemy, alembic, etc)
- [ ] `backend/alembic.ini` con config de migraciones
- [ ] `backend/migrations/env.py` y `versions/` vacío
- [ ] `backend/app/main.py` con aplicación vacía (uvicorn app)
- [ ] `backend/app/core/config.py` con Settings
- [ ] `backend/requirements.txt` generado desde pyproject.toml

**Frontend**:
- [ ] `frontend/package.json` con next, tailwind, typescript
- [ ] `frontend/next.config.ts` con config base
- [ ] `frontend/tsconfig.json`
- [ ] `frontend/pages/index.tsx` o `app/page.tsx` (según App Router)

**Raíz del proyecto**:
- [ ] `.env.example` poblado con todas las variables de control
- [ ] `docker-compose.yml` con servicios postgres, backend, frontend
- [ ] `.gitignore` actualizado
- [ ] `README.md` con instrucciones de arranque

### Fase 0 - Setup base

Que se hace:

- estructura de proyecto
- docker compose
- conexion DB y migraciones
- healthchecks

Por que se hace:

- sin entorno reproducible todo lo demas falla o se retrasa

Entregable visible:

- proyecto levanta y responde healthchecks

Criterio de cierre:

- stack local estable y migracion inicial aplicada

### Fase 1 - Autenticacion OTP

Que se hace:

- request OTP y verify OTP
- persistencia `otp_challenges` con hash, expiracion, intentos y single-use
- emision JWT
- proteccion inicial de rutas

Por que se hace:

- toda operacion del sistema depende de identidad y sesion valida

Entregable visible:

- cliente y admin inician sesion sin password

Criterio de cierre:

- OTP expira, no se reutiliza y JWT protege rutas privadas

### Fase 2 - Servicios

Que se hace:

- CRUD admin de servicios
- listado de servicios activos para cliente

Por que se hace:

- sin servicios no existe disponibilidad ni reserva real

Entregable visible:

- catalogo de servicios activo en panel admin y vista cliente

Criterio de cierre:

- solo admin modifica, cliente solo consulta activos

### Fase 3 - Disponibilidad

Que se hace:

- reglas semanales por servicio
- generacion de bloques por rango
- consulta de bloques disponibles

Por que se hace:

- el negocio necesita transformar reglas en horarios reservables reales

Entregable visible:

- cliente visualiza agenda disponible por servicio

Criterio de cierre:

- no hay superposicion y se respeta `duration_minutes`

### Fase 4 - Reservas

Que se hace:

- reserva atomica de cita con transaccion y lock
- snapshots de cliente en `appointments`
- cambio de estado del bloque

Por que se hace:

- la reserva es el flujo core del negocio y requiere integridad fuerte

Entregable visible:

- cliente reserva y el bloque queda ocupado

Criterio de cierre:

- no existe doble reserva bajo concurrencia basica

### Fase 5 - Panel admin de citas

Que se hace:

- listado de citas por estado/fecha
- confirmar/cancelar cita
- validacion de transiciones

Por que se hace:

- el negocio necesita cerrar el ciclo operativo de atencion

Entregable visible:

- admin gestiona citas pendientes

Criterio de cierre:

- transiciones validas y auditables (`pending_review -> confirmed/cancelled`)

### Fase 6 - Endurecimiento

Que se hace:

- formato uniforme de errores API
- logs estructurados con request_id
- pruebas criticas
- hardening basico (CORS, headers, limites OTP)
- checklist de deploy

Por que se hace:

- salir a produccion sin esta fase aumenta mucho el riesgo operativo

Entregable visible:

- MVP desplegable con riesgo controlado

Criterio de cierre:

- smoke tests y pruebas criticas en verde

## 7. Primer plan de ejecucion (primeras 2 semanas)

Semana 1:

1. cerrar fase 0
2. iniciar fase 1 (request OTP)
3. completar verify OTP + JWT

Semana 2:

1. cerrar fase 1
2. cerrar fase 2
3. iniciar fase 3 (reglas y primer endpoint de bloques)

Meta al final de semana 2:

- login OTP funcionando
- servicios administrables
- primer corte de disponibilidad consultable

## 8. Checklist para saber si puedes comenzar hoy

- tienes herramientas instaladas (docker o python/node/postgres)
- tienes `.env` con valores minimos
- puedes levantar backend, frontend y DB
- puedes correr migraciones sin error
- healthchecks responden
- tienes claro el orden: fase 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6

Si todos los puntos son verdaderos, ya puedes iniciar implementacion.