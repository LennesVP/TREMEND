# 🚀 TREMEND Toolkit V2.7 [ESTABLE Y BLINDADO]
**Desarrollado por:** LDVP (Lennes D. Varela Poveda)

![Versión](https://img.shields.io/badge/Versi%C3%B3n-2.7%20Stable-blue)
![Plataforma](https://img.shields.io/badge/OS-Windows%20%7C%20Android-lightgrey)
![Licencia](https://img.shields.io/badge/Licencia-Open%20Source-brightgreen)
![Visitas](https://komarev.com/ghpvc/?username=LennesVP&repo=TREMEND&label=Visitas+al+Repositorio&color=8B5CF6&style=flat)
![Última Actualización](https://img.shields.io/github/last-commit/LennesVP/TREMEND?color=00FFCC&label=Última%20Actualización&style=flat)

TREMEND Toolkit es una suite avanzada, portátil y sigilosa de diagnóstico y soporte técnico. Diseñada para administradores de sistemas y técnicos de hardware, centraliza comandos nativos y herramientas de élite en una interfaz gráfica interactiva, eliminando la necesidad de recordar extensas líneas de código en PowerShell o CMD.

## 🏗️ Arquitectura del Proyecto (Menú Dinámico)

A partir de la versión V2.7, la interfaz cuenta con un sistema de subcategorías colapsables (Acordeón) y módulos de filtrado inteligente, dividiendo la suite en dos grandes entornos:

### 🪟 SISTEMAS OPERATIVOS

**1. Ecosistema Windows (Ejecución Nativa)**
* **🌐 Redes e Internet:** Escáner de puertos (Sockets nativos), resolución DNS, radar de espectro Wi-Fi, extracción forense de claves inalámbricas, manipulación de Firewall y auditoría de latencia.
* **🧹 Mantenimiento y Optimización:** Limpieza de WinSxS, reparación de imagen (DISM/SFC), purga de VSS y debloat del sistema.
* **🖥️ Diagnóstico e Info del Sistema:** Volcado forense de RAM (Ghost), extracción S.M.A.R.T, monitores de confiabilidad y auditoría de BSOD.
* **📦 Software y Licencias:** Extracción de licencias OEM, inventario a CSV y gestor de paquetes Winget.
* **⚙️ Soporte Técnico:** Borrado forense (Wipe), bypass de contraseñas SAM, Sandbox virtual, destructor de carpetas y descargas multimedia (yt-dlp).

**2. Ecosistemas Móviles y Alternativos**
* **🤖 Android:** Catálogo visual deslizable de aplicaciones (.apk) enfocado en herramientas Open Source y productividad (Ej. Minima Launcher, Aegis, Aurora). Cuenta con enlaces directos a los repositorios oficiales.
* **🍏 Mac, 🐧 Linux, 📱 iOS:** Plataformas en fase de despliegue para futuras actualizaciones.

### ☁️ NUBE Y TIENDA

TREMEND Toolkit no almacena binarios pesados en su código fuente. Utiliza catálogos dinámicos (`.json`) alojados en repositorios satélite para operar:
* **🧰 Portables en la Nube:** Descarga programas en la memoria temporal (`%TEMP%`), los ejecuta y los **destruye automáticamente** al cerrarlos, garantizando cero rastros. (Incluye LaZagne, CrystalMark, AnyDesk, Autoruns, etc).
* **📚 Enciclopedia de Apps:** Módulo visual para despliegues de software complejos (Zero-Touch Install). Permite instalaciones avanzadas desatendidas en segundo plano (Ej. Office 2024) y cuenta con **Filtro Inteligente de Categorías**.
* **🌐 Enciclopedia Web:** Directorio interactivo de marcadores vitales para el técnico. Incluye bases de datos (ROMs, Firmwares), modelos de **Inteligencia Artificial** de ciberseguridad, y plataformas de **Entretenimiento y Estilo de Vida**.
* **🛒 Venta de Licencias Oficiales:** Terminal POS comercial integrada. Muestra un catálogo de software original (Ej. Bandizip Profesional, Internet Download Manager, Office) conectando directamente al WhatsApp de soporte para su adquisición.

---

## 📥 Opciones de Descarga (Release v2.7)

Dirígete a la sección de **[Releases](https://github.com/LennesVP/TREMEND/releases/latest)** para obtener la suite. Tienes dos opciones completamente portables:

1. **El Ejecutable Principal (`TREMEND.exe`):** El programa completo y horneado. Descárgalo y dale doble clic para acceder al instante. Ideal para tener en tu propia estación de trabajo.
2. **El Lanzador en la Nube (`Iniciar_TREMEND.bat`):** Un "Dropper" ultraligero (< 1 KB). Se conecta a este repositorio, descarga silenciosamente la última versión en la memoria RAM y la abre. No deja basura en el disco duro del cliente. Ideal para llevar en una USB.

## 💬 Comunidad y Soporte (Foro Oficial)
¡Únete a nuestra comunidad de técnicos! Dirígete a la pestaña de **[Discussions](https://github.com/LennesVP/TREMEND/discussions)** del repositorio para:
* 💡 Proponer **Ideas** sobre qué programas Portables o Sitios Web agregar al catálogo de la Nube.
* ❓ Recibir ayuda inmediata en la sección de **Preguntas y Respuestas (Q&A)** si alguna herramienta falla.
* 📢 Enterarte de las novedades de desarrollo y los anuncios oficiales del proyecto.

## 🤝 Créditos y Reconocimientos (Motores Integrados)
Este proyecto actúa como una interfaz unificada que rinde tributo y facilita el despliegue del trabajo de desarrolladores de élite. Los derechos pertenecen a sus respectivos autores:

* **Chris Titus Tech:** Utilidad maestra de optimización (winutil).
* **massgravel:** Microsoft Activation Scripts (MAS).
* **AlessandroZ:** LaZagne (Payload forense de contraseñas).
* **pandaadir05:** Ghost (Escáner de memoria RAM en Rust).
* **yt-dlp contributors:** Descargador multimedia y multiplexado.
* **Microsoft Corp:** Motores base de OS, PowerShell, Winget y comandos core.

## ☕ Apoya el Proyecto
Tu apoyo me permite investigar nuevas vulnerabilidades, costear mi tiempo de desarrollo y mantener TREMEND Toolkit 100% gratuito. Pero más allá de eso, tu apoyo construye el futuro.

### 🎁 Apoyo Internacional y Proyecto "TrueNAS" (Opción Principal)
Si valoras mi trabajo, ¡puedes apoyarme enviándome un detalle físico! He creado una lista de Amazon que incluye desde café para las largas noches de código, hasta herramientas y componentes de hardware especializado.

**¿Por qué hay piezas de hardware de alto valor en la lista?**
Estos componentes no son simples herramientas; son las primeras piedras de mi próximo gran emprendimiento profesional: la construcción física de una **Nube Privada** orientada a ofrecer la máxima seguridad y privacidad del mercado. Al adquirir uno de estos equipos o componentes, estás ayudando a levantar la infraestructura de este futuro servidor.

🌟 **Beneficio Exclusivo para Patrocinadores:** Quien decida apoyarme adquiriendo artículos de esta lista se convierte en un pionero de mi empresa. Como muestra de mi total gratitud, **todos los patrocinadores obtendrán un 50% de descuento** en los futuros servicios de nuestra nube privada una vez que la base física esté 100% operativa (el lanzamiento oficial de los servicios se anunciará a través de este mismo Toolkit). 

Cualquier aporte para poner estas primeras piedras, sea grande o pequeño, es inmensamente agradecido:

[![Amazon Wishlist](https://img.shields.io/badge/Amazon-Ver_mi_Lista_de_Deseos-FF9900?style=for-the-badge&logo=amazon&logoColor=black)](https://www.amazon.com/hz/wishlist/ls/3129WX8TBY0J6?ref_=wl_share)

### 🇨🇴 Apoyo Local (Colombia)
Si estás en Colombia y prefieres invitarme un café virtualmente de forma rápida y directa, puedes hacerlo por estos medios:

[![MercadoPago](https://img.shields.io/badge/MercadoPago-Donar_un_Café-00B1EA?style=for-the-badge&logo=mercadopago)](https://link.mercadopago.com.co/tremend)
* 🟣 **Transferencia Bancaria:** LLave De Bre-B: `@LVP671`