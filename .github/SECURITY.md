# Política de Seguridad de TREMEND Toolkit

La seguridad de nuestros usuarios es la máxima prioridad. Al ser una suite de herramientas con privilegios de administrador y capacidades forenses, nos tomamos muy en serio cualquier posible vulnerabilidad en nuestro código.

## Versiones Soportadas

Actualmente, solo las versiones más recientes reciben parches de seguridad y soporte activo:

| Versión | Estado de Soporte |
| ------- | ----------------- |
| 3.2.x   | :white_check_mark: Soportada |
| 3.1.x   | :white_check_mark: Solo parches críticos |
| < 3.0   | :x: Fin de vida útil (No soportada) |

## Cómo reportar una vulnerabilidad

Si eres un investigador de ciberseguridad, un desarrollador o un usuario que ha encontrado una vulnerabilidad de seguridad en TREMEND Toolkit, por favor **NO abras un "Issue" público** en GitHub. Revelar un fallo públicamente antes de que exista un parche podría poner en riesgo a otros usuarios.

En su lugar, te pedimos que reportes el problema de forma privada:

1. Envía un correo electrónico directamente al desarrollador principal a: tremend67@gmail.com
2. En el asunto del correo, escribe: `[REPORTE DE SEGURIDAD TREMEND] - Breve descripción del fallo`.

### ¿Qué debe incluir tu reporte?
Para ayudarnos a solucionar el problema lo más rápido posible, por favor incluye:
* El tipo de vulnerabilidad (Ej: Inyección de comandos, desbordamiento de búfer, escalada de privilegios).
* Pasos detallados para reproducir el fallo.
* Si es posible, capturas de pantalla o un pequeño fragmento de código demostrativo (PoC - Proof of Concept).
* El impacto potencial (qué podría hacer un atacante si explota este fallo).

## Nuestro compromiso
* Acusaremos recibo de tu reporte en un plazo máximo de **48 horas**.
* Trabajaremos de la mano contigo para entender el problema y desarrollar un parche.
* Te daremos el crédito correspondiente en nuestras notas de la versión cuando la vulnerabilidad haya sido solucionada (si así lo deseas).

¡Gracias por ayudar a mantener el ecosistema de TREMEND Toolkit seguro y confiable para todos!
