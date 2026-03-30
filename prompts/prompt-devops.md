# DevOps Prompt

Actúa como DevOps engineer pragmático y ayúdame a definir una estrategia simple de infraestructura y operación para un MVP de gestión de citas.

Quiero una propuesta:
- simple
- mantenible
- dockerizada
- útil para desarrollo y producción
- sin Kubernetes
- sin complejidad innecesaria

---

## Contexto del proyecto

Stack:
- Next.js frontend
- FastAPI backend
- PostgreSQL
- OTP por correo
- JWT
- Docker para desarrollo y producción

Objetivo:
- poder desarrollar localmente sin dolor
- desplegar el MVP de forma confiable
- tener observabilidad básica
- mantener simple la operación

---

## Lo que quiero que produzcas

### 1. Estrategia general
Cómo organizarías la operación del proyecto.

### 2. Docker en desarrollo
Cómo recomiendas correr localmente:
- frontend
- backend
- db
- variables de entorno
- volúmenes
- hot reload si aplica

### 3. Docker en producción
Cómo desplegarías este MVP en producción sin sobrecomplicar.

### 4. docker-compose / compose
Qué servicios tendría y cómo organizarlos.

### 5. Variables de entorno
Qué variables son necesarias y cómo organizarlas.

### 6. Logs y observabilidad básica
Qué logs sí necesitas y qué no.

### 7. Health checks
Qué endpoints o chequeos pondrías.

### 8. Migraciones
Cómo manejar Alembic en dev y prod.

### 9. CI/CD mínimo
Qué pipeline básico sí tendría sentido.

### 10. Riesgos operativos
Qué errores comunes evitar.

### 11. Propuesta final
Cierra con una propuesta concreta y simple para operar este MVP.

---

## Restricciones

- no Kubernetes
- no terraform obligatorio
- no pipelines complejos
- no infraestructura enterprise
- sí docker simple y útil

---

## Resultado esperado

La respuesta debe terminar con:
1. setup docker recomendado
2. estrategia de despliegue simple
3. variables clave
4. pipeline mínimo recomendado