# 🚀 TREMEND Toolkit V2.6 [ESTABLE Y BLINDADO]
**Desarrollado por:** LDVP (Lennes D. Varela Poveda)

![Versión](https://img.shields.io/badge/Versi%C3%B3n-2.6%20Stable-blue)
![Plataforma](https://img.shields.io/badge/OS-Windows%20%7C%20Android-lightgrey)
![Licencia](https://img.shields.io/badge/Licencia-Open%20Source-brightgreen)
![Visitas](https://komarev.com/ghpvc/?username=LennesVP&repo=TREMEND&label=Visitas+al+Repositorio&color=8B5CF6&style=flat)
![Descargas Totales](https://img.shields.io/github/downloads/LennesVP/TREMEND/total?color=00FFCC&label=Descargas%20Totales&style=flat)

TREMEND Toolkit es una suite avanzada, portátil y sigilosa de diagnóstico y soporte técnico. Diseñada para administradores de sistemas y técnicos de hardware, centraliza comandos nativos y herramientas de élite en una interfaz gráfica interactiva, eliminando la necesidad de recordar extensas líneas de código en PowerShell o CMD.

## 🏗️ Arquitectura del Proyecto (Menú Dinámico)

A partir de la versión V2.6, la interfaz cuenta con un sistema de subcategorías colapsables (Acordeón) y módulos de filtrado inteligente, dividiendo la suite en dos grandes entornos:

### 🪟 SISTEMAS OPERATIVOS

**1. Ecosistema Windows (Ejecución Nativa)**
* **🌐 Redes e Internet:** Escáner de puertos (Sockets nativos), resolución DNS, radar de espectro Wi-Fi, extracción forense de claves inalámbricas, manipulación de Firewall y auditoría de latencia.
* **🧹 Mantenimiento y Optimización:** Limpieza de WinSxS, reparación de imagen (DISM/SFC), purga de VSS y debloat del sistema.
* **🖥️ Diagnóstico e Info del Sistema:** Volcado forense de RAM (Ghost), extracción S.M.A.R.T, monitores de confiabilidad y auditoría de BSOD.
* **📦 Software y Licencias:** Extracción de licencias OEM, inventario a CSV y gestor de paquetes Winget.
* **⚙️ Soporte Técnico:** Borrado forense (Wipe), bypass de contraseñas SAM, Sandbox virtual, destructor de carpetas y descargas multimedia (yt-dlp).

**2. Ecosistemas Móviles y Alternativos**
* **🤖 Android:** Catálogo visual deslizable de aplicaciones (.apk) enfocado en herramientas Open Source y productividad (Ej. Minima Launcher). Cuenta con enlaces directos a los repositorios oficiales.
* **🍏 Mac, 🐧 Linux, 📱 iOS:** Plataformas en fase de despliegue para futuras actualizaciones.

### ☁️ NUBE Y TIENDA

TREMEND Toolkit no almacena binarios pesados en su código fuente. Utiliza catálogos dinámicos (`.json`) alojados en repositorios satélite para operar:
* **🧰 Portables en la Nube:** Descarga programas en la memoria temporal (`%TEMP%`), los ejecuta y los **destruye automáticamente** al cerrarlos, garantizando cero rastros. (Incluye LaZagne, CrystalMark, AnyDesk, Autoruns, etc).
* **📚 Enciclopedia de Apps:** Módulo visual para despliegues de software complejos (Zero-Touch Install). Permite instalaciones avanzadas desatendidas en segundo plano (Ej. Office 2024) y cuenta con **Filtro Inteligente de Categorías**.
* **🌐 Enciclopedia Web:** Directorio interactivo de marcadores vitales para el técnico (ROMs, Firmwares, bases de datos).
* **🛒 Venta de Licencias Oficiales:** Terminal POS comercial integrada. Muestra un catálogo de software original conectando directamente al WhatsApp de soporte para su adquisición.

---

## 📥 Opciones de Descarga (Release v2.6)

Dirígete a la sección de **[Releases](https://github.com/LennesVP/TREMEND/releases/latest)** para obtener la suite. Tienes dos opciones completamente portables:

1. **El Ejecutable Principal (`TREMEND.exe`):** El programa completo y horneado. Descárgalo y dale doble clic para acceder al instante. Ideal para tener en tu propia estación de trabajo.
2. **El Lanzador en la Nube (`Iniciar_TREMEND.bat`):** Un "Dropper" ultraligero (< 1 KB). Se conecta a este repositorio, descarga silenciosamente la última versión en la memoria RAM y la abre. No deja basura en el disco duro del cliente. Ideal para llevar en una USB.

## 🤝 Créditos y Reconocimientos (Motores Integrados)
Este proyecto actúa como una interfaz unificada que rinde tributo y facilita el despliegue del trabajo de desarrolladores de élite. Los derechos pertenecen a sus respectivos autores:

* **Chris Titus Tech:** Utilidad maestra de optimización (winutil).
* **massgravel:** Microsoft Activation Scripts (MAS).
* **AlessandroZ:** LaZagne (Payload forense de contraseñas).
* **pandaadir05:** Ghost (Escáner de memoria RAM en Rust).
* **yt-dlp contributors:** Descargador multimedia y multiplexado.
* **0-manbir:** Minima Launcher (Ecosistema Android).
* **Tungtata:** MiFirm (Base de datos Xiaomi - Enciclopedia Web).
* **hiyohiyo (Crystal Dew World) / Igor Pavlov (7-Zip):** Herramientas portables.
* **Sysinternals & NirSoft:** Múltiples utilidades de diagnóstico.
* **Microsoft Corp:** Motores base de OS, PowerShell, Winget y comandos core.

## ☕ Apoya el Proyecto
Tu apoyo me permite investigar nuevas vulnerabilidades y mantener la herramienta gratuita. 
[![MercadoPago](https://img.shields.io/badge/MercadoPago-Donar_un_Café-00B1EA?style=for-the-badge&logo=mercadopago)](https://link.mercadopago.com.co/tremend)
* 🟣 **Transferencia:** LLave De Bre-B: @LVP671

## 🐛 Soporte y Contacto
¿Tienes una sugerencia, propuesta de colaboración o encontraste un bug? 
📧 **Correo Oficial:** [tremend67@gmail.com](mailto:tremend67@gmail.com)

---
*⚠️ **Aviso de Responsabilidad:** Herramienta diseñada para fines educativos y auditorías autorizadas. El uso indebido de las opciones forenses o destructivas es responsabilidad exclusiva del usuario final.*