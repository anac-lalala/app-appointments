# Security Prompt

Actúa como arquitecto de seguridad aplicado a producto web y ayúdame a definir una estrategia de seguridad mínima razonable para un MVP de gestión de citas.

Quiero una propuesta:
- práctica
- enfocada en riesgos reales
- coherente con OTP + JWT
- sin paranoia excesiva
- sin sobreingeniería

---

## Contexto del proyecto

MVP de gestión de citas con:
- Next.js frontend
- FastAPI backend
- PostgreSQL
- auth por OTP por correo
- JWT
- sin contraseñas
- envío real de correos OTP
- Docker

---

## Riesgos más sensibles del proyecto

- login OTP
- emisión y almacenamiento de JWT
- reserva de citas
- protección de endpoints admin
- abuso de request OTP
- expiración y reutilización de códigos
- seguridad básica de datos personales

---

## Lo que quiero que produzcas

### 1. Principios de seguridad para el MVP
Qué nivel de seguridad es razonable para esta etapa.

### 2. Riesgos principales
Cuáles son los riesgos más importantes en este sistema.

### 3. OTP por correo
Cómo implementar OTP de forma segura:
- expiración
- un solo uso
- rate limiting
- intentos máximos
- almacenamiento del código
- invalidación

### 4. JWT
Cómo manejar JWT de forma segura:
- emisión
- expiración
- claims mínimos
- refresh token o no
- revocación o estrategia simple para MVP

### 5. Frontend auth security
Qué recomiendas para frontend:
- cookies httpOnly
- localStorage
- memoria
- protección de rutas
- riesgos de cada opción

### 6. Seguridad de endpoints
Cómo proteger:
- rutas de cliente
- rutas de admin
- validaciones de autorización

### 7. Seguridad de datos
Qué medidas mínimas tomar con:
- datos personales
- logs
- tokens
- OTP
- variables de entorno

### 8. Seguridad de infraestructura
Qué mínimos de seguridad necesitas en Docker, configuración y despliegue.

### 9. Qué no complicar todavía
Qué prácticas de seguridad no metería aún si no aportan suficiente valor al MVP.

### 10. Propuesta final
Cierra con una estrategia concreta de seguridad mínima razonable.

---

## Restricciones

- no paranoia enterprise
- no controles innecesarios
- no soluciones complejas que no pueda mantener un equipo pequeño
- sí foco en auth y abuso de endpoints

---

## Resultado esperado

La respuesta debe terminar con:
1. controles mínimos obligatorios
2. recomendaciones OTP + JWT
3. decisiones frontend/backend de auth
4. riesgos que quedan aceptados en el MVP