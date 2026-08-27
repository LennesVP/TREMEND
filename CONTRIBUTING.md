# Guía de Contribución para TREMEND Toolkit

¡Gracias por tu interés en contribuir a **TREMEND Toolkit**! 🚀

Este proyecto nació con la filosofía de crear una suite de herramientas de diagnóstico, optimización y ciberseguridad que devuelva el control total a los usuarios y técnicos, utilizando código abierto y automatización avanzada.

Cualquier tipo de contribución es bienvenida: desde reportar un simple error, mejorar la documentación, hasta inyectar nuevos módulos de código.

## ¿Cómo puedes contribuir?

### 1. Reportar Errores (Bugs)
Si una herramienta falla o hace que el sistema se comporte de forma inesperada:
* Abre un nuevo **Issue** en GitHub.
* Usa la plantilla de reporte de errores.
* Describe el problema detalladamente, incluyendo tu versión de Windows/Linux/Mac y los pasos exactos para reproducir el fallo.

### 2. Sugerir Nuevas Funciones
¿Tienes una idea para una nueva herramienta en el menú de Redes, Mantenimiento o Diagnóstico?
* Abre un **Issue** seleccionando "Feature Request".
* Explica cómo funcionaría la herramienta y qué problema real soluciona para un técnico o usuario.

### 3. Contribuir con Código (Pull Requests)
Si eres desarrollador y quieres meter las manos en el código fuente de Python:

1. Haz un **Fork** de este repositorio a tu cuenta de GitHub.
2. Clona tu Fork localmente: `git clone https://github.com/TU-USUARIO/TREMEND.git`
3. Crea una nueva rama para tu función: `git checkout -b nombre-de-tu-funcion`
4. Escribe tu código. (Asegúrate de seguir nuestra guía de estilo a continuación).
5. Sube los cambios a tu rama: `git push origin nombre-de-tu-funcion`
6. Abre un **Pull Request (PR)** hacia la rama `main` de nuestro repositorio original.

## Guía de Estilo y Desarrollo

Para mantener el ecosistema de TREMEND Toolkit estable y profesional, te pedimos seguir estas reglas:

* **Python Limpio:** El código base está en Python. Intenta seguir el estándar PEP 8 en la medida de lo posible.
* **Cero Dependencias Innecesarias:** TREMEND se enorgullece de ser ligero. Si tu herramienta requiere instalar módulos externos pesados (vía `pip`), evalúa si es estrictamente necesario o si puedes usar módulos nativos del sistema operativo (Powershell, CMD, Bash).
* **Documentación:** Si agregas una función compleja, añade comentarios breves en el código explicando qué hace la lógica, especialmente si interactúa con el Kernel o el Registro del sistema.
* **Seguridad Primero:** No se aceptará código que extraiga datos del usuario hacia servidores externos no autorizados ni herramientas que ejecuten payloads maliciosos ocultos.

¡Gracias por ayudar a hacer de TREMEND Toolkit la mejor suite para técnicos!
