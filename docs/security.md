# Seguridad MVP - Gestion de Citas

Este documento define una estrategia minima razonable de seguridad para el MVP.

Objetivo:
- practica
- enfocada en riesgos reales
- coherente con OTP + JWT
- mantenible por equipo pequeno
- sin sobreingenieria

## 1. Principios de seguridad para el MVP

Nivel objetivo para esta etapa:
- proteger autenticacion y autorizacion de forma robusta
- reducir abuso de endpoints criticos (OTP, login, admin)
- minimizar exposicion de datos personales
- mantener controles simples de operar

Regla de oro:
- seguridad suficiente para riesgos actuales, no arquitectura enterprise adelantada

## 2. Riesgos principales

Riesgos mas importantes del sistema:
- abuso masivo de `request OTP` (spam, brute force, costo de correo)
- reutilizacion o adivinacion de OTP
- JWT robado o mal almacenado en frontend
- acceso indebido a endpoints admin por mala autorizacion
- doble reserva o manipulación de estados de cita
- filtracion de datos personales en logs o errores
- secretos expuestos en repositorio o imagen Docker

Prioridad real:
1. auth OTP
2. proteccion JWT y sesiones
3. autorizacion de rutas admin
4. abuso de endpoints publicos
5. higiene de datos/logs

## 3. OTP por correo

Controles recomendados:
- longitud: 6 digitos numericos
- expiracion: 5 minutos
- single-use: invalido tras primer uso exitoso
- intentos maximos por challenge: 5
- cooldown por email: 60 segundos entre requests
- rate limit por IP: ejemplo 10 requests OTP / 15 min
- rate limit por email: ejemplo 5 requests OTP / hora

Almacenamiento:
- guardar solo `otp_hash` (hash con salt)
- nunca guardar OTP plano
- registrar `expires_at`, `attempts`, `used_at`, `last_attempt_at`

Invalidacion:
- al emitir nuevo OTP para mismo email, invalidar challenges activos previos
- al llegar a intentos maximos, bloquear challenge
- challenge expirado no puede verificarse

Respuesta segura:
- en `request OTP` usar mensaje generico (no revelar si email existe)

## 4. JWT

Recomendacion MVP:
- usar access token corto
- sin refresh token en primera version (para mantener simple)

Emision:
- algoritmo recomendado: HS256 con clave robusta y rotable
- `exp`: 15-30 minutos

Claims minimos:
- `sub` (user_id)
- `role` (`client` o `admin`)
- `iat`
- `exp`
- opcional: `jti` para trazabilidad

Revocacion MVP:
- estrategia simple: no lista global de revocacion al inicio
- revocar de facto con expiracion corta + re-login OTP
- si ocurre incidente, rotar secret JWT para invalidar tokens activos

## 5. Frontend auth security

Decision recomendada:
- guardar JWT en cookie `HttpOnly`, `Secure`, `SameSite=Lax`
- evitar `localStorage` para tokens

Comparativa breve:
- cookie HttpOnly:
  - pro: reduce riesgo de robo por XSS
  - contra: requiere cuidar CSRF
- localStorage:
  - pro: simple de implementar
  - contra: alto riesgo ante XSS
- memoria (in-memory):
  - pro: reduce persistencia
  - contra: mala UX por perdida de sesion en refresh

Proteccion de rutas:
- middleware en Next.js para rutas privadas
- validacion de rol tambien en backend (nunca confiar solo en frontend)

CSRF:
- si auth va en cookie, usar minimo:
  - `SameSite=Lax`
  - token CSRF en endpoints mutables si hay formularios cross-site posibles

## 6. Seguridad de endpoints

Reglas generales:
- autenticacion obligatoria para endpoints privados
- autorizacion por rol y recurso en backend
- validacion estricta de input (Pydantic)
- respuestas de error sin filtrar detalles sensibles

Rutas cliente:
- requieren JWT valido
- solo permiten operar sobre recursos del cliente autenticado

Rutas admin:
- requieren JWT valido con `role=admin`
- doble chequeo de permisos en cada caso de uso (no solo en router)

Controles anti abuso:
- rate limiting en:
  - OTP request
  - OTP verify
  - endpoints de login
- bloqueo temporal incremental ante fallos repetidos

## 7. Seguridad de datos

Datos personales:
- almacenar solo datos necesarios para operar el MVP
- cifrado en transito obligatorio (HTTPS)
- evitar incluir PII en respuestas innecesarias

Logs:
- no loggear OTP, JWT completos, headers `Authorization`, ni cookies
- mascar emails y telefonos en logs cuando sea posible
- agregar `request_id` para trazabilidad

Tokens y OTP:
- OTP solo hasheado
- JWT secret fuera de codigo fuente
- rotacion de secretos en caso de incidente

Variables de entorno:
- usar `.env` solo local
- nunca commitear `.env` real
- separar secretos por entorno (dev/stage/prod)

## 8. Seguridad de infraestructura (Docker y despliegue)

Minimos recomendados:
- contenedores con usuario no-root
- imagenes base actualizadas y ligeras
- solo puertos necesarios expuestos
- red interna para DB (no publica)
- backups basicos de PostgreSQL
- healthchecks en servicios
- TLS terminado en reverse proxy o plataforma

Configuracion:
- desactivar `debug` en produccion
- CORS restringido a dominios frontend conocidos
- headers de seguridad basicos:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Referrer-Policy: strict-origin-when-cross-origin`

Monitoreo minimo:
- alertas simples por tasa alta de errores 401/403/429
- alerta por pico inusual de `request OTP`

## 9. Que no complicar todavia

No incluir aun (salvo requisito fuerte):
- MFA adicional al OTP por email
- sistema avanzado de revocacion distribuida de JWT
- WAF complejo con reglas personalizadas extensas
- SIEM enterprise
- cifrado campo a campo con KMS dedicado
- politica RBAC granular avanzada

Razon:
- no aporta suficiente valor inmediato vs costo operativo para un MVP pequeno

## 10. Propuesta final

Estrategia concreta de seguridad minima razonable:
- OTP robusto: expiracion corta, single-use, hash, limites por IP/email e intentos maximos
- JWT simple y seguro: access token corto, claims minimos, secret gestionado por entorno
- frontend con cookie HttpOnly/Secure/SameSite, sin localStorage para tokens
- backend con autorizacion estricta por rol y recurso en cada endpoint/caso de uso
- higiene de datos: no filtrar secretos en logs, CORS restringido, HTTPS obligatorio
- Docker/deploy con controles basicos de hardening y exposicion minima

## Cierre solicitado

1. Controles minimos obligatorios
- rate limiting en OTP request/verify
- OTP hasheado, expiracion 5 min, single-use, max 5 intentos
- JWT con expiracion corta (15-30 min)
- rutas admin protegidas por rol en backend
- CORS restringido + HTTPS en produccion
- no loggear OTP ni tokens

2. Recomendaciones OTP + JWT
- OTP: 6 digitos, hash, invalidacion de challenges previos, cooldown por email
- JWT: claims minimos (`sub`, `role`, `iat`, `exp`), sin refresh token inicial
- estrategia de incidente: rotar secret JWT

3. Decisiones frontend/backend de auth
- frontend: cookie HttpOnly/Secure/SameSite=Lax
- backend: validacion de token + validacion de rol/recurso en cada accion
- evitar localStorage para credenciales

4. Riesgos que quedan aceptados en el MVP
- sin revocacion fina por token (compensado con expiracion corta)
- sin analitica antifraude avanzada
- sin RBAC granular enterprise
- defensa anti abuso basica, no deteccion inteligente avanzada
