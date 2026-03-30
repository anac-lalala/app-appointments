# DevOps MVP - Gestion de Citas

Este documento define una estrategia simple de infraestructura y operacion para el MVP.

Objetivo:
- desarrollo local sin friccion
- despliegue confiable sin complejidad enterprise
- observabilidad basica util
- operacion mantenible por equipo pequeno

## 1. Estrategia general

Enfoque recomendado:
- un solo repositorio
- monolito backend + frontend separados por servicio
- Docker Compose para desarrollo
- despliegue en un solo host (VM o servicio de contenedores simple)
- base de datos PostgreSQL gestionada por compose en dev y gestionada/estable en prod

Principios de operacion:
- simplicidad primero
- reproducibilidad por entorno
- cambios pequenos y reversibles
- logs y healthchecks desde el dia 1

## 2. Docker en desarrollo

Servicios locales:
- `frontend` (Next.js con hot reload)
- `backend` (FastAPI con reload)
- `db` (PostgreSQL)

Recomendaciones:
- montar volumen de codigo en `frontend` y `backend`
- volumen persistente para datos de `db`
- archivo `.env.dev` para variables no secretas locales
- archivo `.env.dev.local` fuera de git para secretos locales

Hot reload:
- frontend: `next dev`
- backend: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

Puertos sugeridos:
- frontend: `3000`
- backend: `8000`
- db: `5432` (solo local)

## 3. Docker en producción

Sin Kubernetes:
- construir imagenes versionadas de `frontend` y `backend`
- ejecutar con compose en host Linux estable
- reverse proxy (Nginx o Caddy) delante de frontend/backend
- TLS en reverse proxy

Topologia simple:
- `proxy` publica 80/443
- `frontend` interno
- `backend` interno
- `db` no expuesta a internet

Buenas practicas minimas:
- contenedores como usuario no-root
- politicas de restart (`unless-stopped`)
- imagenes ligeras y actualizadas
- backups de PostgreSQL programados

## 4. Compose recomendado

Servicios:
- `frontend`
- `backend`
- `db`
- `proxy` (solo prod)
- `migrate` (job/one-shot para Alembic, preferido en deploy)

Redes:
- `public` (proxy)
- `private` (backend + db + frontend interno)

Volumenes:
- `postgres_data`
- opcional `backend_logs` si no centralizas stdout

Perfiles compose:
- `dev`: frontend/backend/db con reload
- `prod`: proxy/frontend/backend/db sin mounts de codigo

## 5. Variables de entorno

Organizacion recomendada:
- `.env.example` con claves y placeholders
- `.env.dev` para defaults de desarrollo
- `.env.prod` gestionado en servidor/secret manager

Variables clave backend:
- `APP_ENV`
- `APP_DEBUG`
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `JWT_ACCESS_TOKEN_EXPIRES_MINUTES`
- `OTP_TTL_SECONDS`
- `OTP_MAX_ATTEMPTS`
- `OTP_REQUEST_RATE_LIMIT_PER_EMAIL`
- `OTP_REQUEST_RATE_LIMIT_PER_IP`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `SMTP_FROM_EMAIL`
- `CORS_ALLOWED_ORIGINS`

Variables clave frontend:
- `NEXT_PUBLIC_API_BASE_URL`
- `NEXT_PUBLIC_APP_ENV`

Reglas:
- nunca commitear secretos reales
- rotar `JWT_SECRET_KEY` si hay incidente
- separar valores por entorno

## 6. Logs y observabilidad basica

Que si tener:
- logs estructurados JSON en backend
- access logs de proxy y backend
- `request_id` por request
- metricas simples:
  - latencia p95
  - tasa de error 5xx
  - conteo de 401/403/429
  - tasa de `request OTP`

Que no complicar ahora:
- trazabilidad distribuida completa
- stack de observabilidad enterprise

Alertas minimas:
- caida de healthcheck backend
- pico anormal de 5xx
- pico de 429 en OTP

## 7. Health checks

Endpoints recomendados:
- `GET /health/live` (proceso vivo)
- `GET /health/ready` (dependencias listas: DB y config critica)

Chequeos por servicio:
- frontend: respuesta HTTP 200 en `/`
- backend: `health/ready`
- db: `pg_isready`

Uso:
- compose `healthcheck` en cada servicio
- proxy solo enruta a servicios `healthy`

## 8. Migraciones (Alembic)

Desarrollo:
- generar migracion por cambio de modelo
- revisar migracion antes de aplicar
- aplicar con `alembic upgrade head`

Produccion:
- ejecutar migraciones como paso previo al rollout
- estrategia segura:
  1. backup rapido DB
  2. `alembic upgrade head`
  3. levantar nueva version

Reglas MVP:
- evitar migraciones destructivas sin plan
- no editar migraciones ya aplicadas en prod

## 9. CI/CD minimo

Pipeline recomendado por push/PR:
1. lint frontend/backend
2. tests backend criticos
3. build imagen backend
4. build imagen frontend

Pipeline recomendado para main:
1. repetir checks
2. publicar imagenes versionadas
3. deploy simple por SSH al servidor
4. correr migraciones
5. `docker compose up -d`
6. smoke test (`/health/ready`)

Sin complejidad innecesaria:
- sin entornos efimeros por PR
- sin despliegue canary inicial

## 10. Riesgos operativos y errores comunes

- mezclar configuracion dev/prod en un solo archivo
- no fijar versiones de imagen
- exponer PostgreSQL publicamente
- no tener backup verificado
- no monitorear tasa de errores OTP
- migraciones aplicadas manualmente sin checklist
- no definir politica de restart

Mitigacion simple:
- checklist de release
- backups diarios + prueba de restauracion periodica
- healthchecks obligatorios en despliegue

## 11. Propuesta final

Operacion recomendada para este MVP:
- desarrollo con Docker Compose (`frontend + backend + db`) y hot reload
- produccion con Compose en host Linux y reverse proxy TLS
- migraciones Alembic como paso estandar de despliegue
- logs estructurados + healthchecks + alertas minimas
- CI/CD corto enfocado en calidad basica y deploy repetible

Con esto se obtiene un setup suficiente para operar confiablemente sin Kubernetes ni infraestructura compleja.

## Cierre solicitado

1. Setup docker recomendado

- Dev: `frontend + backend + db` con mounts y reload
- Prod: `proxy + frontend + backend + db` con imagenes versionadas y red privada
- Healthchecks en todos los servicios

2. Estrategia de despliegue simple

- build y push de imagenes
- deploy por SSH
- migracion Alembic previa
- `docker compose up -d`
- smoke test de readiness

3. Variables clave

- Backend: `DATABASE_URL`, `JWT_SECRET_KEY`, `OTP_*`, `SMTP_*`, `CORS_ALLOWED_ORIGINS`
- Frontend: `NEXT_PUBLIC_API_BASE_URL`
- Segmentacion por entorno con `.env.example`, `.env.dev`, `.env.prod`

4. Pipeline minimo recomendado

- PR: lint + test + build
- Main: build + publish + deploy + migrate + smoke test
