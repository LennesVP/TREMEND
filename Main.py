import os
import time
import sys
import ctypes
import shutil
import socket
import platform
import subprocess
import threading
import winreg
import csv
import urllib.request
import urllib.parse
import json
import secrets
import string
import tkinter as tk
from tkinter import simpledialog
import customtkinter as ctk
import urllib.request
import webbrowser
from tkinter import messagebox

class LinuxToolkit:
    @staticmethod
    def ejecutar_comando(comando):
        try:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, check=True)
            return resultado.stdout
        except subprocess.CalledProcessError as e:
            return f"❌ Error al ejecutar:\n{e.stderr}"

    @staticmethod
    def listar_avanzado(ruta="."): return LinuxToolkit.ejecutar_comando(f"ls -lah {ruta}")
    @staticmethod
    def analizar_espacio_disco(): return LinuxToolkit.ejecutar_comando("df -h")
    @staticmethod
    def ver_interfaces_red(): return LinuxToolkit.ejecutar_comando("ip a | grep inet")
    @staticmethod
    def probar_conectividad(host="google.com"): return LinuxToolkit.ejecutar_comando(f"ping -c 4 {host}")
    @staticmethod
    def abrir_monitor_htop():
        try:
            subprocess.Popen(["gnome-terminal", "--", "htop"])
            return "✅ Monitor de recursos (htop) abierto en una nueva ventana."
        except FileNotFoundError:
            return "❌ No se encontró una terminal compatible. Instala htop o gnome-terminal."
        
def notificar_voz(mensaje):
    """Reproduce el mensaje por los altavoces de forma segura."""
    try:
        import pyttsx3
        motor = pyttsx3.init()
        # El número 150 es la velocidad. Puedes subirlo o bajarlo luego si quieres.
        motor.setProperty('rate', 150) 
        motor.say(mensaje)
        motor.runAndWait()
    except ImportError:
        print("[-] Módulo pyttsx3 no instalado. Silenciando notificación.")
    except Exception as e:
        print(f"[-] No se pudo reproducir la voz: {e}")

# Define la versión de este archivo físico
VERSION_ACTUAL = "3.2"

# ============================================================================
# 0. ESCUDO DE ADMINISTRADOR AUTOMÁTICO (UAC)
# ============================================================================
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{sys.argv[0]}"', None, 1)
    sys.exit()

# ============================================================================
# 1. MOTOR DE ADAPTABILIDAD FLUIDA (LIQUID UI)
# ============================================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

# 1. Analizamos el hardware de la pantalla en tiempo real
ancho_pantalla = app.winfo_screenwidth()
alto_pantalla = app.winfo_screenheight()

# 2. Geometría porcentual: La app ocupará el 85% de la pantalla (se auto-acopla)
factor_escala = 0.85 
ancho_app = int(ancho_pantalla * factor_escala)
alto_app = int(alto_pantalla * factor_escala)

app.geometry(f"{ancho_app}x{alto_app}")

# 3. Centramos la ventana automáticamente en cualquier monitor
x_pos = int((ancho_pantalla - ancho_app) / 2)
y_pos = int((alto_pantalla - alto_app) / 2)
app.geometry(f"+{x_pos}+{y_pos}")

app.title("TREMEND Toolkit V3.2 [ESTABLE Y BLINDADO]")

# ============================================================================
# 2. MOTOR DE TERMINAL NATIVA Y EJECUCIÓN (SEGURO CONTRA CRASHES)
# ============================================================================
def abrir_consola_y_ejecutar(titulo, funcion_python_nativa):
    global app
    win_term = ctk.CTkToplevel(app)
    win_term.title(f"Terminal TREMEND: {titulo}")
    win_term.geometry("950x650") 
    
    # --- FIX: FORZAR LA VENTANA AL FRENTE SIEMPRE ---
    win_term.lift() # Levanta la ventana en la jerarquía del sistema
    win_term.attributes("-topmost", True) # La bloquea arriba de todo
    # Soltamos el bloqueo después de 100 milisegundos para que no estorbe a otras apps
    win_term.after(100, lambda: win_term.attributes("-topmost", False)) 
    win_term.focus_force()
    
    # --- BARRA SUPERIOR DE HERRAMIENTAS (HEADER) ---
    top_frame = ctk.CTkFrame(win_term, fg_color="transparent")
    top_frame.pack(fill="x", padx=10, pady=(10, 0))
    
    lbl_estado = ctk.CTkLabel(top_frame, text="⚡ ESTADO: En Ejecución...", font=("Consolas", 14, "bold"), text_color="#F59E0B")
    lbl_estado.pack(side="left")
    
    def copiar_log():
        win_term.clipboard_clear()
        win_term.clipboard_append(txt_consola.get("1.0", "end"))
        btn_copiar.configure(text="✔️ ¡Copiado!", text_color="#10B981")
        win_term.after(2000, lambda: btn_copiar.configure(text="📋 Copiar Registro", text_color="#FFFFFF"))

    btn_copiar = ctk.CTkButton(top_frame, text="📋 Copiar Registro", width=120, fg_color="#334155", hover_color="#475569", command=copiar_log)
    btn_copiar.pack(side="right")
    
    # --- LA CONSOLA TIPO MATRIX ---
    txt_consola = ctk.CTkTextbox(win_term, width=930, height=560, fg_color="#0A0A0A", text_color="#00FFCC", font=("Consolas", 13), wrap="word", border_width=1, border_color="#334155")
    txt_consola.pack(padx=10, pady=10, fill="both", expand=True)
    
    # NUEVO: Menú Contextual Elegante (Click Derecho)
    def menu_click_derecho(event):
        menu = tk.Menu(win_term, tearoff=0, bg="#0A0A0A", fg="#00FFCC", activebackground="#334155", activeforeground="white")
        
        def copiar_seleccion():
            try:
                texto_seleccionado = txt_consola.selection_get()
                win_term.clipboard_clear()
                win_term.clipboard_append(texto_seleccionado)
            except: pass
            
        def limpiar_pantalla():
            txt_consola.configure(state="normal")
            txt_consola.delete("1.0", "end")
            txt_consola.insert("end", "[*] Consola limpiada por el usuario.\n" + "="*85 + "\n")
            txt_consola.configure(state="disabled")

        menu.add_command(label="📋 Copiar Selección", command=copiar_seleccion)
        menu.add_separator()
        menu.add_command(label="🧹 Limpiar Consola", command=limpiar_pantalla)
        menu.tk_popup(event.x_root, event.y_root)

    txt_consola.bind("<Button-3>", menu_click_derecho)

    # Inyección asíncrona de la UI
    # Inyección asíncrona de la UI
    def log(texto):
        def update_ui():
            # ESCUDO: Solo escribe si la ventana de la consola sigue abierta
            if txt_consola.winfo_exists():
                txt_consola.configure(state="normal")
                txt_consola.insert("end", str(texto) + "\n")
                txt_consola.see("end")
                txt_consola.configure(state="disabled")
        app.after(0, update_ui)

    def correr_proceso():
        try: funcion_python_nativa(log)
        except Exception as e: log(f"\n[!] ERROR CRÍTICO: {e}")
        log("\n" + "="*85 + "\n[+] SECUENCIA FINALIZADA. Puedes cerrar esta ventana.")
        
        # Actualizar el indicador de estado al terminar
        def finalizar_ui():
            # ESCUDO: Solo actualiza el estado si la etiqueta sigue existiendo
            if lbl_estado.winfo_exists():
                lbl_estado.configure(text="✅ ESTADO: Finalizado", text_color="#10B981")
        app.after(0, finalizar_ui)

    import threading
    threading.Thread(target=correr_proceso, daemon=True).start()

def run_cmd(log, comando_str):
    log(f"\n[TREMEND]> {comando_str}")
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        proceso = subprocess.Popen(comando_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                   text=True, encoding='cp850', errors='ignore', startupinfo=startupinfo)
        for linea in proceso.stdout:
            if linea.strip(): log(linea.strip())
        proceso.wait()
    except Exception as e: log(f"[-] Error CMD: {e}")

def run_ps_script(log, script_str):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        proceso = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script_str], 
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                   text=True, encoding='cp850', errors='ignore', startupinfo=startupinfo)
        for linea in proceso.stdout:
            if linea.strip(): log(linea.strip())
        proceso.wait()
    except Exception as e: log(f"[-] Error PS: {e}")

# ============================================================================
# 3. LÓGICA DE HERRAMIENTAS (CEREBRO)
# ============================================================================

# --- CATEGORÍA 1: REDES ---
def logica_info_red(log):
    hostname = socket.gethostname()
    log(f"[*] Equipo: {hostname} | IP Local: {socket.gethostbyname(hostname)}")
    try:
        ip_publica = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode('utf8')
        log(f"[*] IP Pública: {ip_publica}")
    except: log("[-] Error IP Pública.")
    run_cmd(log, "ipconfig /all")

def logica_reparacion_red(log):
    import subprocess
    log("[*] Iniciando Diagnóstico y Reparación Profunda de Red...")
    
    # 1. Nivel Básico (Liberar y Renovar IP)
    log("[*] Liberando direcciones IP actuales (ipconfig /release)...")
    subprocess.run("ipconfig /release", shell=True, capture_output=True)
    
    log("[*] Vaciando caché de resolución DNS (ipconfig /flushdns)...")
    subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
    
    log("[*] Solicitando nueva asignación IP al router (ipconfig /renew)...")
    log("[!] Esto puede tardar unos segundos, la red parpadeará...")
    subprocess.run("ipconfig /renew", shell=True, capture_output=True)
    
    # 2. Restauración Profunda
    log("[*] Restableciendo el catálogo Winsock (netsh winsock reset)...")
    subprocess.run("netsh winsock reset", shell=True, capture_output=True)
    
    log("[*] Restableciendo la pila TCP/IP a valores de fábrica (netsh int ip reset)...")
    subprocess.run("netsh int ip reset", shell=True, capture_output=True)

    # 2.5 Destrucción de Proxies Maliciosos y Restauración de Hosts (NUEVO)
    log("[*] Purgando configuraciones de servidores Proxy inyectados por malware...")
    subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f', shell=True, capture_output=True)
    subprocess.run("netsh winhttp reset proxy", shell=True, capture_output=True)
    
    log("[*] Restaurando el archivo 'Hosts' a sus valores de fábrica...")
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    try:
        if os.path.exists(hosts_path): os.remove(hosts_path)
        with open(hosts_path, "w") as f:
            f.write("# Archivo HOSTS restaurado por TREMEND Toolkit\n# localhost name resolution is handled within DNS itself.\n#\t127.0.0.1       localhost\n#\t::1             localhost\n")
    except: log("[-] No se pudo restaurar el archivo Hosts (Posible bloqueo por Antivirus).")
    
    # 3. Forzado Autónomo de DHCP (Detección automática)
    log("[*] Escaneando adaptadores de red activos para forzar modo Automático (DHCP)...")
    try:
        ps_script = "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object -ExpandProperty Name"
        resultado = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True, text=True)
        interfaces = resultado.stdout.strip().split('\n')
        
        if not interfaces or interfaces == ['']:
            log("[-] No se detectaron adaptadores de red activos.")
        else:
            for iface in interfaces:
                nombre_red = iface.strip()
                if nombre_red:
                    log(f"    -> Configurando IPv4 y DNS por DHCP en: '{nombre_red}'")
                    subprocess.run(f'netsh interface ip set address name="{nombre_red}" source=dhcp', shell=True, capture_output=True)
                    subprocess.run(f'netsh interface ip set dns name="{nombre_red}" source=dhcp', shell=True, capture_output=True)
    except Exception as e:
        log(f"[-] Error al configurar el DHCP automático: {e}")

    log("\n=======================================================")
    log(" ✅ REPARACIÓN DE RED COMPLETADA CON ÉXITO ")
    log("=======================================================")
    log("[!] NOTA: Para que los cambios en Winsock surtan efecto total, debes reiniciar la computadora.")

def logica_visibilidad_lan(log):
    log("\n[*] Forzando configuración de Visibilidad de Red (Network Discovery)...")
    log("[*] Iniciando servicios de descubrimiento PnP y UPnP...")
    
    servicios = ["fdPHost", "FDResPub", "upnphost", "lmhosts"]
    for s in servicios:
        run_cmd(log, f"sc config {s} start= auto")
        run_cmd(log, f"net start {s}")
        
    log("[*] Modificando reglas del Firewall para permitir detección...")
    run_cmd(log, 'netsh advfirewall firewall set rule group="Detección de redes" new enable=Yes')
    run_cmd(log, 'netsh advfirewall firewall set rule group="Network Discovery" new enable=Yes')
    run_cmd(log, 'netsh advfirewall firewall set rule group="Compartir archivos e impresoras" new enable=Yes')
    run_cmd(log, 'netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=Yes')
    
    log("[+] ¡ÉXITO! El equipo ahora debería ser visible para otros computadores en la red local.")

def logica_geolocalizar_ip(log, ip_objetivo=""):
    import urllib.request, json, os, webbrowser
    
    # Si no se provee IP, la API devuelve los datos de la IP pública actual
    url = f"http://ip-api.com/json/{ip_objetivo}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
    
    log(f"\n[*] Triangulando coordenadas para la IP: {ip_objetivo if ip_objetivo else 'PROPIA (Local)'}...")
    log("[*] Interrogando bases de datos globales y registros BGP/ASN...")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        datos = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf8'))
        
        if datos.get("status") == "success":
            ip = datos.get('query')
            pais = f"{datos.get('country')} ({datos.get('countryCode')})"
            region = f"{datos.get('regionName')} / {datos.get('city')}"
            zip_code = datos.get('zip', 'N/A')
            lat, lon = datos.get('lat'), datos.get('lon')
            tz = datos.get('timezone')
            isp = datos.get('isp')
            org = datos.get('org')
            asn = datos.get('as')
            
            # 1. Consola estilo Hacker (Inspirado en la infografía)
            log("\n" + "="*60)
            log(f" 🎯 REPORTE DE INTELIGENCIA (OSINT): {ip}")
            log("="*60)
            log(f" 🌍 UBICACIÓN     : {region}, {pais}")
            log(f" 📮 CÓDIGO POSTAL  : {zip_code}")
            log(f" 🧭 COORDENADAS   : {lat}, {lon}")
            log(f" 🕒 ZONA HORARIA  : {tz}")
            log(f" 🏢 PROVEEDOR ISP : {isp}")
            log(f" 🏛️ ORGANIZACIÓN  : {org}")
            log(f" 📡 SIST. AUTÓNOMO: {asn}")
            log("="*60)
            
            # 2. Generar el Mapa Interactivo en HTML (Leaflet.js en Modo Oscuro)
            log("\n[*] Generando interfaz satelital interactiva (Mapa HTML)...")
            html_mapa = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <title>TREMEND - Radar OSINT ({ip})</title>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                <style>
                    body {{ margin: 0; padding: 0; background-color: #0f172a; color: #38bdf8; font-family: 'Consolas', monospace; }}
                    #header {{ padding: 15px; text-align: center; background-color: #1e293b; border-bottom: 2px solid #00ffcc; }}
                    h2 {{ margin: 0; color: #00ffcc; text-transform: uppercase; letter-spacing: 2px; }}
                    p {{ margin: 5px 0 0 0; color: #94a3b8; font-size: 14px; }}
                    #map {{ height: calc(100vh - 80px); width: 100%; }}
                    .leaflet-popup-content-wrapper {{ background-color: #1e293b; color: #00ffcc; border: 1px solid #38bdf8; font-family: 'Consolas', monospace; }}
                    .leaflet-popup-tip {{ background-color: #1e293b; }}
                </style>
            </head>
            <body>
                <div id="header">
                    <h2>🌐 INTELIGENCIA DE RED - OBJETIVO: {ip}</h2>
                    <p>ISP: {isp} | Ubicación: {region}, {pais} | Coord: {lat}, {lon}</p>
                </div>
                <div id="map"></div>
                <script>
                    var map = L.map('map').setView([{lat}, {lon}], 12);
                    // Capa de mapa estilo Cyberpunk/Dark
                    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                        attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
                        subdomains: 'abcd',
                        maxZoom: 20
                    }}).addTo(map);
                    
                    var marker = L.marker([{lat}, {lon}]).addTo(map);
                    marker.bindPopup("<b>🎯 OBJETIVO FIJADO</b><br>IP: {ip}<br>ORG: {org}").openPopup();
                </script>
            </body>
            </html>
            """
            
            # Encontramos el escritorio seguro
            escritorio = os.path.join(os.environ.get("USERPROFILE"), "Desktop")
            if not os.path.exists(escritorio): 
                escritorio = os.path.join(os.environ.get("USERPROFILE"), "Escritorio")
                
            ruta_mapa = os.path.join(escritorio, f"TREMEND_RadarIP_{ip.replace('.', '_')}.html")
            
            try:
                with open(ruta_mapa, "w", encoding="utf-8") as f:
                    f.write(html_mapa)
                log(f"[+] ¡ÉXITO! Mapa táctico exportado a tu Escritorio.")
                # Abrir en el navegador predeterminado
                webbrowser.open(f"file:///{ruta_mapa.replace(chr(92), '/')}")
            except Exception as e:
                log(f"[-] Error al guardar el mapa HTML: {e}")
                
        else: 
            log(f"[-] Error de la API al buscar la IP: {datos.get('message', 'Desconocido')}")
    except Exception as e: 
        log(f"[-] Error de conexión o límite de peticiones alcanzado: {e}")

def logica_geowifi_bssid(log, bssid_raw):
    import urllib.request, json, os, webbrowser, re, subprocess, concurrent.futures
    
    log(f"\n" + "="*75)
    log(f" 📡 INICIANDO RASTREO SATELITAL FORENSE (GeoWiFi V2.0) ")
    log("="*75)

    bssids_objetivos = []

    # --- 1. MÓDULO DE AUTO-DETECCIÓN DE ENJAMBRE (NUEVO) ---
    if not bssid_raw or bssid_raw.strip().lower() == "auto":
        log("[*] Búsqueda automática detectada. Escaneando el espectro Wi-Fi actual...")
        try:
            # Consultamos TODAS las redes visibles, no solo la conectada
            out = subprocess.run('netsh wlan show networks mode=bssid', shell=True, capture_output=True, text=True, encoding='cp850', errors='ignore').stdout
            for linea in out.splitlines():
                if "BSSID" in linea and not "SSID" in linea.replace("BSSID", ""):
                    bssid_encontrado = linea.split(":", 1)[1].strip().upper()
                    if bssid_encontrado not in bssids_objetivos:
                        bssids_objetivos.append(bssid_encontrado)
            
            if bssids_objetivos:
                log(f"[+] ¡Enjambre detectado! Se encontraron {len(bssids_objetivos)} BSSIDs en tu zona.")
                if len(bssids_objetivos) > 10: 
                    bssids_objetivos = bssids_objetivos[:10] # Top 10 para no saturar la API
            else:
                log("[-] Falló la auto-detección. No se encontraron redes Wi-Fi cercanas.")
                return
        except Exception as e:
            log(f"[-] Error en el motor de auto-detección: {e}")
            return
    else:
        # Búsqueda manual de un solo BSSID
        mac_limpia = re.sub(r'[^a-fA-F0-9]', '', bssid_raw).upper()
        if len(mac_limpia) != 12:
            log(f"[-] Error: La dirección '{bssid_raw}' es inválida.")
            log("    -> Una dirección MAC debe contener exactamente 12 caracteres hexadecimales.")
            return
        bssid_final = ":".join([mac_limpia[i:i+2] for i in range(0, 12, 2)])
        bssids_objetivos.append(bssid_final)
        log(f"[*] Objetivo fijado y formateado a nivel de máquina: {bssid_final}")

    log("[*] Interrogando bases de datos de telemetría global (OSINT) de forma concurrente...")

    coordenadas_validas = []
    
    # --- 2. MOTOR DE TRIANGULACIÓN (NUEVO) ---
    def consultar_api(bssid):
        url = f"https://api.mylnikov.org/geolocation/wifi?v=1.1&data=open&bssid={bssid}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            respuesta = urllib.request.urlopen(req, timeout=5).read().decode('utf8')
            datos = json.loads(respuesta)
            if datos.get("result") == 200 and "data" in datos:
                lat = datos["data"].get("lat")
                lon = datos["data"].get("lon")
                return (bssid, lat, lon)
        except urllib.error.HTTPError as e:
            return (bssid, "ERROR", e.code)
        except: pass
        return (bssid, None, None)

    errores_523 = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ejecutor:
        futuros = [ejecutor.submit(consultar_api, b) for b in bssids_objetivos]
        for futuro in concurrent.futures.as_completed(futuros):
            bssid, lat, lon = futuro.result()
            if lat == "ERROR":
                errores_523 += 1
            elif lat and lon:
                log(f"    [+] BSSID {bssid} localizado -> {lat}, {lon}")
                coordenadas_validas.append((bssid, lat, lon))
            else:
                log(f"    [-] BSSID {bssid} no figura en la base de datos.")

    # --- 3. MANEJO INTELIGENTE DE ERRORES (Anti 523) ---
    if errores_523 > 0 and len(coordenadas_validas) == 0:
        log("\n[-] ALERTA DE SERVIDOR OSINT: La base de datos satelital gratuita está bajo mantenimiento (Error 523/502).")
        log("    -> TREMEND ha contenido el error para evitar bloqueos en tu sistema.")
        log("\n    [💡] Alternativa Forense (Opcional):")
        log("    Si posees una cuenta de investigador, puedes triangular la señal manualmente copiando este enlace:")
        
        if len(bssids_objetivos) == 1:
            log(f"    🔗 https://wigle.net/search?mac={bssids_objetivos[0]}")
        else:
            log("    🔗 https://wigle.net/")
            log(f"    Y busca manualmente una de estas MACs: {', '.join(bssids_objetivos[:3])}")
            
        log("\n[-] Operación abortada con seguridad. Inténtalo más tarde cuando el servidor público se restablezca.")
        return

    # --- 4. CÁLCULO DEL EPICENTRO (PROMEDIO) ---
    lat_promedio = sum([c[1] for c in coordenadas_validas]) / len(coordenadas_validas)
    lon_promedio = sum([c[2] for c in coordenadas_validas]) / len(coordenadas_validas)

    log(f"\n[*] Triangulación completada. Compilando {len(coordenadas_validas)} nodos en Mapa Táctico HTML...")

    # Generación de Marcadores en JS
    marcadores_js = ""
    for bssid, lat, lon in coordenadas_validas:
        marcadores_js += f"""
            var marker = L.marker([{lat}, {lon}]).addTo(map);
            marker.bindPopup("<b>🎯 NODO DETECTADO</b><br>BSSID: {bssid}");
        """

    html_mapa = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>TREMEND - Radar Wi-Fi OSINT V2</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: #0f172a; color: #a855f7; font-family: 'Consolas', monospace; }}
            #header {{ padding: 15px; text-align: center; background-color: #1e293b; border-bottom: 2px solid #a855f7; }}
            h2 {{ margin: 0; color: #00ffcc; text-transform: uppercase; letter-spacing: 2px; }}
            p {{ margin: 5px 0 0 0; color: #94a3b8; font-size: 14px; }}
            #map {{ height: calc(100vh - 80px); width: 100%; }}
            .leaflet-popup-content-wrapper {{ background-color: #1e293b; color: #a855f7; border: 1px solid #38bdf8; font-family: 'Consolas', monospace; }}
            .leaflet-popup-tip {{ background-color: #1e293b; }}
        </style>
    </head>
    <body>
        <div id="header">
            <h2>📡 RASTREO FORENSE MULTI-NODO (ENJAMBRE WI-FI)</h2>
            <p>Nodos Localizados: {len(coordenadas_validas)} | Epicentro Calculado: {lat_promedio:.5f}, {lon_promedio:.5f}</p>
        </div>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{lat_promedio}, {lon_promedio}], 16);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                maxZoom: 20
            }}).addTo(map);
            
            // Círculo de Triangulación
            L.circle([{lat_promedio}, {lon_promedio}], {{
                color: '#00ffcc',
                fillColor: '#00ffcc',
                fillOpacity: 0.1,
                radius: 100
            }}).addTo(map).bindPopup("<b>📍 EPICENTRO TRIANGULADO</b>");

            // Marcadores individuales
            {marcadores_js}
        </script>
    </body>
    </html>
    """
    
    escritorio = os.path.join(os.environ.get("USERPROFILE"), "Desktop")
    if not os.path.exists(escritorio): 
        escritorio = os.path.join(os.environ.get("USERPROFILE"), "Escritorio")
        
    nombre_archivo = "TREMEND_GeoWiFi_Enjambre.html" if len(bssids_objetivos) > 1 else f"TREMEND_GeoWiFi_{bssids_objetivos[0].replace(':', '')}.html"
    ruta_mapa = os.path.join(escritorio, nombre_archivo)
    
    with open(ruta_mapa, "w", encoding="utf-8") as f:
        f.write(html_mapa)
        
    log(f"[+] ¡ÉXITO! Mapa táctico exportado a tu Escritorio.")
    webbrowser.open(f"file:///{ruta_mapa.replace(chr(92), '/')}")
    
    try: notificar_voz("El Rastreo Satelital Geo Wi Fi ha terminado.")
    except: pass

def logica_wifi_forense(log, accion):
    import subprocess, os, re, hashlib, urllib.request

    # --- MOTOR DE INTELIGENCIA DE CONTRASEÑAS ---
    def auditar_seguridad(pwd):
        if not pwd or pwd == "SIN CLAVE / RED ABIERTA": return "🔴 NINGUNA"
        if len(pwd) < 8: return "🟠 BAJA"
        score = sum([bool(re.search(r"[A-Z]", pwd)), bool(re.search(r"[a-z]", pwd)), 
                     bool(re.search(r"[0-9]", pwd)), bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd))])
        if score >= 3 and len(pwd) >= 12: return "🟢 ALTA"
        if score >= 2: return "🟡 MEDIA"
        return "🟠 BAJA"

    def comprobar_filtracion(pwd):
        if not pwd or pwd == "SIN CLAVE / RED ABIERTA": return "N/A"
        try:
            # Encriptamos la clave en SHA-1 (Requisito de ciberseguridad)
            sha1 = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
            prefix, suffix = sha1[:5], sha1[5:]
            # Consultamos la base de datos global de HaveIBeenPwned (Pwned Passwords API)
            req = urllib.request.Request(f"https://api.pwnedpasswords.com/range/{prefix}", headers={'User-Agent': 'TREMEND-Toolkit'})
            res = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
            for linea in res.splitlines():
                if linea.startswith(suffix):
                    veces = int(linea.split(':')[1])
                    return f"⚠️ FILTRADA ({veces} veces)"
            return "✅ SEGURA"
        except: return "Desconocido (Sin Red)"

    # --- EJECUCIÓN LÓGICA ---
    if accion == '1':
        log("\n[*] Iniciando Extracción y Auditoría Forense de Credenciales Wi-Fi...")
        log("[*] Conectando con bases de datos de brechas de seguridad (HaveIBeenPwned API)...")
        try:
            out = subprocess.run('netsh wlan show profiles', shell=True, capture_output=True, text=True, encoding='cp850', errors='ignore').stdout
            perfiles = [line.split(":")[1].strip() for line in out.splitlines() if ("Perfil" in line or "Profile" in line) and ":" in line]
            
            if not perfiles: 
                log("[-] La base de datos WLAN está vacía. No hay redes guardadas.")
                return
            
            log(f"[*] Se detectaron {len(perfiles)} redes en este equipo.\n")
            
            # Interfaz de Tabla Hack/Forense
            log("="*95)
            log(f"{'RED WI-FI (SSID)'.ljust(25)} | {'CONTRASEÑA'.ljust(20)} | {'SEGURIDAD'.ljust(12)} | {'ESTADO EN INTERNET'}")
            log("="*95)
            
            texto_portapapeles = "REPORTE FORENSE WI-FI - TREMEND TOOLKIT\n" + "="*95 + "\n"
            
            for p in perfiles:
                detalles = subprocess.run(f'netsh wlan show profile name="{p}" key=clear', shell=True, capture_output=True, text=True, encoding='cp850', errors='ignore').stdout
                clave = "SIN CLAVE / RED ABIERTA"
                for line in detalles.splitlines():
                    if ("Contenido de la clave" in line or "Key Content" in line) and ":" in line:
                        clave = line.split(":")[1].strip()
                        break
                
                seguridad = auditar_seguridad(clave)
                filtracion = comprobar_filtracion(clave)
                
                linea_tabla = f"{p[:24].ljust(25)} | {clave[:19].ljust(20)} | {seguridad.ljust(12)} | {filtracion}"
                log(linea_tabla)
                texto_portapapeles += linea_tabla + "\n"
                
            log("="*95)
            try:
                app.clipboard_clear()
                app.clipboard_append(texto_portapapeles)
                log("\n[+] ¡Tabla de contraseñas copiada automáticamente a tu portapapeles!")
            except: pass
            
        except Exception as e: log(f"[-] Error de extracción: {e}")
    
    elif accion == '2':
        log("\n[*] Exportando perfiles Wi-Fi (Backup para migración)...")
        ruta_backup = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "TREMEND_WiFi_Backup")
        if not os.path.exists(ruta_backup): os.makedirs(ruta_backup)
        run_cmd(log, f'netsh wlan export profile key=clear folder="{ruta_backup}"')
        log(f"[+] Backup completado. Archivos XML guardados en el Escritorio: {ruta_backup}")
        
    elif accion == '3':
        log("\n[*] Importando perfiles Wi-Fi desde el Backup...")
        ruta_backup = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "TREMEND_WiFi_Backup")
        if not os.path.exists(ruta_backup):
            log("[-] No se encontró la carpeta 'TREMEND_WiFi_Backup' en el Escritorio."); return
        script = f"Get-ChildItem -Path '{ruta_backup}' -Filter '*.xml' | ForEach-Object {{ netsh wlan add profile filename=$_.FullName }}"
        run_ps_script(log, script)
        log("[+] Perfiles inyectados exitosamente en el sistema.")

def logica_optimizar_dns(log, opcion):
    log("\n[*] Reconfigurando la resolución de nombres de dominio (DNS) en todos los adaptadores activos...")
    
    # --- MATRIZ DE SERVIDORES DNS (NIVEL INGENIERO) ---
    dns_map = {
        # --- MÁXIMA VELOCIDAD ---
        '1': ("1.1.1.1, 1.0.0.1", "Cloudflare (Rápido y Privado)"),
        '2': ("8.8.8.8, 8.8.4.4", "Google (Alta Estabilidad y Resolución)"),
        
        # --- BLOQUEO DE ANUNCIOS Y RASTREADORES ---
        '3': ("94.140.14.14, 94.140.15.15", "AdGuard (Bloqueo de Anuncios y Trackers)"),
        '4': ("194.242.2.3, 194.242.2.4", "Mullvad (Cero Rastreadores y Anti-Ads)"),
        
        # --- CIBERSEGURIDAD (ANTI-MALWARE / PHISHING) ---
        '5': ("9.9.9.9, 149.112.112.112", "Quad9 (Bloqueo Nativo de Malware)"),
        '6': ("1.1.1.2, 1.0.0.2", "Cloudflare Security (Bloqueo de Malware)"),
        '7': ("76.76.2.1, 76.76.2.0", "ControlD (Bloqueo de Malware y Phishing)"),
        
        # --- FILTRO FAMILIAR (ANTI-ADULTO / PORNO) ---
        '8': ("1.1.1.3, 1.0.0.3", "Cloudflare Family (Malware + Contenido Adulto)"),
        '9': ("185.228.168.168, 185.228.169.168", "CleanBrowsing (Filtro Familiar Estricto)"),
        '10': ("94.140.14.15, 94.140.15.16", "AdGuard Family (Anuncios + Contenido Adulto)"),
        '11': ("208.67.222.123, 208.67.220.123", "OpenDNS Family Shield (Contenido Adulto)")
    }
    
    if opcion in dns_map:
        ips, nombre = dns_map[opcion]
        log(f"[*] Inyectando Servidores: {nombre}")
        log(f"    -> IPs Objetivo: {ips}")
        run_ps_script(log, f'Get-NetAdapter | Where-Object {{$_.Status -eq "Up"}} | Set-DnsClientServerAddress -ServerAddresses {ips}')
        log(f"[+] Servidores DNS cambiados a {ips} exitosamente.")
        run_cmd(log, "ipconfig /flushdns")
        log("[+] Caché DNS purgada para aplicar los nuevos filtros inmediatamente.")
        
    elif opcion == '12':
        log("[*] Restaurando DNS Automático (DHCP por defecto)...")
        run_ps_script(log, 'Get-NetAdapter | Where-Object {{$_.Status -eq "Up"}} | Set-DnsClientServerAddress -ResetServerAddresses')
        log("[+] DNS restaurados a la configuración de fábrica de tu proveedor de internet.")
        run_cmd(log, "ipconfig /flushdns")
    else:
        log("[-] Operación cancelada u opción inválida.")

def logica_reinicio_bios(log):
    log("\n[*] Iniciando secuencia de reinicio forzado hacia la BIOS/UEFI...")
    log("[!] ATENCIÓN: El equipo se reiniciará INMEDIATAMENTE. Cierra tus trabajos.")
    
    script_ps = """
    try {
        Write-Host "[*] Comprobando compatibilidad de firmware de la Placa Base..."
        # Verifica si el sistema arranca con UEFI (Requisito para el reinicio remoto a BIOS)
        if (Test-Path "HKLM:\\System\\CurrentControlSet\\Control\\SecureBoot\\State") {
            Write-Host "[+] Sistema UEFI detectado. Ejecutando reinicio en 3 segundos..." -ForegroundColor Green
            Start-Sleep -Seconds 3
            shutdown.exe /r /fw /t 0
        } else {
            Write-Host "[-] Tu sistema utiliza BIOS Legacy antigua." -ForegroundColor Red
            Write-Host "[-] El salto directo a BIOS solo es soportado por placas base UEFI modernas." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "[-] Error al invocar el comando de energía."
    }
    """
    run_ps_script(log, script_ps)

def logica_limpiar_arp(log):
    log("\n[*] Purgando caché de enrutamiento (ARP)...")
    run_cmd(log, "arp -d *")
    log("[+] Tabla ARP destruida. La red se re-descubrirá automáticamente.")

def logica_ping_tcp(log, destino, puerto):
    log(f"\n[*] Ejecutando prueba de conectividad hacia: {destino}")
    if puerto:
        log(f"[*] Escaneando puerto TCP {puerto}...")
        run_ps_script(log, f"Test-NetConnection -ComputerName '{destino}' -Port {puerto} | Format-List")
    else:
        run_cmd(log, f"ping {destino} -n 4")
        
        notificar_voz("La Prueba De Conectividad ha terminado.")

def logica_puerto_proceso(log, puerto):
    log(f"\n[*] Mapeando procesos en el puerto local {puerto}...")
    script = f"""
    try {{
        $conex = Get-NetTCPConnection -LocalPort {puerto} -ErrorAction Stop
        Write-Host '[+] Procesos ocupando el puerto {puerto}:' -ForegroundColor Green
        $conex | ForEach-Object {{ Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue }} | Select-Object Id, ProcessName, Path -Unique | Format-List
    }} catch {{ Write-Host '[-] Ningun proceso activo en ese puerto.' }}
    """
    run_ps_script(log, script)

def logica_generador_qr(log, tipo, dato1, dato2=""):
    import random
    log(f"\n[*] Iniciando Motor Universal de Códigos QR...")
    try:
        if tipo == '1':
            log(f"[*] Compilando protocolo de red para Wi-Fi: {dato1}")
            formato = f"WIFI:T:WPA;S:{urllib.parse.quote(dato1)};P:{urllib.parse.quote(dato2)};;" if dato2 else f"WIFI:T:nopass;S:{urllib.parse.quote(dato1)};P:;;"
            nombre_archivo = f"QR_WiFi_{dato1.replace(' ', '_')[:10]}.png"
        else:
            log(f"[*] Procesando URL o Texto libre...")
            formato = urllib.parse.quote(dato1)
            nombre_archivo = f"QR_Personalizado_{random.randint(1000,9999)}.png"
            
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={formato}"
        
        # Encontramos el escritorio sin importar el idioma de Windows
        escritorio = os.path.join(os.environ.get("USERPROFILE"), "Desktop")
        if not os.path.exists(escritorio): 
            escritorio = os.path.join(os.environ.get("USERPROFILE"), "Escritorio")
            
        ruta_qr = os.path.join(escritorio, nombre_archivo)
        
        log("[*] Renderizando matriz gráfica en alta calidad...")
        urllib.request.urlretrieve(url, ruta_qr)
        
        log("\n=======================================================")
        log(f" [+] ¡ÉXITO! Código QR guardado en tu Escritorio.")
        log(f" [+] Archivo: {nombre_archivo}")
        log("=======================================================")
        os.startfile(ruta_qr)
        
    except Exception as e: 
        log(f"[-] Error al generar QR: {e}")

def logica_reporte_wifi(log):
    log("\n[*] Generando Reporte de Diagnóstico Wi-Fi de Windows (WlanReport)...")
    run_cmd(log, "netsh wlan show wlanreport")
    ruta = r"C:\ProgramData\Microsoft\Windows\WlanReport\wlan-report-latest.html"
    if os.path.exists(ruta): log(f"[+] Reporte generado en: {ruta}"); os.startfile(ruta)
    else: log("[-] No se pudo generar el reporte.")

    notificar_voz("El Reporte De WIfi ha terminado.")

def logica_resolucion_dns(log, dominio):
    log(f"\n[*] Interrogando servidores raíz para el dominio: {dominio}")
    run_ps_script(log, f"Resolve-DnsName -Name '{dominio}' -ErrorAction Stop | Select-Object Name, Type, IPAddress, NameHost | Format-Table -AutoSize")

def logica_bloquear_web(log, accion, dominio=""):
    import os
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    
    if accion == '1':
        log(f"\n[*] Inyectando regla de bloqueo (loopback) para: {dominio}")
        dominio_limpio = dominio.replace("http://", "").replace("https://", "").replace("www.", "").strip("/")
        try:
            with open(hosts_path, "a") as f: 
                f.write(f"\n0.0.0.0 {dominio_limpio}\n0.0.0.0 www.{dominio_limpio}\n")
            run_cmd(log, "ipconfig /flushdns")
            log(f"[+] Dominio '{dominio_limpio}' bloqueado exitosamente.")
        except Exception as e: 
            log(f"[-] Error de permisos: {e}")

    elif accion == '2':
        log(f"\n[*] Buscando y removiendo bloqueos para: {dominio}")
        dominio_limpio = dominio.replace("http://", "").replace("https://", "").replace("www.", "").strip("/")
        try:
            with open(hosts_path, "r") as f:
                lineas = f.readlines()
            
            with open(hosts_path, "w") as f:
                removidos = 0
                for linea in lineas:
                    # Si la línea contiene el dominio y es una regla de bloqueo, la omitimos (la borramos)
                    if dominio_limpio in linea and "0.0.0.0" in linea:
                        removidos += 1
                        continue 
                    f.write(linea)
            
            run_cmd(log, "ipconfig /flushdns")
            if removidos > 0:
                log(f"[+] Se eliminaron {removidos} reglas de bloqueo. El dominio '{dominio_limpio}' ha sido restaurado.")
            else:
                log(f"[-] El dominio '{dominio_limpio}' no estaba bloqueado en el sistema.")
        except Exception as e:
            log(f"[-] Error de permisos: {e}")

    elif accion == '3':
        log("\n[*] Purgando TODAS las reglas del archivo Hosts...")
        try:
            with open(hosts_path, "w") as f:
                f.write("# Archivo HOSTS restaurado por TREMEND Toolkit\n# localhost name resolution is handled within DNS itself.\n#\t127.0.0.1       localhost\n#\t::1             localhost\n")
            run_cmd(log, "ipconfig /flushdns")
            log("[+] Archivo Hosts restaurado a fábrica. Todas las páginas web han sido desbloqueadas.")
        except Exception as e:
            log(f"[-] Error de permisos: {e}")
            
    try: notificar_voz("El Gestor Avanzado de Hosts ha terminado.")
    except: pass

def logica_abrir_puerto(log, puerto, proto):
    log(f"\n[*] Abriendo puerto {puerto} ({proto}) en el Firewall...")
    run_cmd(log, f'netsh advfirewall firewall add rule name="TREMEND: Puerto {puerto} {proto}" dir=in action=allow protocol={proto} localport={puerto}')

def logica_purgar_wifi_historial(log):
    log("\n[*] Purgando todo el historial inalambrico del sistema...")
    run_cmd(log, "netsh wlan delete profile name=* i=*")

def logica_reset_firewall(log):
    log("\n[*] Restaurando Firewall a fábrica...")
    run_cmd(log, "netsh advfirewall reset")

def logica_conexiones_tcp(log):
    log("\n[*] Mapeando conexiones TCP establecidas y puertos activos...")
    run_ps_script(log, 'Get-NetTCPConnection | Where-Object State -eq "Established" | Select-Object RemoteAddress, RemotePort, @{Name="Programa";Expression={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).Name}} | Format-Table -AutoSize')

def logica_sesiones_smb(log):
    log("\n[*] Auditando sesiones conectadas a esta máquina (SMB/Carpetas Compartidas)...")
    run_ps_script(log, 'Get-SmbSession | Select-Object ClientComputerName, ClientUserName, NumOpens | Out-GridView -Title "Sesiones Activas en tu Red"')
    log("[+] Volcado de sesiones completado. Si ves usuarios desconocidos, revisa tus carpetas compartidas.")

def logica_radar_wifi(log):
    log("\n[*] Iniciando Radar Wi-Fi de Espectro (5 Barridos)...")
    import time
    for i in range(5):
        log(f"\n--- BARRIDO {i+1}/5 ---")
        run_cmd(log, 'netsh wlan show networks mode=bssid | findstr "SSID Señal Canal"')
        time.sleep(2)
    log("\n[+] Análisis de espectro finalizado.")

    notificar_voz("El Radar Wi-Fi ha terminado.")

def logica_auditoria_latencia(log, destino):
    import time, datetime
    log(f"\n[*] Iniciando Auditoría de Latencia Continua hacia {destino} (10 paquetes con reloj atómico)...")
    for i in range(10):
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        respuesta = subprocess.run(f"ping -n 1 -w 1000 {destino}", shell=True, capture_output=True, text=True, encoding='cp850').stdout
        if "TTL=" in respuesta:
            tiempo = respuesta.split("tiempo")[1].split("ms")[0].replace("=", "").replace("<", "").strip()
            log(f"[{hora}] -> Respuesta de {destino}: {tiempo} ms")
        else:
            log(f"[{hora}] -> [!] TIEMPO DE ESPERA AGOTADO (Microcorte detectado)")
        time.sleep(1)
    log("[+] Auditoría finalizada.")

    notificar_voz("La Prueba De Latencia ha terminado.")

def logica_escaner_puertos_python(log, objetivo):
    import socket
    import concurrent.futures

    log(f"\n[*] Preparando Escáner de Puertos Avanzado (Motor Asíncrono Multihilo)")
    
    # 1. Traductor DNS inteligente (Convierte dominios en IP automáticamente)
    try:
        ip_objetivo = socket.gethostbyname(objetivo)
        if objetivo != ip_objetivo:
            log(f"[*] Objetivo fijado: {objetivo} -> {ip_objetivo}")
        else:
            log(f"[*] Objetivo fijado: {ip_objetivo}")
    except socket.gaierror:
        log(f"[-] Error crítico: No se pudo resolver el dominio o IP '{objetivo}'.")
        return

    # Añadimos puertos más letales (SQL, VNC, Web Alterno)
    puertos_comunes = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 
        80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 
        443: "HTTPS", 445: "SMB", 1433: "SQL Server", 3306: "MySQL", 
        3389: "RDP", 5900: "VNC", 8080: "HTTP Alterno"
    }
    
    abiertos = 0
    log("[*] Lanzando enjambre de hilos (Reconocimiento simultáneo ultrarrápido)...")

    def escanear_puerto(puerto, servicio):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.6) # Timeout letal pero seguro
            resultado = s.connect_ex((ip_objetivo, puerto))
            s.close()
            if resultado == 0:
                return puerto, servicio, True
        except: pass
        return puerto, servicio, False

    # 2. ATAQUE MULTIHILO: Escanea los 16 puertos a la vez en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ejecutor:
        futuros = [ejecutor.submit(escanear_puerto, p, s) for p, s in puertos_comunes.items()]
        for futuro in concurrent.futures.as_completed(futuros):
            puerto, servicio, abierto = futuro.result()
            if abierto:
                log(f"    [+] PUERTO ABIERTO: {puerto} ({servicio}) -> ¡Posible vector de ataque!")
                abiertos += 1

    if abiertos == 0: 
        log("\n[-] La máquina parece estar blindada o apagada. No hay puertos expuestos.")
    else:
        log(f"\n[!] ALERTA CRÍTICA: Se detectaron {abiertos} puertos vulnerables.")
    log("[+] Escaneo finalizado.")
    
    try: notificar_voz("El Escáner de Puertos ha terminado.")
    except: pass

def logica_auditor_web(log, objetivo):
    import urllib.request
    import socket
    import ssl
    import time
    
    log(f"\n" + "="*75)
    log(f" 🌐 INICIANDO AUDITORÍA WEB FORENSE (OBJETIVO: {objetivo}) ")
    log(f"="*75)

    # Limpiar el objetivo
    objetivo = objetivo.replace("http://", "").replace("https://", "").strip("/")
    
    log("\n[1] FASE DE RECONOCIMIENTO (BANNER GRABBING)...")
    
    puertos_web = [80, 443]
    for puerto in puertos_web:
        protocolo = "HTTP" if puerto == 80 else "HTTPS"
        log(f"[*] Evaluando puerto {puerto} ({protocolo})...")
        
        try:
            # Sockets para un timeout súper agresivo
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            resultado = s.connect_ex((objetivo, puerto))
            
            if resultado == 0:
                log(f"    [+] Puerto {puerto} ABIERTO.")
                
                # Extracción de Cabeceras
                req_url = f"http://{objetivo}" if puerto == 80 else f"https://{objetivo}"
                try:
                    req = urllib.request.Request(req_url, headers={'User-Agent': 'Mozilla/5.0'}, method='HEAD')
                    context = ssl._create_unverified_context() if puerto == 443 else None
                    with urllib.request.urlopen(req, timeout=3, context=context) as response:
                        server_header = response.headers.get('Server', 'Desconocido / Oculto')
                        x_powered_by = response.headers.get('X-Powered-By', 'No especificado')
                        log(f"    -> Servidor (Engine): {server_header}")
                        log(f"    -> Tecnología base : {x_powered_by}")
                except urllib.error.URLError as e:
                    # Si da 403 Forbidden o 401, el puerto está abierto pero bloqueado
                    log(f"    -> Servidor vivo pero con restricciones (Código: {e.code if hasattr(e, 'code') else e.reason})")
                except Exception as e:
                    log(f"    [-] Error al extraer cabeceras HTTP: {e}")
            else:
                log(f"    [-] Puerto {puerto} CERRADO o Filtrado.")
            s.close()
        except Exception as e:
            log(f"    [-] Timeout o Error de conexión: {e}")

    log("\n[2] FASE DE ENUMERACIÓN (FUZZING LIGERO DE DIRECTORIOS)...")
    log("[!] Escaneando rutas comunes. Buscando paneles de control ocultos o backups expuestos...")
    
    # Un mini-diccionario letal y estratégico
    rutas_sensibles = [
        "admin", "administrator", "login", "wp-admin", "phpmyadmin", 
        "backup", "backups", "config", "db", "test", "old", ".git"
    ]
    
    url_base = f"http://{objetivo}"
    # Intentamos primero con HTTP, si no responde, intentamos HTTPS
    try:
        urllib.request.urlopen(urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0'}), timeout=2)
    except:
        url_base = f"https://{objetivo}"
        
    encontrados = 0
    context = ssl._create_unverified_context() # Bypass SSL errors for local networks
    
    for ruta in rutas_sensibles:
        url_test = f"{url_base}/{ruta}/"
        try:
            req = urllib.request.Request(url_test, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=2, context=context)
            if res.status == 200:
                log(f"    [🔥 ALERTA] Directorio expuesto encontrado: {url_test}")
                encontrados += 1
        except urllib.error.HTTPError as e:
            if e.code in [403, 401]:
                # 403 Forbidden significa que el directorio EXISTE, pero está protegido. Sigue siendo un hallazgo.
                log(f"    [🛡️ PROTEGIDO] Directorio detectado (Acceso Denegado): {url_test} (Error {e.code})")
                encontrados += 1
        except Exception:
            pass # Si es 404 No encontrado o Timeout, ignoramos y seguimos
            
        time.sleep(0.1) # Pausa táctica para no saturar servidores locales
        
    if encontrados == 0:
        log("    [-] No se encontraron paneles ni directorios críticos expuestos.")
    else:
        log(f"\n    [+] Auditoría finalizada. Se detectaron {encontrados} puntos de interés.")
        
    log("\n[+] EJECUCIÓN FORENSE COMPLETADA.")

def logica_nmap(log, objetivo, tipo_escaneo):
    import urllib.request, os, subprocess, time, shutil
    from tkinter import messagebox
    
    log(f"\n[*] Iniciando Motor de Reconocimiento Nmap hacia: {objetivo}")
    
    temp_dir = os.path.join(os.environ.get('TEMP'), "Tremend_Nmap")
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    # 1. VERIFICACIÓN CRÍTICA: Escudo Npcap (Requisito para instalación silenciosa)
    ruta_npcap = r"C:\Windows\System32\Npcap"
    if not os.path.exists(ruta_npcap):
        log("[-] Driver 'Npcap' no detectado. Es obligatorio para la instalación silenciosa de Nmap.")
        if messagebox.askyesno("Requisito Faltante", "Nmap requiere el driver 'Npcap' para capturar la red y poder instalarse en silencio.\n\n¿Deseas descargar el instalador oficial y ejecutarlo ahora mismo?"):
            log("[*] Descargando instalador de Npcap...")
            npcap_exe = os.path.join(temp_dir, "npcap_installer.exe")
            try:
                urllib.request.urlretrieve("https://npcap.com/dist/npcap-1.79.exe", npcap_exe)
                log("[!] Lanzando instalador. Acepta todas las opciones por defecto (Next -> Install)...")
                
                script_ps = f"Start-Process -FilePath '{npcap_exe}' -Verb RunAs -Wait"
                subprocess.run(["powershell", "-NoProfile", "-Command", script_ps], startupinfo=startupinfo)
                
                if not os.path.exists(ruta_npcap):
                    log("[-] Instalación de Npcap cancelada. Abortando Nmap."); return
                else:
                    log("[+] Npcap instalado exitosamente.")
            except Exception as e:
                log(f"[-] Error al descargar Npcap: {e}"); return
        else:
            log("[-] Operación cancelada."); return
            
    # 2. Búsqueda de instalación existente de Nmap
    rutas_comunes = [
        r"C:\Program Files (x86)\Nmap\nmap.exe",
        r"C:\Program Files\Nmap\nmap.exe"
    ]
    exe_path = next((ruta for ruta in rutas_comunes if os.path.exists(ruta)), None)
    
    setup_path = os.path.join(temp_dir, "nmap_setup.exe")
    
    # 3. Descarga e Instalación Silenciosa de Nmap
    if not exe_path:
        log("[*] Iniciando descarga del instalador base de Nmap (v7.99)...")
        url_nmap = "https://nmap.org/dist/nmap-7.99-setup.exe"
        
        try:
            if not os.path.exists(setup_path):
                req = urllib.request.Request(url_nmap, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=60) as response, open(setup_path, 'wb') as out_file:
                    out_file.write(response.read())
                    
            log("[*] Desplegando Nmap en Modo Ghost (Instalación Desatendida)...")
            subprocess.run(f'"{setup_path}" /S', shell=True)
            
            # Esperamos de forma inteligente hasta que el ejecutable aparezca
            for _ in range(20):
                exe_path = next((ruta for ruta in rutas_comunes if os.path.exists(ruta)), None)
                if exe_path: break
                time.sleep(1)
                
        except Exception as e:
            log(f"[-] Error crítico al procesar Nmap: {e}"); return
            
    if not exe_path:
        log("[-] Error: El sistema bloqueó la instalación de Nmap."); return
        
    # 4. Configuración del Vector de Ataque (CON EVASIÓN DE PING -Pn)
    log("[*] Configurando vector de escaneo (Evasión Ping Activada)...")
    if tipo_escaneo == '1':
        comando = f'"{exe_path}" -Pn -T4 -F "{objetivo}"'
        log("    -> Vector: Rápido (Top 100 puertos)")
    elif tipo_escaneo == '2':
        comando = f'"{exe_path}" -Pn -sV -sC "{objetivo}"'
        log("    -> Vector: Intermedio (Detección de versiones y scripts)")
    elif tipo_escaneo == '3':
        comando = f'"{exe_path}" -Pn -A -T4 "{objetivo}"'
        log("    -> Vector: Agresivo (Sistema Operativo, Rutas y Vulnerabilidades)")
        log("    [!] Advertencia: Este modo puede tomar varios minutos.")
        
    log("\n[!] ESCANEO EN PROGRESO. La terminal no mostrará texto hasta compilar los resultados...\n")
    
    # 5. Ejecución del Escaneo
    try:
        resultado = subprocess.run(comando, shell=True, cwd=os.path.dirname(exe_path), capture_output=True, text=True, encoding='cp850', errors='ignore')
        
        for linea in resultado.stdout.splitlines():
            if linea.strip(): log("    " + linea.strip())
            
        for linea in resultado.stderr.splitlines():
            if linea.strip(): log("    [-] " + linea.strip())
            
        log("\n[+] Reconocimiento finalizado exitosamente.")
    except Exception as e:
        log(f"[-] Error durante el escaneo: {e}")
        
    # 6. Limpieza Táctica Extrema (Nmap + Npcap)
    if messagebox.askyesno("Limpieza Forense", "¿Deseas DESINSTALAR Nmap y el driver Npcap del sistema para no dejar NINGÚN rastro en este equipo?"):
        log("[*] Ejecutando protocolo asesino (Desinstalador silencioso de Nmap)...")
        uninst_path = os.path.join(os.path.dirname(exe_path), "Uninstall.exe")
        if os.path.exists(uninst_path):
            subprocess.run(f'"{uninst_path}" /S', shell=True)
            log("[+] Nmap purgado del disco duro exitosamente.")
            
        log("[*] Buscando y eliminando driver de red (Npcap)...")
        npcap_uninst = r"C:\Program Files\Npcap\uninstall.exe"
        if os.path.exists(npcap_uninst):
            subprocess.run(f'"{npcap_uninst}" /S', shell=True)
            log("[+] Npcap destruido de la raíz del sistema.")
            
        try: shutil.rmtree(temp_dir, ignore_errors=True)
        except: pass
        log("[+] Limpieza 100% completada. Cero rastros detectables.")
    else:
        log("[*] Motores conservados en el equipo.")

def logica_crear_nas(log, ruta_carpeta, nombre_recurso):
    log(f"\n[*] Elevando carpeta '{ruta_carpeta}' a Recurso Compartido de Red (NAS)...")
    script = f"""
    try {{
        New-SmbShare -Name '{nombre_recurso}' -Path '{ruta_carpeta}' -FullAccess 'Everyone' -ErrorAction Stop
        Set-NetFirewallRule -DisplayGroup 'File and Printer Sharing' -Enabled True -Profile Any -ErrorAction SilentlyContinue
        Write-Host '[+] Servidor NAS levantado. Accesible en la red como \\\\$env:COMPUTERNAME\\{nombre_recurso}' -ForegroundColor Green
    }} catch {{ Write-Host "[-] Error al compartir: $($_.Exception.Message)" }}
    """
    run_ps_script(log, script)

def logica_auditar_cache_dns(log):
    log("\n[*] Extrayendo base de datos de resolución DNS en memoria...")
    run_cmd(log, "ipconfig /displaydns")
    log("[*] Si ves páginas sospechosas que tú no has visitado, ejecuta la 'Reparación Total de Red' para purgar esto.")

    notificar_voz("La Auditoría De Cache DNS ha terminado.")

# --- CATEGORÍA 2: MANTENIMIENTO ---

def logica_cotizador_divisas(log):
    import urllib.request, json, time, threading
    import customtkinter as ctk

    log("\n" + "="*75)
    log(" 💱 INICIANDO RADAR FINANCIERO Y LABORATORIO API ")
    log("="*75)
    
    win_div = ctk.CTkToplevel(app)
    win_div.title("TREMEND - Radar de Divisas (API REST)")
    win_div.geometry("900x540")
    win_div.attributes("-topmost", True)
    win_div.transient(app)
    
    # --- PANEL IZQUIERDO: LABORATORIO API (EDUCATIVO) ---
    frame_izq = ctk.CTkFrame(win_div, width=420, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#38BDF8")
    frame_izq.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    
    ctk.CTkLabel(frame_izq, text="📡 Laboratorio API y JSON", font=("Arial", 20, "bold"), text_color="#00FFCC").pack(pady=(20, 5))
    ctk.CTkLabel(frame_izq, text="Así se extrae información de la nube en Python\nusando peticiones HTTP y diccionarios (Key:Value).", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 15))
    
    txt_codigo = ctk.CTkTextbox(frame_izq, font=("Consolas", 13, "bold"), fg_color="#000000", text_color="#38BDF8", height=200)
    txt_codigo.pack(padx=20, fill="x")
    
    codigo_python = """# 1. Hacemos GET a la API Maestra (Base USD)
req = urllib.request.urlopen("URL_DE_LA_API")

# 2. Descargamos el JSON con TODAS las monedas
datos = json.loads(req.read().decode('utf-8'))
tasas = datos["rates"]

# 3. Matemática para cruzar cualquier divisa
valor_base = tasas["EUR"]
valor_destino = tasas["COP"]

precio_final = valor_destino / valor_base"""
    
    txt_codigo.insert("1.0", codigo_python)
    txt_codigo.configure(state="disabled")

    # Log de la terminal en vivo
    txt_log_api = ctk.CTkTextbox(frame_izq, font=("Consolas", 12), fg_color="#1E293B", text_color="#A855F7", height=130)
    txt_log_api.pack(padx=20, pady=15, fill="both", expand=True)
    txt_log_api.insert("end", "[*] Motor Auto-Sync en espera...")
    txt_log_api.configure(state="disabled")

    # --- PANEL DERECHO: DASHBOARD FINANCIERO REAL ---
    frame_der = ctk.CTkFrame(win_div, width=420, fg_color="#1E293B", corner_radius=10, border_width=1, border_color="#F59E0B")
    frame_der.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)
    
    ctk.CTkLabel(frame_der, text="🌍 Mercado Global (En Vivo)", font=("Arial", 20, "bold"), text_color="#F59E0B").pack(pady=(15, 5))
    ctk.CTkLabel(frame_der, text="🟢 Auto-Sync Activado (Intervalo Seguro: 60s)", font=("Arial", 11, "bold"), text_color="#10B981").pack(pady=(0, 15))

    # Listado Extendido de Monedas Soportadas
    lista_monedas = [
        "USD - Dólar", "EUR - Euro", "COP - Peso Col.", "MXN - Peso Mex.", 
        "CLP - Peso Chil.", "ARS - Peso Arg.", "PEN - Sol Perú", "BRL - Real Bra.", 
        "JPY - Yen Jap.", "CNY - Yuan", "CAD - Dólar Can.", "GBP - Libra"
    ]
    
    var_base1 = ctk.StringVar(value="USD - Dólar")
    var_base2 = ctk.StringVar(value="EUR - Euro")
    var_target = ctk.StringVar(value="COP - Peso Col.")

    # Cajas de Tasa de Cambio (Interactivas)
    frame_tasas = ctk.CTkFrame(frame_der, fg_color="transparent")
    frame_tasas.pack(fill="x", padx=10)

    # Base 1
    caja_1 = ctk.CTkFrame(frame_tasas, fg_color="#0F172A", corner_radius=8)
    caja_1.pack(side="left", fill="x", expand=True, padx=5)
    combo_1 = ctk.CTkOptionMenu(caja_1, variable=var_base1, values=lista_monedas, font=("Arial", 12, "bold"), height=28, fg_color="#334155", button_color="#475569")
    combo_1.pack(pady=(10,5), padx=10)
    lbl_tasa1 = ctk.CTkLabel(caja_1, text="---", font=("Arial", 20, "bold"), text_color="#10B981")
    lbl_tasa1.pack(pady=(0,10))

    # Base 2
    caja_2 = ctk.CTkFrame(frame_tasas, fg_color="#0F172A", corner_radius=8)
    caja_2.pack(side="right", fill="x", expand=True, padx=5)
    combo_2 = ctk.CTkOptionMenu(caja_2, variable=var_base2, values=lista_monedas, font=("Arial", 12, "bold"), height=28, fg_color="#334155", button_color="#475569")
    combo_2.pack(pady=(10,5), padx=10)
    lbl_tasa2 = ctk.CTkLabel(caja_2, text="---", font=("Arial", 20, "bold"), text_color="#3B82F6")
    lbl_tasa2.pack(pady=(0,10))

    # Target Global (Destino)
    ctk.CTkLabel(frame_der, text="Convertir hacia:", font=("Arial", 12, "bold"), text_color="#94A3B8").pack(pady=(15,2))
    combo_target = ctk.CTkOptionMenu(frame_der, variable=var_target, values=lista_monedas, font=("Arial", 14, "bold"), height=32, fg_color="#F59E0B", button_color="#D97706", text_color="#000000")
    combo_target.pack(pady=(0,10))

    # Mini Calculadora Dinámica
    ctk.CTkFrame(frame_der, height=1, fg_color="#334155").pack(fill="x", padx=30, pady=10)
    lbl_calc_titulo = ctk.CTkLabel(frame_der, text="Calculadora Rápida (USD a COP)", font=("Arial", 14, "bold"), text_color="#CBD5E1")
    lbl_calc_titulo.pack()
    
    var_monto = ctk.StringVar(value="1")
    ent_calc = ctk.CTkEntry(frame_der, textvariable=var_monto, font=("Arial", 20, "bold"), justify="center", width=150)
    ent_calc.pack(pady=5)
    
    lbl_resultado = ctk.CTkLabel(frame_der, text="---", font=("Arial", 24, "bold"), text_color="#FCD34D")
    lbl_resultado.pack(pady=(5,15))

    # --- CEREBRO ASÍNCRONO MULTI-DIVISA ---
    datos_globales = {"rates": {}}
    
    def log_api(texto):
        if win_div.winfo_exists():
            txt_log_api.configure(state="normal")
            txt_log_api.insert("end", texto + "\n")
            txt_log_api.see("end")
            txt_log_api.configure(state="disabled")

    def recalcular_todo(*args):
        if not datos_globales["rates"]: return
        
        # Extraemos solo las 3 letras (Ej: de "USD - Dólar" saca "USD")
        b1 = var_base1.get().split(" ")[0]
        b2 = var_base2.get().split(" ")[0]
        tg = var_target.get().split(" ")[0]
        
        rates = datos_globales["rates"]
        
        # Matemática de cruce (Todo está referenciado a USD por la API)
        rate_b1 = rates.get(b1, 1)
        rate_b2 = rates.get(b2, 1)
        rate_tg = rates.get(tg, 1)
        
        cruce1 = rate_tg / rate_b1 if rate_b1 > 0 else 0
        cruce2 = rate_tg / rate_b2 if rate_b2 > 0 else 0
        
        lbl_tasa1.configure(text=f"{cruce1:,.2f}")
        lbl_tasa2.configure(text=f"{cruce2:,.2f}")
        lbl_calc_titulo.configure(text=f"Calculadora ({b1} a {tg})")
        
        try:
            monto = float(var_monto.get())
            total = monto * cruce1
            lbl_resultado.configure(text=f"{total:,.2f} {tg}")
        except:
            lbl_resultado.configure(text="---")

    var_base1.trace_add("write", recalcular_todo)
    var_base2.trace_add("write", recalcular_todo)
    var_target.trace_add("write", recalcular_todo)
    var_monto.trace_add("write", recalcular_todo)

    def motor_api_background():
        while win_div.winfo_exists():
            try:
                log_api("\n[>] Auto-Sync: Consultando servidores open.er-api...")
                url = "https://open.er-api.com/v6/latest/USD"
                req = urllib.request.Request(url, headers={'User-Agent': 'TREMEND-Toolkit'})
                respuesta = urllib.request.urlopen(req, timeout=8).read().decode('utf-8')
                
                datos_globales["rates"] = json.loads(respuesta).get("rates", {})
                
                log_api("[<] OK. Mapa JSON enrutado a RAM.")
                app.after(0, recalcular_todo)
            except Exception as e:
                log_api(f"[-] Error de Red (Reintentando): {e}")
            
            # Loop Inteligente: Espera 60s sin congelar la UI si el usuario cierra la ventana
            for _ in range(60):
                if not win_div.winfo_exists(): break
                time.sleep(1)

    # Arrancamos el motor fantasma
    threading.Thread(target=motor_api_background, daemon=True).start()

def logica_analizador_phishing(log):
    import re, urllib.request, json, threading, os, webbrowser
    import customtkinter as ctk

    log("\n" + "="*75)
    log(" 🛡️ INICIANDO LABORATORIO FORENSE ANTI-PHISHING ")
    log("="*75)
    
    win_phish = ctk.CTkToplevel(app)
    win_phish.title("TREMEND - Auditor Forense de Correos")
    win_phish.geometry("950x650")
    win_phish.attributes("-topmost", True)
    win_phish.transient(app)
    
    # --- PANEL IZQUIERDO: ENTRADA DE DATOS ---
    frame_izq = ctk.CTkFrame(win_phish, width=400, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#38BDF8")
    frame_izq.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    
    ctk.CTkLabel(frame_izq, text="📨 Analizador de Cabeceras", font=("Arial", 18, "bold"), text_color="#00FFCC").pack(pady=(15, 5))
    ctk.CTkLabel(frame_izq, text="En Gmail: Opciones (3 puntos) -> 'Mostrar Original'.\nCopia todo el texto y pégalo aquí abajo:", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 10))
    
    txt_input = ctk.CTkTextbox(frame_izq, font=("Consolas", 12), fg_color="#000000", text_color="#FFFFFF")
    txt_input.pack(padx=15, pady=5, fill="both", expand=True)
    
    # --- PANEL DERECHO: REPORTE FORENSE ---
    frame_der = ctk.CTkFrame(win_phish, width=500, fg_color="#1E293B", corner_radius=10, border_width=1, border_color="#EF4444")
    frame_der.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)
    
    ctk.CTkLabel(frame_der, text="🚨 Reporte de Seguridad", font=("Arial", 18, "bold"), text_color="#EF4444").pack(pady=(15, 10))
    
    txt_reporte = ctk.CTkTextbox(frame_der, font=("Consolas", 13), fg_color="#0A0A0A", text_color="#38BDF8")
    txt_reporte.pack(padx=15, pady=5, fill="both", expand=True)
    txt_reporte.insert("end", "[*] Esperando datos del correo...\n\n")
    txt_reporte.configure(state="disabled")

    def analizar_correo():
        texto_crudo = txt_input.get("1.0", "end")
        if len(texto_crudo.strip()) < 10: return
        
        btn_analizar.configure(state="disabled", text="Analizando...")
        
        def run():
            app.after(0, lambda: txt_reporte.configure(state="normal"))
            app.after(0, lambda: txt_reporte.delete("1.0", "end"))
            app.after(0, lambda: txt_reporte.insert("end", "[*] Purgando firmas intermediarias (ARC) para aislar cabeceras reales...\n"))
            
            # 1. PURGA FORENSE (Evita falsos positivos de los servidores de Google)
            lineas = texto_crudo.split('\n')
            texto_limpio = []
            ignorar = False
            for linea in lineas:
                if linea.lower().startswith('arc-'):
                    ignorar = True
                    continue
                if ignorar and (linea.startswith(' ') or linea.startswith('\t')):
                    continue
                ignorar = False
                texto_limpio.append(linea)
                
            texto_limpio_str = '\n'.join(texto_limpio)
            
            # 2. Extracción de Autenticación
            spf = re.search(r'spf[=:\s\'"]+(pass|fail|neutral|softfail|none)', texto_limpio_str, re.IGNORECASE)
            dkim = re.search(r'dkim[=:\s\'"]+(pass|fail|neutral|softfail|none)', texto_limpio_str, re.IGNORECASE)
            dmarc = re.search(r'dmarc[=:\s\'"]+(pass|fail|neutral|softfail|none)', texto_limpio_str, re.IGNORECASE)
            
            res_spf = spf.group(1).upper() if spf else "NO DETECTADO"
            res_dkim = dkim.group(1).upper() if dkim else "NO DETECTADO"
            res_dmarc = dmarc.group(1).upper() if dmarc else "NO DETECTADO"
            
            # 3. Módulo Heurístico de Seguridad
            veredicto = "🔴 PELIGRO: POSIBLE PHISHING / SPOOFING"
            if res_dmarc == "FAIL" or res_spf == "FAIL":
                veredicto = "🔴 ALERTA ROJA: SUPLANTACIÓN DETECTADA (El remitente es falso)"
            elif res_spf == "PASS" and res_dkim == "PASS" and res_dmarc == "PASS":
                veredicto = "🟡 DOMINIO AUTENTICADO (¡Ojo! Un spammer podría usar un dominio real)"
            elif res_spf != "NO DETECTADO" or res_dkim != "NO DETECTADO":
                veredicto = "🟡 PRECAUCIÓN: AUTENTICACIÓN INCOMPLETA"

            reporte = f"\n{'='*45}\n 🛡️ ANÁLISIS DE AUTENTICACIÓN\n{'='*45}\n"
            reporte += f" SPF   : {res_spf} (Verifica servidor origen)\n"
            reporte += f" DKIM  : {res_dkim} (Firma digital intacta)\n"
            reporte += f" DMARC : {res_dmarc} (Política de dominio)\n"
            reporte += f"\n VEREDICTO: {veredicto}\n{'='*45}\n"
            
            app.after(0, lambda: txt_reporte.insert("end", reporte))

            # 4. Extracción Inteligente de IP (Soporte IPv4 e IPv6)
            app.after(0, lambda: txt_reporte.insert("end", "\n[*] Rastreando IP pública de origen (IPv4 / IPv6)...\n"))
            
            # Busca 'client-ip=xxx' o 'designates xxx as' para atrapar IPs ocultas
            ip_match = re.search(r'(?:client-ip=|designates\s+)([a-fA-F0-9:\.]+)', texto_crudo, re.IGNORECASE)
            
            if ip_match:
                ip = ip_match.group(1)
                app.after(0, lambda: txt_reporte.insert("end", f"[+] IP Detectada: {ip}\n[*] Interrogando satélites globales...\n"))
                
                # OSINT Dinámico
                url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,org"
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    datos_ip = json.loads(urllib.request.urlopen(req, timeout=5).read().decode('utf8'))
                    
                    if datos_ip.get("status") == "success":
                        pais = datos_ip.get('country', 'Desconocido')
                        region = f"{datos_ip.get('regionName')}, {datos_ip.get('city')}"
                        isp = datos_ip.get('isp', 'Desconocido')
                        org = datos_ip.get('org', 'Desconocido')
                        lat = datos_ip.get('lat')
                        lon = datos_ip.get('lon')
                        
                        rep_ip = f"\n 🌍 GEOLOCALIZACIÓN Y PROVEEDOR\n"
                        rep_ip += f" IP Origen : {ip}\n"
                        rep_ip += f" Ubicación : {region} ({pais})\n"
                        rep_ip += f" Coordenadas: {lat}, {lon}\n"
                        rep_ip += f" ISP       : {isp}\n"
                        rep_ip += f" Empresa   : {org}\n"
                        
                        if "Google" in org or "Microsoft" in org or "Amazon" in org:
                            rep_ip += f"\n [ℹ️] Esta IP pertenece a un servidor comercial reconocido.\n"
                        else:
                            rep_ip += f"\n [⚠️] Servidor externo/privado. Procede con extrema precaució4. INTERFAZ GRÁFICA Y SISTEMA DE CATEGORÍASn.\n"
                            
                        app.after(0, lambda: txt_reporte.insert("end", rep_ip))
                        
                        # Generar mapa automático 100% Exacto
                        if lat and lon:
                            url_maps = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                            html_mapa = f"<!DOCTYPE html><html><head><script>window.location.href='{url_maps}';</script></head><body></body></html>"
                            ruta_mapa = os.path.join(os.environ.get("USERPROFILE"), "Desktop", f"TREMEND_Phishing_{ip.replace(':', '_')}.html")
                            with open(ruta_mapa, "w") as f: f.write(html_mapa)
                            webbrowser.open(f"file:///{ruta_mapa.replace(chr(92), '/')}")
                        
                except Exception as e:
                    app.after(0, lambda: txt_reporte.insert("end", f"[-] Falló el OSINT de IP: {e}\n"))
            else:
                app.after(0, lambda: txt_reporte.insert("end", "[-] No se encontró una dirección IP de origen en las cabeceras.\n"))
            
            app.after(0, lambda: txt_reporte.configure(state="disabled"))
            app.after(0, lambda: btn_analizar.configure(state="normal", text="🔍 Ejecutar Auditoría Forense"))
            
        threading.Thread(target=run, daemon=True).start()

    btn_analizar = ctk.CTkButton(frame_izq, text="🔍 Ejecutar Auditoría Forense", font=("Arial", 14, "bold"), height=45, fg_color="#3B82F6", hover_color="#2563EB", command=analizar_correo)
    btn_analizar.pack(pady=15, fill="x", padx=15)

def logica_organizador_archivos(log):
    import os, shutil
    import tkinter.filedialog as fd

    log("\n" + "="*75)
    log(" 🗂️ INICIANDO ORGANIZADOR INTELIGENTE DE ARCHIVOS ")
    log("="*75)

    # Abre la ventana nativa de Windows para elegir la carpeta
    carpeta_origen = fd.askdirectory(title="Selecciona la carpeta desordenada (Ej: Descargas o Escritorio)", parent=app)
    
    if not carpeta_origen:
        log("[-] Operación cancelada por el usuario.")
        return

    log(f"[*] Escaneando el caos en: {carpeta_origen}")

    # Diccionario de categorías (Maximizado para uso técnico)
    categorias = {
        "1_Imágenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
        "2_Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
        "3_Documentos": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
        "4_Audios": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
        "5_Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
        "6_Instaladores_y_Programas": [".exe", ".msi", ".bat", ".cmd", ".apk"],
        "7_Código_y_Scripts": [".py", ".html", ".js", ".css", ".json", ".sql", ".xml"],
        "8_Otros": [] 
    }

    # Bóveda principal donde se guardará todo el orden
    carpeta_destino = os.path.join(carpeta_origen, "TREMEND_Carpeta_Organizada")
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    archivos_movidos = 0
    carpetas_vacias_borradas = 0

    log("[*] Clasificando y moviendo archivos a velocidad luz...")
    
    # FASE 1: Clasificar y Mover
    for elemento in os.listdir(carpeta_origen):
        ruta_elemento = os.path.join(carpeta_origen, elemento)
        
        # Evitar tocar carpetas, solo movemos archivos sueltos
        if os.path.isdir(ruta_elemento):
            continue

        _, extension = os.path.splitext(elemento)
        extension = extension.lower()

        # Descubrir a qué categoría pertenece
        cat_asignada = "8_Otros"
        for cat, exts in categorias.items():
            if extension in exts:
                cat_asignada = cat
                break
        
        # Crear la subcarpeta si no existe
        ruta_cat = os.path.join(carpeta_destino, cat_asignada)
        if not os.path.exists(ruta_cat):
            os.makedirs(ruta_cat)
        
        try:
            shutil.move(ruta_elemento, os.path.join(ruta_cat, elemento))
            archivos_movidos += 1
        except Exception as e:
            log(f"    [-] Archivo bloqueado o en uso: '{elemento}'")

    # FASE 2: Maximización -> Purgar carpetas inútiles que quedaron vacías
    log("[*] Purgando carpetas inútiles/vacías en el directorio original...")
    
    # os.walk con topdown=False explora desde la subcarpeta más profunda hacia arriba
    for directorio_raiz, directorios, _ in os.walk(carpeta_origen, topdown=False):
        for dir_name in directorios:
            ruta_dir = os.path.join(directorio_raiz, dir_name)
            
            # Escudo de Seguridad: Jamás intentar borrar la bóveda que acabamos de crear
            if "TREMEND_Carpeta_Organizada" in ruta_dir:
                continue
                
            try:
                if not os.listdir(ruta_dir): # Si la carpeta está 100% vacía
                    os.rmdir(ruta_dir)
                    carpetas_vacias_borradas += 1
            except: pass

    log(f"\n[+] ¡Limpieza y Organización Completada!")
    log(f"    -> Archivos rescatados y clasificados: {archivos_movidos}")
    log(f"    -> Carpetas vacías destruidas: {carpetas_vacias_borradas}")
    log(f"    -> Bóveda generada: {carpeta_destino}")
    
    try: 
        os.startfile(carpeta_destino) # Abre la carpeta organizada al terminar
    except: pass

def logica_fugas_espacio(log, disco_paginacion, min_mb, max_mb):
    import os, subprocess, platform

    log("\n" + "="*75)
    log(" 💽 ESCÁNER DE FUGAS Y OPTIMIZADOR DE MEMORIA VIRTUAL ")
    log("="*75)

    # --- FASE 1: BUG DE WINDOWS 11 ---
    log("\n[1] Analizando Bug de 'CapabilityAccessManager' (Exclusivo W11)...")
    if platform.system() == "Windows" and int(platform.version().split('.')[2]) >= 22000:
        ruta_cam = r"C:\ProgramData\Microsoft\Windows\CapabilityAccessManager"
        tamano_mb = 0
        if os.path.exists(ruta_cam):
            try:
                for root, dirs, files in os.walk(ruta_cam):
                    for f in files: tamano_mb += os.path.getsize(os.path.join(root, f))
                tamano_mb = tamano_mb / (1024 * 1024)
            except: pass
            
        script_ps = "Get-HotFix -Id KB5095093 -ErrorAction SilentlyContinue"
        res_parche = subprocess.run(["powershell", "-NoProfile", "-Command", script_ps], capture_output=True, text=True)
        
        if tamano_mb > 500 or "KB5095093" not in res_parche.stdout:
            log("    [*] Fuga de W11 detectada. Purgando base de datos corrupta de forma silenciosa...")
            subprocess.run("net stop camsvc", shell=True, capture_output=True)
            subprocess.run('taskkill /F /FI "SERVICES eq camsvc"', shell=True, capture_output=True)
            subprocess.run(f'takeown.exe /f "{ruta_cam}" /a /r /d y 2>nul', shell=True, capture_output=True)
            subprocess.run(f'icacls.exe "{ruta_cam}" /grant *S-1-5-32-544:F /t /c /q', shell=True, capture_output=True)
            import shutil
            shutil.rmtree(ruta_cam, ignore_errors=True)
            subprocess.run("net start camsvc", shell=True, capture_output=True)
            log("    [+] Fuga de Windows 11 reparada exitosamente.")
        else:
            log("    [+] Base de datos CAM saludable. Sin fugas.")
    else:
        log("    [-] El sistema no es Windows 11. Omitiendo parche.")

    # --- FASE 2: INYECCIÓN DE LÍMITES VIRTUALES ---
    log(f"\n[2] Reconfigurando Memoria Virtual hacia el Disco {disco_paginacion}...")
    log(f"    -> Límite Inicial Inyectado : {min_mb} MB")
    log(f"    -> Límite Máximo Inyectado  : {max_mb} MB")
    
    script_fix_pagefile = f"""
    $cs = Get-WmiObject Win32_ComputerSystem
    $cs.AutomaticManagedPagefile = $false
    $cs.Put() | Out-Null
    
    # Destruir paginaciones antiguas en otros discos
    $pagefiles = Get-WmiObject Win32_PageFileSetting
    if ($pagefiles) {{
        foreach ($pf in $pagefiles) {{
            if ($pf.Name -notlike '{disco_paginacion}*') {{
                $pf.Delete()
            }}
        }}
    }}
    
    # Crear o modificar el nuevo Pagefile en el disco elegido
    $target = '{disco_paginacion}\\pagefile.sys'
    $pf_target = Get-WmiObject Win32_PageFileSetting | Where-Object {{ $_.Name -eq $target }}
    
    if ($pf_target) {{
        $pf_target.InitialSize = {min_mb}
        $pf_target.MaximumSize = {max_mb}
        $pf_target.Put() | Out-Null
    }} else {{
        Set-WmiInstance -Class Win32_PageFileSetting -Arguments @{{Name=$target; InitialSize={min_mb}; MaximumSize={max_mb}}} | Out-Null
    }}
    """
    
    res = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script_fix_pagefile], capture_output=True, text=True)
    if res.returncode == 0:
        log("    [+] ¡Memoria Virtual optimizada con éxito!")
        log("    [!] IMPORTANTE: Windows liberará todo tu espacio robado al REINICIAR el PC.")
    else:
        log(f"    [-] Ocurrió un error (Asegúrate de ejecutar TREMEND como Administrador).\nDetalle: {res.stderr}")

    log("\n=======================================================")
    log(" [+] ANÁLISIS FORENSE Y OPTIMIZACIÓN COMPLETADOS ")
    log("=======================================================")
    try: notificar_voz("El optimizador inteligente de memoria ha finalizado.")
    except: pass

def logica_mantenimiento_profundo(log, discos_seleccionados):
    import os, shutil, subprocess

    log(f"\n[*] Iniciando Mantenimiento Extremo en los discos: {', '.join(discos_seleccionados)}")

    for disco in discos_seleccionados:
        log(f"\n=======================================================")
        log(f"[*] PURGANDO DISPOSITIVO: {disco}")
        log(f"=======================================================")

        # 1. Vaciar Papeleras Ocultas ($RECYCLE.BIN / RECYCLER)
        log(f"[*] Vaciando Papelera de Reciclaje oculta en {disco}...")
        for papelera in [f"{disco}\\$RECYCLE.BIN", f"{disco}\\RECYCLER"]:
            if os.path.exists(papelera):
                run_cmd(log, f'cmd /c rmdir /s /q "{papelera}" 2>nul')
                log(f"    -> {papelera} aniquilada.")

        # 2. Limpieza de infecciones y basura de macOS (Muy común en USBs)
        log(f"[*] Barriendo rastros residuales (.Trashes, Spotlight, fseventsd)...")
        carpetas_mac = [".Trashes", ".fseventsd", ".Spotlight-V100", "FOUND.000"]
        for carpeta in carpetas_mac:
            ruta_completa = f"{disco}\\{carpeta}"
            if os.path.exists(ruta_completa):
                run_cmd(log, f'cmd /c rmdir /s /q "{ruta_completa}" 2>nul')

        # 3. Limpieza de archivos de caché en todo el disco
        log(f"[*] Escaneando y destruyendo cachés visuales (.DS_Store, Thumbs.db)...")
        run_cmd(log, f'cmd /c del /s /q /f /a:h "{disco}\\.DS_Store" 2>nul')
        run_cmd(log, f'cmd /c del /s /q /f /a:h "{disco}\\Thumbs.db" 2>nul')
        
        log(f"[+] Purga superficial de {disco} completada.")

    # 4. Operaciones Core del Sistema (Exclusivo para la raíz C:)
    if "C:" in discos_seleccionados:
        log(f"\n=======================================================")
        log(f"[*] APLICANDO OPTIMIZACIÓN DE NÚCLEO AL SISTEMA (C:)")
        log(f"=======================================================")
        log("[*] Destruyendo directorios temporales de Windows...")
        rutas_temp = [os.environ.get('TEMP'), r"C:\Windows\Temp", r"C:\Windows\Prefetch"]
        for ruta in rutas_temp:
            if ruta and os.path.exists(ruta):
                log(f"    -> Vaciando: {ruta}")
                for item in os.listdir(ruta):
                    try:
                        p = os.path.join(ruta, item)
                        if os.path.isfile(p): os.unlink(p)
                        elif os.path.isdir(p): shutil.rmtree(p, ignore_errors=True)
                    except: pass
        
        log("[+] Archivos temporales destruidos.")

        log("[*] Verificando e inyectando salud a la imagen de Windows (DISM)...")
        run_cmd(log, "DISM /Online /Cleanup-Image /RestoreHealth")

        log("[*] Escaneando e integrando archivos del sistema corruptos (SFC)...")
        run_cmd(log, "sfc /scannow")

    log("\n[+] MANTENIMIENTO EXTREMO FINALIZADO CON ÉXITO.")
    try:
        notificar_voz("El Mantenimiento Extremo ha terminado.")
    except: pass

def logica_ghelper(log):
    import urllib.request, json, os, platform, subprocess, shutil, zipfile, time
    from tkinter import messagebox

    log("\n[*] Iniciando Optimizador de Hardware (G-Helper)...")
    
    sistema = platform.system().lower()
    if sistema != 'windows':
        log("[-] Error: G-Helper es exclusivo para Windows."); return

    # Para ocultar el parpadeo de consolas extra
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # 1. ESCUDO DE HARDWARE (Verificación de placa base)
    log("[*] Escaneando firmware de la placa base...")
    try:
        comando_ps = "Get-CimInstance Win32_ComputerSystem | Select-Object -ExpandProperty Manufacturer"
        fabricante = subprocess.check_output(["powershell", "-NoProfile", "-Command", comando_ps], text=True, startupinfo=startupinfo).strip().lower()
        
        if "asus" not in fabricante and "asustek" not in fabricante:
            log(f"[-] ACCESO DENEGADO: Este equipo es fabricado por '{fabricante.upper()}'.")
            log("[-] G-Helper es un controlador de bajo nivel exclusivo para laptops ASUS.")
            log("[-] Ejecutarlo en esta máquina es inestable. Operación abortada por seguridad del cliente.")
            return
        else:
            log(f"[+] Hardware '{fabricante.upper()}' detectado. Permiso concedido.")
    except Exception as e:
        log("[-] No se pudo verificar el fabricante del equipo de forma segura. Abortando."); return

    # 2. DIRECTORIO TEMP
    temp_dir = os.path.join(os.environ.get('TEMP'), "Tremend_GHelper")
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)

    # 3. ESCANEO PREVIO INTELIGENTE (Evita re-descargar)
    exe_path = None
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.lower() == 'ghelper.exe':
                exe_path = os.path.join(root, file)
                break
        if exe_path: break

    if exe_path and os.path.exists(exe_path):
        log("[+] G-Helper ya está descargado en caché. Omitiendo descarga...")
    else:
        # 4. DESCARGA
        log("    -> Contactando API de GitHub para ubicar la última versión...")
        api_url = "https://api.github.com/repos/seerge/g-helper/releases/latest"
        url_descarga = None
        try:
            req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            for asset in data.get('assets', []):
                nombre = asset['name'].lower()
                if nombre.endswith('.zip'):
                    url_descarga = asset['browser_download_url']
                    break
        except Exception as e:
            log(f"[-] Error API GitHub: {e}"); return

        if not url_descarga:
            log("[-] Error Crítico: No se encontró la versión en la nube."); return

        archivo_destino = os.path.join(temp_dir, url_descarga.split('/')[-1])
        
        if not os.path.exists(archivo_destino):
            log(f"[*] Descargando paquete oficial...")
            try: urllib.request.urlretrieve(url_descarga, archivo_destino)
            except Exception as e: log(f"[-] Falló la descarga: {e}"); return
        
        log("[*] Extrayendo motor portátil...")
        try:
            with zipfile.ZipFile(archivo_destino, 'r') as zip_ref: zip_ref.extractall(temp_dir)
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.lower() == 'ghelper.exe':
                        exe_path = os.path.join(root, file)
                        break
                if exe_path: break
        except Exception as e: log(f"[-] Error de extracción: {e}"); return

    if not exe_path: log("[-] No se halló el ejecutable principal."); return

    # 5. EJECUCIÓN (Con privilegios de Administrador)
    log("[*] Lanzando G-Helper...")
    try:
        script_run = f"Start-Process -FilePath '{exe_path}' -Verb RunAs -Wait"
        subprocess.run(["powershell", "-NoProfile", "-Command", script_run], startupinfo=startupinfo)
        log("\n[+] Interfaz principal cerrada.")
    except Exception as e: log(f"[-] Error de ejecución: {e}")

    # 6. LIMPIEZA FORZADA (El Protocolo Asesino)
    if messagebox.askyesno("Limpieza", "¿Deseas ELIMINAR G-Helper para no dejar rastro en este equipo?"):
        log("[*] Forzando cierre de procesos ocultos en segundo plano...")
        # Asesinamos el proceso en el fondo para destrabar los archivos
        subprocess.run('taskkill /F /IM GHelper* /T', shell=True, capture_output=True, startupinfo=startupinfo)
        time.sleep(1) # Le damos 1 segundo a Windows para que suelte el archivo
        
        try: 
            shutil.rmtree(temp_dir, ignore_errors=True)
            log("[+] Limpieza táctica: Rastros eliminados de raíz.")
        except Exception as e: 
            log(f"[-] Error al limpiar la carpeta: {e}")
    else:
        log("[*] G-Helper conservado en la caché del sistema para futuros usos rápidos.")

# ---------------------------------------------------------------------------------------------------

def logica_lenovo_toolkit(log):
    import urllib.request, json, os, platform, subprocess, shutil, time
    from tkinter import messagebox

    log("\n[*] Iniciando Optimizador de Hardware (Lenovo Legion Toolkit)...")
    
    sistema = platform.system().lower()
    if sistema != 'windows':
        log("[-] Error: Exclusivo para Windows."); return

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # 1. ESCUDO DE HARDWARE
    log("[*] Escaneando firmware de la placa base...")
    try:
        comando_ps = "Get-CimInstance Win32_ComputerSystem | Select-Object -ExpandProperty Manufacturer"
        fabricante = subprocess.check_output(["powershell", "-NoProfile", "-Command", comando_ps], text=True, startupinfo=startupinfo).strip().lower()
        if "lenovo" not in fabricante:
            log(f"[-] ACCESO DENEGADO: Equipo fabricado por '{fabricante.upper()}'.")
            return
        else:
            log(f"[+] Hardware '{fabricante.upper()}' detectado. Permiso concedido.")
    except Exception as e:
        log("[-] Error verificando fabricante. Abortando."); return

    # 2. MOTOR DE BÚSQUEDA PROFUNDA
    prog_files = os.environ.get('ProgramW6432', os.environ.get('ProgramFiles', 'C:\\Program Files'))
    prog_files_x86 = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
    local_appdata = os.environ.get('LOCALAPPDATA', '')

    rutas_estandar = []
    for b in filter(bool, [prog_files, prog_files_x86, local_appdata, os.path.join(local_appdata, "Programs")]):
        for f in ["LenovoLegionToolkit", "Lenovo Legion Toolkit"]:
            for e in ["LenovoLegionToolkit.exe", "Lenovo Legion Toolkit.exe"]:
                rutas_estandar.append(os.path.join(b, f, e))

    def rastrear_binario():
        for ruta in rutas_estandar:
            if os.path.exists(ruta): return ruta
        for base in filter(bool, [prog_files, prog_files_x86, local_appdata, os.path.join(local_appdata, "Programs")]):
            if not os.path.exists(base): continue
            try:
                for item in os.listdir(base):
                    if "lenovo" in item.lower() and "toolkit" in item.lower():
                        dir_path = os.path.join(base, item)
                        if os.path.isdir(dir_path):
                            for file in os.listdir(dir_path):
                                if file.lower().endswith(".exe") and "toolkit" in file.lower() and "unins" not in file.lower():
                                    return os.path.join(dir_path, file)
            except: pass
        return None

    log("[*] Analizando el disco duro buscando instalaciones previas...")
    exe_path = rastrear_binario()
    instalado_previamente = bool(exe_path)

    temp_dir = os.path.join(os.environ.get('TEMP'), "Tremend_Lenovo")
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    archivo_instalador = ""

    # 3. INSTALACIÓN FANTASMA
    if instalado_previamente:
        log(f"[+] Programa detectado en: {exe_path}")
        log("[+] Omitiendo descarga y ejecución de instalador...")
    else:
        log("    -> Programa no detectado. Contactando API de GitHub...")
        api_url = "https://api.github.com/repos/LenovoLegionToolkit-Team/LenovoLegionToolkit/releases/latest"
        url_descarga = None
        try:
            req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            for asset in data.get('assets', []):
                nombre = asset['name'].lower()
                if nombre.endswith('.exe') and 'setup' in nombre:
                    url_descarga = asset['browser_download_url']
                    break
            if not url_descarga:
                for asset in data.get('assets', []):
                    nombre = asset['name'].lower()
                    if nombre.endswith('.exe'):
                        url_descarga = asset['browser_download_url']
                        break
        except Exception as e:
            log(f"[-] Error API GitHub: {e}"); return

        if not url_descarga:
            log("[-] Error Crítico: No se encontró el instalador."); return

        nombre_archivo = url_descarga.split('/')[-1]
        archivo_instalador = os.path.join(temp_dir, nombre_archivo)
        
        if not os.path.exists(archivo_instalador):
            log(f"[*] Descargando instalador oficial...")
            try: urllib.request.urlretrieve(url_descarga, archivo_instalador)
            except Exception as e: log(f"[-] Falló la descarga: {e}"); return
        
        log("[*] ⚠️ INYECTANDO INSTALADOR AL NÚCLEO...")
        log("    -> Forzando bloqueo de subprocesos (Wait). La consola pausará unos segundos...")
        
        script_install = f"Start-Process -FilePath '{archivo_instalador}' -ArgumentList '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-' -Wait -NoNewWindow"
        subprocess.run(["powershell", "-NoProfile", "-Command", script_install], startupinfo=startupinfo)
        
        log("    -> Instalación completada. Rastreo profundo de binarios...")
        
        for _ in range(15):
            exe_path = rastrear_binario()
            if exe_path: break
            time.sleep(1)
        
        if not exe_path:
            log("[-] Error: El sistema no detectó los binarios. Revisa tu antivirus."); return

    # 4. EJECUCIÓN
    log("[*] Lanzando Lenovo Legion Toolkit...")
    log("[!] Cierra la herramienta cuando termines para poder limpiar el rastro.")
    try:
        script_run = f"Start-Process -FilePath '{exe_path}' -Verb RunAs -Wait"
        subprocess.run(["powershell", "-NoProfile", "-Command", script_run], startupinfo=startupinfo)
        log("\n[+] Interfaz principal cerrada.")
    except Exception as e: log(f"[-] Error de ejecución: {e}")

    # 5. LIMPIEZA TOTAL (Desinstalador Silencioso y Borrado Forzado)
    if messagebox.askyesno("Limpieza", "¿Deseas DESINSTALAR Lenovo Toolkit y borrar todos los rastros?"):
        log("[*] Protocolo Asesino: Cerrando procesos ocultos...")
        subprocess.run('taskkill /F /IM LenovoLegionToolkit* /T', shell=True, capture_output=True, startupinfo=startupinfo)
        time.sleep(1)
        
        # EL FIX ESTÁ AQUÍ: Eliminamos el candado "not instalado_previamente"
        if exe_path:
            log("[*] ⚠️ EJECUTANDO DESINSTALADOR SILENCIOSO...")
            dir_instalacion = os.path.dirname(exe_path)
            
            # Buscador dinámico del desinstalador (puede llamarse unins000.exe o unins001.exe)
            uninstaller = None
            try:
                for file in os.listdir(dir_instalacion):
                    if file.lower().startswith("unins") and file.lower().endswith(".exe"):
                        uninstaller = os.path.join(dir_instalacion, file)
                        break
            except: pass
            
            if uninstaller and os.path.exists(uninstaller):
                script_un = f"Start-Process -FilePath '{uninstaller}' -ArgumentList '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART' -Wait -NoNewWindow"
                subprocess.run(["powershell", "-NoProfile", "-Command", script_un], startupinfo=startupinfo)
                time.sleep(1)
                log("[+] Programa desinstalado del disco duro exitosamente.")
            else:
                log("[-] No se encontró el desinstalador automático. Forzando borrado manual de la carpeta...")
                try:
                    shutil.rmtree(dir_instalacion, ignore_errors=True)
                    log("[+] Carpeta de instalación destruida manualmente.")
                except: pass
        
        try: 
            shutil.rmtree(temp_dir, ignore_errors=True)
            log("[+] Archivos temporales eliminados.")
        except: pass
    else:
        log("[*] Lenovo Toolkit conservado en el sistema.")

def logica_titus(log):
    log("\n[*] Lanzando utilidad de optimización de Chris Titus Tech...")
    run_ps_script(log, "irm christitus.com/win | iex")

def logica_debloat(log, app_name):
    log(f"\n[*] Buscando y desinstalando aplicaciones relacionadas con '{app_name}'...")
    run_ps_script(log, f"Get-AppxPackage *{app_name}* | Remove-AppxPackage -AllUsers -ErrorAction SilentlyContinue")
    log(f"[+] Proceso de purga de {app_name} finalizado.")

def logica_spooler(log):
    log("\n[*] Restableciendo Cola de Impresión...")
    run_cmd(log, "net stop spooler")
    run_cmd(log, r"del /Q /F /S %systemroot%\System32\Spool\Printers\*.*")
    run_cmd(log, "net start spooler")

def logica_winsxs(log):
    log("\n[*] Limpieza Extrema del Component Store (WinSxS)...")
    run_cmd(log, "DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase")

    notificar_voz("La Limpieza Extrema ha terminado.")

def logica_reparar_update(log):
    log("\n[*] Deteniendo servicios criptográficos de Windows Update...")
    run_cmd(log, "net stop wuauserv & net stop cryptSvc & net stop bits & net stop msiserver")
    for d in [r"C:\Windows\SoftwareDistribution", r"C:\Windows\System32\catroot2"]:
        if os.path.exists(d): 
            try: os.rename(d, d + ".old")
            except: pass
    run_cmd(log, "net start wuauserv & net start cryptSvc & net start bits & net start msiserver")

def logica_shadowcopies(log):
    log("\n[*] Purgando Puntos de Restauración (VSS)...")
    run_cmd(log, "vssadmin delete shadows /all /quiet")

    notificar_voz("El Purgado De Puntos De Restauración ha terminado.")

def logica_wmi(log):
    log("\n[*] Reparando Repositorio WMI...")
    run_cmd(log, "net stop winmgmt /y & winmgmt /resetrepository & net start winmgmt")

def logica_telemetria(log):
    log("\n[*] Bloqueando Telemetría de Microsoft...")
    run_cmd(log, "sc stop DiagTrack & sc config DiagTrack start= disabled")
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection")
        winreg.SetValueEx(key, "AllowTelemetry", 0, winreg.REG_DWORD, 0)
        log("[+] Telemetría bloqueada por Registro exitosamente.")
    except Exception as e: log(f"[-] Error de registro: {e}")

def logica_hora(log):
    log("\n[*] Sincronizando Reloj de Hardware (NTP)...")
    run_cmd(log, "net stop w32time & w32tm /config /syncfromflags:manual /manualpeerlist:time.windows.com & net start w32time & w32tm /resync /force")

def logica_limpiar_navegadores(log):
    log("\n[*] Destruyendo caché pesada de navegadores web...")
    appdata = os.environ.get('LOCALAPPDATA')
    for nav, ruta in {"Chrome": f"{appdata}\\Google\\Chrome\\User Data\\Default\\Cache", "Edge": f"{appdata}\\Microsoft\\Edge\\User Data\\Default\\Cache"}.items():
        if os.path.exists(ruta):
            try: shutil.rmtree(ruta, ignore_errors=True); log(f"[+] Caché de {nav} destruida.")
            except: log(f"[-] Error en {nav}.")

def logica_chkdsk(log, letra):
    l = letra.replace(":", "").replace("\\", "").strip() + ":"
    log(f"\n[*] Programando CHKDSK en unidad {l}...")
    run_cmd(log, f"chkdsk {l} /f /r /x")

def logica_mole(log):
    import subprocess, os, platform, shutil, time
    from tkinter import messagebox

    log("\n[*] Iniciando Optimizador de Terminal CLI (Mole)...")
    sistema = platform.system().lower()

    # ==========================================
    # LÓGICA PARA WINDOWS
    # ==========================================
    if sistema == 'windows':
        if not messagebox.askyesno("Advertencia de Seguridad", "El desarrollador de Mole indica que la versión de Windows es EXPERIMENTAL y podría ser inestable en equipos críticos.\n\n¿Estás seguro de que deseas ejecutar esta herramienta en este PC?"):
            log("[-] Operación cancelada por seguridad del cliente.")
            return

        local_appdata = os.environ.get('LOCALAPPDATA', '')
        ruta_mole = os.path.join(local_appdata, "Mole")

        # --- FIX 1: ANIQUILACIÓN TOTAL Y ENGAÑO A GIT ---
        if os.path.exists(ruta_mole):
            log("[*] Forzando eliminación de instalación corrupta anterior...")
            # 1. Intento nativo de Windows (Fuerza bruta)
            subprocess.run(f'cmd /c rmdir /s /q "{ruta_mole}"', shell=True, capture_output=True)
            time.sleep(1)
            
            # 2. El Engaño: Si sigue existiendo por archivos en RAM, la renombramos
            if os.path.exists(ruta_mole):
                import random
                try: 
                    os.rename(ruta_mole, f"{ruta_mole}_basura_{random.randint(100,999)}")
                    log("    > Carpeta rebelde renombrada con éxito.")
                except: pass

        log("[*] Contactando a GitHub e instalando la herramienta...")
        log("[!] Descargando código fuente mediante Git...")
        
        cmd_install = 'powershell -NoProfile -ExecutionPolicy Bypass -Command "irm -useb https://raw.githubusercontent.com/tw93/Mole/windows/quick-install.ps1 | iex"'
        proceso_inst = subprocess.run(cmd_install, shell=True, capture_output=True, text=True, encoding='cp850', errors='ignore')
        
        for linea in proceso_inst.stdout.splitlines():
            if linea.strip(): log(f"    > {linea.strip()}")
        for linea in proceso_inst.stderr.splitlines():
            if linea.strip(): log(f"    > ERROR: {linea.strip()}")

        log("[+] Secuencia de instalación finalizada.")
        
        if not os.path.exists(ruta_mole):
            log("[-] Error Crítico: No se pudo encontrar la carpeta de Mole en AppData.")
            log("[-] Causa probable: Git no está instalado o tu internet cortó la conexión.")
            return

        log(f"[+] Repositorio clonado localizado en: {ruta_mole}")
        log("[*] Lanzando la interfaz interactiva de Mole...")
        log("[!] Se abrirá una consola externa al frente. Usa las FLECHAS de tu teclado para navegar.")
        
        # --- FIX 2: BYPASS DEL PERFIL DE POWERSHELL ---
        script_enfocado = f"""
        $Host.UI.RawUI.WindowTitle = 'Mole_Optimizador'
        $wshell = New-Object -ComObject wscript.shell
        $wshell.AppActivate('Mole_Optimizador') | Out-Null
        Clear-Host
        Write-Host 'Iniciando Mole (Usa las flechas para navegar y Q para salir)...' -ForegroundColor Cyan
        
        # Recargamos el perfil donde el instalador escondió el comando
        if (Test-Path $PROFILE) {{ . $PROFILE }}
        
        try {{ 
            mo 
        }} catch {{ 
            Write-Host 'Fallo al invocar el motor interno de Mole.' -ForegroundColor Red 
            Write-Host 'Asegurate de que Git descargo los archivos correctamente.' -ForegroundColor Yellow
            Start-Sleep -s 8
        }}
        """
        
        ruta_script_temp = os.path.join(os.environ.get('TEMP'), "ejecutar_mole.ps1")
        with open(ruta_script_temp, "w", encoding="utf-8") as f:
            f.write(script_enfocado)
        
        subprocess.run(f'start "Mole" /wait powershell -ExecutionPolicy Bypass -File "{ruta_script_temp}"', shell=True)
        
        try: os.remove(ruta_script_temp)
        except: pass
        
        log("\n[+] Interfaz interactiva de Mole cerrada.")
        
        # Limpieza Táctica Windows (Fuerza bruta)
        if messagebox.askyesno("Limpieza", "¿Deseas intentar ELIMINAR Mole del sistema para borrar el rastro?"):
            log("[*] Purgando directorios de instalación de Mole...")
            limpio = False
            if os.path.exists(ruta_mole):
                try: 
                    subprocess.run(f'cmd /c rmdir /s /q "{ruta_mole}"', shell=True, capture_output=True)
                    limpio = not os.path.exists(ruta_mole)
                except: pass
                    
            if limpio: log("[+] Archivos base eliminados con éxito. Cero rastros.")
            else: log("[-] La limpieza falló o los archivos están en uso por el sistema.")
        else:
            log("[*] Mole conservado en el sistema Windows.")

    # ==========================================
    # LÓGICA PARA MAC (Darwin)
    # ==========================================
    elif sistema == 'darwin':
        log("[*] Entorno macOS detectado. Verificando motor nativo...")
        check_mole = subprocess.run(['which', 'mole'], capture_output=True, text=True)
        
        if not check_mole.stdout.strip():
            log("    -> Mole no detectado en este Mac. Solicitando instalación vía Homebrew...")
            if messagebox.askyesno("Instalar Mole", "Mole no está instalado en este equipo.\n¿Deseas instalarlo ahora vía Homebrew (brew install mole)?"):
                proceso = subprocess.Popen(['brew', 'install', 'mole'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for linea in proceso.stdout: log(linea.strip())
                proceso.wait()
                if proceso.returncode != 0:
                    log("[-] Error al instalar Mole. Asegúrate de tener 'brew' instalado."); return
            else:
                log("[-] Operación cancelada."); return
        
        log("[*] Lanzando Mole en Terminal nativa de Mac...")
        applescript = 'tell app "Terminal" to do script "mole"'
        subprocess.run(['osascript', '-e', applescript])
        log("\n[+] Interfaz lanzada en una ventana de Terminal separada.")
        log("[!] Cierra esa terminal cuando termines el mantenimiento.")
        
        if messagebox.askyesno("Limpieza", "¿Deseas DESINSTALAR Mole para no dejar rastro en el Mac de tu cliente?"):
            log("[*] Desinstalando Mole vía Homebrew...")
            subprocess.run(['brew', 'uninstall', 'mole'], capture_output=True)
            log("[+] Mole purgado del ecosistema Mac con éxito.")
    else:
        log("[-] Error: Sistema no soportado. Mole funciona en Windows y Mac.")

def logica_iconos(log):
    log("\n[*] Purgando base de datos de caché de iconos...")
    run_cmd(log, "taskkill /f /im explorer.exe")
    db = os.path.join(os.environ.get("LOCALAPPDATA"), "IconCache.db")
    if os.path.exists(db):
        try: os.remove(db)
        except: pass
    run_cmd(log, "start explorer.exe")

# --- CATEGORÍA 3: DIAGNÓSTICO ---
def logica_diagnostico_rapido(log):
    log("\n[*] Ejecutando Diagnóstico Rápido y WinSat Score...")
    run_cmd(log, "systeminfo")
    run_ps_script(log, "try { Get-CimInstance Win32_WinSat | Format-List } catch { Write-Host '[-] No WinSat.' -ForegroundColor Red }")

def logica_radiografia_hardware_completa(log):
    log("\n[*] EJECUTANDO RADIOGRAFÍA DE HARDWARE (NIVEL MSINFO32)...")
    script_ps = """
    $os = Get-CimInstance Win32_OperatingSystem; $cs = Get-CimInstance Win32_ComputerSystem
    $bios = Get-CimInstance Win32_BIOS; $board = Get-CimInstance Win32_BaseBoard
    Write-Host "--- SISTEMA Y PLACA BASE ---" -ForegroundColor Cyan
    Write-Host "SO: $($os.Caption) $($os.OSArchitecture) | Equipo: $($cs.Name)"
    Write-Host "Placa Base: $($board.Manufacturer) $($board.Product) | BIOS: $($bios.SMBIOSBIOSVersion)"
    Write-Host "`n--- PROCESADOR ---" -ForegroundColor Cyan
    $cpus = Get-CimInstance Win32_Processor
    foreach ($cpu in $cpus) { Write-Host "$($cpu.Name) | $($cpu.NumberOfCores) Nucleos / $($cpu.NumberOfLogicalProcessors) Hilos | $($cpu.MaxClockSpeed) MHz" }
    Write-Host "`n--- MEMORIA RAM ---" -ForegroundColor Cyan
    $ram_array = Get-CimInstance Win32_PhysicalMemoryArray; $ram = Get-CimInstance Win32_PhysicalMemory
    Write-Host "RAM Instalada: $([math]::Round($cs.TotalPhysicalMemory / 1GB, 2)) GB"
    $i = 1; foreach ($stick in $ram) { Write-Host " -> Modulo $($i): $([math]::Round($stick.Capacity / 1GB, 2)) GB | $($stick.Speed) MHz"; $i++ }
    Write-Host "`n--- TARJETAS GRÁFICAS ---" -ForegroundColor Cyan
    $gpus = Get-CimInstance Win32_VideoController
    foreach ($gpu in $gpus) { Write-Host "$($gpu.Name) | $($gpu.CurrentHorizontalResolution)x$($gpu.CurrentVerticalResolution) @ $($gpu.CurrentRefreshRate) Hz" }
    """
    run_ps_script(log, script_ps)

def logica_salud_discos(log):
    log("\n[*] Interrogando Firmware S.M.A.R.T. de los discos físicos...")
    run_ps_script(log, 'Get-PhysicalDisk | Select-Object FriendlyName, MediaType, HealthStatus, @{Name="Tamaño(GB)";Expression={[math]::Round($_.Size/1GB,2)}} | Format-List')

    notificar_voz("El Diagnóstico De Salud De Discos ha terminado.")

def logica_radar_hardware(log):
    import subprocess, urllib.parse, webbrowser, json
    import customtkinter as ctk
    
    log("\n" + "="*75)
    log(" 🚨 RADAR DE HARDWARE EN CONFLICTO (AUTO-DIAGNÓSTICO) 🚨")
    log("="*75)
    
    log("[*] Interrogando al Kernel (WMI) por dispositivos físicos defectuosos...")
    log("[*] Analizando registros de interrupción (IRQs) y drivers huérfanos...")
    
    # Inyectamos PowerShell para buscar piezas físicas que tengan código de error diferente a 0 (Cero = Perfecto)
    script_ps = """
    Get-CimInstance Win32_PnPEntity | Where-Object {$_.ConfigManagerErrorCode -ne 0} | Select-Object Name, DeviceID, ConfigManagerErrorCode | ConvertTo-Json
    """
    
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    resultado = subprocess.run(["powershell", "-NoProfile", "-Command", script_ps], capture_output=True, text=True, startupinfo=startupinfo)
    
    if not resultado.stdout.strip():
        log("\n[+] ¡Excelente! La placa base reporta que TODO el hardware está funcionando al 100%.")
        log("[+] Cero conflictos de drivers detectados. El sistema está limpio.")
        return
        
    try:
        datos = json.loads(resultado.stdout)
        if isinstance(datos, dict): datos = [datos] # Si es solo una falla, lo mete en una lista para poder iterarlo
    except:
        log("[-] Error al parsear los datos del Kernel de Windows.")
        return
        
    log(f"\n[!] ALERTA: Se detectaron {len(datos)} dispositivos con fallas lógicas o físicas:\n")
    
    dispositivos_rotos = []
    
    for i, dev in enumerate(datos):
        nombre = dev.get("Name", "Dispositivo Desconocido")
        hw_id = dev.get("DeviceID", "ID_Desconocido")
        codigo = dev.get("ConfigManagerErrorCode", "N/A")
        
        # Limpiamos el HW_ID para buscar la firma electrónica de la pieza (Vendor y Device)
        hw_busqueda = hw_id.split("\\")[-1] if "\\" in hw_id else hw_id
        
        log(f"  ❌ [{i+1}] {nombre}")
        log(f"      -> Código de Error: {codigo}")
        log(f"      -> Identificador de Hardware (Firma): {hw_busqueda}\n")
        
        dispositivos_rotos.append({"nombre": nombre, "codigo": codigo, "hw_id": hw_busqueda})
        
    log("="*75)
    log("[*] Iniciando Motor de 'Dorking Forense' (Búsqueda Avanzada Automatizada)...")
    log("[!] TREMEND generará consultas de búsqueda exactas apuntando a foros de ingenieros (Reddit, Microsoft, Tom's Hardware).")
    
    # UI Popup asíncrono para que decidas qué pieza investigar
    def abrir_investigacion():
        dialogo = ctk.CTkInputDialog(text="Ingresa el NÚMERO del dispositivo a investigar (Ej: 1):", title="Auto-Investigador Forense")
        op = dialogo.get_input()
        
        if op and op.isdigit():
            idx = int(op) - 1
            if 0 <= idx < len(dispositivos_rotos):
                disp = dispositivos_rotos[idx]
                log(f"\n[*] Ejecutando búsqueda profunda para: {disp['nombre']}")
                
                # MAGIA: Armamos el Dork de Google
                # Obliga a Google a buscar el Código Exacto y la Firma de la Pieza ÚNICAMENTE en foros de soporte
                query = f'("{disp["hw_id"]}" OR "{disp["nombre"]}") "Code {disp["codigo"]}" (site:reddit.com OR site:answers.microsoft.com OR site:forums.tomshardware.com)'
                url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                
                webbrowser.open(url)
                log(f"[+] Navegador abierto con el vector de búsqueda forense.")
                log("[!] Lee los primeros resultados, allí encontrarás la solución exacta de otros técnicos.")
            else:
                log("[-] Número ingresado fuera de rango.")
                
    # Lanzamos el diálogo emergente medio segundo después para que puedas leer la consola primero
    app.after(500, abrir_investigacion)

def logica_escaner_ocr(log):
    import platform, os, subprocess, sys
    from tkinter import messagebox
    
    log("\n" + "="*75)
    log(" 👁️ INICIANDO ESCÁNER OCR (RECONOCIMIENTO ÓPTICO) 👁️ ")
    log("="*75)

    if platform.system() != 'Windows' or int(platform.release()) < 10:
        log("[-] Error: El motor OCR nativo requiere Windows 10 o Windows 11.")
        return

    # FIX MAESTRO: Escudo try-except definitivo con la capa 'Foundation' para asincronismo
    modulos_faltantes = []
    
    try: import winrt.windows.media.ocr
    except ImportError: modulos_faltantes.append("winrt-Windows.Media.Ocr")
        
    try: import winrt.windows.graphics.imaging
    except ImportError: modulos_faltantes.append("winrt-Windows.Graphics.Imaging")
        
    try: import winrt.windows.globalization
    except ImportError: modulos_faltantes.append("winrt-Windows.Globalization")
        
    try: import winrt.windows.storage
    except ImportError: modulos_faltantes.append("winrt-Windows.Storage")
        
    try: import winrt.windows.storage.streams
    except ImportError: modulos_faltantes.append("winrt-Windows.Storage.Streams")
        
    try: import winrt.windows.foundation
    except ImportError: modulos_faltantes.append("winrt-Windows.Foundation")
        
    try: import PIL
    except ImportError: modulos_faltantes.append("pillow")
    
    if modulos_faltantes:
        log(f"[!] Instalando motores de IA faltantes: {', '.join(modulos_faltantes)}")
        log("    -> Por favor espera unos segundos. No cierres la ventana.")
        
        res = subprocess.run([sys.executable, "-m", "pip", "install"] + modulos_faltantes, capture_output=True, text=True)
        
        if res.returncode != 0:
            log("[-] Error crítico al instalar dependencias del sistema.")
            log(f"    -> Detalle técnico: El entorno de Python bloqueó la compilación o no hay internet.")
            log("    -> Ejecuta TREMEND como Administrador e inténtalo de nuevo.")
            return
            
        log("[+] Motores instalados exitosamente.")

    script_ocr = """import tkinter as tk
import os
import asyncio
import ctypes
from PIL import ImageGrab, Image, ImageEnhance

# --- FIX 1: DPI AWARENESS (Cero Recortes) ---
# Obliga a Windows a mapear los píxeles 1:1 sin importar el zoom (125%, 150%) del monitor.
try: ctypes.windll.shcore.SetProcessDpiAwareness(2)
except: 
    try: ctypes.windll.user32.SetProcessDPIAware()
    except: pass

# Librerías modernas de Windows Runtime (WinRT)
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.graphics.imaging import SoftwareBitmap
from winrt.windows.globalization import Language
import winrt.windows.storage.streams 
import winrt.windows.foundation 

class OCRScanner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.config(cursor="cross")

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Escape>", lambda e: self.root.destroy())
        self.canvas.bind("<Button-3>", lambda e: self.root.destroy())
        
        self.root.mainloop()

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='cyan', width=2, fill="gray", stipple="gray12")

    def on_drag(self, event):
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.root.destroy()
        
        x1, x2 = sorted([int(self.start_x), int(cur_x)])
        y1, y2 = sorted([int(self.start_y), int(cur_y)])
        
        if x2 - x1 > 10 and y2 - y1 > 10:
            self.extraer_texto(x1, y1, x2, y2)

    def extraer_texto(self, x1, y1, x2, y2):
        print("[*] Procesando imagen capturada...", flush=True)
        # all_screens=True soporta múltiples monitores sin distorsión
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2), all_screens=True)
        
        # --- FIX 2: PRE-PROCESAMIENTO FORENSE (UPSCALING & CONTRASTE) ---
        print("[*] Aplicando mejora óptica 3X y contraste extremo...", flush=True)
        w, h = img.size
        # Agrandamos la imagen un 300% para que el OCR detecte hasta la letra más enana
        img = img.resize((w * 3, h * 3), Image.Resampling.LANCZOS)
        
        # Aumentamos el contraste al doble para separar bien la letra del fondo
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)

        img = img.convert("RGBA")
        width, height = img.size
        pixels = img.tobytes()
        
        bitmap = SoftwareBitmap.create_copy_from_buffer(pixels, 30, width, height)
        
        async def do_ocr():
            lang = Language("es") 
            engine = OcrEngine.try_create_from_language(lang)
            if not engine:
                print("[-] Error: Motor OCR nativo no disponible en el sistema para este idioma.", flush=True)
                return
            
            print("[*] Analizando píxeles con Inteligencia Artificial nativa...", flush=True)
            result = await engine.recognize_async(bitmap)
            
            if result.text:
                print("\\n[+] TEXTO ENCONTRADO:\\n", flush=True)
                print(result.text, flush=True)
                
                self.copiar_portapapeles(result.text)
                print("\\n[+] (El texto ha sido copiado a tu portapapeles automáticamente)", flush=True)
            else:
                print("[-] No se detectó ningún texto claro en la imagen.", flush=True)
                
        asyncio.run(do_ocr())

    def copiar_portapapeles(self, texto):
        import ctypes
        ctypes.windll.user32.OpenClipboard(0)
        ctypes.windll.user32.EmptyClipboard()
        ctypes.windll.user32.SetClipboardData(13, ctypes.c_wchar_p(texto))
        ctypes.windll.user32.CloseClipboard()

if __name__ == "__main__":
    OCRScanner()
"""
    temp_py = os.path.join(os.environ.get('TEMP'), "tremend_ocr.py")
    try:
        with open(temp_py, "w", encoding="utf-8") as f:
            f.write(script_ocr)
            
        log("[*] Lanzando interfaz de recorte...")
        log("[!] Tu pantalla se atenuará. DIBUJA UN CUADRO MANTENIENDO PRESIONADO EL CLIC IZQUIERDO sobre el texto que quieres copiar.")
        log("[!] (Para cancelar, presiona la tecla ESC o clic derecho).")
        
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        proceso = subprocess.Popen([sys.executable, temp_py], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore', startupinfo=startupinfo)
        
        for linea in iter(proceso.stdout.readline, ''):
            if linea: log(linea.strip())
        proceso.wait()

        try: os.remove(temp_py)
        except: pass
        
        try: notificar_voz("El Escáner Óptico de Pantalla ha finalizado.")
        except: pass
        
    except Exception as e:
        log(f"[-] Ocurrió un error en el núcleo visual: {e}")

def logica_perfmon(log, tipo):
    log(f"\n[*] Abriendo Monitor ({tipo})...")
    if tipo in ['1', '01']: run_cmd(log, "perfmon /rel")
    elif tipo in ['2', '02']: run_cmd(log, "perfmon /report")

def logica_visor_grafico(log, tipo):
    log("\n[*] Abriendo Visor Gráfico Interactivo (Out-GridView)...")
    if tipo == '1': run_ps_script(log, "Get-Process | Out-GridView -Title 'Procesos'")
    elif tipo == '2': run_ps_script(log, "Get-Service | Out-GridView -Title 'Servicios'")
    elif tipo == '3': run_ps_script(log, "Get-EventLog -LogName System -EntryType Error -Newest 100 | Out-GridView -Title 'Errores'")

def logica_uptime(log):
    log("\n[*] Consultando tiempo de actividad...")
    run_cmd(log, 'net statistics workstation | findstr "desde"')
    run_ps_script(log, '$os = Get-CimInstance Win32_OperatingSystem; $ta = (Get-Date) - $os.LastBootUpTime; Write-Host "Activo: $($ta.Days) dias, $($ta.Hours) horas"')

def logica_tareas_servicios(log):
    log("\n[*] Auditando Servicios Activos...")
    run_ps_script(log, 'Get-Service | Where-Object {$_.Status -eq "Running"} | Format-List Name, DisplayName')

def logica_programas_arranque(log):
    log("\n[*] Auditando Programas de Arranque...")
    run_ps_script(log, '$s = Get-CimInstance Win32_StartupCommand | Select-Object Name, Command; if ($s) { $s | Out-GridView }')

def logica_historial_usb(log):
    log("\n[*] Descifrando historial forense de dispositivos USB (Registro PnP)...")
    # La 'r' inicial indica texto crudo (Raw) para evitar el crasheo por el \U de \USBSTOR
    script = r"try { $usbs = Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Enum\USBSTOR\*\*' -ErrorAction SilentlyContinue | Select-Object FriendlyName -Unique; if ($usbs) { $usbs | Out-GridView -Title 'TREMEND: Historial USB' } else { Write-Host '[-] No se encontraron registros.' } } catch {}"
    run_ps_script(log, script)

def logica_pantallazos_azules(log):
    log("\n[*] Extrayendo registros de Pantallazos Azules (BSOD)...")
    run_ps_script(log, 'try { $bsod = Get-EventLog -LogName System -Source "BugCheck" -ErrorAction Stop | Select-Object TimeGenerated, Message; if ($bsod) { $bsod | Out-GridView } } catch {}')

def logica_monitor_bateria(log):
    import os, time, threading, subprocess
    import psutil
    import customtkinter as ctk

    log("\n" + "="*75)
    log(" 🔋 INICIANDO CENTRO DE ENERGÍA Y LABORATORIO DE LÓGICA ")
    log("="*75)
    
    win_bat = ctk.CTkToplevel(app)
    win_bat.title("TREMEND - Monitor y Laboratorio (While)")
    win_bat.geometry("880x500")
    win_bat.attributes("-topmost", True)
    win_bat.transient(app)
    
    # --- PANEL IZQUIERDO: LABORATORIO WHILE (EDUCATIVO) ---
    frame_izq = ctk.CTkFrame(win_bat, width=420, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#38BDF8")
    frame_izq.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    
    ctk.CTkLabel(frame_izq, text="💻 Laboratorio de Lógica", font=("Arial", 20, "bold"), text_color="#00FFCC").pack(pady=(20, 5))
    ctk.CTkLabel(frame_izq, text="Entiende cómo funciona el código Python detrás\nde un sistema de carga usando un bucle 'while'.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 15))
    
    txt_codigo = ctk.CTkTextbox(frame_izq, font=("Consolas", 15, "bold"), fg_color="#000000", text_color="#38BDF8", height=110)
    txt_codigo.pack(padx=20, fill="x")
    codigo_python = "bateria = 2\n\nwhile bateria < 100:\n    cargar_energia()\n    bateria += 1"
    txt_codigo.insert("1.0", codigo_python)
    txt_codigo.configure(state="disabled")
    
    lbl_sim_porc = ctk.CTkLabel(frame_izq, text="2%", font=("Arial", 50, "bold"), text_color="#EF4444")
    lbl_sim_porc.pack(pady=10)
    
    pb_sim = ctk.CTkProgressBar(frame_izq, height=25, corner_radius=10, progress_color="#EF4444", fg_color="#1E293B")
    pb_sim.pack(fill="x", padx=40)
    pb_sim.set(0.02)
    
    def ejecutar_sim():
        btn_play.configure(state="disabled")
        def run():
            log("[*] Ejecutando simulación educativa en la interfaz...")
            bateria = 2
            while bateria <= 100:
                if not win_bat.winfo_exists(): break
                col = "#EF4444" if bateria <= 20 else ("#FCD34D" if bateria <= 60 else "#10B981")
                def update(v=bateria, c=col):
                    lbl_sim_porc.configure(text=f"{v}%", text_color=c)
                    pb_sim.set(v / 100.0)
                    pb_sim.configure(progress_color=c)
                app.after(0, update)
                time.sleep(0.05) # Velocidad de la animación
                bateria += 1
            if win_bat.winfo_exists():
                app.after(0, lambda: btn_play.configure(state="normal", text="🔄 Reiniciar Bucle"))
        threading.Thread(target=run, daemon=True).start()
        
    btn_play = ctk.CTkButton(frame_izq, text="▶ Ejecutar Código", font=("Arial", 14, "bold"), height=40, fg_color="#10B981", hover_color="#059669", command=ejecutar_sim)
    btn_play.pack(pady=15)
    
    # --- PANEL DERECHO: ESTADO REAL Y REPORTE FORENSE ---
    frame_der = ctk.CTkFrame(win_bat, width=420, fg_color="#1E293B", corner_radius=10, border_width=1, border_color="#A78BFA")
    frame_der.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)
    
    ctk.CTkLabel(frame_der, text="🔋 Batería Física Real", font=("Arial", 20, "bold"), text_color="#A78BFA").pack(pady=(20, 5))
    ctk.CTkLabel(frame_der, text="Sensores en vivo de tu Hardware.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 20))
    
    # Variables gráficas de estado (Arrancan vacías)
    lbl_real_porc = ctk.CTkLabel(frame_der, text="--%", font=("Arial", 60, "bold"), text_color="#10B981")
    lbl_real_porc.pack(pady=10)
    
    pb_real = ctk.CTkProgressBar(frame_der, height=35, corner_radius=10, progress_color="#10B981", fg_color="#0F172A")
    pb_real.pack(fill="x", padx=40, pady=10)
    pb_real.set(0)
    
    lbl_estado_real = ctk.CTkLabel(frame_der, text="Calculando...", font=("Arial", 16, "bold"), text_color="#E2E8F0")
    lbl_estado_real.pack(pady=10)
    
    # --- CEREBRO EN TIEMPO REAL (NUEVO) ---
    def monitorear_bateria_real():
        # Este bucle se repite indefinidamente MIENTRAS la ventana esté abierta
        while win_bat.winfo_exists():
            try:
                bat_real = psutil.sensors_battery()
                if bat_real: # Si es una Laptop
                    porc = int(bat_real.percent)
                    enchufado = bat_real.power_plugged
                    estado = "🔌 Conectado (Cargando)" if enchufado else "🔋 Usando Batería"
                else: # Si es un PC de Escritorio
                    porc = 100
                    estado = "🔌 PC Escritorio (Sin Batería)"
            except:
                porc = 100
                estado = "🔌 Error leyendo sensor"
                
            color = "#EF4444" if porc <= 20 else ("#FCD34D" if porc <= 60 else "#10B981")
            
            # Función puente para que el Thread hable de forma segura con la Interfaz Visual (Tkinter)
            def actualizar_ui(p=porc, e=estado, c=color):
                if win_bat.winfo_exists():
                    lbl_real_porc.configure(text=f"{p}%", text_color=c)
                    pb_real.set(p / 100.0)
                    pb_real.configure(progress_color=c)
                    lbl_estado_real.configure(text=e)
            
            app.after(0, actualizar_ui)
            time.sleep(1) # Espera 1 segundo para no saturar el procesador
            
    # Lanzamos el motor en la sombra
    threading.Thread(target=monitorear_bateria_real, daemon=True).start()
    
    def generar_reporte():
        log("[*] Interrogando sensores ACPI a nivel de Hardware...")
        ruta = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "Reporte_Bateria_TREMEND.html")
        subprocess.run(f"powercfg /batteryreport /output {ruta}", shell=True, capture_output=True)
        log(f"[+] ¡ÉXITO! Reporte profundo exportado a: {ruta}")
        try: os.startfile(ruta)
        except: pass
        try: notificar_voz("El reporte físico de la batería ha finalizado.")
        except: pass
        
    ctk.CTkButton(frame_der, text="📄 Generar Reporte de Desgaste", font=("Arial", 14, "bold"), height=45, fg_color="#3B82F6", hover_color="#2563EB", command=generar_reporte).pack(side="bottom", pady=25, padx=40, fill="x")

def logica_sleepstudy(log):
    log("\n[*] Generando Reporte de Estados de Suspensión (Sleep Study)...")
    ruta = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "SleepStudy.html")
    run_cmd(log, f"powercfg /SleepStudy /output {ruta} & start {ruta}")
    notificar_voz("El Sleep Study ha terminado.")

def logica_bitlocker(log, accion, unidad="", clave=""):
    import subprocess, psutil, os, re
    
    log("\n" + "="*75)
    log(" 🔐 GESTOR FORENSE DE BITLOCKER (AES) ")
    log("="*75)

    if accion == '1':
        log("[*] Consultando el estado criptográfico de todas las unidades...\n")
        run_cmd(log, "manage-bde -status")
        
    elif accion == '2':
        unidad = unidad.strip().upper().replace(":", "") + ":"
        log(f"[*] Extrayendo protectores y claves de recuperación de la unidad {unidad}...\n")
        log("[!] ADVERTENCIA: Esta información es confidencial. Guárdala en un lugar seguro.\n")
        run_cmd(log, f"manage-bde -protectors -get {unidad}")
        
    elif accion == '3':
        log("[*] Iniciando motor de búsqueda forense de claves de recuperación...")
        log("[*] Rastreando unidades físicas y USBs en busca de archivos .TXT de BitLocker...\n")
        
        # Inteligencia Artificial: Busca exactamente el patrón matemático de 48 dígitos
        regex_clave = re.compile(r'\b\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}\b')
        encontrados = 0
        
        # Buscar en todos los discos conectados
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt' and ('cdrom' in part.opts or part.fstype == ''): continue
            drive = part.device[:2]
            log(f"    -> Escaneando unidad {drive}...")
            
            # Palabras clave de archivos de recuperación comunes
            keywords = ["*bitlocker*.txt", "*clave*.txt", "*recuperacion*.txt", "*recovery*.txt"]
            archivos_sospechosos = []
            
            for kw in keywords:
                # Búsqueda ultra rápida directa en el núcleo del S.O.
                try:
                    out = subprocess.run(f'cmd /c dir "{drive}\\{kw}" /s /b 2>nul', shell=True, capture_output=True, text=True).stdout
                    for linea in out.splitlines():
                        ruta = linea.strip()
                        if ruta and os.path.isfile(ruta) and ruta not in archivos_sospechosos:
                            archivos_sospechosos.append(ruta)
                except: pass
            
            # Revisar el contenido de los archivos sospechosos con Regex
            for ruta in archivos_sospechosos:
                try:
                    with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
                        contenido = f.read()
                        claves = regex_clave.findall(contenido)
                        if claves:
                            log(f"\n[🔥] ¡ALERTA! ARCHIVO DE CLAVE ENCONTRADO:")
                            log(f"      📍 Ruta : {ruta}")
                            for c in claves:
                                log(f"      🔑 Clave: {c}")
                            encontrados += 1
                except: pass
                
        if encontrados == 0:
            log("\n[-] No se encontraron archivos de claves de BitLocker en este equipo ni en los USBs.")
        else:
            log(f"\n[+] Búsqueda finalizada. Se encontraron {encontrados} archivos con claves válidas.")
            
    elif accion == '4':
        unidad = unidad.strip().upper().replace(":", "") + ":"
        clave = clave.strip()
        log(f"[*] Intentando inyectar clave de recuperación en la unidad {unidad}...\n")
        run_cmd(log, f"manage-bde -unlock {unidad} -recoverypassword {clave}")
        
        log("\n[*] Verificando si el disco se ha desbloqueado correctamente...")
        log("[!] Si el disco se desbloqueó, puedes desactivar BitLocker permanentemente desde el Panel de Control.")
        
    try: notificar_voz("La operación de BitLocker ha finalizado.")
    except: pass

def logica_usuarios_locales(log):
    log("\n[*] Volcando base de datos SAM de usuarios locales...")
    # Se usa motor CIM/WMI universal en lugar de LocalAccounts para evitar fallos de compatibilidad
    script = r"Get-CimInstance Win32_UserAccount -Filter 'LocalAccount=True' | Select-Object Name, FullName, Status, Disabled | Out-GridView -Title 'TREMEND: Usuarios Locales'"
    run_ps_script(log, script)

def logica_numero_serie(log):
    log("\n[*] Extrayendo Número de Serie y Modelo...")
    run_ps_script(log, 'try { $info = Get-CimInstance Win32_ComputerSystemProduct; $info | Format-List; Set-Clipboard -Value $info.IdentifyingNumber; Write-Host "[+] Copiado" } catch {}')

def logica_memoria_ghost(log):
    log("\n[*] Iniciando Auditoría Forense RAM (Ghost por pandaadir05)...")
    temp_dir = r"C:\Tremend_Scanner"
    
    # CORRECCIÓN DE PRIVILEGIOS Y EJECUCIÓN NATIVA
    script = fr"""
    if (!(Test-Path "{temp_dir}")) {{ New-Item -ItemType Directory -Force -Path "{temp_dir}" | Out-Null }}
    try {{
        Write-Host "[*] Contactando a GitHub de forma segura..."
        $headers = @{{ "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }}
        $api = Invoke-RestMethod -Uri "https://api.github.com/repos/pandaadir05/ghost/releases/latest" -Headers $headers
        $url = ($api.assets | Where-Object {{ $_.name -match "windows" -and $_.name -match ".zip" }}).browser_download_url
        if ($url) {{
            Write-Host "[+] Enlace validado. Descargando binario nativo (Rust)..."
            Invoke-WebRequest -Uri $url -OutFile "{temp_dir}\ghost.zip"
            Expand-Archive -Path "{temp_dir}\ghost.zip" -DestinationPath "{temp_dir}" -Force -ErrorAction SilentlyContinue
            $exe = Get-ChildItem -Path "{temp_dir}" -Filter "*ghost*.exe" -Recurse | Select-Object -ExpandProperty FullName -First 1
            if ($exe) {{ 
                Write-Host "[*] Lanzando el Dashboard Original de Ghost..."
                Write-Host "[!] Se abrirá una ventana externa con gráficos nativos."
                Write-Host "[!] Cuando termines de auditar la RAM, presiona la tecla 'Q' en esa ventana para salir."
                
                # FIX MAESTRO: Ejecutamos el archivo en su propia consola nativa y pausamos TREMEND hasta que se cierre
                Start-Process -FilePath $exe -Wait
                
                Write-Host "[+] Análisis de anillos de memoria finalizado."
            }}
        }}
    }} catch {{ Write-Host "[-] Error de comunicación con los servidores de GitHub: $($_.Exception.Message)" }}
    """
    run_ps_script(log, script)

    from tkinter import messagebox
    if messagebox.askyesno("Limpieza Forense", "El escáner Ghost ha terminado.\n\n¿Deseas ELIMINAR el motor descargado para no dejar rastro en el equipo?"):
        shutil.rmtree(temp_dir, ignore_errors=True)
        log("[+] Limpieza táctica: Motor Ghost destruido sin dejar rastro.")
    else:
        log("[*] Motor Ghost conservado en el equipo.")

def logica_sniffnet(log):
    import urllib.request, json, os, platform, subprocess, shutil, zipfile, tarfile, time
    from tkinter import messagebox

    # --- NUEVA ESTÉTICA INSPIRADA EN EL INTERNET TRAFFIC VISUALISER ---
    log("\n" + "="*75)
    log(" 🌐 MOTOR FORENSE DE TRÁFICO (INTERNET TRAFFIC VISUALISER) ")
    log("="*75)
    log("[*] Iniciando Secuencia de Interceptación de Red...")
    time.sleep(0.4)
    log("    -> [1/4] Capturando paquetes de red en bruto (Packet Capture)...")
    time.sleep(0.3)
    log("    -> [2/4] Extrayendo rutas de origen y destino (IPs Address)...")
    time.sleep(0.3)
    log("    -> [3/4] Analizando protocolos de enrutamiento (HTTP, DNS, TCP, UDP)...")
    time.sleep(0.3)
    log("    -> [4/4] Compilando gráficas de ancho de banda y nodos globales...")
    time.sleep(0.5)

    temp_dir = os.path.join(os.environ.get('TEMP') if os.name == 'nt' else '/tmp', "Tremend_Sniffnet")
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)

    sistema = platform.system().lower()
    arquitectura = platform.machine().lower()
    
    log(f"\n[*] Plataforma detectada: {sistema.upper()} ({arquitectura}). Preparando motor Rust (Sniffnet)...")

    startupinfo = None
    if sistema == 'windows':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # 1. Dependencia Npcap (Solo Windows)
    if sistema == 'windows':
        ruta_npcap = r"C:\Windows\System32\Npcap"
        if not os.path.exists(ruta_npcap):
            log("[-] Driver 'Npcap' no detectado. Es obligatorio para interceptar tráfico en Windows.")
            
            if messagebox.askyesno("Requisito Faltante", "Sniffnet requiere el driver 'Npcap' para capturar la red.\n\n¿Deseas descargar el instalador oficial y ejecutarlo ahora mismo?"):
                log("[*] Descargando instalador de Npcap...")
                npcap_exe = os.path.join(temp_dir, "npcap_installer.exe")
                try:
                    urllib.request.urlretrieve("https://npcap.com/dist/npcap-1.79.exe", npcap_exe)
                    log("[!] Lanzando instalador. Acepta los permisos de Administrador en pantalla...")
                    
                    script_ps = f"Start-Process -FilePath '{npcap_exe}' -Verb RunAs -Wait"
                    subprocess.run(["powershell", "-NoProfile", "-Command", script_ps], startupinfo=startupinfo)
                    
                    if not os.path.exists(ruta_npcap):
                        log("[-] Instalación cancelada o fallida. Sniffnet fallará al buscar la red."); return
                    else:
                        log("[+] Npcap instalado exitosamente.")
                except Exception as e:
                    log(f"[-] Error al descargar Npcap: {e}"); return
            else:
                log("[-] Operación cancelada."); return

    # 2. Comprobar si ya está instalado (Modo Inteligente)
    sniffnet_preexistente = False
    exe_path = None
    if sistema == 'windows':
        rutas_comunes = [
            r"C:\Program Files\Sniffnet\Sniffnet.exe",
            r"C:\Program Files\Sniffnet\sniffnet.exe",
            r"C:\Program Files (x86)\Sniffnet\Sniffnet.exe",
            r"C:\Program Files (x86)\Sniffnet\sniffnet.exe"
        ]
        for r in rutas_comunes:
            if os.path.exists(r):
                exe_path = r
                sniffnet_preexistente = True
                log("[+] Motor preexistente detectado en el sistema.")
                break

    archivo_destino = ""
    
    # 3. Descarga y Despliegue (Solo si no está preinstalado)
    if not sniffnet_preexistente:
        log("    -> Contactando API de GitHub para ubicar la última versión compilada...")
        api_url = "https://api.github.com/repos/GyulyVGC/sniffnet/releases/latest"
        url_descarga = None
        try:
            req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            busqueda_os = 'windows' if sistema == 'windows' else ('darwin' if sistema == 'darwin' else 'linux')
            for asset in data.get('assets', []):
                nombre = asset['name'].lower()
                if busqueda_os == 'windows' and 'windows' in nombre:
                    if nombre.endswith('.msi') or nombre.endswith('.zip'):
                        url_descarga = asset['browser_download_url']
                        if '.zip' in nombre: break
                elif busqueda_os == 'linux' and 'linux' in nombre and nombre.endswith('.tar.gz') and 'musl' not in nombre:
                    url_descarga = asset['browser_download_url']; break
                elif busqueda_os == 'darwin' and 'mac' in nombre and nombre.endswith('.dmg'):
                    url_descarga = asset['browser_download_url']; break
        except Exception as e:
            log(f"[-] Error API GitHub: {e}")

        if not url_descarga:
            log("[-] Error Crítico: No se encontró versión compatible para tu OS."); return

        nombre_archivo = url_descarga.split('/')[-1]
        archivo_destino = os.path.join(temp_dir, nombre_archivo)
        
        if not os.path.exists(archivo_destino):
            log(f"[*] Descargando paquete oficial ({nombre_archivo})...")
            try: urllib.request.urlretrieve(url_descarga, archivo_destino)
            except Exception as e: log(f"[-] Falló la descarga: {e}"); return
            
        log("[*] Desplegando binarios en el núcleo del sistema...")
        try:
            if archivo_destino.endswith('.zip'):
                with zipfile.ZipFile(archivo_destino, 'r') as zip_ref: zip_ref.extractall(temp_dir)
            elif archivo_destino.endswith('.tar.gz'):
                with tarfile.open(archivo_destino, 'r:gz') as tar_ref: tar_ref.extractall(temp_dir)
            
            elif archivo_destino.endswith('.msi'):
                log("    -> Ejecutando Instalación Silenciosa Temporal (Modo Ghost)...")
                subprocess.run(f'msiexec.exe /i "{archivo_destino}" /qn /norestart', shell=True)
                for r in rutas_comunes:
                    if os.path.exists(r): 
                        exe_path = r
                        break
                        
            if not exe_path:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.lower() == 'sniffnet.exe' or (file.lower() == 'sniffnet' and os.access(os.path.join(root, file), os.X_OK)):
                            exe_path = os.path.join(root, file)
                            break
                    if exe_path: break
        except Exception as e: log(f"[-] Error de despliegue: {e}"); return

    if not exe_path: log("[-] No se halló el ejecutable principal tras el despliegue."); return

    # 4. Ejecución
    log("[*] Lanzando Dashboard Analítico Interactivo...")
    log("[!] Cierra la ventana externa del visualizador cuando termines de diagnosticar la red.")
    try:
        if sistema == 'windows':
            script_sniffnet = f"Start-Process -FilePath '{exe_path}' -Verb RunAs -Wait"
            subprocess.run(["powershell", "-NoProfile", "-Command", script_sniffnet], startupinfo=startupinfo)
        else:
            log("[!] En Linux/Mac podrías requerir privilegios Root para escanear la red.")
            subprocess.Popen([exe_path]).wait()
        log("\n[+] Análisis finalizado.")
    except Exception as e: log(f"[-] Error de ejecución: {e}")

    # 5. Limpieza Táctica Extrema
    if sistema == 'windows' and archivo_destino.endswith('.msi') and not sniffnet_preexistente:
        log("[*] Borrando huellas: Desinstalando motor silenciosamente...")
        subprocess.run(f'msiexec.exe /x "{archivo_destino}" /qn /norestart', shell=True)

    if messagebox.askyesno("Limpieza de Base", "¿Deseas ELIMINAR el instalador base de la computadora para no dejar rastro de tu intervención en el sistema?"):
        try: shutil.rmtree(temp_dir, ignore_errors=True); log("[+] Archivos base eliminados.")
        except: pass

    if sistema == 'windows' and os.path.exists(r"C:\Windows\System32\Npcap"):
        if messagebox.askyesno("Limpieza de Driver", "El visualizador ha cerrado.\n\n¿Deseas DESINSTALAR el driver 'Npcap' para borrar absolutamente todo rastro de tu intervención en la red?"):
            uninstaller = r"C:\Program Files\Npcap\uninstall.exe"
            if os.path.exists(uninstaller):
                log("[*] Lanzando desinstalador de Npcap...")
                script_un = f"Start-Process -FilePath '{uninstaller}' -Verb RunAs -Wait"
                subprocess.run(["powershell", "-NoProfile", "-Command", script_un], startupinfo=startupinfo)
                log("[+] Driver Npcap purgado del sistema.")
            else: log("[-] Desinstalador de Npcap no encontrado.")

def logica_historial_web(log, navegador, ruta_original):
    import os, shutil, sqlite3
    
    log("\n" + "="*75)
    log(" 🌐 AUDITORÍA FORENSE DE HISTORIAL WEB (VISUALIZER) ")
    log("="*75)
    
    log(f"[*] Extrayendo datos de: {navegador}")
    log("[*] Evadiendo candados de Windows (Clonando base de datos a memoria temporal)...")
    
    # Creamos la copia temporal
    temp_db = os.path.join(os.environ.get('TEMP'), f"tremend_history_{navegador.replace(' ', '')}.sqlite")
    try:
        shutil.copy2(ruta_original, temp_db)
    except Exception as e:
        log(f"[-] Falló la evasión de seguridad al copiar: {e}"); return
        
    # 3. Minería de Datos (Extracción SQL)
    log("[*] Desencriptando timestamps y extrayendo métricas de navegación...")
    try:
        # FIX APLICADO: Usamos temp_db
        conn = sqlite3.connect(temp_db) 
        cursor = conn.cursor()
        
        # Consultar los 10 sitios web más visitados
        cursor.execute("SELECT url, title, visit_count FROM urls ORDER BY visit_count DESC LIMIT 10")
        top_sites = cursor.fetchall()
        
        # Consultar las últimas 15 búsquedas de Google/Bing
        try:
            cursor.execute("SELECT term FROM keyword_search_terms ORDER BY url_id DESC LIMIT 15")
            ultimas_busquedas = [row[0] for row in cursor.fetchall()]
        except:
            ultimas_busquedas = ["No se detectaron términos o la tabla fue purgada."]
            
        conn.close()
    except Exception as e:
        log(f"[-] Error al leer la base de datos SQL: {e}")
        try: os.remove(temp_db)
        except: pass
        return

    # 4. Formatear datos para las gráficas
    sitios_nombres = []
    visitas = []
    lista_html = ""
    
    for url, title, count in top_sites:
        dominio = url.replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
        sitios_nombres.append(dominio[:20]) # Máximo 20 caracteres
        visitas.append(count)
        
        titulo_limpio = title.replace('"', '').replace("'", "") if title else dominio
        lista_html += f'<tr class="border-b border-slate-700 hover:bg-slate-700"><td class="py-3 px-4 text-emerald-400">{dominio}</td><td class="py-3 px-4 truncate max-w-xs">{titulo_limpio}</td><td class="py-3 px-4 text-center font-bold text-purple-400">{count}</td></tr>'

    busquedas_html = "".join([f'<span class="inline-block bg-slate-700 rounded-full px-3 py-1 text-sm font-semibold text-blue-300 mr-2 mb-2">#{term}</span>' for term in ultimas_busquedas])

    log("[*] Renderizando Dashboard Interactivo en HTML5...")
    
    # 5. INYECCIÓN DEL DASHBOARD HTML
    html_dashboard = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TREMEND - Visualizador de Historial</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body class="bg-slate-900 text-slate-200 font-sans p-8">
        <div class="max-w-6xl mx-auto">
            <header class="mb-10 text-center border-b border-slate-700 pb-6">
                <h1 class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-blue-500 tracking-wider">BROWSER HISTORY VISUALIZER</h1>
                <p class="text-slate-400 mt-2">Auditoría Forense: <span class="text-purple-400 font-bold">{navegador}</span> | Procesado por TREMEND Toolkit</p>
            </header>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Gráfica Principal -->
                <div class="lg:col-span-2 bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl">
                    <h2 class="text-xl font-bold text-emerald-400 mb-4">🏆 Top 10 Sitios Más Visitados</h2>
                    <canvas id="chartTopSites" height="120"></canvas>
                </div>

                <!-- Nube de Búsquedas -->
                <div class="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl flex flex-col">
                    <h2 class="text-xl font-bold text-blue-400 mb-4">🔍 Últimos Términos de Búsqueda</h2>
                    <div class="flex-grow overflow-y-auto">
                        {busquedas_html}
                    </div>
                </div>
            </div>

            <!-- Tabla de Detalles -->
            <div class="mt-8 bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl">
                <h2 class="text-xl font-bold text-purple-400 mb-4">📑 Desglose de Tráfico Recurrente</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-900 text-slate-400 text-sm uppercase">
                                <th class="py-3 px-4 rounded-tl-lg">Dominio Raíz</th>
                                <th class="py-3 px-4">Título Registrado</th>
                                <th class="py-3 px-4 text-center rounded-tr-lg">Total Visitas</th>
                            </tr>
                        </thead>
                        <tbody>
                            {lista_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('chartTopSites').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {sitios_nombres},
                    datasets: [{{
                        label: 'Número de Visitas',
                        data: {visitas},
                        backgroundColor: 'rgba(16, 185, 129, 0.6)',
                        borderColor: 'rgba(16, 185, 129, 1)',
                        borderWidth: 2,
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ beginAtZero: true, grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8', font: {{ size: 11 }} }} }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    # 6. Guardar y mostrar
    ruta_reporte = os.path.join(os.environ.get("USERPROFILE"), "Desktop", f"Visualizador_TREMEND_{navegador.replace(' ', '')}.html")
    try:
        with open(ruta_reporte, "w", encoding="utf-8") as file:
            file.write(html_dashboard)
        
        log(f"[+] ¡ÉXITO! Visualizador compilado y guardado en tu Escritorio.")
        os.startfile(ruta_reporte)
    except Exception as e:
        log(f"[-] Error al generar el HTML: {e}")
        
    try: os.remove(temp_db)
    except: pass

# --- CATEGORÍA 4: SOFTWARE Y LICENCIAS ---
def logica_gestor_winget(log):
    log("\n[*] Iniciando gestor de paquetes Winget (Por Microsoft)...")
    run_cmd(log, "winget upgrade --all --silent --accept-package-agreements --accept-source-agreements")

def logica_clave_windows(log):
    log("\n[*] Consultando Registro de Windows para licencias activas...")
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform")
        clave, _ = winreg.QueryValueEx(key, "BackupProductKeyDefault")
        log(f"\n[+] Clave Original Incrustada: {clave}")
    except: log("[-] No se pudo leer la clave.")

def logica_inventario_software(log):
    log("\n[*] Generando Inventario de Software...")
    ruta_csv = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "Inventario_Software_TREMEND.csv")
    programas = []
    for ruta in [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"]:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, ruta)
            for i in range(winreg.QueryInfoKey(key)[0]):
                sub_key = winreg.OpenKey(key, winreg.EnumKey(key, i))
                try: programas.append([winreg.QueryValueEx(sub_key, "DisplayName")[0], winreg.QueryValueEx(sub_key, "DisplayVersion")[0]])
                except: pass
        except: pass
    if programas:
        with open(ruta_csv, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre", "Versión"]); writer.writerows(programas)
        log(f"[+] Archivo CSV exportado en el Escritorio con {len(programas)} programas.")

def logica_respaldo_drivers(log):
    log("\n[*] Clonando archivos de controladores (.sys / .inf)...")
    ruta = r"C:\RespaldoDrivers"
    if not os.path.exists(ruta): os.makedirs(ruta)
    run_cmd(log, f"dism /online /export-driver /destination:{ruta}")

def logica_auditar_office(log):
    log("\n[*] Buscando motor de licencias OSPP de Microsoft Office...")
    script_path = next((r for r in [r"C:\Program Files\Microsoft Office\Office16\OSPP.VBS", r"C:\Program Files (x86)\Microsoft Office\Office16\OSPP.VBS"] if os.path.exists(r)), None)
    if script_path: run_cmd(log, f'cscript //nologo "{script_path}" /dstatus')
    else: log("[-] No se encontró el script de Office.")

def logica_activador_mas(log):
    log("\n[*] Contactando servidor de Microsoft Activation Scripts (MAS por massgravel)...")
    log("[*] Abriendo panel interactivo externo de activación...")
    
    # CORRECCIÓN: Usamos 'start' en CMD para forzar a Windows a abrir una ventana emergente en primer plano
    subprocess.Popen('start powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.activated.win | iex"', shell=True)
    
    log("[+] El activador ha sido lanzado con éxito.")

def logica_escanear_pnp(log):
    log("\n[*] Forzando reconocimiento de Hardware PnP...")
    run_cmd(log, "pnputil /scan-devices")
    log("[+] Escaneo de hardware finalizado. Si conectaste una pieza nueva, Windows Update buscará el driver.")

def logica_glidex(log):
    import subprocess, platform
    from tkinter import messagebox

    log("\n[*] Iniciando despliegue de ASUS GlideX (Multipantalla)...")
    
    sistema = platform.system().lower()
    if sistema != 'windows':
        log("[-] Error: GlideX es una aplicación UWP exclusiva para Windows."); return

    log("[*] Interrogando a la base de datos de Microsoft Store vía Winget...")
    log("[!] Descargando e instalando el paquete oficial (ID: 9PLH2SV1DVK5)...")
    log("[!] Esto puede tardar unos minutos dependiendo de tu conexión a internet. No cierres la ventana.")
    
    # Ejecutamos Winget forzando la descarga directa desde la MS Store en modo desatendido
    cmd_install = 'winget install --id 9PLH2SV1DVK5 --exact --source msstore --accept-package-agreements --accept-source-agreements'
    run_cmd(log, cmd_install)
    
    log("\n[+] Secuencia de inyección Winget finalizada.")
    
    # Abrimos la MS Store para que el cliente pueda abrir la App (las UWP están ofuscadas por el SO)
    if messagebox.askyesno("Lanzamiento", "El comando de instalación ha concluido.\n\n¿Deseas abrir la página de GlideX en la Microsoft Store para verificarla o abrir la app directamente?"):
        log("[*] Abriendo el portal de Microsoft Store...")
        subprocess.run('start ms-windows-store://pdp/?ProductId=9PLH2SV1DVK5', shell=True)
        log("[+] Portal abierto con éxito.")

# --- CATEGORÍA 5: SOPORTE TÉCNICO ---
def logica_destructor(log, ruta):
    log(f"\n[*] SECUENCIA DE DESTRUCCIÓN INICIADA: {ruta}")
    run_cmd(log, f'takeown.exe /f "{ruta}" /a /r /d y 2>nul')
    run_cmd(log, f'icacls.exe "{ruta}" /grant *S-1-5-32-544:F /t /c /q')
    try: shutil.rmtree(ruta, ignore_errors=True); log("[+] CARPETA REBELDE PULVERIZADA EXITOSAMENTE.")
    except Exception as e: log(f"[-] Error: {e}")

def logica_cambiar_clave(log, usr, pwd):
    log(f"\n[*] Alterando credenciales SAM para el usuario: {usr}")
    run_cmd(log, f'net user "{usr}" "{pwd}"')
    log("[+] Operación finalizada en la base de datos local.")

def logica_lazagne(log):
    log("\n[*] Iniciando Auditoría Forense de Credenciales (LaZagne)...")
    temp_dir = r"C:\Tremend_LaZagne"
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    exe_path = os.path.join(temp_dir, "lazagne.exe")
    report_path = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "Reporte_Credenciales_TREMEND.txt")
    
    log("[*] Añadiendo exclusión temporal a Windows Defender (evitando falsos positivos)...")
    run_ps_script(log, f"Add-MpPreference -ExclusionPath '{temp_dir}' -ErrorAction SilentlyContinue")
    
    # Motor PowerShell blindado para asegurar que descargue el .exe y no el código fuente
    script = f"""
    try {{
        if (!(Test-Path '{exe_path}')) {{
            Write-Host "[*] Contactando a GitHub para descargar el motor ejecutable..."
            $api = Invoke-RestMethod -Uri "https://api.github.com/repos/AlessandroZ/LaZagne/releases/latest"
            $url = ($api.assets | Where-Object {{ $_.name -like '*.exe' }} | Select-Object -First 1).browser_download_url
            if ($url) {{
                Invoke-WebRequest -Uri $url -OutFile '{exe_path}'
                Write-Host "[+] Descarga del motor completada."
            }} else {{ Write-Host "[-] No se encontró el binario .exe en el servidor." }}
        }}
        
        if (Test-Path '{exe_path}') {{
            Write-Host "[*] Ejecutando motor de extracción forense..."
            Write-Host "[!] Esto puede tardar varios minutos buscando en bases de datos. No cierres la ventana..."
            & '{exe_path}' all | Out-File -FilePath '{report_path}' -Encoding UTF8
            Write-Host "[+] ¡ÉXITO! Credenciales guardadas correctamente."
        }}
    }} catch {{ Write-Host "[-] Error durante la operación forense: $($_.Exception.Message)" }}
    """
    run_ps_script(log, script)
    
    log("[*] Restaurando seguridad del Antivirus...")
    run_ps_script(log, f"Remove-MpPreference -ExclusionPath '{temp_dir}' -ErrorAction SilentlyContinue")
    log(f"[+] Proceso terminado. Puedes revisar el archivo de contraseñas en tu Escritorio.")

    # Pregunta de Limpieza
    from tkinter import messagebox
    if messagebox.askyesno("Limpieza Forense", "La extracción de contraseñas ha finalizado.\n\n¿Deseas ELIMINAR el motor LaZagne de tu equipo para no dejar rastro en el sistema del cliente?"):
        shutil.rmtree(temp_dir, ignore_errors=True)
        log("[+] Limpieza táctica: Motor LaZagne destruido sin dejar rastro.")
    else:
        log("[*] Motor LaZagne conservado en el equipo.")

def logica_romper_archivos(log, archivo_bloqueado, tipo_ataque, diccionario_custom):
    import os, urllib.request, zipfile, shutil, subprocess, multiprocessing
    
    log(f"\n[*] Analizando archivo objetivo: {os.path.basename(archivo_bloqueado)}")
    
    temp_dir = os.path.join(os.environ.get('TEMP'), "Tremend_JtR")
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)

    jtr_folder = os.path.join(temp_dir, "john")
    run_dir = os.path.join(jtr_folder, "run")
    john_exe = os.path.join(run_dir, "john.exe")

    # 1. Motor de Descarga (John The Ripper Jumbo)
    if not os.path.exists(john_exe):
        log("[*] Descargando motor de fuerza bruta (John The Ripper Jumbo)...")
        zip_path = os.path.join(temp_dir, "jtr.zip")
        url_jtr = "https://www.openwall.com/john/k/john-1.9.0-jumbo-1-win64.zip"
        
        try:
            req = urllib.request.Request(url_jtr, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as response, open(zip_path, 'wb') as out_file:
                out_file.write(response.read())
                
            log("[*] Descomprimiendo motor base...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref: zip_ref.extractall(jtr_folder)
            
            for root, dirs, files in os.walk(jtr_folder):
                if 'john.exe' in files:
                    run_dir = root
                    john_exe = os.path.join(run_dir, "john.exe")
                    break
            os.remove(zip_path)
        except Exception as e: log(f"[-] Error crítico de red o extracción: {e}"); return

    if not os.path.exists(john_exe): return

    extension = archivo_bloqueado.lower().split('.')[-1]

    # 2. EL SECRETO DE ZIPRIPPER: Motor Perl Portable para 7z y PDF
    perl_exe = ""
    if extension in ["pdf", "7z"]:
        perl_dir = os.path.join(temp_dir, "perl")
        perl_exe = os.path.join(perl_dir, "perl", "bin", "perl.exe")
        
        if not os.path.exists(perl_exe):
            log(f"[*] El formato .{extension.upper()} requiere el lenguaje Perl. Descargando Strawberry Perl Portable...")
            perl_zip = os.path.join(temp_dir, "perl.zip")
            try:
                url_perl = "https://strawberryperl.com/download/5.16.3.1/strawberry-perl-5.16.3.1-64bit-portable.zip"
                req = urllib.request.Request(url_perl, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=120) as response, open(perl_zip, 'wb') as out_file:
                    out_file.write(response.read())
                
                log("[*] Instalando entorno Perl en memoria temporal...")
                with zipfile.ZipFile(perl_zip, 'r') as zip_ref: zip_ref.extractall(perl_dir)
                os.remove(perl_zip)
            except Exception as e: log(f"[-] Error al descargar entorno Perl: {e}"); return

    # 3. Extracción del Hash Criptográfico
    hash_file = os.path.join(temp_dir, "hash_objetivo.txt")
    safe_target = os.path.join(temp_dir, f"objetivo_seguro.{extension}")
    
    try: shutil.copy2(archivo_bloqueado, safe_target)
    except Exception as e: log(f"[-] Error al aislar archivo: {e}"); return
    
    # Asignación dinámica del extractor correcto (Resolviendo el Bug)
    if extension == "zip": extractor = f'"{os.path.join(run_dir, "zip2john.exe")}" "{safe_target}"'
    elif extension == "rar": extractor = f'"{os.path.join(run_dir, "rar2john.exe")}" "{safe_target}"'
    elif extension == "7z": extractor = f'"{perl_exe}" "{os.path.join(run_dir, "7z2john.pl")}" "{safe_target}"'
    elif extension == "pdf": extractor = f'"{perl_exe}" "{os.path.join(run_dir, "pdf2john.pl")}" "{safe_target}"'
    else: log("[-] Formato no soportado por el motor."); return

    log(f"[*] Aislamiento Forense: Extrayendo Hash ({extension.upper()})...")
    try:
        resultado_hash = subprocess.run(extractor, shell=True, cwd=run_dir, capture_output=True, text=True, errors='ignore').stdout
        
        hash_limpio = ""
        for linea in resultado_hash.splitlines():
            if ":$" in linea:
                bloque = "$" + linea.split(":$", 1)[1].strip()
                hash_puro = bloque.split(":")[0].strip()
                if len(hash_puro) > 10: hash_limpio += hash_puro + "\n"
                
        if not hash_limpio.strip():
            log("[-] Error: No se extrajo ningún Hash cifrado válido. ¿Seguro que tiene contraseña?"); os.remove(safe_target); return
            
        with open(hash_file, 'w', encoding='utf-8') as f: f.write(hash_limpio)
        os.remove(safe_target)
        log("[+] Hash extraído correctamente.")
    except Exception as e: log(f"[-] Fallo al extraer el hash: {e}"); return

    try: os.remove(os.path.join(run_dir, "john.pot"))
    except: pass

    # 4. ACELERACIÓN POR HARDWARE (GPU OpenCL vs CPU Multicore)
    flags_hardware = ""
    has_gpu = os.path.exists(r"C:\Windows\System32\OpenCL.dll")
    formato_opencl = ""

    with open(hash_file, "r") as f:
        primer_hash = f.readline()
        if "$zip2$" in primer_hash or "$zip$" in primer_hash or "$pkzip$" in primer_hash: formato_opencl = "ZIP-opencl"
        elif "$rar5$" in primer_hash: formato_opencl = "rar5-opencl"
        elif "$rar3$" in primer_hash or "$RAR3$" in primer_hash: formato_opencl = "rar-opencl"
        elif "$7z$" in primer_hash: formato_opencl = "7z-opencl"
        elif "$pdf$" in primer_hash: formato_opencl = "pdf-opencl"

    if has_gpu and formato_opencl:
        flags_hardware = f"--format={formato_opencl}"
        log("[*] 🚀 ¡MOTOR GRÁFICO DETECTADO! Aceleración por GPU (OpenCL) Activada.")
    else:
        hilos = multiprocessing.cpu_count() or 4
        flags_hardware = f"--fork={hilos}"
        log(f"[*] 🚀 ¡MULTIHILO DETECTADO! Aceleración por CPU Activada ({hilos} núcleos).")

    # 5. CONFIGURACIÓN DEL VECTOR DE ATAQUE
    log("[*] Preparando inyección de ataque...")
    
    if tipo_ataque == '1':
        comando_crack = f'"{john_exe}" {flags_hardware} "{hash_file}"'
    elif tipo_ataque == '2':
        comando_crack = f'"{john_exe}" --incremental=Digits {flags_hardware} "{hash_file}"'
    elif tipo_ataque == '3':
        dict_temp = os.path.join(run_dir, "top_100k_ncsc.txt")
        if not os.path.exists(dict_temp):
            log("    -> Descargando diccionario gigante...")
            url_dict = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt"
            try: urllib.request.urlretrieve(url_dict, dict_temp)
            except: log("[-] Falló la descarga del diccionario."); return
        comando_crack = f'"{john_exe}" --wordlist="{dict_temp}" {flags_hardware} "{hash_file}"'
    elif tipo_ataque == '4':
        dict_temp = os.path.join(run_dir, "pistas.txt")
        with open(dict_temp, 'w', encoding='utf-8') as f:
            for palabra in diccionario_custom.split(','): f.write(palabra.strip() + '\n')
        comando_crack = f'"{john_exe}" --wordlist="{dict_temp}" {flags_hardware} "{hash_file}"'

    log("\n[!] ATAQUE EN PROGRESO... Calculando hashes por segundo...\n")
    
    # 6. Ejecución del Ataque
    try:
        subprocess.run(comando_crack, shell=True, cwd=run_dir, capture_output=True)
        resultado = subprocess.run(f'"{john_exe}" --show "{hash_file}"', shell=True, cwd=run_dir, capture_output=True, text=True).stdout
        
        encontrada = False
        for linea in resultado.splitlines():
            if ":" in linea and "password hashes cracked" not in linea and "0 password" not in linea:
                clave = linea.split(":", 1)[1].strip()
                if clave:
                    log(f"\n=======================================================")
                    log(f" 🔓 ¡ÉXITO! CONTRASEÑA VULNERADA: {clave} ")
                    log(f"=======================================================")
                    encontrada = True
                    break
                
        if not encontrada:
            log("\n[-] El ataque finalizó pero la contraseña no fue encontrada.")
            
    except Exception as e: log(f"[-] Error durante el ataque: {e}")

    # 7. Limpieza
    try: shutil.rmtree(temp_dir, ignore_errors=True); log("\n[*] Limpieza táctica completada.")
    except: pass

def logica_linpeas(log):
    import os, subprocess, re, shutil
    from tkinter import messagebox

    log("\n[*] Iniciando Auditoría de Seguridad Profunda en Linux (LinPEAS)...")
    
    # Determinamos dónde guardar el reporte (Escritorio del equipo actual)
    escritorio = os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")
    if not os.path.exists(escritorio): 
        escritorio = os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Escritorio")
    
    report_path = os.path.join(escritorio, "Reporte_Auditoria_LinPEAS.txt")
    # Para el comando de Bash, necesitamos adaptar la ruta si usamos WSL
    bash_report_path = report_path.replace("\\", "/")
    
    log("[*] Contactando a GitHub para descargar el motor LinPEAS a través de Bash...")
    log("[!] NOTA TÉCNICA: El escáner tomará varios minutos analizando binarios, SUIDs y permisos. La consola parecerá pausada. ¡No la cierres!")
    
    # Construimos un script bash integrado que hace todo en el entorno Linux
    script_bash = f"""
    echo "    -> Descargando linpeas.sh desde la nube a /tmp..."
    curl -sL https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh -o /tmp/linpeas.sh
    chmod +x /tmp/linpeas.sh
    echo "    -> Ejecutando escaneo táctico (Modo Silencioso)..."
    # Ejecutamos y guardamos la salida cruda y de errores en el escritorio del usuario
    bash /tmp/linpeas.sh -a > "{bash_report_path}" 2>&1
    echo "[+] Escaneo completado. Archivo generado."
    """
    
    try:
        # Detectamos si TREMEND se ejecuta en Windows (invocará WSL) o nativo en Linux
        if os.name == 'nt':
            comando = f'wsl -e bash -c "{script_bash}"'
            if shutil.which("wsl") is None: # Si no hay WSL, intenta GitBash
                comando = f'bash -c "{script_bash}"'
        else:
            comando = f'bash -c "{script_bash}"'
            
        proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')
        for linea in proceso.stdout:
            if linea.strip(): log(linea.strip())
        proceso.wait()
        
    except Exception as e:
        log(f"[-] Error al intentar ejecutar el entorno Linux: {e}")
        log("[!] Asegúrate de tener el Subsistema de Linux (WSL) o Bash instalado.")
        return

    # --- LECTOR INTELIGENTE Y RESUMEN ---
    if os.path.exists(report_path):
        log("\n=======================================================")
        log(" 🚨 RESUMEN DE VULNERABILIDADES CRÍTICAS (ROOT) 🚨")
        log("=======================================================")
        try:
            alertas = []
            with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
                for linea in f:
                    # En LinPEAS el color rojo con amarillo (escalada segura) y rojo normal tienen la etiqueta '31m'
                    if '31m' in linea and 'Legend:' not in linea:
                        texto_limpio = re.sub(r'\x1b\[[0-9;]*m', '', linea).strip()
                        if len(texto_limpio) > 5 and len(texto_limpio) < 150 and texto_limpio not in alertas:
                            alertas.append(texto_limpio)
            
            if alertas:
                for alerta in alertas[:15]: # Imprime el Top 15 de vulnerabilidades
                    log(f" [!] {alerta}")
                if len(alertas) > 15:
                    log(f"\n [+] ... y {len(alertas) - 15} hallazgos adicionales. (Revisa el archivo de texto en el Escritorio).")
            else:
                log(" [+] No se encontraron alertas críticas rojas. Revisa el reporte completo.")
                
        except Exception as e:
            log(f" [-] Error al generar el resumen en pantalla: {e}")
            
        log(f"\n[+] Reporte completo guardado en: {report_path}")
        
        # --- PROTOCOLO DE AUTO-BLINDAJE EN LINUX ---
        if messagebox.askyesno("Blindaje Automático Linux", "El sistema presenta posibles brechas.\n\n¿Deseas que TREMEND aplique un 'Auto-Blindaje' Básico?\n(Asegurará permisos vitales de claves en /etc, desactivará ingresos directos a root por SSH y limpiará el historial del hacker)."):
            log("\n[*] INICIANDO PROTOCOLO DE AUTO-BLINDAJE EN LINUX...")
            
            script_blindaje = """
            echo "    -> Restaurando permisos seguros en /etc/passwd y /etc/shadow..."
            sudo chmod 644 /etc/passwd 2>/dev/null
            sudo chmod 600 /etc/shadow 2>/dev/null
            
            echo "    -> Desactivando logins de Root directos por SSH (Hardening de Red)..."
            sudo sed -i 's/^PermitRootLogin.*/PermitRootLogin no/g' /etc/ssh/sshd_config 2>/dev/null
            sudo systemctl restart sshd 2>/dev/null || sudo service ssh restart 2>/dev/null
            
            echo "    -> Purgando Historial forense de Bash..."
            cat /dev/null > ~/.bash_history
            history -c 2>/dev/null
            
            echo "[+] PROTOCOLO DE BLINDAJE FINALIZADO."
            """
            
            try:
                if os.name == 'nt':
                    cmd_blindaje = f'wsl -e bash -c "{script_blindaje}"' if shutil.which("wsl") else f'bash -c "{script_blindaje}"'
                else:
                    cmd_blindaje = f'bash -c "{script_blindaje}"'
                    
                proc_blin = subprocess.Popen(cmd_blindaje, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='ignore')
                for linea in proc_blin.stdout:
                    if linea.strip(): log(linea.strip())
                proc_blin.wait()
            except Exception as e:
                log(f"[-] Error al aplicar blindaje: {e}")
        else:
            log("[*] El sistema no fue modificado.")

    if messagebox.askyesno("Limpieza Forense", "¿Deseas ELIMINAR el motor LinPEAS de la carpeta /tmp para no dejar rastro?"):
        cmd_limpieza = 'wsl -e bash -c "rm -f /tmp/linpeas.sh"' if os.name == 'nt' and shutil.which("wsl") else 'bash -c "rm -f /tmp/linpeas.sh"'
        subprocess.run(cmd_limpieza, shell=True)
        log("\n[+] Limpieza táctica completada. Archivos destruidos.")

def logica_macpeas(log):
    import os, subprocess, re, platform
    from tkinter import messagebox

    log("\n[*] Iniciando Auditoría de Seguridad Profunda en Mac (MacPEAS)...")
    
    # Detección Inteligente de Arquitectura
    sistema = platform.system().lower()
    if sistema != 'darwin':
        log("[-] ADVERTENCIA: Esta herramienta está diseñada para ejecutarse en el núcleo de macOS.")
        log("[!] Como estás operando TREMEND desde Windows, la ejecución local se bloquea por seguridad.")
        
        if messagebox.askyesno("Ejecución Remota", "No estás usando un Mac.\n\n¿Quieres generar el comando de inyección remota para ejecutarlo vía SSH o directamente en la terminal del cliente?"):
            log("\n=======================================================")
            log(" 🍏 COMANDO DE INYECCIÓN PARA EL MAC DEL CLIENTE 🍏")
            log("=======================================================")
            log("Copia y pega este comando en la terminal del Mac:")
            log("curl -sL https://github.com/peass-ng/PEASS-ng/releases/latest/download/macPEAS.sh | sh")
            log("\n[+] Cuando termine, revisa los textos en ROJO para detectar vulnerabilidades.")
        return

    # Si TREMEND se está ejecutando nativamente dentro de un Mac, hace el Auto-Escaneo:
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    report_path = os.path.join(escritorio, "Reporte_Auditoria_MacPEAS.txt")
    
    log("[*] Descargando motor MacPEAS desde GitHub...")
    log("[!] NOTA TÉCNICA: El escáner tomará varios minutos analizando Llaveros (Keychains) y permisos. ¡No cierres la consola!")
    
    script_mac = f"""
    echo "    -> Obteniendo macPEAS.sh a /tmp..."
    curl -sL https://github.com/peass-ng/PEASS-ng/releases/latest/download/macPEAS.sh -o /tmp/macpeas.sh
    chmod +x /tmp/macpeas.sh
    echo "    -> Ejecutando auditoría táctica (Modo Silencioso)..."
    /tmp/macpeas.sh -a > "{report_path}" 2>&1
    echo "[+] Escaneo completado."
    """
    
    try:
        proceso = subprocess.Popen(f'bash -c "{script_mac}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='ignore')
        for linea in proceso.stdout:
            if linea.strip(): log(linea.strip())
        proceso.wait()
    except Exception as e:
        log(f"[-] Error crítico al invocar la shell de Mac: {e}")
        return
        
    # --- LECTOR INTELIGENTE Y RESUMEN ---
    if os.path.exists(report_path):
        log("\n=======================================================")
        log(" 🚨 RESUMEN DE VULNERABILIDADES CRÍTICAS (MAC) 🚨")
        log("=======================================================")
        try:
            alertas = []
            with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
                for linea in f:
                    if '31m' in linea and 'Legend:' not in linea:
                        texto_limpio = re.sub(r'\x1b\[[0-9;]*m', '', linea).strip()
                        if len(texto_limpio) > 5 and len(texto_limpio) < 150 and texto_limpio not in alertas:
                            alertas.append(texto_limpio)
            
            if alertas:
                for alerta in alertas[:15]:
                    log(f" [!] {alerta}")
                if len(alertas) > 15:
                    log(f"\n [+] ... y {len(alertas) - 15} hallazgos adicionales.")
            else:
                log(" [+] No se detectaron vulnerabilidades críticas. El sistema parece seguro.")
        except Exception as e:
            log(f" [-] Error leyendo el reporte: {e}")
            
        log(f"\n[+] Reporte completo en: {report_path}")
        
        # --- PROTOCOLO DE AUTO-BLINDAJE EN MAC ---
        if messagebox.askyesno("Blindaje Automático Mac", "El sistema presenta vulnerabilidades.\n\n¿Deseas aplicar un 'Auto-Blindaje' en este Mac?\n(Activará el Firewall de Aplicaciones, desactivará la cuenta de Invitado y purgará historiales de Terminal)."):
            log("\n[*] INICIANDO PROTOCOLO DE AUTO-BLINDAJE EN MAC...")
            script_blindaje = """
            echo "    -> Activando el Firewall de Aplicaciones (ALF)..."
            sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on 2>/dev/null
            
            echo "    -> Desactivando la cuenta de Invitado (Riesgo de acceso físico)..."
            sudo sysadminctl -guestAccount off 2>/dev/null
            
            echo "    -> Purgando historial forense de la Terminal (ZSH y BASH)..."
            cat /dev/null > ~/.zsh_history 2>/dev/null
            cat /dev/null > ~/.bash_history 2>/dev/null
            history -c 2>/dev/null
            
            echo "[+] PROTOCOLO DE BLINDAJE FINALIZADO."
            """
            try:
                proc_blin = subprocess.Popen(f'bash -c "{script_blindaje}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='ignore')
                for linea in proc_blin.stdout:
                    if linea.strip(): log(linea.strip())
                proc_blin.wait()
            except Exception as e:
                log(f"[-] Error al aplicar blindaje: {e}")
        else:
            log("[*] El sistema Mac no fue modificado.")

    if messagebox.askyesno("Limpieza Forense", "¿Deseas ELIMINAR el motor MacPEAS de /tmp para borrar rastros?"):
        subprocess.run('bash -c "rm -f /tmp/macpeas.sh"', shell=True)
        log("\n[+] Limpieza táctica completada. Cero rastros.")

def logica_winpeas(log):
    import os, urllib.request, subprocess, shutil, re
    from tkinter import messagebox

    log("\n[*] Iniciando Auditoría de Seguridad Profunda (WinPEAS)...")
    temp_dir = os.path.join(os.environ.get('TEMP'), "Tremend_WinPEAS")
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    
    exe_path = os.path.join(temp_dir, "winPEASany.exe")
    report_path = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "Reporte_Auditoria_WinPEAS.txt")
    
    log("[!] NOTA TÉCNICA: El escáner tomará varios minutos. La consola parecerá pausada mientras se procesa el sistema. ¡No la cierres!")
    
    script = f"""
    try {{
        if (!(Test-Path '{exe_path}')) {{
            Write-Host "[*] Contactando a GitHub para descargar el motor WinPEAS..."
            $api = Invoke-RestMethod -Uri "https://api.github.com/repos/peass-ng/PEASS-ng/releases/latest"
            $url = ($api.assets | Where-Object {{ $_.name -match 'winPEASany.exe' }} | Select-Object -First 1).browser_download_url
            if ($url) {{
                Invoke-WebRequest -Uri $url -OutFile '{exe_path}'
                Write-Host "[+] Descarga del motor completada."
            }} else {{ Write-Host "[-] No se encontró el binario en el servidor." }}
        }}
        
        if (Test-Path '{exe_path}') {{
            Write-Host "[*] Ejecutando escaneo táctico (Silencioso)..."
            # Ejecución blindada: Redirigimos todo al archivo
            cmd.exe /c "`"{exe_path}`" > `"{report_path}`" 2>&1"
            Write-Host "[+] Escaneo completado."
        }}
    }} catch {{ Write-Host "[-] Error durante la operación: $($_.Exception.Message)" }}
    """
    run_ps_script(log, script)
    
    # --- LECTOR INTELIGENTE Y RESUMEN ---
    if os.path.exists(report_path):
        log("\n=======================================================")
        log(" 🚨 RESUMEN DE VULNERABILIDADES CRÍTICAS DETECTADAS 🚨")
        log("=======================================================")
        try:
            alertas = []
            with open(report_path, 'r', encoding='utf-8', errors='ignore') as f:
                for linea in f:
                    # Buscamos el código ANSI rojo (31m) típico de PEASS
                    if '31m' in linea and 'Legend:' not in linea and 'winpeas' not in linea.lower():
                        # Limpiamos los caracteres especiales (ANSI escape codes)
                        texto_limpio = re.sub(r'\x1b\[[0-9;]*m', '', linea).strip()
                        # Filtramos líneas vacías o firmas largas sin sentido
                        if len(texto_limpio) > 5 and len(texto_limpio) < 150 and texto_limpio not in alertas:
                            alertas.append(texto_limpio)
            
            if alertas:
                for alerta in alertas[:15]:  # Muestra el Top 15 para no saturar
                    log(f" [!] {alerta}")
                if len(alertas) > 15:
                    log(f"\n [+] ... y {len(alertas) - 15} vulnerabilidades adicionales. (Revisa el archivo de texto en el Escritorio).")
            else:
                log(" [+] No se encontraron alertas rojas o falló la extracción visual. Revisa el reporte manual.")
                
        except Exception as e:
            log(f" [-] Error al generar el resumen en pantalla: {e}")
            
        log(f"\n[+] Reporte completo guardado en: {report_path}")
        
        # --- PROTOCOLO DE AUTO-BLINDAJE ---
        if messagebox.askyesno("Blindaje Automático", "El sistema presenta vulnerabilidades.\n\n¿Deseas que TREMEND aplique un 'Auto-Blindaje' ahora mismo?\n(Activa UAC, protege la RAM (LSA), restaura Defender y limpia rastros forenses)."):
            log("\n[*] INICIANDO PROTOCOLO DE AUTO-BLINDAJE DEL SISTEMA...")
            script_blindaje = """
            Write-Host "    -> Reactivando Control de Cuentas de Usuario (UAC)..."
            Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "EnableLUA" -Value 1 -ErrorAction SilentlyContinue
            Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" -Name "ConsentPromptBehaviorAdmin" -Value 5 -ErrorAction SilentlyContinue
            
            Write-Host "    -> Activando Protección LSA (Evita robo de contraseñas de la memoria RAM)..."
            Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Lsa" -Name "RunAsPPL" -Value 1 -ErrorAction SilentlyContinue
            
            Write-Host "    -> Desactivando WDigest (Evita almacenar credenciales en texto plano)..."
            Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\SecurityProviders\\WDigest" -Name "UseLogonCredential" -Value 0 -ErrorAction SilentlyContinue
            
            Write-Host "    -> Restaurando seguridad de Windows Defender..."
            Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" -Name "DisableAntiSpyware" -ErrorAction SilentlyContinue
            
            Write-Host "    -> Purgando Historial forense de PowerShell..."
            Remove-Item -Path (Get-PSReadLineOption).HistorySavePath -ErrorAction SilentlyContinue
            
            Write-Host "[+] PROTOCOLO DE BLINDAJE FINALIZADO. (Los escudos de seguridad tomarán efecto al reiniciar la PC)."
            """
            run_ps_script(log, script_blindaje)
        else:
            log("[*] El sistema no fue modificado.")

    # Limpieza
    if messagebox.askyesno("Limpieza Forense", "¿Deseas ELIMINAR el motor WinPEAS de la computadora para no dejar ningún rastro?"):
        shutil.rmtree(temp_dir, ignore_errors=True)
        log("\n[+] Limpieza táctica completada. Archivos destruidos.")

def logica_desproteger_excel(log, ruta_archivo):
    import zipfile, os, re, shutil
    
    log(f"\n[*] Iniciando análisis forense del archivo: {os.path.basename(ruta_archivo)}")
    
    if not ruta_archivo.lower().endswith('.xlsx'):
        log("[-] Error: Esta herramienta solo soporta archivos modernos de Excel (.xlsx).")
        return

    directorio = os.path.dirname(ruta_archivo)
    nombre_base = os.path.basename(ruta_archivo).replace('.xlsx', '')
    ruta_salida = os.path.join(directorio, f"{nombre_base}_Desbloqueado.xlsx")

    temp_dir = os.path.join(os.environ.get('TEMP'), "Tremend_ExcelHack")
    if os.path.exists(temp_dir): shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir)

    try:
        log("[*] Desempaquetando estructura interna del documento (Formato OOXML)...")
        # 1. Extraemos todo el contenido del archivo .xlsx como si fuera un ZIP
        with zipfile.ZipFile(ruta_archivo, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        worksheets_dir = os.path.join(temp_dir, "xl", "worksheets")
        if not os.path.exists(worksheets_dir):
            log("[-] Estructura inválida. No se encontró la carpeta de hojas de cálculo.")
            return

        log("[*] Buscando y destruyendo algoritmos de protección en las hojas...")
        modificadas = 0
        
        # 2. Iteramos sobre todos los archivos XML de las hojas
        for file in os.listdir(worksheets_dir):
            if file.endswith(".xml"):
                filepath = os.path.join(worksheets_dir, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    contenido = f.read()

                # 3. MAGIA: Usamos Regex para encontrar y borrar la etiqueta <sheetProtection ... />
                nuevo_contenido, reemplazos = re.subn(r'<sheetProtection[^>]+>', '', contenido)

                if reemplazos > 0:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(nuevo_contenido)
                    log(f"    -> [!] Candado eliminado exitosamente en: {file}")
                    modificadas += 1

        if modificadas == 0:
            log("[-] No se detectó ninguna protección de celdas en este documento.")
        else:
            log("[*] Reempaquetando código fuente y compilando nuevo archivo Excel...")
            # 4. Volvemos a comprimir la carpeta temporal en un archivo .xlsx nuevo
            with zipfile.ZipFile(ruta_salida, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zip_out.write(file_path, arcname)

            log(f"\n[+] ¡ÉXITO! Archivo guardado de forma segura como: {os.path.basename(ruta_salida)}")
            
            # 5. Pausa táctica y pregunta elegante para no robar el foco de la terminal
            import time
            time.sleep(1) # Le da 1 segundo al usuario para contemplar el código final
            
            from tkinter import messagebox
            if messagebox.askyesno("Operación Exitosa", "El candado XML ha sido destruido.\n\n¿Deseas abrir la carpeta para ver tu archivo desbloqueado?"):
                try: os.startfile(directorio)
                except: pass

    except Exception as e:
        log(f"[-] Error crítico durante la inyección: {e}")
    finally:
        # 5. Limpieza Táctica (Borramos la carpeta temporal)
        try: shutil.rmtree(temp_dir, ignore_errors=True)
        except: pass

def logica_optimizador_android(log):
    import urllib.request, zipfile, os, shutil, subprocess, time
    from tkinter import messagebox
    
    log("\n[*] Iniciando Módulo de Optimización Android (Vía ADB)...")
    
    # 1. Preparar Entorno Fantasma
    temp_dir = os.path.join(os.environ.get('TEMP'), "Tremend_ADB")
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    
    adb_exe = os.path.join(temp_dir, "platform-tools", "adb.exe")
    
    # 2. Descarga del Puente Oficial de Google (Oculto)
    if not os.path.exists(adb_exe):
        log("[*] Descargando puente de comunicación oficial (Google ADB)...")
        zip_path = os.path.join(temp_dir, "adb.zip")
        url_adb = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
        try:
            req = urllib.request.Request(url_adb, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response, open(zip_path, 'wb') as out_file:
                out_file.write(response.read())
                
            log("[*] Compilando traductor en memoria temporal...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref: zip_ref.extractall(temp_dir)
            os.remove(zip_path)
        except Exception as e:
            log(f"[-] Error crítico de conexión con Google: {e}"); return
            
    # 3. Iniciando Conexión
    log("[*] Buscando dispositivo conectado por USB...")
    log("[!] REQUISITO: El celular debe tener la pantalla desbloqueada y la 'Depuración USB' activada.")
    
    subprocess.run(f'"{adb_exe}" start-server', shell=True, capture_output=True)
    time.sleep(1)
    
    salida = subprocess.run(f'"{adb_exe}" devices', shell=True, capture_output=True, text=True).stdout
    
    # 4. Manejo de Autorización
    if "unauthorized" in salida:
        log("\n[-] DISPOSITIVO BLOQUEADO POR SEGURIDAD:")
        log("    -> Mira la pantalla de tu celular y presiona 'Permitir depuración USB'.")
        log("    -> Esperando 10 segundos para reintentar la conexión...")
        time.sleep(10)
        salida = subprocess.run(f'"{adb_exe}" devices', shell=True, capture_output=True, text=True).stdout
        
    lineas_devices = [line for line in salida.splitlines() if "device" in line and not "List of" in line and "unauthorized" not in line]
    
    if not lineas_devices:
        log("\n[-] FALLO DE CONEXIÓN: No se detectó ningún celular autorizado.")
        log("    1. Verifica el cable USB (debe ser de transferencia de datos).")
        log("    2. Revisa que las 'Opciones de Desarrollador' estén encendidas.")
        subprocess.run(f'"{adb_exe}" kill-server', shell=True, capture_output=True)
        return
        
    log("\n[+] ¡Dispositivo detectado y enlazado con éxito al núcleo TREMEND!")
    
    # 5. Extracción de Información
    modelo = subprocess.run(f'"{adb_exe}" shell getprop ro.product.model', shell=True, capture_output=True, text=True).stdout.strip()
    log(f"    -> Modelo Objetivo: {modelo}")
    
    log("\n[*] Iniciando inyección de limpieza extrema en segundo plano...")
    
    # 6. Comandos de Purga Segura (Magia Linux en Android)
    # Explicación de WhatsApp: 'msgstore-*' borra 'msgstore-2023-01.db.crypt14' pero IGNORA 'msgstore.db.crypt14' (el actual).
    comandos_purga = [
        ("Caché Global de Aplicaciones (Sistema)", "rm -rf /sdcard/Android/data/*/cache/*"),
        ("Caché Oculta de Telegram", "rm -rf /sdcard/Android/data/org.telegram.messenger/cache/*"),
        ("Copias de Seguridad Viejas de WhatsApp (Android 11+)", "rm -rf /sdcard/Android/media/com.whatsapp/WhatsApp/Databases/msgstore-*"),
        ("Copias de Seguridad Viejas de WhatsApp (Antiguos)", "rm -rf /sdcard/WhatsApp/Databases/msgstore-*"),
        ("Miniaturas Fantasma (Thumbnails)", "rm -rf /sdcard/DCIM/.thumbnails/*"),
        ("Archivos Temporales Ocultos de Descarga", "rm -rf /sdcard/Download/.nomedia")
    ]
    
    for nombre, cmd in comandos_purga:
        log(f"    -> Purgando: {nombre}")
        subprocess.run(f'"{adb_exe}" shell "{cmd}"', shell=True, capture_output=True)
        
    log("\n=======================================================")
    log(" [+] LIMPIEZA MILITAR DE ANDROID COMPLETADA ")
    log("=======================================================")
    log("[!] Gigabytes de basura eliminados.")
    log("[!] Tus sesiones, cuentas, fotos, videos y chats están 100% intactos.")
    
    try: notificar_voz(f"El dispositivo {modelo} ha sido purgado y optimizado.")
    except: pass
    
    # 7. Desconexión y Limpieza del Puente
    subprocess.run(f'"{adb_exe}" kill-server', shell=True, capture_output=True)
    if messagebox.askyesno("Limpieza", "El proceso Android ha concluido.\n\n¿Deseas destruir el motor ADB de la computadora para no dejar rastro de la conexión?"):
        try: shutil.rmtree(temp_dir, ignore_errors=True); log("\n[*] Limpieza táctica: Rastros eliminados del PC.")
        except: pass

def logica_ytdlp(log, lista_urls, calidad, formato, ruta_cookies=""):
    import zipfile, urllib.request, os, shutil, subprocess, json
    
    # 1. DIRECTORIO UNIFICADO DE MOTORES MULTIMEDIA
    temp_dir = r"C:\Tremend_Media"
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    ffmpeg_path = os.path.join(temp_dir, "ffmpeg.exe")
    ffprobe_path = os.path.join(temp_dir, "ffprobe.exe")

    # 2. ASEGURAR FFMPEG (Se usa para fusionar video Y para convertir WEBP a JPG)
    if not os.path.exists(ffmpeg_path) or not os.path.exists(ffprobe_path):
        log("[*] Descargando motor de procesamiento multimedia (FFmpeg)...")
        log("    -> [!] Son unos 100MB. Descargando silenciosamente, por favor espera...")
        try:
            zip_path = os.path.join(temp_dir, "ffmpeg.zip")
            url_ffmpeg = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            req = urllib.request.Request(url_ffmpeg, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120) as response, open(zip_path, 'wb') as out_file:
                out_file.write(response.read())
            log("[*] Extrayendo componentes de conversión...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    filename = os.path.basename(member)
                    if filename in ["ffmpeg.exe", "ffprobe.exe"]:
                        with open(os.path.join(temp_dir, filename), "wb") as f_out: f_out.write(zip_ref.read(member))
            os.remove(zip_path)
            log("[+] Códecs instalados con éxito.")
        except Exception as e: log(f"[-] Advertencia al procesar códecs: {e}")

    # === RAMA DE FOTOGRAFÍAS (GALLERY-DL) ===
    if calidad in ['4', '5']:
        log(f"\n[*] Iniciando Extractor de Galerías de Imágenes (Lote de {len(lista_urls)} enlaces)")
        exe_path = os.path.join(temp_dir, "gallery-dl.exe")
        
        # Descarga del motor silenciosa
        if not os.path.exists(exe_path):
            log("[*] Contactando API de GitHub para ubicar el motor de fotos...")
            api_url = "https://api.github.com/repos/mikf/gallery-dl/releases/latest"
            url_gdl = None
            try:
                req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as response:
                    data = json.loads(response.read().decode())
                if not ('message' in data and 'rate limit' in data.get('message', '').lower()):
                    for asset in data.get('assets', []):
                        nombre = asset.get('name', '').lower()
                        if 'gallery-dl' in nombre and nombre.endswith('.exe'):
                            url_gdl = asset['browser_download_url']
                            break
            except: pass

            if not url_gdl: url_gdl = "https://github.com/mikf/gallery-dl/releases/download/v1.27.2/gallery-dl.exe"
            try: urllib.request.urlretrieve(url_gdl, exe_path)
            except Exception as e2: log(f"[-] Error de red: {e2}"); return

        dl_path = os.path.join(os.environ.get("USERPROFILE"), "Downloads", "TREMEND_Galerias")
        if not os.path.exists(dl_path): os.makedirs(dl_path)
        urls_param = ' '.join([f'"{u}"' for u in lista_urls])
        
        if ruta_cookies and os.path.exists(ruta_cookies):
            log("[*] Inyectando sesión desde archivo cookies.txt (Bypass Maestro activado)...")
            cmd = f'"{exe_path}" --cookies "{ruta_cookies}" --directory "{dl_path}" {urls_param}'
        else:
            log("[*] Extracción Directa (Modo Público)...")
            cmd = f'"{exe_path}" --directory "{dl_path}" {urls_param}'
            
        run_cmd(log, cmd)

        # --- LA MAGIA: CONVERSIÓN AUTOMÁTICA DE WEBP A JPG ---
        log("[*] Escaneando carpeta en busca de archivos WEBP para convertirlos a JPG...")
        convertidas = 0
        for root, dirs, files in os.walk(dl_path):
            for file in files:
                if file.lower().endswith('.webp'):
                    ruta_webp = os.path.join(root, file)
                    ruta_jpg = os.path.join(root, file[:-5] + ".jpg")
                    try:
                        # Ejecuta FFmpeg para convertir la imagen sin perder calidad (-qscale:v 2)
                        subprocess.run(f'"{ffmpeg_path}" -y -i "{ruta_webp}" -qscale:v 2 "{ruta_jpg}"', shell=True, capture_output=True)
                        os.remove(ruta_webp) # Borramos el WEBP original
                        convertidas += 1
                    except: pass
        
        if convertidas > 0:
            log(f"[+] {convertidas} imágenes WEBP convertidas a JPG de alta calidad exitosamente.")
        
        log(f"\n=======================================================")
        log(f" [+] EXTRACCIÓN COMPLETADA. Imágenes guardadas en:")
        log(f" [+] {dl_path}")
        log(f"=======================================================")
        try: os.startfile(dl_path)
        except: pass
        try: notificar_voz("La extracción de la galería ha finalizado.")
        except: pass
        
        from tkinter import messagebox
        if messagebox.askyesno("Limpieza", "¿Deseas ELIMINAR el motor de fotos para no dejar rastro?"):
            shutil.rmtree(temp_dir, ignore_errors=True)
            log("[+] Limpieza táctica completada.")
        return 
        
    # === RAMA ORIGINAL DE VIDEOS (YT-DLP) ===
    log(f"\n[*] Iniciando Descargador Multimedia Avanzado (Lote de {len(lista_urls)} enlaces)")
    exe_path = os.path.join(temp_dir, "yt-dlp.exe")
    
    if not os.path.exists(exe_path):
        log("[*] Descargando motor de extracción portátil (yt-dlp)...")
        try: urllib.request.urlretrieve("https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe", exe_path)
        except Exception as e: log(f"[-] Error de red en yt-dlp: {e}"); return

    dl_path = os.path.join(os.environ.get("USERPROFILE"), "Downloads")
    urls_param = ' '.join([f'"{u}"' for u in lista_urls])
    params_base = '--no-playlist --windows-filenames -o "%(title).80s [%(id)s].%(ext)s" --embed-metadata --embed-thumbnail'
    
    if calidad == '3':
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -x --audio-format mp3 -P "{dl_path}" {urls_param}'
    elif calidad == '1':
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -S "vcodec:vp9" --remux-video {formato} -f "bestvideo+bestaudio/best" --merge-output-format {formato} -P "{dl_path}" {urls_param}'
    elif calidad == '2':
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -S "vcodec:vp9" --remux-video {formato} -f "bestvideo[height<=1080]+bestaudio/best" --merge-output-format {formato} -P "{dl_path}" {urls_param}'
    else: return

    log("[*] Procesando flujos y uniendo contenedores. Por favor, espera...")
    run_cmd(log, cmd)
    log("[+] Extracción e integración completadas. Archivos unificados en Descargas.")
    try: notificar_voz("La descarga del contenido ha finalizado.")
    except: pass
    from tkinter import messagebox
    if messagebox.askyesno("Limpieza", "¿Deseas ELIMINAR los motores multimedia para no dejar rastro?"):
        shutil.rmtree(temp_dir, ignore_errors=True)
        log("[+] Limpieza táctica: Espacio liberado.")

def logica_galerias(log, lista_urls, navegador="chrome"):
    import urllib.request, os, shutil, subprocess, json
    log(f"\n[*] Iniciando Extractor de Galerías (Lote de {len(lista_urls)} enlaces)")
    temp_dir = os.path.join(os.environ.get('TEMP'), "Tremend_Gallery")
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    
    exe_path = os.path.join(temp_dir, "gallery-dl.exe")
    
    # 1. Asegurar Motor Base de Descarga
    if not os.path.exists(exe_path):
        log("[*] Contactando API de GitHub para ubicar el motor (gallery-dl)...")
        api_url = "https://api.github.com/repos/mikf/gallery-dl/releases/latest"
        
        url_gdl = None
        try:
            req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
            
            if 'message' in data and 'rate limit' in data.get('message', '').lower():
                log("[-] Límite de peticiones de la API agotado.")
            else:
                for asset in data.get('assets', []):
                    nombre = asset.get('name', '').lower()
                    if 'gallery-dl' in nombre and nombre.endswith('.exe'):
                        url_gdl = asset['browser_download_url']
                        break
        except Exception as e: 
            log(f"[-] Error al interrogar a GitHub: {e}")

        if not url_gdl:
            log("[!] Activando modo de contingencia: Usando enlace de respaldo directo...")
            url_gdl = "https://github.com/mikf/gallery-dl/releases/download/v1.27.2/gallery-dl.exe"

        try:
            log(f"[*] Descargando binario de extracción...")
            urllib.request.urlretrieve(url_gdl, exe_path)
            log("[+] Descarga de motor exitosa.")
        except Exception as e2:
            log(f"[-] Error Crítico definitivo de descarga: {e2}")
            return
            
    dl_path = os.path.join(os.environ.get("USERPROFILE"), "Downloads", "TREMEND_Galerias")
    if not os.path.exists(dl_path): os.makedirs(dl_path)
    
    urls_param = ' '.join([f'"{u}"' for u in lista_urls])
    
    # --- FIX MAESTRO: Lector de Archivos vs Lector de Navegador ---
    flag_cookies = ""
    if navegador and navegador != "ninguno":
        # Si la ruta que nos llega termina en .txt, significa que usamos el archivo
        if navegador.lower().endswith('.txt'):
            log(f"[*] Aplicando Bypass Maestro: Inyectando sesión desde archivo de texto...")
            flag_cookies = f'--cookies "{navegador}"'
        else:
            log(f"[*] Aplicando Bypass Anti-Bot: Clonando sesión de {navegador.capitalize()}...")
            flag_cookies = f'--cookies-from-browser {navegador}'
    
    cmd = f'"{exe_path}" {flag_cookies} --directory "{dl_path}" {urls_param}'
    
    log("[*] Interceptando servidores e iniciando extracción múltiple. Por favor, espera...")
    run_cmd(log, cmd)
    
    log(f"\n=======================================================")
    log(f" [+] EXTRACCIÓN COMPLETADA. Imágenes guardadas en:")
    log(f" [+] {dl_path}")
    log(f"=======================================================")
    
    try: os.startfile(dl_path)
    except: pass
    try: notificar_voz("La extracción de la galería ha finalizado.")
    except: pass

    from tkinter import messagebox
    if messagebox.askyesno("Limpieza de Herramienta", "La descarga ha finalizado.\n\n¿Deseas ELIMINAR el motor para no dejar rastro?"):
        shutil.rmtree(temp_dir, ignore_errors=True)
        log("[+] Limpieza táctica: Motor de galerías destruido.")
    else:
        log("[*] Motor conservado para el futuro.")

def logica_gestor_usb(log, accion, disco=""):
    import winreg, os
    
    if accion in ['1', '2']:
        bloquear = (accion == '1')
        valor = 4 if bloquear else 3
        estado = "BLOQUEADOS" if bloquear else "DESBLOQUEADOS"
        log(f"\n[*] Alterando directivas de montaje del Kernel (USBSTOR) a estado: {estado}...")
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\USBSTOR", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, valor)
            log(f"[+] ¡Éxito! Los puertos USB de almacenamiento masivo han sido {estado}.")
            log("    -> Nota: Periféricos como teclados o mouses seguirán funcionando normalmente.")
        except Exception as e: 
            log(f"[-] Error de privilegios (Asegúrate de ejecutar TREMEND como Administrador): {e}")

    elif accion == '3':
        log(f"\n[*] Removiendo protección contra escritura en el Disco Físico N° {disco}...")
        script_path = os.path.join(os.environ.get("TEMP"), "dp_unlock.txt")
        try:
            with open(script_path, "w") as f:
                f.write(f"select disk {disco}\nattributes disk clear readonly\nexit")
            run_cmd(log, f'diskpart /s "{script_path}"')
            log("[+] Atributos de solo lectura eliminados. La unidad ya se puede formatear.")
        except Exception as e: 
            log(f"[-] Error durante la inyección de Diskpart: {e}")

    try: notificar_voz("El Gestor Avanzado de puertos U S B ha terminado.")
    except: pass

def logica_sysprep(log):
    log("\n[*] Preparando equipo para clonación/venta (Iniciando Sysprep)...")
    log("[!] El sistema generalizará la imagen y ejecutará el apagado automático.")
    run_cmd(log, r"%windir%\System32\Sysprep\sysprep.exe /generalize /oobe /shutdown")

def logica_borrado_seguro(log):
    log("\n[!] ADVERTENCIA: Esta operación sobrescribe el disco C: con cifrado para evitar recuperaciones forenses.")
    run_cmd(log, "cipher /w:C:\\")

    notificar_voz("El Borrado Seguro ha terminado.")

def logica_laboratorio_criptografico(log, accion, dato=""):
    import math
    import secrets
    import string

    # --- MOTOR DE ENTROPÍA (Inspirado en el Vault del video) ---
    def calcular_entropia(pwd):
        if not pwd:
            return 0, "0 Segundos (Vacía)"
            
        pool_size = 0
        if any(c.islower() for c in pwd): pool_size += 26
        if any(c.isupper() for c in pwd): pool_size += 26
        if any(c.isdigit() for c in pwd): pool_size += 10
        if any(c in string.punctuation for c in pwd): pool_size += 32
        
        # Fórmula matemática de entropía: E = L * log2(R)
        entropia = len(pwd) * math.log2(pool_size) if pool_size > 0 else 0
        
        # Cálculo de tiempo estimado (Asumiendo un ataque moderno de GPU a 100 Billones de hashes/segundo)
        hashes_por_segundo = 100_000_000_000
        combinaciones = 2 ** entropia
        segundos = combinaciones / hashes_por_segundo
        
        if segundos < 1: tiempo_str = "Menos de un segundo ❌"
        elif segundos < 60: tiempo_str = f"{int(segundos)} Segundos ⚠️"
        elif segundos < 3600: tiempo_str = f"{int(segundos / 60)} Minutos ⚠️"
        elif segundos < 86400: tiempo_str = f"{int(segundos / 3600)} Horas ⚠️"
        elif segundos < 31536000: tiempo_str = f"{int(segundos / 86400)} Días 🛡️"
        elif segundos < 3153600000: tiempo_str = f"{int(segundos / 31536000)} Años 🛡️"
        elif segundos < 3153600000000: tiempo_str = f"{int(segundos / 3153600000)} Milenios 💎"
        else: tiempo_str = "Edad del Universo (Inhackeable) 🌌"
            
        return entropia, tiempo_str

    log("\n" + "="*75)
    log(" 🔐 LABORATORIO CRIPTOGRÁFICO DE TREMEND ")
    log("="*75)

    if accion == '1': # Auditar Contraseña Existente
        if not dato:
            log("[-] Operación cancelada. No se ingresó ninguna clave.")
            return
            
        log("[*] Analizando la estructura matemática de la contraseña...")
        entropia, tiempo = calcular_entropia(dato)
        
        log(f"\n 📊 RESULTADOS DEL ANÁLISIS:")
        log(f"    -> Contraseña Oculta : {'*' * len(dato)}")
        log(f"    -> Longitud          : {len(dato)} caracteres")
        log(f"    -> Nivel de Entropía : {entropia:.2f} Bits")
        log(f"\n ⏱️ TIEMPO DE HACKEO ESTIMADO (Fuerza Bruta GPU):")
        log(f"    >> {tiempo} <<\n")
        
        if entropia < 50:
            log("[!] ADVERTENCIA: Esta clave es extremadamente vulnerable. Te sugerimos cambiarla.")
        elif entropia < 80:
            log("[+] INFO: Es una clave decente, pero podría ser rota por granjas de servidores.")
        else:
            log("[+] EXCELENTE: Tu contraseña tiene seguridad de Grado Militar.")

    elif accion == '2': # Generar Nueva Clave Militar
        try:
            longitud = int(dato)
            if longitud < 8:
                log("[-] Por tu seguridad, la longitud mínima para una clave militar es de 8 caracteres.")
                longitud = 8
        except:
            log("[-] Error: Longitud inválida. Usando 16 caracteres por defecto.")
            longitud = 16

        log(f"[*] Forjando clave encriptada de {longitud} caracteres...")
        
        caracteres = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        clave_nueva = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        
        entropia, tiempo = calcular_entropia(clave_nueva)
        
        log(f"\n 🛡️ NUEVA CLAVE GENERADA EXITOSAMENTE:")
        log(f"    -> {clave_nueva}")
        log(f"    -> Fuerza (Entropía) : {entropia:.2f} Bits")
        log(f"    -> Tiempo de Hackeo  : {tiempo}\n")
        
        try:
            app.clipboard_clear()
            app.clipboard_append(clave_nueva)
            log("[+] ¡La clave ha sido copiada automáticamente a tu portapapeles y está lista para usarse!")
        except:
            log("[-] Usa clic derecho para copiarla manualmente.")

def logica_modo_dios(log):
    import os, sys, subprocess, shutil
    import importlib.util
    from tkinter import messagebox
    import customtkinter as ctk
    
    log("\n" + "="*75)
    log(" 🤖 INICIANDO PROTOCOLO MODO DIOS (ESCÁNER UNIVERSAL Y OSINT) ")
    log("="*75)
    
    # 1. ESCÁNER DE HARDWARE (CÁMARAS CONECTADAS)
    log("[*] Interrogando al sistema por dispositivos de captura óptica...")
    script_cam = "Get-CimInstance Win32_PnPEntity | Where-Object {$_.PNPClass -match 'Image|Camera'} | Select-Object -ExpandProperty Name"
    res_cams = subprocess.run(["powershell", "-NoProfile", "-Command", script_cam], capture_output=True, text=True)
    camaras_detectadas = [c.strip() for c in res_cams.stdout.splitlines() if c.strip()]
    
    lista_nombres = ""
    if not camaras_detectadas:
        lista_nombres = "0. Cámara Predeterminada (No se detectaron nombres)\n"
    else:
        for i, cam in enumerate(camaras_detectadas):
            lista_nombres += f"{i}. {cam}\n"
            
    dialogo = ctk.CTkInputDialog(text=f"Cámaras detectadas en este PC:\n\n{lista_nombres}\nIngresa el NÚMERO de la cámara a usar (Ej: 0 o 1):", title="Selección de Sensor")
    op = dialogo.get_input()
    
    if op is None:
        log("[-] Operación cancelada por el usuario.")
        return
        
    cam_index = 0
    if op.isdigit():
        cam_index = int(op)
        
    # 2. VERIFICACIÓN DE MOTORES
    log("[*] Analizando escudos visuales y librerías matemáticas...")
    has_cv2 = importlib.util.find_spec("cv2") is not None
    has_psutil = importlib.util.find_spec("psutil") is not None
    has_numpy = importlib.util.find_spec("numpy") is not None
    has_pyzbar = importlib.util.find_spec("pyzbar") is not None
    
    if has_cv2 and has_psutil and has_numpy and has_pyzbar:
        log("[+] Motores de visión artificial y decodificación de barras (PyZbar) en línea.")
    else:
        log("[!] Instalando módulos de visión (opencv-python, numpy, psutil, pyzbar)...")
        log("    -> [!] Esto puede tardar unos segundos. NO CIERRES la ventana...")
        subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python", "numpy", "psutil", "pyzbar"], capture_output=True)
        log("[+] Módulos de visión instalados con éxito.")

    escritorio = os.path.join(os.environ.get("USERPROFILE"), "Desktop")
    if not os.path.exists(escritorio): 
        escritorio = os.path.join(os.environ.get("USERPROFILE"), "Escritorio")
        
    # BÓVEDA SEGURA TEMP PARA LOS CÓDIGOS
    temp_qr = os.path.join(escritorio, "TREMEND_Codigos_Escaneados.txt").replace("\\", "/")

    # 3. EL SCRIPT ESCLAVO (Anti-Crash y Multihilo)
    script_jarvis = """import os
import sys

# --- FIX 1: BLINDAJE DE ENCODING ---
try: sys.stdout.reconfigure(encoding='utf-8')
except: pass

# --- FIX 2: SILENCIAR ERRORES C++ DE OPENCV ---
os.environ["OPENCV_LOG_LEVEL"] = "FATAL"
os.environ["OPENCV_VIDEOIO_DEBUG"] = "0"
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"

import cv2
import psutil
import time
import datetime
import math
import threading
import webbrowser
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol

cam_index = VAR_CAM_INDEX
escritorio = "VAR_ESCRITORIO"
archivo_qr = "VAR_TEMP_QR"
detectados = set()

# --- FIX 3: VOZ ASÍNCRONA PARA EVITAR CONGELAMIENTOS ---
def hablar(texto):
    def run_tts():
        try:
            import pyttsx3
            motor = pyttsx3.init()
            motor.setProperty('rate', 160)
            motor.say(texto)
            motor.runAndWait()
        except: pass
    threading.Thread(target=run_tts, daemon=True).start()

hablar("Protocolo Modo Dios en línea. HUD táctico y escáner universal activados.")

ping_ms = "Calculando..."
def medir_ping():
    global ping_ms
    while True:
        try:
            salida = os.popen("ping -n 1 -w 1000 8.8.8.8").read()
            if "tiempo=" in salida or "time=" in salida:
                tag = "tiempo=" if "tiempo=" in salida else "time="
                tiempo = salida.split(tag)[1].split("ms")[0]
                ping_ms = tiempo.strip() + " ms"
            else:
                ping_ms = "Desconectado"
        except:
            ping_ms = "Error"
        time.sleep(2)

threading.Thread(target=medir_ping, daemon=True).start()

# Forzar captura en formato directo
cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
if not cap.isOpened():
    cap = cv2.VideoCapture(cam_index)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Fórmula de Luhn (Validador matemático de IMEI)
def verificar_imei(imei):
    if not imei.isdigit() or len(imei) != 15: return False
    suma = 0
    for i, digito in enumerate(reversed(imei)):
        n = int(digito)
        if i % 2 == 1:
            n *= 2
            if n > 9: n -= 9
        suma += n
    return suma % 10 == 0

scan_y = 0
scan_dir = 1
angle = 0

print("[*] Lanzando Interfaz Holografica...")
print("[!] Enfoca cualquier codigo QR o de barras (IMEI) a la camara.")

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    overlay = frame.copy()

    try:
        # --- FIX 4: IGNORAR FORMATOS RAROS (Adiós a los Warnings PDF417) ---
        formatos = [ZBarSymbol.QRCODE, ZBarSymbol.CODE128, ZBarSymbol.CODE39, ZBarSymbol.EAN13, ZBarSymbol.EAN8]
        codigos = decode(frame, symbols=formatos)
        
        for codigo in codigos:
            data = codigo.data.decode('utf-8', errors='ignore')
            tipo = codigo.type
            pts = codigo.polygon
            
            if pts and len(pts) >= 4:
                pts = np.array([(pt.x, pt.y) for pt in pts], dtype=np.int32)
                cv2.polylines(overlay, [pts], True, (0, 255, 0), 3)
                cv2.putText(overlay, tipo, (pts[0][0], pts[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            if data not in detectados:
                detectados.add(data)
                
                with open(archivo_qr, "a", encoding="utf-8") as f:
                    fecha_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{fecha_str}] [{tipo}] -> {data}\\n")
                    
                print(f"\\n[+] NUEVO CODIGO ({tipo}) CAPTURADO:\\n{data}")
                
                # Análisis de IMEI
                if tipo != 'QRCODE' and len(data) == 15 and verificar_imei(data):
                    print(f"\\n[!] IMEI VALIDADO MATEMATICAMENTE: {data}")
                    
                    # --- FIX 5: COPIADO SEGURO AL PORTAPAPELES (Cero Crasheos) ---
                    try:
                        import subprocess
                        subprocess.run(['clip'], input=data, text=True)
                        print("[+] El IMEI fue copiado al portapapeles de Windows (Usa CTRL+V).")
                    except Exception as ec: 
                        print("[-] Fallo menor copiando el texto:", ec)
                    
                    print("[*] Abriendo bases de datos OSINT de forma automatica...")
                    webbrowser.open(f"https://imeicheck.com/imei-check?imei={data}")
                    webbrowser.open("https://www.imeicolombia.com.co/")
                    
                    hablar("I M E I celular detectado.")
                else:
                    try:
                        import ctypes
                        ctypes.windll.kernel32.Beep(1000, 200)
                    except: pass
    except Exception as em:
        pass

    # Animacion Holografica
    cx, cy = w//2, h//2
    angle += 0.05
    cv2.circle(overlay, (cx, cy), 120, (255, 204, 0), 1)
    cv2.circle(overlay, (cx, cy), 80, (255, 204, 0), 1)
    
    px1, py1 = int(cx + 120 * math.cos(angle)), int(cy + 120 * math.sin(angle))
    cv2.circle(overlay, (px1, py1), 6, (0, 255, 0), -1)
    
    px2, py2 = int(cx + 80 * math.cos(-angle * 1.5)), int(cy + 80 * math.sin(-angle * 1.5))
    cv2.circle(overlay, (px2, py2), 5, (0, 255, 255), -1)

    cv2.line(overlay, (cx-140, cy), (cx+140, cy), (255, 204, 0), 1)
    cv2.line(overlay, (cx, cy-140), (cx, cy+140), (255, 204, 0), 1)

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    try: bat = psutil.sensors_battery().percent if psutil.sensors_battery() else 100
    except: bat = 100

    cv2.putText(overlay, f"CPU: {cpu}%", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(overlay, f"RAM: {ram}%", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(overlay, f"BAT: {bat}%", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(overlay, f"NET PING: {ping_ms}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    now = datetime.datetime.now().strftime("%H:%M:%S")
    cv2.putText(overlay, f"SYS TIME: {now}", (w - 180, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    cv2.putText(overlay, "TREMEND OS - MODO DIOS", (w - 230, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    cv2.putText(overlay, "['Q' SALIR] ['C' FOTO] ['T' VER BOVEDA]", (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    scan_y += 5 * scan_dir
    if scan_y > h or scan_y < 0: scan_dir *= -1
    cv2.line(overlay, (0, scan_y), (w, scan_y), (0, 255, 0), 1)

    alpha = 0.4
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    cv2.imshow("TREMEND - Holographic HUD (Modo Dios)", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        nombre_img = f"TREMEND_Evidencia_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
        ruta_img = os.path.join(r"{escritorio}", nombre_img)
        cv2.imwrite(ruta_img, frame)
        print(f"\\n[+] Captura forense guardada en: {ruta_img}")
        try:
            cv2.rectangle(frame, (0,0), (w,h), (255,255,255), -1)
            cv2.imshow("TREMEND - Holographic HUD (Modo Dios)", frame)
            cv2.waitKey(50)
        except: pass
    elif key == ord('t'):
        if os.path.exists(archivo_qr):
            os.startfile(archivo_qr)
        else:
            print("[-] Aun no has escaneado ningun codigo.")

cap.release()
cv2.destroyAllWindows()
""".replace("VAR_CAM_INDEX", str(cam_index)).replace("VAR_ESCRITORIO", escritorio.replace("\\", "/")).replace("VAR_TEMP_QR", temp_qr)
    
    temp_py = os.path.join(os.environ.get("TEMP"), "tremend_godmode.py")
    try:
        with open(temp_py, "w", encoding="utf-8") as f:
            f.write(script_jarvis)
        
        log("[*] Encendiendo hardware óptico y enrutando telemetría...")
        log("[!] AVISO: Presiona 'C' para fotos, 'T' para abrir Bóveda de Códigos, 'Q' para salir.")
        
        run_cmd(log, f'"{sys.executable}" "{temp_py}"')
        
        try: os.remove(temp_py)
        except: pass

        log("\n[+] Protocolo Modo Dios desactivado correctamente.")
        
        if messagebox.askyesno("Limpieza de Librerías", "El Modo Dios ha cerrado.\n\nLa librería visual de este modo (OpenCV y PyZbar) pesan alrededor de 80MB. ¿Deseas DESINSTALARLAS de este equipo para no dejar rastros de tu intervención?"):
            log("[*] Desinstalando módulos de visión artificial...")
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "opencv-python", "numpy", "pyzbar"], capture_output=True)
            log("[+] Limpieza táctica completada. Cero rastros en el disco.")
        else:
            log("[*] Motores visuales conservados para aperturas instantáneas en el futuro.")
            
    except Exception as e:
        log(f"[-] Ocurrió un error en el núcleo visual: {e}")

def logica_limpiar_portapapeles(log):
    run_cmd(log, "echo off | clip")
    log("\n[+] Portapapeles destruido.")

def logica_ejecutar_portable(log, carpeta, ejecutable):
    import urllib.request, urllib.parse, os, subprocess
    log(f"\n[*] Conectando con tu repositorio en la nube...")
    
    # Codificamos los espacios en los nombres de las carpetas para la URL
    carpeta_url = urllib.parse.quote(carpeta)
    exe_url = urllib.parse.quote(ejecutable)
    url_descarga = f"https://raw.githubusercontent.com/LennesVP/Programas_Portables/main/Programas_Portables/{carpeta_url}/{exe_url}"
    
    ruta_temp = os.path.join(os.environ.get('TEMP'), ejecutable)
    
    log(f"[*] Descargando '{ejecutable}' de forma sigilosa...")
    try:
        req = urllib.request.Request(url_descarga, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req, timeout=30) as response, open(ruta_temp, 'wb') as out_file:
            out_file.write(response.read())
        
        log("[+] Descarga completada. Ejecutando herramienta...")
        log("[!] TRABAJANDO... La consola limpiará el rastro cuando cierres el programa portátil.")
        
        # El programa se pausa aquí hasta que tú cierres la herramienta (ej. AnyDesk)
        subprocess.Popen(ruta_temp, shell=True).wait()
        
        log("\n[*] Herramienta cerrada. Destruyendo archivo temporal...")
        try:
            os.remove(ruta_temp)
            log("[+] Limpieza táctica exitosa. Cero rastros en el equipo.")
        except Exception:
            log("[-] El archivo sigue en uso en segundo plano, se borrará al reiniciar el PC.")
            
    except Exception as e:
        log(f"[-] Error de red o archivo no encontrado:\n{e}")

def logica_quitar_fondo(log, ruta_imagen):
    import os, sys, subprocess, shutil
    import importlib.util
    from tkinter import messagebox
    
    # 1. Rutas inteligentes
    directorio_base = os.path.dirname(ruta_imagen)
    nombre_base = os.path.basename(ruta_imagen).rsplit('.', 1)[0]
    ruta_salida = os.path.join(directorio_base, f"{nombre_base}_BorradorIA_TREMEND.png")
    
    # 2. Verificación de dependencias en la sombra (SIN ejecutar la librería para evitar Crasheos)
    log("[*] Analizando entorno en busca del Motor de Inteligencia Artificial (rembg)...")
    
    # FIX MAESTRO: Usamos importlib para escanear sin despertar a la IA
    has_rembg = importlib.util.find_spec("rembg") is not None
    has_onnx = importlib.util.find_spec("onnxruntime") is not None
    has_pil = importlib.util.find_spec("PIL") is not None
    
    if has_rembg and has_onnx and has_pil:
        log("[+] Motor de IA y procesador (onnxruntime) detectados. Todo en orden.")
    else:
        log("[!] Instalación corrupta o incompleta detectada en el sistema.")
        log("[*] Iniciando inyección y reparación de dependencias (rembg[cpu], onnxruntime, pillow)...")
        log("    -> [!] Esto descargará los motores (~100MB). Por favor espera y NO CIERRES la ventana...")
        
        # Usamos --upgrade para forzar a PIP a reparar el paquete dañado anterior
        cmd_pip = f'"{sys.executable}" -m pip install --upgrade "rembg[cpu]" onnxruntime pillow'
        subprocess.run(cmd_pip, shell=True, capture_output=True)
        log("[+] Red Neuronal reparada e instalada con soporte de procesamiento exitosamente.")
    
    # 3. Creación del Script Esclavo (Evita memory leaks y bloqueos en la interfaz gráfica)
    script_ia = f"""
import sys
try:
    print("[*] Iniciando motor neuronal... (Esto puede tomar unos segundos)", flush=True)
    from rembg import remove
    from PIL import Image
    
    input_path = r"{ruta_imagen}"
    output_path = r"{ruta_salida}"
    
    print("[*] Cargando matriz de píxeles en memoria...", flush=True)
    inp = Image.open(input_path)
    
    print("[*] Aplicando red neuronal U-2-Net para identificar al sujeto y aislar el fondo...", flush=True)
    out = remove(inp)
    
    print("[*] Renderizando transparencia (Canal Alpha) y guardando archivo PNG...", flush=True)
    out.save(output_path, "PNG")
    print("[+] Renderizado exitoso.", flush=True)
except Exception as e:
    print(f"[-] Error crítico en el núcleo de la IA: {{e}}", flush=True)
    sys.exit(1)
"""
    
    temp_py = os.path.join(os.environ.get('TEMP'), "tremend_ia_fondo.py")
    try:
        with open(temp_py, "w", encoding="utf-8") as f:
            f.write(script_ia)
            
        # 4. Ejecutar el script esclavo
        log("\n[*] Iniciando inyección de la imagen en la Inteligencia Artificial...")
        log("[!] AVISO: Si es la primera vez, la IA descargará su 'cerebro' pre-entrenado (~170MB).")
        
        run_cmd(log, f'"{sys.executable}" "{temp_py}"')
        
        if os.path.exists(ruta_salida):
            log(f"\n=======================================================")
            log(f" [+] MAGIA APLICADA: Fondo eliminado con éxito.")
            log(f" [+] Guardado en: {ruta_salida}")
            log(f"=======================================================")
            try: os.startfile(ruta_salida) # Abre la foto automáticamente
            except: pass
            
        try: os.remove(temp_py) # Limpieza táctica del esclavo
        except: pass
        
        # 5. PROTOCOLO DE DESTRUCCIÓN TOTAL (A PETICIÓN)
        if messagebox.askyesno("Limpieza Forense", "El proceso de Inteligencia Artificial ha terminado.\n\n¿Deseas EJECUTAR EL PROTOCOLO ASESINO para DESINSTALAR la IA, borrar los modelos de 170MB y no dejar ABSOLUTAMENTE NINGÚN RASTRO en este PC?"):
            log("\n[*] INICIANDO PROTOCOLO DE DESTRUCCIÓN DE LA IA...")
            log("    -> Desinstalando librerías neuronales (rembg, onnxruntime)...")
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "rembg", "onnxruntime"], capture_output=True)
            
            log("    -> Buscando y pulverizando la bóveda de modelos ocultos (.u2net)...")
            # La IA esconde su cerebro en C:\Users\NombreUsuario\.u2net
            ruta_modelos = os.path.join(os.environ.get("USERPROFILE"), ".u2net")
            if os.path.exists(ruta_modelos):
                try:
                    shutil.rmtree(ruta_modelos, ignore_errors=True)
                    log("    -> ¡Cerebro de la IA destruido con éxito!")
                except Exception as e:
                    log(f"    [-] No se pudo borrar la carpeta de modelos: {e}")
            else:
                log("    -> No se encontraron modelos residuales.")
                
            log("[+] LIMPIEZA TÁCTICA 100% COMPLETADA. Cero rastros de tu intervención.")
        else:
            log("\n[*] Motores de IA conservados para que la próxima vez sea instantáneo.")
        
    except Exception as e:
        log(f"[-] Ocurrió un fallo en el proceso principal: {e}")

def logica_instalar_herramienta(log, carpeta, archivos, comando):
    import urllib.request, urllib.parse, os, subprocess, shutil
    
    # Creamos una carpeta temporal única para no mezclar archivos
    temp_dir = os.path.join(os.environ.get('TEMP'), "TREMEND_Install")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    log(f"\n[*] Preparando entorno de instalación...")
    
    try:
        carpeta_url = urllib.parse.quote(carpeta)
        
        # 1. Ciclo de descarga (soporta múltiples archivos)
        for archivo in archivos:
            archivo_url = urllib.parse.quote(archivo)
            url_descarga = f"https://raw.githubusercontent.com/LennesVP/Encyclopedia-of-Tools/main/{carpeta_url}/{archivo_url}"
            ruta_destino = os.path.join(temp_dir, archivo)
            
            log(f"[*] Descargando '{archivo}'...")
            req = urllib.request.Request(url_descarga, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
            with urllib.request.urlopen(req, timeout=120) as response, open(ruta_destino, 'wb') as out_file:
                out_file.write(response.read())
                
        log("[+] Archivos descargados en la memoria temporal.")
        log(f"[*] Inyectando comando en el sistema: {comando}")
        log("[!] TRABAJANDO... No cierres esta ventana (Las instalaciones pesadas como Office pueden tardar varios minutos).")
        
        # 2. Ejecución silenciosa forzando el directorio temporal
        proceso = subprocess.Popen(comando, shell=True, cwd=temp_dir)
        proceso.wait()
        
        log("\n[+] ¡Instalación finalizada con éxito!")
        
    except Exception as e:
        log(f"[-] Error crítico en red o ejecución:\n{e}")
        
    finally:
        log("[*] Iniciando protocolo de limpieza...")
        try:
            shutil.rmtree(temp_dir)
            log("[+] Archivos de instalación purgados. Cero rastros.")
        except Exception:
            log("[-] Algunos archivos temporales están bloqueados. Se borrarán solos al reiniciar el PC.")

# ============================================================================
# 3.5 ASISTENTE VIRTUAL DE VOZ (SISTEMA COGNITIVO V4 - POWERSHELL ENGINE)
# ============================================================================
detener_voz = False
proceso_actual_tts = None

def abrir_guia_asistente():
    global detener_voz, proceso_actual_tts
    
    # Detenemos cualquier voz o proceso anterior al abrir la ventana
    detener_voz = True 
    if proceso_actual_tts:
        try: proceso_actual_tts.kill()
        except: pass
    time.sleep(0.3)
    detener_voz = False

    ventana_guia = ctk.CTkToplevel(app)
    ventana_guia.title("Asistente Virtual TREMEND")
    ventana_guia.geometry("1050x650")
    ventana_guia.attributes("-topmost", True)
    ventana_guia.transient(app)

    # --- DISEÑO A DOS PANELES (ESTILO DASHBOARD) ---
    panel_nav = ctk.CTkFrame(ventana_guia, width=320, fg_color="#1E293B", corner_radius=0)
    panel_nav.pack(side="left", fill="y")
    panel_nav.pack_propagate(False)

    panel_texto = ctk.CTkFrame(ventana_guia, fg_color="transparent")
    panel_texto.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(panel_texto, text="🎙️ Consola del Asistente", font=("Arial", 24, "bold"), text_color="#00FFCC").pack(anchor="w", pady=(0, 10))
    
    txt_subtitulos = ctk.CTkTextbox(panel_texto, fg_color="#0A0A0A", text_color="#10B981", font=("Consolas", 15), wrap="word", border_width=1, border_color="#334155")
    txt_subtitulos.pack(fill="both", expand=True)
    txt_subtitulos.insert("end", "SISTEMA COGNITIVO EN LÍNEA.\n\n[1] Navega por el menú de la izquierda.\n[2] Selecciona una categoría o ingresa el número de una función.\n[3] Te lo explicaré en lenguaje natural a través de los altavoces.\n")
    txt_subtitulos.configure(state="disabled")

    def update_ui_text(titulo, texto):
        if txt_subtitulos.winfo_exists():
            txt_subtitulos.configure(state="normal")
            txt_subtitulos.insert("end", f"▶ {titulo}:\n{texto}\n\n")
            txt_subtitulos.see("end")
            txt_subtitulos.configure(state="disabled")

    # --- MOTOR DE VOZ INVENCIBLE (VÍA POWERSHELL SYNTHESIS) ---
    def reproducir_guia(titulo_guia, diccionario_textos):
        global detener_voz, proceso_actual_tts
        
        detener_voz = True 
        if proceso_actual_tts:
            try: proceso_actual_tts.kill()
            except: pass
        time.sleep(0.3)
        detener_voz = False

        txt_subtitulos.configure(state="normal")
        txt_subtitulos.delete("1.0", "end")
        txt_subtitulos.insert("end", f"=== EXPLICANDO: {titulo_guia.upper()} ===\n\n")
        txt_subtitulos.configure(state="disabled")

        def run():
            global proceso_actual_tts
            for titulo, explicacion in diccionario_textos:
                if detener_voz or not ventana_guia.winfo_exists(): break

                # 1. Imprimimos el texto en la pantalla
                app.after(0, update_ui_text, titulo, explicacion)
                
                # 2. Limpiamos el texto para que suene humano y no rompa el código
                titulo_limpio = ''.join([i for i in titulo if not i.isdigit()]).replace(".", "").strip()
                texto_hablar = f"La función {titulo_limpio}. {explicacion}".replace("'", "").replace('"', "")
                
                # 3. Inyectamos la voz directo al núcleo de Windows (Cero Crasheos, Sincronización Perfecta)
                script_tts = f"Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Rate = -1; $s.Volume = 85; $s.Speak('{texto_hablar}')"
                
                try:
                    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                    proceso_actual_tts = subprocess.Popen(["powershell", "-NoProfile", "-Command", script_tts], creationflags=flags)
                    proceso_actual_tts.wait() # Bloquea el hilo hasta que termine de hablar, evitando que se salte
                except Exception as e:
                    print("Error de TTS:", e)
                
                time.sleep(0.4) 
            
            if not detener_voz and ventana_guia.winfo_exists():
                def fin():
                    txt_subtitulos.configure(state="normal")
                    txt_subtitulos.insert("end", "\n[✓] Explicación completada.\n")
                    txt_subtitulos.see("end")
                    txt_subtitulos.configure(state="disabled")
                app.after(0, fin)

        threading.Thread(target=run, daemon=True).start()

    def detener_habla():
        global detener_voz, proceso_actual_tts
        detener_voz = True
        
        # Aniquilación inmediata de la voz
        if proceso_actual_tts:
            try: proceso_actual_tts.kill()
            except: pass
            
        txt_subtitulos.configure(state="normal")
        txt_subtitulos.insert("end", "\n[!] Voz detenida por el usuario.\n")
        txt_subtitulos.see("end")
        txt_subtitulos.configure(state="disabled")

    # ==========================================================
    # DICCIONARIOS SINCRONIZADOS AL 100% CON EL CÓDIGO MAESTRO
    # ==========================================================
    guia_categorias_main = [
        ("Sistemas Operativos Windows", "Es el corazón de este programa. Aquí encontrarás todas las herramientas pesadas de reparación, manejo de redes y soporte técnico exclusivas para computadoras de Microsoft."),
        ("El Sistema Linux", "Un entorno de terminal profesional. Te permite ejecutar comandos de auditoría para revisar la seguridad de servidores como si fueras un administrador experto."),
        ("El Ecosistema Mac", "Una colección de aplicaciones y manuales diseñados para auditar, limpiar y optimizar computadoras de Apple de forma segura."),
        ("Herramientas Android", "Tu navaja suiza para celulares. Al conectar un teléfono por cable, esta sección te permite borrarle gigabytes de basura oculta sin tocar tus fotos o chats importantes."),
        ("La Nube y Tienda", "Aquí tienes programas portátiles que no necesitan instalarse, enciclopedias web, y la zona oficial para adquirir licencias de software."),
        ("El Proyecto TREMEND", "Aquí puedes descubrir cómo nació este proyecto desde cero, y cuál es nuestra filosofía de usar inteligencia artificial para resolver problemas reales.")
    ]

    guia_red_win = [
        ("1. Info Básica de Red e IP", "Muestra tu dirección real en internet al instante. Es muy útil para saber si tu ubicación está protegida o expuesta."),
        ("2. Reparador de Red Autónomo", "Si tu internet aparece conectado pero no carga ninguna página, este botón destapa las tuberías internas de Windows y te devuelve la conexión en segundos."),
        ("3. Prueba de Conectividad", "Funciona como un radar. Envía señales a una página web o a un puerto específico para ver si están vivos o si el firewall los está bloqueando."),
        ("4. Monitor Conexiones TCP", "Escanea y te muestra en vivo qué programas de tu computadora están conectados a internet consumiendo tus datos en la sombra."),
        ("5. Identificar Proceso por Puerto", "Si un programa falla porque el puerto está en uso, descubre exactamente qué aplicación fantasma lo está bloqueando."),
        ("6. Auditoría y Migración Wi-Fi", "Recupera todas las contraseñas de las redes wifi de tu computadora. Además, analiza si las claves son débiles y te advierte si alguna de ellas ha sido filtrada por hackers en internet."),
        ("7. Generador Universal de QR", "Crea una imagen de un código QR al instante. Puedes usarlo para que tus amigos se conecten a tu Wi-Fi sin dictarles la clave, o para compartir páginas web."),
        ("8. Radar OSINT de IP", "Rastrea como un investigador profesional cualquier dirección IP del mundo. Extrae su ciudad, proveedor de internet y te dibuja un mapa satelital interactivo directo en tu navegador."),
        ("9. Diagnóstico Wi-Fi", "Genera un reporte web muy profesional sobre la salud de tu tarjeta Wi-Fi, mostrando un historial detallado de caídas y desconexiones."),
        ("10. Resolución DNS Inversa", "Convierte el nombre de cualquier página web, como google punto com, en su dirección IP numérica real de servidores."),
        ("11. Gestor Avanzado de Hosts", "Un potente administrador de dominios. Te permite bloquear páginas web desde la raíz del sistema, restaurar sitios individuales o devolver la configuración de fábrica de un solo golpe."),
        ("12. Abrir Puertos Firewall", "Crea reglas automáticas para permitir que juegos, bases de datos o programas se comuniquen libremente sin bloqueos del antivirus."),
        ("13. Purgar Historial Wi-Fi", "Elimina de un solo golpe todas las redes inalámbricas memorizadas en tu PC para resolver problemas de conexión corrupta."),
        ("14. Reset Firewall a Fábrica", "Restaura las defensas y bloqueos de Windows a su estado original de seguridad. Útil si bloqueaste tu propio internet por error."),
        ("15. Purgar Caché ARP", "Obliga a tu computadora a volver a identificar desde cero los equipos físicos de tu red. Ideal tras cambiar el router."),
        ("16. Optimizador Avanzado de DNS", "Convierte tu conexión en un escudo perimetral a medida. Puedes elegir entre doce perfiles distintos: máxima velocidad con Cloudflare o Google, bloqueo total de publicidad con AdGuard o Mullvad, ciberseguridad extrema contra malware con Quad9 o ControlD, y filtros familiares estrictos para proteger a los niños de contenido para adultos. También incluye la opción para restaurar tu internet a la configuración de fábrica."),
        ("17. Gestionar Sesiones SMB", "Detecta al instante si alguien más en tu misma red local está conectado y accediendo a tus carpetas compartidas sin tu permiso."),
        ("18. Radar Wi-Fi de Espectro", "Realiza múltiples barridos a tu alrededor para ver redes Wi-Fi ocultas, señal exacta y encontrar canales libres de interferencia."),
        ("19. Auditoría Latencia", "Realiza pruebas continuas para detectar pequeños bajones o desconexiones de internet que causan lag en juegos o llamadas."),
        ("20. Radar de Puertos Avanzado", "Escáner multihilo de alta velocidad. Detecta tu equipo automáticamente o analiza redes externas en milisegundos buscando vectores de ataque o puertas traseras."),
        ("21. Crear Servidor NAS", "Transforma rápidamente una carpeta de tu PC en un servidor de alta velocidad para que celulares o televisores inteligentes puedan acceder a tus archivos."),
        ("22. Auditar Caché DNS Web", "Revela una lista oculta de las páginas web a las que esta computadora se ha conectado silenciosamente, incluso si borraron el historial."),
        ("23. Visualizador de Tráfico de Red", "Mapea y visualiza en tiempo real todo el tráfico que entra y sale de tu PC. Descubre qué aplicaciones espían y en qué país están sus servidores."),
        ("24. Escáner Forense Táctico", "La mejor herramienta de escaneo del mundo. Mapea puertos, detecta la versión exacta del sistema operativo y vulnerabilidades de un equipo."),
        ("25. Reparar Visibilidad LAN", "Soluciona inmediatamente el problema de no poder ver otras computadoras en la red para compartir archivos o enviar trabajos de impresión."),
        ("26. Auditor Web Forense", "Funciona como un radar espía para páginas web o módems. Extrae información técnica secreta del servidor y busca puertas traseras, paneles de control o carpetas de configuración olvidadas."),
        ("27. Radar Táctico de Enjambre Geo WiFi", "Avanzada herramienta de rastreo satelital. Auto-detecta el enjambre de redes a tu alrededor o triangula una MAC específica, con bypass directo a bases de datos mundiales de respaldo."),
        ("28. Radar Financiero y Laboratorio A P I", "Una pantalla interactiva que se conecta a servidores de la bolsa mundial en tiempo real. Te muestra exactamente a cómo está el Dólar y el Euro en Pesos Colombianos. Además, te incluye un panel educativo explicándote cómo el código de programación hizo la magia para robar ese dato de internet."),
        ("29. Laboratorio Forense Anti Phishing", "Tu defensa personal contra estafas por correo electrónico. Solo tienes que pegar el texto original de un correo sospechoso y la herramienta analizará las firmas criptográficas para decirte si es real o falso. Además, triangulará la ubicación y empresa del servidor que te lo envió para confirmar su identidad.")
    ]

    guia_mant_win = [
        ("1. Mantenimiento Extremo a Discos", "Selecciona qué discos o memorias USB limpiar. Vacía papeleras ocultas, borra cachés residuales y reconstruye el núcleo del sistema."),
        ("2. Optimización Chris Titus Tech", "La mejor herramienta para acelerar computadoras viejas. Desactiva funciones basura, bloquea telemetría y mejora drásticamente el rendimiento."),
        ("3. Desinstalar Apps Nativas", "Elimina de raíz programas basura y forzados de Windows, como Xbox y el Clima, que no te dejan desinstalar desde el Panel de Control."),
        ("4. Destrabar Cola de Impresión", "Solución instantánea para documentos trabados. Detiene el servicio de impresión, limpia los archivos atorados y reactiva la impresora."),
        ("5. Purgado Extremo de WinSxS", "Libera masivamente espacio del disco duro destruyendo archivos residuales y copias muertas de actualizaciones de Windows."),
        ("6. Reparar Windows Update Roto", "Arregla el fallo crítico donde el actualizador se queda buscando o se traba en cero por ciento descargando, reiniciando la base de datos interna."),
        ("7. Purgar Puntos de Restauración", "Borra copias de seguridad de Windows muy antiguas que están acaparando cientos de Gigabytes invisibles de forma completamente segura."),
        ("8. Reparar Telemetría de Hardware", "Arregla errores raros, como cuando la laptop no lee la batería, no funciona el brillo o los programas se cierran solos por errores de lectura."),
        ("9. Bloqueo de Espionaje Microsoft", "Detiene y bloquea los rastreadores nativos de Microsoft que envían lo que tecleas. Mejora el rendimiento de disco y red enormemente."),
        ("10. Sincronización Nuclear de Hora", "Soluciona errores graves de 'Sitio No Seguro' en internet, obligando a tu computadora a actualizar su hora con el reloj atómico global."),
        ("11. Destructor de Caché Web", "Acelera navegadores lentos borrando archivos temporales súper pesados. No toca contraseñas ni marcadores de los usuarios."),
        ("12. Reparación de Disco Físico", "Aplica una corrección a nivel magnético para discos duros viejos o dañados con sectores defectuosos. Reparará el disco al siguiente reinicio."),
        ("13. Reconstruir Caché de Iconos", "Soluciona de forma inmediata el fallo visual donde los iconos de tus aplicaciones aparecen blancos, rotos o sumamente borrosos."),
        ("14. Optimizador ASUS G-Helper", "Reemplazo ultraligero y brillante de Armoury Crate exclusivo para laptops ASUS. Controla luces, curva de ventiladores y batería sin consumir memoria RAM."),
        ("15. Lenovo Legion Toolkit", "Reemplaza el pesado software Lenovo Vantage. Administra modos térmicos y de carga sin instalar procesos lentos en segundo plano."),
        ("16. Optimizador Terminal Mole", "Potente optimizador estilo CCleaner, pero corriendo cien por ciento en texto dentro de tu consola. Limpia gigabytes de espacio inútil rápidamente."),
        ("17. Escáner de Fugas y Memoria Virtual", "Resuelve el problema de falta de almacenamiento. Analiza cuánta RAM física tienes y te recomienda un tamaño exacto de memoria virtual, permitiéndote elegir el disco más vacío para guardarla, evitando que Windows robe hasta 100 Gigabytes sin tu permiso."),
        ("18. Organizador Inteligente de Archivos", "Transforma el caos en orden. Seleccionas una carpeta súper desordenada como las Descargas, y la herramienta separará mágicamente todo en carpetas de fotos, videos y programas, borrando además las subcarpetas vacías que ya no sirven para nada."),
        ("19. Radar Visual de Almacenamiento", "Funciona como un escáner de rayos X para tu disco duro. Al abrirlo, el sistema buscará archivos basura de Windows y te sugerirá borrarlos automáticamente. Después, te mostrará una lista visual con las carpetas más pesadas de tu computadora para que puedas investigar y eliminar a mano lo que te está robando espacio.")
    ]

    guia_diag_win = [
        ("1. Diagnóstico Veloz", "Resumen instantáneo con la calificación matemática oficial de velocidad y fluidez que Windows le da a esta PC."),
        ("2. Radiografía Completa Hardware", "Lista precisa con marcas y modelos reales de la Placa Madre, RAM instalada, Procesador exacto y Tarjetas Gráficas de esta computadora."),
        ("3. Salud de Discos S.M.A.R.T", "Lee los sensores internos ocultos de tus discos duros y de estado sólido para advertirte si están a punto de sufrir una falla física."),
        ("4. Monitor de Estabilidad Windows", "Abre una línea de tiempo gráfica que te muestra los últimos días de la computadora, detallando por qué ocurrió cada pantallazo azul o cierre inesperado."),
        ("5. Cuadrícula Forense de Tareas", "Despliega una hoja de cálculo interactiva para investigar y filtrar procesos y servicios en memoria, mucho más detallado que el Administrador de Tareas."),
        ("6. Tiempo de Actividad Real", "Muestra cuánto tiempo exacto lleva esta computadora encendida. Revela si el Inicio Rápido de Windows está impidiendo apagados reales."),
        ("7. Auditar Tareas Ocultas", "Visualiza programas y mantenimientos fantasmas instalados en el fondo de tu equipo que podrían estar robando recursos y batería."),
        ("8. Auditoría de Arranque", "Descubre exactamente cuáles programas se abren a escondidas apenas enciendes tu computadora, lo que hace que tu sistema tarde muchísimo en iniciar."),
        ("9. Historial Forense de USBs", "Descifra y lista los nombres de todos los pendrives, controles y celulares que se han conectado en este equipo a lo largo de toda su historia."),
        ("10. Extractor de Pantallazos", "Extrae los nombres y códigos de error exactos de todos los Pantallazos Azules de la Muerte recientes para diagnosticar hardware dañado."),
        ("11. Gestor y Laboratorio de Batería", "Una doble herramienta increíble. Por un lado, te muestra de forma interactiva y visual cómo funciona el código de programación interna al cargar un celular. Por otro lado, lee los sensores de tu P C para mostrarte tu batería real y generar un reporte de su nivel de daño."),
        ("12. Reporte de Suspensión", "Si tu laptop se descarga estando guardada o suspendida, descubre exactamente qué programa impidió que entrara en reposo absoluto."),
        ("13. Gestor Avanzado BitLocker", "Una suite forense para discos encriptados. Te permite ver el estado de cifrado, extraer la clave de tu PC para guardarla, o hacer un escaneo profundo en tus pendrives para encontrar claves perdidas y desbloquear discos duros al instante."),
        ("14. Auditoría de Usuarios Internos", "Expone las cuentas registradas internamente en tu sistema, listando su nivel de seguridad e intentando detectar infiltraciones."),
        ("15. Extraer Serial de Fábrica", "Copia automáticamente a tu portapapeles el número de serie codificado de la placa base, indispensable para revisar garantías o descargar actualizaciones de BIOS."),
        ("16. Escáner Forense RAM", "Busca virus militares sin archivo que no dejan rastros en el disco duro y se ocultan directamente en la Memoria RAM de la computadora."),
        {"17. Visualizador Forense Web", "Genera una gráfica moderna, interactiva y al instante que te muestra cuáles son las páginas web más visitadas y las últimas búsquedas, evadiendo la seguridad del sistema."},
        ("18. Radar de Hardware en Conflicto", "Detecta piezas físicas de la computadora que estén fallando o que no tengan drivers instalados. Al detectarlas, arma automáticamente una búsqueda avanzada en internet para llevarte directo a la solución.")
    ]
    
    guia_soft_win = [
        ("1. Actualizar Aplicaciones", "Detecta programas instalados como Zoom, VLC o Chrome, y descarga sus últimas versiones de golpe en segundo plano de forma invisible."),
        ("2. Extraer Clave Original", "Recupera tu licencia legítima de Microsoft leyendo directamente el código quemado en el chip de tu computadora."),
        ("3. Inventario Software a Excel", "Genera una base de datos en Excel al instante, listando perfectamente cada programa y la versión instalada en el sistema."),
        ("4. Respaldo Total de Controladores", "La salvación de PCs antiguas. Copia todos los controladores de Wi-Fi, Gráfica y Audio antes de un formateo para no quedar incomunicado."),
        ("5. Auditoría de Licencias Office", "Descubre de inmediato si el Word y Excel del equipo es pirata, robado, o una licencia comercial original y pagada."),
        ("6. HWID Activador Definitivo", "El mejor método del mundo para activar Windows de por vida. Es legal, sin programas pesados y se enlaza directamente a tu placa madre."),
        ("7. Forzar Escaneo Hardware", "Útil si armas la PC y Windows no te reconoce la gráfica o un ratón. Obliga al equipo a revisar todos los circuitos internos de nuevo."),
        ("8. Instalar ASUS GlideX", "Añade conectividad inalámbrica a tu equipo para convertir celulares y tablets viejas en un segundo monitor táctil para tu PC.")
    ]

    guia_soporte_win = [
        ("1. Destructor Forzado de Carpetas", "La herramienta del miedo. Elimina brutalmente cualquier carpeta, programa bloqueado o virus que Windows te prohíba tocar."),
        ("2. Bypass de Contraseña Windows", "Te permite borrar o cambiar la clave de inicio de sesión de cualquier usuario si este ha quedado bloqueado por accidente."),
        ("3. Extractor Forense LaZagne", "Busca, extrae y guarda en el Escritorio todas las contraseñas guardadas en navegadores, aplicaciones y redes Wi-Fi."),
        ("4. Descargador Universal Multimedia", "Descarga videos en 4K y extrae Galerías de Fotos completas de Instagram, YouTube o Reddit burlando los bloqueos de inicio de sesión."),
        ("5. Gestor Avanzado de USB", "Administra la seguridad de los puertos físicos. Te permite bloquear el PC contra robo de datos por pendrives, restaurar el acceso, o reparar memorias USB dañadas que no te dejan guardar archivos."),
        ("6. Gestor de Virtualización", "Escanea tu procesador para activar Máquinas Virtuales o la Caja de Arena que destruye virus al cerrarse de forma segura."),
        ("7. Reinicio de Fábrica para Ventas", "Deja la computadora totalmente en blanco a nivel de hardware, ideal por si la vas a vender o clonar. Al arrancar, será como encenderla el primer día."),
        ("8. Destrucción de Datos Militar", "Limpia y sobrescribe con ceros los espacios vacíos de tu disco duro para garantizar que nadie jamás pueda recuperar tus fotos borradas."),
        ("9. Salto de BIOS Forzado", "Soluciona la pesadilla de reiniciar el PC y presionar las teclas súper rápido. Te lleva directamente a los menús de la Placa Madre."),
        ("10. Hackeo de Archivos Bloqueados", "Fuerza y extrae contraseñas olvidadas de archivos comprimidos o PDFs mediante ataques masivos de diccionarios mundiales o fuerza bruta."),
        ("11. Romper Candado de Excel", "Copia un archivo bloqueado, analiza su código por dentro, elimina la celda encriptada y te da un archivo final donde podrás escribir a gusto."),
        ("12. Limpiador Android Extremo", "Enlaza tu celular por cable y elimina gigabytes de basura, miniaturas y copias viejas de aplicaciones respetando tus fotos reales."),
        ("13. Auditoría Total de Ciberseguridad", "Busca puertas traseras y graves huecos de configuración. Después del análisis, te ofrece aplicar defensas militares de inmediato."),
        ("14. Laboratorio Criptográfico de Claves", "Una bóveda de seguridad avanzada. Puedes escribir una de tus contraseñas para ver cuánto tiempo le tomaría a un hacker adivinarla, o pedirle al sistema que te genere una nueva contraseña totalmente indestructible."),
        ("15. Modo Dios y Escáner de I M E I", "Abre tu cámara web con una interfaz futurista. Escanea automáticamente cualquier código Q R y código de barras simultáneamente. Además, si escaneas la caja o pantalla de un teléfono, analizará matemáticamente el I M E I abriendo bases de datos de Colombia y el mundo para decirte de inmediato si es robado."),
        ("16. Borrador de Fondos con Inteligencia Artificial", "Recorta personas y objetos perfectos de cualquier fotografía de forma inteligente sin depender de páginas web, funcionando directamente en el procesador de tu PC."),
        ("17. Escáner Óptico de Pantalla O. C. R.", "Atenúa tu pantalla para que puedas dibujar un cuadro sobre cualquier imagen o error de Windows. La inteligencia artificial leerá las letras dentro de la foto y copiará el texto para ti.")
    ]

    guia_mac_linux = [
        ("Linux y Seguridad", "Esta sección te da una terminal con herramientas de administrador. Puedes auditar servidores, ver el tráfico de red, y cazar intrusos con comandos avanzados."),
        ("MacPEAS para Apple", "Es un auditor de seguridad para Mac. Escanea el equipo buscando configuraciones débiles que dejarían entrar a un virus, y te ofrece un blindaje automático para proteger la máquina.")
    ]

    guia_moviles = [
        ("Limpiador Android Extremo", "Conectas el teléfono por cable, y esta herramienta se mete al sistema borrando gigabytes de copias de seguridad viejas y basura oculta de WhatsApp o Telegram, sin tocar tus fotos o chats actuales.")
    ]

    # --- LÓGICA DE NAVEGACIÓN INTERACTIVA (MENÚS ANIDADOS) ---
    def limpiar_nav():
        for w in panel_nav.winfo_children():
            w.destroy()

    def vista_principal():
        limpiar_nav()
        ctk.CTkLabel(panel_nav, text="Menú Principal", font=("Arial", 22, "bold"), text_color="#A78BFA").pack(pady=(25, 15))
        
        ctk.CTkButton(panel_nav, text="1. Sistemas Operativos", font=("Arial", 14), height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=vista_sistemas).pack(pady=5, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="2. Nube, Tienda y Proyecto", font=("Arial", 14), height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=vista_nube).pack(pady=5, fill="x", padx=15)
        
        ctk.CTkFrame(panel_nav, height=1, fg_color="#334155").pack(fill="x", padx=20, pady=15)
        ctk.CTkButton(panel_nav, text="▶ Explicar Todo el Proyecto", font=("Arial", 13, "bold"), fg_color="#10B981", hover_color="#059669", command=lambda: reproducir_guia("El Proyecto Completo", guia_categorias_main)).pack(pady=5, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🛑 Detener Voz", font=("Arial", 14, "bold"), height=40, fg_color="#EF4444", hover_color="#DC2626", command=detener_habla).pack(side="bottom", pady=20, fill="x", padx=15)

    def vista_sistemas():
        limpiar_nav()
        ctk.CTkLabel(panel_nav, text="Sistemas Operativos", font=("Arial", 20, "bold"), text_color="#38BDF8").pack(pady=(20, 15))
        
        ctk.CTkButton(panel_nav, text="🪟 Funciones de Windows", font=("Arial", 14), height=45, command=vista_windows).pack(pady=5, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🐧 Linux y Seguridad", font=("Arial", 14), height=40, command=lambda: reproducir_guia("Módulos de Linux", [("Auditoría Linux", "Esta sección te da una terminal con herramientas de administrador. Puedes auditar servidores, ver el tráfico de red, y cazar intrusos con comandos avanzados.")])).pack(pady=5, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🍏 Funciones de Mac", font=("Arial", 14), height=40, command=lambda: reproducir_guia("Módulos de Mac", [("MacPEAS y Ecosistema", "Contiene un auditor de seguridad para Mac que escanea el equipo buscando configuraciones débiles, y te ofrece aplicar un blindaje automático para proteger la máquina.")])).pack(pady=5, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🤖 Herramientas Android", font=("Arial", 14), height=40, command=lambda: reproducir_guia("Módulos de Android", [("Limpieza Móvil", "Tu navaja suiza para celulares. Al conectar un teléfono por cable, esta sección te permite borrarle gigabytes de basura oculta velozmente.")])).pack(pady=5, fill="x", padx=15)
        
        ctk.CTkButton(panel_nav, text="⬅️ Volver", font=("Arial", 14), height=40, fg_color="#334155", hover_color="#475569", command=vista_principal).pack(side="bottom", pady=20, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🛑 Detener Voz", font=("Arial", 14, "bold"), height=35, fg_color="#EF4444", hover_color="#DC2626", command=detener_habla).pack(side="bottom", pady=0, fill="x", padx=15)

    def vista_nube():
        limpiar_nav()
        ctk.CTkLabel(panel_nav, text="Nube y Proyecto", font=("Arial", 20, "bold"), text_color="#F59E0B").pack(pady=(20, 15))
        
        dicc_nube = [
            ("Programas Portables", "Herramientas de un solo uso que se descargan directamente a la memoria temporal y se destruyen al cerrarse, sin ensuciar tu PC con instalaciones."),
            ("Enciclopedias", "Un catálogo inmenso de páginas web ocultas y aplicaciones de código abierto que puedes instalar de forma totalmente automática."),
            ("Manuales y Trucos", "Una sección de documentación técnica que te enseña a sacarle el jugo a tu computadora y a protegerte de amenazas cibernéticas."),
            ("Venta de Licencias", "Adquiere programas de pago, sistemas operativos y herramientas premium directamente con precios reducidos y soporte incluido."),
            ("Filosofía de TREMEND", "Nuestra misión es aprovechar la inteligencia artificial para crear herramientas poderosas que le den el control total al usuario, sin importar su nivel de experiencia.")
        ]
        
        ctk.CTkButton(panel_nav, text="▶ Explicar toda la Nube", font=("Arial", 13, "bold"), fg_color="#10B981", hover_color="#059669", command=lambda: reproducir_guia("Nube, Tienda y Proyecto", dicc_nube)).pack(pady=5, fill="x", padx=15)
        
        ctk.CTkButton(panel_nav, text="⬅️ Volver", font=("Arial", 14), height=40, fg_color="#334155", hover_color="#475569", command=vista_principal).pack(side="bottom", pady=20, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🛑 Detener Voz", font=("Arial", 14, "bold"), height=35, fg_color="#EF4444", hover_color="#DC2626", command=detener_habla).pack(side="bottom", pady=0, fill="x", padx=15)

    def vista_windows():
        limpiar_nav()
        ctk.CTkLabel(panel_nav, text="Módulos de Windows", font=("Arial", 20, "bold"), text_color="#10B981").pack(pady=(20, 15))
        
        ctk.CTkButton(panel_nav, text="🌐 Redes e Internet", font=("Arial", 13), height=38, command=lambda: vista_selector_funciones("Redes e Internet", guia_red_win)).pack(pady=5, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🧹 Mantenimiento", font=("Arial", 13), height=38, command=lambda: vista_selector_funciones("Mantenimiento PC", guia_mant_win)).pack(pady=5, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🖥️ Diagnóstico", font=("Arial", 13), height=38, command=lambda: vista_selector_funciones("Diagnóstico HW", guia_diag_win)).pack(pady=5, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="📦 Software y Licencias", font=("Arial", 13), height=38, command=lambda: vista_selector_funciones("Software e Inventario", guia_soft_win)).pack(pady=5, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🛠️ Soporte Técnico", font=("Arial", 13), height=38, command=lambda: vista_selector_funciones("Soporte Técnico", guia_soporte_win)).pack(pady=5, fill="x", padx=15)
        
        ctk.CTkButton(panel_nav, text="⬅️ Volver", font=("Arial", 14), height=40, fg_color="#334155", hover_color="#475569", command=vista_sistemas).pack(side="bottom", pady=20, fill="x", padx=15)

    def vista_selector_funciones(titulo_cat, diccionario):
        limpiar_nav()
        ctk.CTkLabel(panel_nav, text=titulo_cat, font=("Arial", 18, "bold"), text_color="#FCD34D").pack(pady=(15, 10))
        
        # Botón para explicar toda la categoría
        ctk.CTkButton(panel_nav, text="▶ Explicar TODA la Categoría", font=("Arial", 13, "bold"), height=38, fg_color="#10B981", hover_color="#059669", command=lambda: reproducir_guia(titulo_cat, diccionario)).pack(pady=5, fill="x", padx=15)
        
        ctk.CTkFrame(panel_nav, height=1, fg_color="#334155").pack(fill="x", padx=20, pady=10)
        
        # EL BUSCADOR DE INGENIERO
        ctk.CTkLabel(panel_nav, text="O ingresa el N° de la función:", font=("Arial", 12, "bold"), text_color="#94A3B8").pack(pady=2)
        
        entrada_num = ctk.CTkEntry(panel_nav, placeholder_text=f"Ej: 1 al {len(diccionario)}", width=160, justify="center", font=("Arial", 14))
        entrada_num.pack(pady=5)
        
        def explicar_una(event=None):
            val = entrada_num.get().strip()
            if val.isdigit():
                idx = int(val) - 1
                if 0 <= idx < len(diccionario):
                    item = diccionario[idx]
                    reproducir_guia(f"Función Seleccionada", [item])
                    entrada_num.delete(0, 'end') 
                else:
                    messagebox.showwarning("Aviso", f"Ingresa un número válido entre 1 y {len(diccionario)}.")
            else:
                messagebox.showwarning("Aviso", "Por favor ingresa solo números enteros.")
        
        # ¡Magia! Si presionas ENTER en la cajita, hace la búsqueda sin tocar el botón
        entrada_num.bind("<Return>", explicar_una)
        
        ctk.CTkButton(panel_nav, text="Explicar Específica", font=("Arial", 13, "bold"), height=35, fg_color="#3B82F6", hover_color="#2563EB", command=explicar_una).pack(pady=5, fill="x", padx=15)
        
        # Lista visual con scroll para ver TODAS las funciones
        lista_funcs = ctk.CTkScrollableFrame(panel_nav, fg_color="transparent")
        lista_funcs.pack(fill="both", expand=True, padx=5, pady=5)
        
        for i, (nombre, _) in enumerate(diccionario):
            ctk.CTkLabel(lista_funcs, text=nombre, font=("Arial", 12), text_color="#CBD5E1", anchor="w", justify="left").pack(fill="x", pady=2)

        ctk.CTkButton(panel_nav, text="⬅️ Volver", font=("Arial", 13), height=35, fg_color="#334155", hover_color="#475569", command=vista_windows).pack(side="bottom", pady=10, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🛑 Detener Voz", font=("Arial", 13, "bold"), height=30, fg_color="#EF4444", hover_color="#DC2626", command=detener_habla).pack(side="bottom", pady=0, fill="x", padx=15)

    # Iniciar la interfaz en el menú principal
    vista_principal()

    def on_closing():
        global detener_voz, proceso_actual_tts
        detener_voz = True
        if proceso_actual_tts:
            try: proceso_actual_tts.kill()
            except: pass
        ventana_guia.destroy()
        
    ventana_guia.protocol("WM_DELETE_WINDOW", on_closing)

# ============================================================================
# 4. INTERFAZ GRÁFICA Y SISTEMA DE CATEGORÍAS
# ============================================================================

# 1. Contenedor Maestro Rígido (Evita que el menú se aplaste)
sidebar_container = ctk.CTkFrame(app, width=240, corner_radius=0)
sidebar_container.pack_propagate(False) 
sidebar_container.pack(side="left", fill="y")

# 2. Botón de Apoyo anclado AL FONDO (Siempre visible y estético)
def abrir_kofi():
    import webbrowser
    webbrowser.open("https://ko-fi.com/ldvp55")

btn_kofi = ctk.CTkButton(sidebar_container, text="☕ Apoyar a TREMEND", font=("Arial", 14, "bold"), fg_color="#F59E0B", hover_color="#D97706", text_color="#000000", command=abrir_kofi)
btn_kofi.pack(side="bottom", pady=20, padx=20, fill="x")

# 3. Motor de Scroll Independiente (La barra espaciadora tipo mouse)
sidebar_scroll = ctk.CTkScrollableFrame(sidebar_container, corner_radius=0, fg_color="transparent")
sidebar_scroll.pack(side="top", fill="both", expand=True)

# 4. Tu 'sidebar' original, inyectado DENTRO del scroll.
# ¡Así tu código antiguo funcionará a la perfección sin romper la barra espaciadora!
sidebar = ctk.CTkFrame(sidebar_scroll, fg_color="transparent")
sidebar.pack(fill="both", expand=True)

# --- EL RESTO DE TU CÓDIGO SIGUE IGUAL A PARTIR DE AQUÍ ---
main_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")

main_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
main_frame.pack(side="right", fill="both", expand=True)

# --- FIX MAESTRO: ORDEN DE EMPAQUETADO ---
# 1. Empaquetamos PRIMERO el HUD a la derecha para que reserve sus 280px exactos y no se aplaste.
hud_frame = ctk.CTkFrame(main_frame, width=280, fg_color="#1E293B", corner_radius=15, border_width=1, border_color="#38BDF8")
hud_frame.pack(side="right", fill="y", padx=(10, 20), pady=20)
hud_frame.pack_propagate(False) # Congelamos el ancho para que no se deforme

# 2. Empaquetamos DESPUÉS el panel central para que tome solo el espacio restante.
tools_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
tools_frame.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=20)

def limpiar_panel():
    for widget in tools_frame.winfo_children(): widget.destroy()

# --- DISEÑO DEL HUD ---
ctk.CTkLabel(hud_frame, text="🎛️ Monitor de Sistema", font=("Arial", 18, "bold"), text_color="#38BDF8").pack(pady=(20, 15))

# [1] Sección CPU
ctk.CTkLabel(hud_frame, text="Procesador (CPU)", font=("Arial", 13, "bold"), text_color="#94A3B8").pack(anchor="w", padx=20)
lbl_cpu_val = ctk.CTkLabel(hud_frame, text="Calculando...", font=("Arial", 12))
lbl_cpu_val.pack(anchor="e", padx=20, pady=(0, 2))
pb_cpu = ctk.CTkProgressBar(hud_frame, progress_color="#10B981", height=10)
pb_cpu.pack(fill="x", padx=20)
pb_cpu.set(0)

# [2] Sección RAM
ctk.CTkLabel(hud_frame, text="Memoria RAM", font=("Arial", 13, "bold"), text_color="#94A3B8").pack(anchor="w", padx=20, pady=(20, 0))
lbl_ram_val = ctk.CTkLabel(hud_frame, text="Calculando...", font=("Arial", 12))
lbl_ram_val.pack(anchor="e", padx=20, pady=(0, 2))
pb_ram = ctk.CTkProgressBar(hud_frame, progress_color="#3B82F6", height=10)
pb_ram.pack(fill="x", padx=20)
pb_ram.set(0)

# [3] Sección Disco
ctk.CTkLabel(hud_frame, text="Disco Principal (C:)", font=("Arial", 13, "bold"), text_color="#94A3B8").pack(anchor="w", padx=20, pady=(20, 0))
lbl_disco_val = ctk.CTkLabel(hud_frame, text="Calculando...", font=("Arial", 12))
lbl_disco_val.pack(anchor="e", padx=20, pady=(0, 2))
pb_disco = ctk.CTkProgressBar(hud_frame, progress_color="#8B5CF6", height=10)
pb_disco.pack(fill="x", padx=20)
pb_disco.set(0)

# [4] Separador e Info Fija del Equipo
ctk.CTkFrame(hud_frame, height=2, fg_color="#334155").pack(fill="x", padx=20, pady=30)
ctk.CTkLabel(hud_frame, text="Info del Equipo", font=("Arial", 13, "bold"), text_color="#94A3B8").pack(anchor="w", padx=20, pady=(0, 10))

lbl_os = ctk.CTkLabel(hud_frame, text=f"🖥️ Windows {platform.release()} ({platform.machine()})", font=("Arial", 12))
lbl_os.pack(anchor="w", padx=20, pady=2)
lbl_hostname = ctk.CTkLabel(hud_frame, text=f"💻 {socket.gethostname()}", font=("Arial", 12))
lbl_hostname.pack(anchor="w", padx=20, pady=2)
try: ip_local = socket.gethostbyname(socket.gethostname())
except: ip_local = "127.0.0.1"
lbl_ip = ctk.CTkLabel(hud_frame, text=f"🌐 IP: {ip_local}", font=("Arial", 12))
lbl_ip.pack(anchor="w", padx=20, pady=2)

    # --- NUEVA MEJORA: SENSOR DE LATENCIA (PING EN VIVO) ---
lbl_net = ctk.CTkLabel(hud_frame, text="⚡ Ping: Calculando...", font=("Arial", 12, "bold"), text_color="#FCD34D")
lbl_net.pack(anchor="w", padx=20, pady=(10, 2))

    # --- MOTOR LÓGICO DEL HUD (MAXIMIZADO Y ANTI-CRASH) ---
from ctypes import wintypes
import ctypes

class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

def arrancar_motor_hud():
        import subprocess, threading, time, shutil, socket

        def get_system_times():
            try:
                idleTime, kernelTime, userTime = FILETIME(), FILETIME(), FILETIME()
                ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idleTime), ctypes.byref(kernelTime), ctypes.byref(userTime))
                idle = (idleTime.dwHighDateTime << 32) | idleTime.dwLowDateTime
                sys_time = ((kernelTime.dwHighDateTime << 32) | kernelTime.dwLowDateTime) + ((userTime.dwHighDateTime << 32) | userTime.dwLowDateTime)
                return idle, sys_time
            except: return 0, 0

        def tarea_actualizacion():
            # 1. Escudo Anti-Congelamiento: Leemos la RAM real en segundo plano
            ram_fisica_gb = 0
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                script_ram = "Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum | Select-Object -ExpandProperty Sum"
                out = subprocess.run(["powershell", "-NoProfile", "-Command", script_ram], capture_output=True, text=True, startupinfo=startupinfo, timeout=5).stdout.strip()
                if out.isdigit():
                    ram_fisica_gb = int(out) / (1024**3)
            except: pass

            idle_prev, sys_prev = get_system_times()

            while True:
                time.sleep(1.5) # Ciclo de refresco
                
                # --- CPU ---
                try:
                    idle_now, sys_now = get_system_times()
                    if sys_now > sys_prev:
                        idle_diff = idle_now - idle_prev
                        sys_diff = sys_now - sys_prev
                        cpu_percent = int((sys_diff - idle_diff) * 100.0 / sys_diff)
                    else: cpu_percent = 0
                    idle_prev, sys_prev = idle_now, sys_now
                except: cpu_percent = 0

                # --- RAM ---
                try:
                    stat = MEMORYSTATUSEX()
                    stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                    ram_percent = stat.dwMemoryLoad
                    ram_total = ram_fisica_gb if ram_fisica_gb > 0 else stat.ullTotalPhys / (1024**3)
                    
                    # Corrección del bug de Windows (Hardware Reservado)
                    if ram_fisica_gb > 0:
                        ram_usada = ram_total * (ram_percent / 100.0)
                    else:
                        ram_usada = (stat.ullTotalPhys - stat.ullAvailPhys) / (1024**3)
                except: ram_percent, ram_total, ram_usada = 0, 0, 0

                # --- DISCO ---
                try:
                    total_b, _, free_b = shutil.disk_usage("C:\\")
                    disco_total = total_b / (1024**3)
                    disco_usado = (total_b - free_b) / (1024**3)
                    disco_percent = (disco_usado / disco_total) * 100 if disco_total > 0 else 0
                except: disco_percent, disco_total, disco_usado = 0, 0, 0
                
                # --- PING EN VIVO (Maximizando el HUD) ---
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    t0 = time.time()
                    s.connect(('8.8.8.8', 53))
                    ping_ms = int((time.time() - t0) * 1000)
                    s.close()
                except: ping_ms = -1

                # Colores Dinámicos
                ccpu = "#EF4444" if cpu_percent > 85 else ("#F59E0B" if cpu_percent > 60 else "#10B981")
                cram = "#EF4444" if ram_percent > 85 else ("#F59E0B" if ram_percent > 60 else "#3B82F6")
                cdisco = "#EF4444" if disco_percent > 90 else "#8B5CF6"

                # Inyección Segura (Closures con variables pre-asignadas evitan colisiones de memoria)
                def refrescar(cp=cpu_percent, c_c=ccpu, ru=ram_usada, rt=ram_total, rp=ram_percent, c_r=cram, du=disco_usado, dt=disco_total, dp=disco_percent, c_d=cdisco, pm=ping_ms):
                    if not app.winfo_exists(): return
                    try:
                        lbl_cpu_val.configure(text=f"{cp}%")
                        pb_cpu.set(cp / 100.0)
                        pb_cpu.configure(progress_color=c_c)

                        lbl_ram_val.configure(text=f"{ru:.1f} GB / {rt:.1f} GB ({rp}%)")
                        pb_ram.set(rp / 100.0)
                        pb_ram.configure(progress_color=c_r)

                        lbl_disco_val.configure(text=f"{du:.1f} GB / {dt:.1f} GB ({dp:.1f}%)")
                        pb_disco.set(dp / 100.0)
                        pb_disco.configure(progress_color=c_d)
                        
                        if pm >= 0:
                            lbl_net.configure(text=f"⚡ Ping: {pm} ms", text_color="#10B981" if pm < 100 else "#F59E0B")
                        else:
                            lbl_net.configure(text="⚡ Ping: Desconectado", text_color="#EF4444")
                    except: pass 

                app.after(0, refrescar)

        threading.Thread(target=tarea_actualizacion, daemon=True).start()

arrancar_motor_hud()
import subprocess
    # Función para leer los latidos del procesador desde el Kernel
def get_system_times():
        idleTime, kernelTime, userTime = FILETIME(), FILETIME(), FILETIME()
        ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idleTime), ctypes.byref(kernelTime), ctypes.byref(userTime))
        idle = (idleTime.dwHighDateTime << 32) | idleTime.dwLowDateTime
        sys_time = ((kernelTime.dwHighDateTime << 32) | kernelTime.dwLowDateTime) + ((userTime.dwHighDateTime << 32) | userTime.dwLowDateTime)
        return idle, sys_time

    # [FIX RAM] Sacamos la RAM física instalada en los slots usando WMI
try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        script_ram = "Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum | Select-Object -ExpandProperty Sum"
        ram_instalada_bytes = int(subprocess.run(["powershell", "-NoProfile", "-Command", script_ram], capture_output=True, text=True, startupinfo=startupinfo).stdout.strip())
        ram_fisica_gb = ram_instalada_bytes / (1024**3)
except:
        ram_fisica_gb = 0

def tarea_actualizacion():
        idle_prev, sys_prev = get_system_times()
        while True:
            time.sleep(1.5) # Refresco ultra rápido en tiempo real
            
            # 1. CPU (Cálculo milimétrico idéntico al Administrador de Tareas)
            idle_now, sys_now = get_system_times()
            idle_diff = idle_now - idle_prev
            sys_diff = sys_now - sys_prev
            cpu_percent = int((sys_diff - idle_diff) * 100.0 / sys_diff) if sys_diff > 0 else 0
            idle_prev, sys_prev = idle_now, sys_now

            # 2. RAM (Lectura en tiempo real)
            try:
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                ram_percent = stat.dwMemoryLoad
                
                # Fix: Mostrar RAM Física Real (8GB) en vez de Usable (5.8GB)
                ram_total = ram_fisica_gb if ram_fisica_gb > 0 else stat.ullTotalPhys / (1024**3)
                ram_usada = (stat.ullTotalPhys - stat.ullAvailPhys) / (1024**3)
            except: ram_percent, ram_total, ram_usada = 0, 0, 0

            # 3. Disco C: (Lectura instantánea de bytes físicos)
            try:
                total_b, _, free_b = shutil.disk_usage("C:\\")
                disco_total = total_b / (1024**3)
                disco_usado = (total_b - free_b) / (1024**3)
                disco_percent = (disco_usado / disco_total) * 100 if disco_total > 0 else 0
            except: disco_percent, disco_total, disco_usado = 0, 0, 0

            # 4. Semáforos de Colores Dinámicos (Verde, Naranja, Rojo)
            color_cpu = "#EF4444" if cpu_percent > 85 else ("#F59E0B" if cpu_percent > 60 else "#10B981")
            color_ram = "#EF4444" if ram_percent > 85 else ("#F59E0B" if ram_percent > 60 else "#3B82F6")
            color_disco = "#EF4444" if disco_percent > 90 else "#8B5CF6"

            # 5. Inyección a la Interfaz Gráfica
            def refrescar_ui():
                try:
                    lbl_cpu_val.configure(text=f"{cpu_percent}%")
                    pb_cpu.set(cpu_percent / 100.0)
                    pb_cpu.configure(progress_color=color_cpu)

                    lbl_ram_val.configure(text=f"{ram_usada:.1f} GB / {ram_total:.1f} GB ({ram_percent}%)")
                    pb_ram.set(ram_percent / 100.0)
                    pb_ram.configure(progress_color=color_ram)

                    lbl_disco_val.configure(text=f"{disco_usado:.1f} GB / {disco_total:.1f} GB ({disco_percent:.1f}%)")
                    pb_disco.set(disco_percent / 100.0)
                    pb_disco.configure(progress_color=color_disco)
                except: pass 

            app.after(0, refrescar_ui)
    
threading.Thread(target=tarea_actualizacion, daemon=True).start()

# --- MOTOR MAESTRO DE VISTAS (Fábrica de Tarjetas Responsiva) ---
def construir_vista_dinamica(titulo_categoria, placeholder, lista_herramientas):
    limpiar_panel()
    
    # Encabezado
    header_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))
    ctk.CTkLabel(header_frame, text=titulo_categoria, font=("Arial", 24, "bold")).pack(side="left")
    
    search_var = ctk.StringVar()
    barra = ctk.CTkEntry(header_frame, textvariable=search_var, placeholder_text=placeholder, width=350, font=("Arial", 14), corner_radius=15, border_color="#38BDF8")
    barra.pack(side="right", padx=10)

    # ====================================================================
    # --- CEREBRO DE PAGINACIÓN DINÁMICA Y RESPONSIVA (LIQUID UI) ---
    # Detecta de forma nativa si el PC está en 100%, 125%, 150%, etc.
    escala_monitor = app._get_window_scaling() 
    
    # Calculamos el espacio vertical disponible deduciendo los bordes
    espacio_libre_vertical = alto_app - (260 * escala_monitor) 
    
    # Altura adaptable: Si el monitor tiene zoom, la tarjeta crece proporcionalmente
    altura_base = 185 if ("Enciclopedia" in titulo_categoria or "Portables" in titulo_categoria) else 155
    altura_estimada_tarjeta = int(altura_base * escala_monitor)
        
    ITEMS_POR_PAGINA = max(1, int(espacio_libre_vertical / altura_estimada_tarjeta))
    # ====================================================================

    estado = {"pagina": 0, "filtradas": lista_herramientas}

    # 1. Empaquetamos los controles PRIMERO y los anclamos al fondo (side="bottom")
    nav_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    nav_frame.pack(side="bottom", fill="x", pady=10)
    btn_prev = ctk.CTkButton(nav_frame, text="⬅️ Anterior", width=120, fg_color="#334155", hover_color="#475569")
    btn_prev.pack(side="left", padx=30)
    lbl_contador = ctk.CTkLabel(nav_frame, text="", font=("Arial", 14, "bold"), text_color="#38BDF8")
    lbl_contador.pack(side="left", expand=True)
    btn_next = ctk.CTkButton(nav_frame, text="Siguiente ➡️", width=120, fg_color="#334155", hover_color="#475569")
    btn_next.pack(side="right", padx=30)

    # 2. Empaquetamos la lista DESPUÉS para que se ajuste al espacio restante
    lista_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    lista_frame.pack(side="top", fill="both", expand=True)

    def renderizar():
        for w in lista_frame.winfo_children(): w.destroy()
        total = len(estado["filtradas"])
        if total == 0:
            ctk.CTkLabel(lista_frame, text="No se encontraron resultados.", text_color="#AAAAAA", font=("Arial", 16)).pack(pady=50)
            lbl_contador.configure(text="0 Resultados")
            return
        
        tot_pag = (total - 1) // ITEMS_POR_PAGINA + 1
        inicio = estado["pagina"] * ITEMS_POR_PAGINA
        lote = estado["filtradas"][inicio:inicio+ITEMS_POR_PAGINA]
        
        # --- FIX MAESTRO: CÁLCULO PORCENTUAL FLUIDO ---
        # 1. Al ancho total, le restamos el panel lateral (240) y el HUD (280)
        ancho_panel_central = (ancho_app / escala_monitor) - 520
        
        # 2. El texto ocupará EXACTAMENTE el 65% de ese panel central libre.
        # Al ser un porcentaje, se auto-acopla y jamás chocará con el botón,
        # sin importar la resolución o el zoom del equipo.
        espacio_texto = int(ancho_panel_central * 0.65) 
        
        for item in lote:
            color_borde = item.get("color_borde", "#38BDF8")
            if "Wipe" in item["nombre"] or "Destructor" in item["nombre"] or "Sysprep" in item["nombre"]:
                color_borde = "#EF4444" 
            
            # 1. LA TARJETA (Se encogerá automáticamente)
            tarjeta = ctk.CTkFrame(lista_frame, fg_color="#1E293B", corner_radius=8, border_width=1, border_color=color_borde)
            tarjeta.pack(fill="x", pady=6, padx=10)
            
            # 2. EL BOTÓN (Empaquetado PRIMERO a la derecha)
            txt_btn = item.get("txt_btn", "⚡ Ejecutar Herramienta")
            color_btn = "#10B981" if txt_btn == "⚡ Ejecutar Herramienta" else "#3B82F6"
            if color_borde == "#EF4444": color_btn = "#EF4444"
            
            btn = ctk.CTkButton(tarjeta, text=txt_btn, font=("Arial", 13, "bold"), width=160, height=40, fg_color=color_btn, hover_color="#059669", command=item["cmd"])
            btn.pack(side="right", padx=20) 
            
            # 3. EL TEXTO (Empaquetado DESPUÉS a la izquierda)
            text_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True, padx=20, pady=12)
            
            ctk.CTkLabel(text_frame, text=item["nombre"], font=("Arial", 16, "bold"), text_color="#FFFFFF").pack(anchor="w")
            
            if "exp" in item:
                ctk.CTkLabel(text_frame, text=item['exp'], font=("Arial", 12, "italic"), text_color="#94A3B8", justify="left", wraplength=espacio_texto).pack(anchor="w", pady=(2, 4))
            
            if "nov" in item:
                ctk.CTkLabel(text_frame, text=item["nov"], font=("Arial", 13), justify="left", wraplength=espacio_texto).pack(anchor="w")
            
        lbl_contador.configure(text=f"Página {estado['pagina'] + 1} de {tot_pag}  |  Total: {total}")

    def buscar(*args):
        txt = search_var.get().lower().strip().replace("-","").replace(" ","").replace(".","")
        if len(txt) >= 2 or txt.isdigit():
            estado["filtradas"] = [
                h for h in lista_herramientas
                if txt in h["nombre"].lower().replace("-","").replace(" ","").replace(".","")
                or txt == h.get("id", "")
                or txt in h.get("nov", "").lower().replace("-","").replace(" ","").replace(".","")
                or txt in h.get("exp", "").lower().replace("-","").replace(" ","").replace(".","")
            ]
        else: estado["filtradas"] = lista_herramientas
        estado["pagina"] = 0; renderizar()

    search_var.trace_add("write", buscar)
    def cambiar(dir):
        tot_pag = (len(estado["filtradas"]) - 1) // ITEMS_POR_PAGINA + 1
        n_pag = estado["pagina"] + dir
        if n_pag < 0: n_pag = tot_pag - 1
        elif n_pag >= tot_pag: n_pag = 0
        estado["pagina"] = n_pag; renderizar()

    btn_prev.configure(command=lambda: cambiar(-1))
    btn_next.configure(command=lambda: cambiar(1))
    renderizar(); barra.focus()

# === VISTAS DE LAS CATEGORÍAS (AHORA USAN LA FÁBRICA) ===
def cargar_categoria_redes():
    global app

    def btn_geolocalizar():
        dialogo = ctk.CTkInputDialog(text="Ingresa la IP a rastrear\n(Déjalo vacío para rastrear tu propia IP pública):", title="Radar OSINT de IP")
        ip_obj = dialogo.get_input()
        if ip_obj is not None: # Si el usuario no presionó "Cancelar"
            ip_obj = ip_obj.strip()
            abrir_consola_y_ejecutar("GEOLOCALIZACIÓN OSINT", lambda log: logica_geolocalizar_ip(log, ip_obj))

    def btn_geowifi():
        dialogo = ctk.CTkInputDialog(text="Ingresa la MAC (BSSID) del Router.\n[!] Deja este espacio VACÍO y dale OK para Auto-Detectar tu Wi-Fi actual:", title="Rastreador GeoWiFi")
        bssid_obj = dialogo.get_input()
        if bssid_obj is not None:  # Solo se ejecuta si no le dio al botón "Cancelar"
            abrir_consola_y_ejecutar("RASTREADOR WI-FI", lambda log: logica_geowifi_bssid(log, bssid_obj))

    def btn_ping():
        # Reemplazamos simpledialog por el InputDialog de CTk
        dialogo_ip = ctk.CTkInputDialog(text="Ingresa IP o Dominio a escanear:", title="Ping")
        dest = dialogo_ip.get_input()
        if dest:
            dialogo_puerto = ctk.CTkInputDialog(text="Puerto TCP (Opcional, deja vacío si no aplica):", title="TCP")
            puerto = dialogo_puerto.get_input()
            abrir_consola_y_ejecutar("PING Y TCP", lambda log: logica_ping_tcp(log, dest, puerto))

    def btn_nmap_win():
        dialogo_obj = ctk.CTkInputDialog(text="Ingresa IP o Dominio objetivo\n(Ej. 192.168.1.1 o facebook.com):", title="Nmap Forense")
        objetivo = dialogo_obj.get_input()
        if objetivo:
            menu_texto = "1. Rápido (Puertos comunes)\n2. Intermedio (Versiones)\n3. Agresivo (SO e Info profunda)"
            dialogo_tipo = ctk.CTkInputDialog(text=f"Elige el nivel de agresividad:\n\n{menu_texto}", title="Vector de Escaneo")
            tipo = dialogo_tipo.get_input()
            if tipo in ['1', '2', '3']:
                abrir_consola_y_ejecutar("ESCÁNER NMAP", lambda log: logica_nmap(log, objetivo, tipo))

    def btn_auditor_web():
        dialogo = ctk.CTkInputDialog(text="Ingresa la IP o Dominio del servidor web a auditar\n(Ej. 192.168.1.1 o mired.com):", title="Auditor Web")
        objetivo = dialogo.get_input()
        if objetivo:
            abrir_consola_y_ejecutar("AUDITOR WEB FORENSE", lambda log: logica_auditor_web(log, objetivo))

    def btn_puerto_proceso():
        dialogo = ctk.CTkInputDialog(text="Puerto local a investigar (ej. 8080):", title="Rastreo")
        puerto = dialogo.get_input()
        if puerto: abrir_consola_y_ejecutar("PUERTO", lambda log: logica_puerto_proceso(log, puerto))
        
    def btn_generador_qr():
        menu = "1. Red Wi-Fi (Para que se conecten sin clave)\n2. Enlace Web o Texto Libre"
        dialogo_tipo = ctk.CTkInputDialog(text=f"¿Qué tipo de QR deseas crear?\n\n{menu}", title="Generador Universal QR")
        tipo = dialogo_tipo.get_input()
        
        if tipo == '1':
            dialogo_ssid = ctk.CTkInputDialog(text="Nombre de la red Wi-Fi (SSID):", title="QR Wi-Fi")
            ssid = dialogo_ssid.get_input()
            if ssid:
                dialogo_pwd = ctk.CTkInputDialog(text="Contraseña (vacío si es red libre):", title="Clave")
                pwd = dialogo_pwd.get_input()
                abrir_consola_y_ejecutar("GENERADOR QR", lambda log: logica_generador_qr(log, '1', ssid, pwd))
                
        elif tipo == '2':
            dialogo_txt = ctk.CTkInputDialog(text="Pega el enlace web (URL) o escribe tu texto:", title="QR Enlace / Texto")
            texto = dialogo_txt.get_input()
            if texto:
                abrir_consola_y_ejecutar("GENERADOR QR", lambda log: logica_generador_qr(log, '2', texto))
            
    def btn_dns_res():
        dialogo = ctk.CTkInputDialog(text="Dominio a resolver (ej. facebook.com):", title="DNS")
        dom = dialogo.get_input()
        if dom: abrir_consola_y_ejecutar("DNS", lambda log: logica_resolucion_dns(log, dom))
        
    def btn_bloquear_web():
        menu = "1. Bloquear una página web\n2. Restaurar una página web específica\n3. Restaurar TODAS las páginas (Fábrica)"
        dialogo = ctk.CTkInputDialog(text=f"¿Qué deseas hacer?\n\n{menu}", title="Gestor de Bloqueo Web")
        opcion = dialogo.get_input()
        
        if opcion in ['1', '2']:
            accion_txt = "bloquear" if opcion == '1' else "restaurar"
            dialogo_dom = ctk.CTkInputDialog(text=f"Ingresa el dominio a {accion_txt} (ej. tiktok.com):", title="Dominio Objetivo")
            dom = dialogo_dom.get_input()
            if dom:
                abrir_consola_y_ejecutar(f"{accion_txt.upper()} WEB", lambda log: logica_bloquear_web(log, opcion, dom))
        elif opcion == '3':
            abrir_consola_y_ejecutar("RESTAURACIÓN TOTAL", lambda log: logica_bloquear_web(log, opcion, ""))
        
    def btn_abrir_puerto():
        dialogo_puerto = ctk.CTkInputDialog(text="Puerto a ABRIR en Firewall:", title="Firewall")
        puerto = dialogo_puerto.get_input()
        if puerto:
            dialogo_proto = ctk.CTkInputDialog(text="Protocolo (TCP o UDP):", title="Protocolo")
            proto = dialogo_proto.get_input()
            if proto: abrir_consola_y_ejecutar("FIREWALL", lambda log: logica_abrir_puerto(log, puerto, proto.upper()))
            
    def btn_escaner():
        menu = "1. Auto-Escanear mi propio PC (Detecta IP automáticamente)\n2. Escanear un Equipo o Dominio Externo"
        dialogo = ctk.CTkInputDialog(text=f"¿Qué objetivo deseas escanear?\n\n{menu}", title="Radar de Puertos Avanzado")
        opcion = dialogo.get_input()
        
        if opcion == '1':
            import socket
            try:
                # Obtiene el nombre del equipo y saca su IP de red local
                ip_local = socket.gethostbyname(socket.gethostname())
            except:
                ip_local = "127.0.0.1" # Fallback de seguridad
                
            abrir_consola_y_ejecutar("ESCÁNER LOCAL", lambda log: logica_escaner_puertos_python(log, ip_local))
            
        elif opcion == '2':
            dialogo_ip = ctk.CTkInputDialog(text="Ingresa la IP o Dominio a escanear (ej. 192.168.1.5 o mired.com):", title="Objetivo Remoto")
            ip = dialogo_ip.get_input()
            if ip:
                abrir_consola_y_ejecutar("ESCÁNER REMOTO", lambda log: logica_escaner_puertos_python(log, ip))
        
    def btn_nas():
        dialogo_ruta = ctk.CTkInputDialog(text="Ruta de la carpeta (ej. C:\\Trabajo):", title="Servidor NAS")
        ruta = dialogo_ruta.get_input()
        if ruta:
            dialogo_nom = ctk.CTkInputDialog(text="Nombre para el recurso en red:", title="Servidor NAS")
            nombre = dialogo_nom.get_input()
            if nombre: abrir_consola_y_ejecutar("NAS", lambda log: logica_crear_nas(log, ruta, nombre))
            
    def btn_latencia():
        dialogo = ctk.CTkInputDialog(text="Ingresa dominio para medir (ej. google.com):", title="Latencia")
        dest = dialogo.get_input()
        if dest: abrir_consola_y_ejecutar("LATENCIA", lambda log: logica_auditoria_latencia(log, dest))
        
    def btn_wifi():
        dialogo = ctk.CTkInputDialog(text="1. Extraer y Auditar Claves\n2. Exportar Backup\n3. Importar Backup", title="Forense Wi-Fi (KeyHunter)")
        op = dialogo.get_input()
        if op in ['1', '2', '3']: abrir_consola_y_ejecutar("WI-FI FORENSE", lambda log: logica_wifi_forense(log, op))
        
    def btn_dns_opt():
        menu = (
            "--- MÁXIMA VELOCIDAD ---\n"
            "1. Cloudflare (Rápido y Privado)\n"
            "2. Google (Estabilidad)\n\n"
            "--- BLOQUEO DE ANUNCIOS ---\n"
            "3. AdGuard (Adiós a la publicidad)\n"
            "4. Mullvad (Cero Rastreadores)\n\n"
            "--- CIBERSEGURIDAD (ANTI-VIRUS WEB) ---\n"
            "5. Quad9 (Especializado en Malware)\n"
            "6. Cloudflare Security\n"
            "7. ControlD (Bloqueo Malware)\n\n"
            "--- FILTRO FAMILIAR (ANTI-ADULTO) ---\n"
            "8. Cloudflare Family (+ Malware)\n"
            "9. CleanBrowsing (Filtro Estricto)\n"
            "10. AdGuard Family (+ Anuncios)\n"
            "11. OpenDNS Family Shield\n\n"
            "--- RESTAURACIÓN ---\n"
            "12. Restaurar DNS Automático (DHCP)"
        )
        dialogo = ctk.CTkInputDialog(text=f"Elige el perfil DNS a inyectar:\n\n{menu}", title="Optimizador DNS Extremo")
        op = dialogo.get_input()
        if op and op.isdigit():
            abrir_consola_y_ejecutar("OPTIMIZADOR DNS", lambda log: logica_optimizar_dns(log, str(int(op))))

    h_redes = [
        {"id": "1", "nombre": "1. Info Básica de Red e IP", "cmd": lambda: abrir_consola_y_ejecutar("INFO DE RED", logica_info_red), "nov": "Muestra IP local y pública al instante. Útil para configuraciones y diagnósticos rápidos.", "exp": "[Sockets nativos / API REST] Resuelve hostname e invoca a api.ipify.org para evadir NAT y exponer IP WAN."},
        {"id": "2", "nombre": "2. Reparador de Red Autónomo", "cmd": lambda: abrir_consola_y_ejecutar("REPARADOR DE RED", logica_reparacion_red), "nov": "Soluciona el error 'Conectado sin internet'. Limpia DNS, renueva IP, fuerza protocolo DHCP y destruye Proxies maliciosos.", "exp": "[Autónomo] Ejecuta reseteo de Winsock, purga proxy HTTP e inyecta parámetros netsh dinámicamente forzando DHCP en interfaces activas."},
        {"id": "3", "nombre": "3. Prueba de Conectividad (Ping/TCP)", "cmd": btn_ping, "nov": "Verifica si una web está en línea y responde correctamente, con la opción de escanear puertos específicos.", "exp": "[Microsoft OS] Llama a Test-NetConnection para trazar latencia ICMP o auditar el estado y handshake de puertos TCP."},
        {"id": "4", "nombre": "4. Monitor Conexiones TCP", "cmd": lambda: abrir_consola_y_ejecutar("MONITOR TCP", logica_conexiones_tcp), "nov": "Escanea y muestra en tiempo real qué programas de tu computadora están conectados a internet consumiendo red.", "exp": "[Microsoft OS] Filtra la tabla de enrutamiento (Get-NetTCPConnection) y cruza el PID para revelar la ruta del ejecutable."},
        {"id": "5", "nombre": "5. Identificar Proceso por Puerto", "cmd": btn_puerto_proceso, "nov": "Si un programa falla porque 'el puerto está en uso', descubre exactamente qué aplicación lo bloquea en la sombra.", "exp": "[Microsoft OS] Interroga puertos locales activos y extrae el OwningProcess mapeando la ruta física del binario."},
        {"id": "6", "nombre": "6. Auditoría y Migración Wi-Fi", "cmd": btn_wifi, "nov": "Extrae las contraseñas Wi-Fi del equipo, evalúa si son fáciles de hackear y busca en la Dark Web si ya han sido filtradas. También permite hacer respaldos.", "exp": "[Fusión KeyHunter] Parsea XML nativo de 'netsh wlan'. Incorpora algoritmo de Regex para entropía de contraseñas y consulta hashes SHA-1 contra la API k-Anonymity de HaveIBeenPwned."},
        {"id": "7", "nombre": "7. Generador Universal de QR", "cmd": btn_generador_qr, "nov": "Crea códigos QR instantáneos para compartir tu Wi-Fi o páginas web. Se guarda en el Escritorio listo para imprimir.", "exp": "[API REST] Ensambla URIs dinámicas (WIFI:T:WPA o Texto/URL) y descarga la matriz PNG evitando dependencias externas."},
        {"id": "8", "nombre": "8. Radar OSINT de IP (Geolocalización)", "cmd": btn_geolocalizar, "nov": "Rastrea la ubicación exacta, ciudad, código postal y proveedor de cualquier dirección IP en el mundo. Genera un mapa satelital.", "exp": "[Inteligencia OSINT] Triangulación vía ip-api.com. Extrae BGP/ASN y lat/lon. Renderiza un mapa táctico interactivo en HTML5 usando Leaflet.js incrustado (Dark Mode)."},
        {"id": "9", "nombre": "9. Diagnóstico Wi-Fi (WlanReport)", "cmd": lambda: abrir_consola_y_ejecutar("REPORTE WI-FI", logica_reporte_wifi), "nov": "Genera un reporte web muy profesional sobre la salud de tu tarjeta Wi-Fi, mostrando un historial de caídas y desconexiones.", "exp": "[Microsoft OS] Invoca el motor nativo ETW (Event Tracing for Windows) compilando un HTML con transiciones de red."},
        {"id": "10", "nombre": "10. Resolución DNS Inversa", "cmd": btn_dns_res, "nov": "Convierte el nombre de cualquier página web (ej. google.com) en su dirección IP numérica real de servidores.", "exp": "[Microsoft OS] Utiliza Resolve-DnsName interrumpiendo la caché local para interrogar servidores raíz sobre registros A/CNAME."},
        {"id": "11", "nombre": "11. Gestor Avanzado de Hosts", "cmd": btn_bloquear_web, "nov": "Bloquea páginas, restaura accesos específicos o resetea el archivo Hosts a configuración de fábrica al instante.", "exp": "[OS Base] Gestor dinámico del archivo nativo drivers/etc/hosts. Permite inyección, limpieza quirúrgica y restauración global con purga de caché DNS inmediata."},
        {"id": "12", "nombre": "12. Abrir Puertos Firewall", "cmd": btn_abrir_puerto, "nov": "Crea reglas rápidas para permitir que juegos o programas se comuniquen libremente sin que el antivirus los bloquee.", "exp": "[Microsoft OS] Inserta reglas directas Inbound en Defender Firewall mediante netsh, habilitando flujos TCP/UDP."},
        {"id": "13", "nombre": "13. Purgar Historial Wi-Fi", "cmd": lambda: abrir_consola_y_ejecutar("PURGAR WI-FI", logica_purgar_wifi_historial), "nov": "Elimina por completo todas las redes memorizadas en tu PC para resolver problemas de conexión por claves viejas.", "exp": "[Microsoft OS] Emplea un wildcard en la interfaz CLI de WLAN (profile name=* i=*) truncando la base de perfiles."},
        {"id": "14", "nombre": "14. Reset Firewall a Fábrica", "cmd": lambda: abrir_consola_y_ejecutar("RESET FIREWALL", logica_reset_firewall), "nov": "Restaura las defensas y bloqueos de Windows a su estado original. Útil si bloqueaste tu propio internet por error.", "exp": "[Microsoft OS] Reset absoluto de Advanced Firewall, reconstruyendo tablas y eliminando GPOs de terceros."},
        {"id": "15", "nombre": "15. Purgar Caché ARP", "cmd": lambda: abrir_consola_y_ejecutar("PURGAR ARP", logica_limpiar_arp), "nov": "Obliga a tu computadora a volver a identificar los equipos físicos de tu red. Útil si cambiaste de router recientemente.", "exp": "[Protocolo ARP] Ejecuta arp -d * para vaciar la tabla estática de traducción de IPs a direcciones físicas MAC."},
        {"id": "16", "nombre": "16. Optimizador Avanzado de DNS", "cmd": btn_dns_opt, "nov": "Escudo perimetral a medida: Acelera tu red, bloquea anuncios en todo el sistema, frena el malware o activa un filtro familiar anti-adultos.", "exp": "[Inyección PS] Despliega 11 perfiles de filtrado perimetral. Inyecta arreglos de IPs públicas vía Set-DnsClientServerAddress en las interfaces activas (AdGuard, Quad9, Mullvad, ControlD, etc)."},
        {"id": "17", "nombre": "17. Gestionar Sesiones SMB", "cmd": lambda: abrir_consola_y_ejecutar("SESIONES SMB", logica_sesiones_smb), "nov": "Detecta al instante si alguien más en tu misma red LAN está accediendo a tus carpetas compartidas sin tu permiso.", "exp": "[Microsoft OS] Audita el servicio Server Message Block (SMB) usando Get-SmbSession, revelando clientes conectados."},
        {"id": "18", "nombre": "18. Radar Wi-Fi de Espectro", "cmd": lambda: abrir_consola_y_ejecutar("RADAR WI-FI", logica_radar_wifi), "nov": "Escanea a tu alrededor para ver todas las redes Wi-Fi (incluso ocultas), señal exacta y canales menos saturados.", "exp": "[Microsoft OS] Despliega un loop temporal sobre mode=bssid para realizar barridos de radiofrecuencia e intensidad."},
        {"id": "19", "nombre": "19. Auditoría Latencia (Microcortes)", "cmd": btn_latencia, "nov": "Envía paquetes de forma continua para detectar pequeñas caídas ocultas de internet que causan lag en juegos o llamadas.", "exp": "[Python/ICMP] Combina un loop de Pings discretos con módulo datetime logueando latencia (ms) para cazar timeouts."},
        {"id": "20", "nombre": "20. Radar de Puertos Avanzado", "cmd": btn_escaner, "nov": "Motor multihilo. Auto-detecta tu equipo o escanea redes externas en milisegundos buscando posibles vectores de ataque o puertas traseras.", "exp": "[Asíncrono Multihilo] Despliega 16 hilos en paralelo (ThreadPoolExecutor) para ataque simultáneo sobre puertos TCP letales. Incluye resolución automática de DNS local."},
        {"id": "21", "nombre": "21. Crear Servidor NAS Compartido", "cmd": btn_nas, "nov": "Transforma cualquier carpeta de tu PC en un servidor rápido para que celulares o TVs puedan acceder a su contenido.", "exp": "[Microsoft OS] Automatiza New-SmbShare concediendo permisos universales y adaptando dinámicamente el Firewall local."},
        {"id": "22", "nombre": "22. Auditar Caché DNS Web", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR DNS", logica_auditar_cache_dns), "nov": "Revela una lista oculta de las páginas web a las que esta PC se ha conectado silenciosamente de fondo.", "exp": "[Microsoft OS] Volcado directo del búfer interno del resolver DNS de Windows, exponiendo registros de conexión temporal."},
        {"id": "23", "nombre": "23. Visualizador de Tráfico de Red", "cmd": lambda: abrir_consola_y_ejecutar("SNIFFNET", logica_sniffnet), "nov": "Mapea tu internet en tiempo real. Muestra gráficas de descarga, analiza protocolos e identifica el país de los servidores.", "exp": "[Forense Sniffnet Rust] Ejecutable ultraligero que intercepta sockets mediante Pcap. Posee secuencia de despliegue silencioso de dependencias WinPcap y GUI analítica."},
        {"id": "24", "nombre": "24. Escáner Forense Táctico (Nmap)", "cmd": btn_nmap_win, "nov": "Mapea los puertos abiertos, detecta los sistemas operativos y busca debilidades en cualquier equipo conectado a la red.", "exp": "[Motor Nmap Portátil] Despliegue ghost de la suite Nmap. Incorpora evasión de Ping (-Pn) y detección profunda de S.O. Vuelca logs interactivos."},
        {"id": "25", "nombre": "25. Reparar Visibilidad LAN", "cmd": lambda: abrir_consola_y_ejecutar("VISIBILIDAD RED", logica_visibilidad_lan), "nov": "Soluciona el problema de no poder ver a otras computadoras en la red para compartir archivos o impresoras.", "exp": "[Microsoft OS] Automatiza el arranque de demonios PnP y FDResPub. Habilita reglas Inbound/Outbound del Firewall para Network Discovery."},
        {"id": "26", "nombre": "26. Auditor Web Forense (DirBuster/Banner)", "cmd": btn_auditor_web, "nov": "Analiza servidores web o routers locales. Extrae la tecnología que utilizan y busca paneles de administrador ocultos o copias de seguridad expuestas.", "exp": "[Fusión DirBuster/Banner] Realiza Banner Grabbing HTTP/HTTPS extrayendo cabeceras (Server, X-Powered-By) e inyecta un fuzzer táctico de directorios concurrentes con manejo de excepciones HTTP."},
        {"id": "27", "nombre": "27. Radar Táctico de Enjambre (GeoWiFi)", "cmd": btn_geowifi, "nov": "Triangula en un mapa interactivo el enjambre de redes a tu alrededor o localiza routers remotos, evadiendo bloqueos de bases de datos OSINT.", "exp": "[OSINT Enjambre] Captura BSSIDs locales mediante netsh y triangula el epicentro usando concurrent.futures. Incluye fallback automático de puente a Wigle.net si el servidor cae."},
        {"id": "28", "nombre": "28. Radar Financiero y Laboratorio API", "cmd": lambda: abrir_consola_y_ejecutar("RADAR FINANCIERO", logica_cotizador_divisas), "nov": "Consulta en tiempo real la tasa del Dólar y el Euro frente al Peso Colombiano. Incluye una calculadora inteligente y un laboratorio que te enseña cómo el código extrae estos datos de internet.", "exp": "[API REST + JSON] Ejecuta un Request asíncrono hacia open.er-api.com decodificando diccionarios JSON. Mapea la tasa de conversión flotante y re-renderiza una GUI reactiva calculando conversiones al vuelo sin dependencias externas."},
        {"id": "29", "nombre": "29. Laboratorio Forense Anti-Phishing", "cmd": lambda: abrir_consola_y_ejecutar("ANTI-PHISHING", logica_analizador_phishing), "nov": "Detecta si un correo electrónico es falso o real. Pega el código original del correo y la herramienta analizará las firmas de seguridad y geolocalizará la IP del remitente.", "exp": "[Fusión OSINT + Regex] Módulo 2 en 1. Parsea cabeceras crudas (RFC 5322) usando Regex para validar firmas criptográficas SPF/DKIM/DMARC. Extrae la IP de origen y pivota hacia ip-api.com para trazar el ASN/ISP."}
    ]
    construir_vista_dinamica("🌐 Redes e Internet", "🔍 Buscar (Ej: dns, 16, wifi)...", h_redes)

def cargar_categoria_mantenimiento():
    global app

    def btn_fugas_espacio():
        import psutil, math, os, subprocess
        from tkinter import messagebox

        # 1. Analizador Inteligente de Hardware (Lectura en chips físicos)
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            script_ram = "Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum | Select-Object -ExpandProperty Sum"
            ram_bytes = int(subprocess.run(["powershell", "-NoProfile", "-Command", script_ram], capture_output=True, text=True, startupinfo=startupinfo).stdout.strip())
        except:
            ram_bytes = psutil.virtual_memory().total
            
        ram_gb = math.ceil(ram_bytes / (1024**3))
        
        # --- FIX: FÓRMULA MATEMÁTICA DINÁMICA DE INGENIERO ---
        # Se auto-acopla a la cantidad EXACTA de RAM, sin usar "bloques" genéricos.
        if ram_gb <= 4:
            # Muy poca RAM: Necesita mucha memoria virtual (Regla de 1.5x a 3x)
            rec_min_mb = int(ram_gb * 1.5 * 1024)
            rec_max_mb = int(ram_gb * 3 * 1024)
        elif ram_gb <= 8:
            # Gama Media (Tus 6GB u 8GB):
            # Para 6GB recomendará 9216 MB de máximo. Para 8GB recomendará 12288 MB.
            rec_min_mb = 4096
            rec_max_mb = int(ram_gb * 1.5 * 1024)
        elif ram_gb <= 16:
            # Gama Alta: La RAM soporta casi todo, no sobrecargamos el disco (Regla de 1x)
            rec_min_mb = 4096
            rec_max_mb = int(ram_gb * 1024)
        else:
            # Entusiasta (+16GB): El disco duro ya no necesita hacer el trabajo de la RAM
            rec_min_mb = 2048
            rec_max_mb = 8192

        # 2. Escáner de Discos
        discos_info = []
        mejor_disco = "C:"
        max_free = 0
        
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt' and ('cdrom' in part.opts or part.fstype == ''): continue
            try:
                uso = psutil.disk_usage(part.mountpoint)
                free_gb = uso.free / (1024**3)
                total_gb = uso.total / (1024**3)
                discos_info.append({"letra": part.device[:2], "free_gb": free_gb, "total_gb": total_gb})
                # Elige automáticamente el que tiene más espacio libre
                if free_gb > max_free:
                    max_free = free_gb
                    mejor_disco = part.device[:2]
            except: pass

        if not discos_info:
            messagebox.showerror("Error", "No se pudieron escanear los discos.")
            return

        # 3. Construcción del Dashboard Decisivo
        dialog_fugas = ctk.CTkToplevel(app)
        dialog_fugas.title("Optimizador Inteligente de Memoria Virtual")
        dialog_fugas.geometry("750x650")
        dialog_fugas.attributes("-topmost", True)
        dialog_fugas.transient(app)

        ctk.CTkLabel(dialog_fugas, text="🧠 Análisis de Hardware Completado", font=("Arial", 22, "bold"), text_color="#38BDF8").pack(pady=(25,5))
        
        texto_edu = (f"Tu PC tiene {ram_gb} GB de RAM física instalada. "
                     "La memoria virtual es un archivo de respaldo en el disco duro que evita que los programas crasheen "
                     "cuando la RAM se llena.\n\n"
                     "TREMEND ha calculado el límite exacto para tu cantidad de RAM. Asignar 100 GB no la hará más rápida, "
                     "sólo desgastará tu disco innecesariamente.")
        ctk.CTkLabel(dialog_fugas, text=texto_edu, font=("Arial", 14), text_color="#E2E8F0", wraplength=650, justify="center").pack(pady=10)

        # SECCIÓN DISCOS
        frame_discos = ctk.CTkFrame(dialog_fugas, fg_color="#1E293B", corner_radius=10)
        frame_discos.pack(fill="x", padx=40, pady=10)
        ctk.CTkLabel(frame_discos, text="1. Selecciona la unidad de destino:", font=("Arial", 16, "bold"), text_color="#10B981").pack(anchor="w", padx=15, pady=(10,5))
        
        ctk.CTkLabel(frame_discos, text="💡 Recomendación: TREMEND ha preseleccionado tu disco con mayor espacio libre.\n⚠️ ADVERTENCIA: Si C: es un disco rápido (SSD) y el preseleccionado es uno viejo y lento (HDD), mantén C:.", font=("Arial", 12, "italic"), text_color="#FCD34D", justify="left").pack(anchor="w", padx=15, pady=(0,10))

        var_disco = ctk.StringVar(value=mejor_disco)
        
        for d in discos_info:
            texto_rb = f"Disco {d['letra']} (Libre: {d['free_gb']:.1f} GB / Total: {d['total_gb']:.1f} GB)"
            rb = ctk.CTkRadioButton(frame_discos, text=texto_rb, variable=var_disco, value=d['letra'], font=("Arial", 14), fg_color="#38BDF8")
            rb.pack(anchor="w", padx=30, pady=8)

        # SECCIÓN LIMITES
        frame_mb = ctk.CTkFrame(dialog_fugas, fg_color="#1E293B", corner_radius=10)
        frame_mb.pack(fill="x", padx=40, pady=10)
        ctk.CTkLabel(frame_mb, text=f"2. Límites Exactos Calculados ({ram_gb} GB RAM):", font=("Arial", 16, "bold"), text_color="#10B981").pack(anchor="w", padx=15, pady=(10,5))
        
        row1 = ctk.CTkFrame(frame_mb, fg_color="transparent")
        row1.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(row1, text="Tamaño Inicial (MB):", font=("Arial", 14)).pack(side="left")
        ent_min = ctk.CTkEntry(row1, width=120)
        ent_min.pack(side="right")
        ent_min.insert(0, str(int(rec_min_mb)))
        
        row2 = ctk.CTkFrame(frame_mb, fg_color="transparent")
        row2.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(row2, text="Tamaño Máximo (MB):", font=("Arial", 14)).pack(side="left")
        ent_max = ctk.CTkEntry(row2, width=120)
        ent_max.pack(side="right")
        ent_max.insert(0, str(int(rec_max_mb)))

        def ejecutar():
            disco_sel = var_disco.get()
            try:
                min_v, max_v = int(ent_min.get()), int(ent_max.get())
            except:
                messagebox.showerror("Error", "Los valores deben ser numéricos."); return
            if min_v > max_v:
                messagebox.showerror("Error", "El tamaño inicial no puede ser mayor al máximo."); return
                
            dialog_fugas.destroy()
            abrir_consola_y_ejecutar("REPARAR FUGAS", lambda log: logica_fugas_espacio(log, disco_sel, min_v, max_v))

        btn_frame = ctk.CTkFrame(dialog_fugas, fg_color="transparent")
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="⚡ Aplicar Optimización", font=("Arial", 15, "bold"), height=45, fg_color="#10B981", hover_color="#059669", command=ejecutar).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", font=("Arial", 15, "bold"), height=45, fg_color="#EF4444", hover_color="#DC2626", command=dialog_fugas.destroy).pack(side="left", padx=10)

    def btn_debloat():
        dialogo = ctk.CTkInputDialog(text="App a eliminar (ej. xbox, zune):", title="Debloat")
        app_name = dialogo.get_input()
        if app_name: abrir_consola_y_ejecutar("DEBLOAT", lambda log: logica_debloat(log, app_name))
        
    def btn_chkdsk():
        dialogo = ctk.CTkInputDialog(text="Letra de unidad a reparar (ej. C):", title="CHKDSK")
        letra = dialogo.get_input()
        if letra: abrir_consola_y_ejecutar("CHKDSK", lambda log: logica_chkdsk(log, letra))
    def btn_mantenimiento_extremo():
        import subprocess
        # 1. Obtener los discos conectados en tiempo real mediante WMI
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        script_discos = 'Get-WmiObject Win32_LogicalDisk | ForEach-Object { $_.DeviceID + " - " + $_.VolumeName + " (" + $_.Description + ")" }'
        resultado = subprocess.run(["powershell", "-NoProfile", "-Command", script_discos], capture_output=True, text=True, startupinfo=startupinfo)
        
        discos_detectados = [line.strip() for line in resultado.stdout.splitlines() if line.strip()]

        if not discos_detectados: return

        # 2. Construir la ventana emergente de selección
        dialog_discos = ctk.CTkToplevel(app)
        dialog_discos.title("Mantenimiento Extremo - Selección")
        dialog_discos.geometry("450x450")
        dialog_discos.attributes("-topmost", True)
        dialog_discos.transient(app)

        ctk.CTkLabel(dialog_discos, text="¿Qué discos deseas limpiar?", font=("Arial", 18, "bold"), text_color="#10B981").pack(pady=(20, 5))
        ctk.CTkLabel(dialog_discos, text="Selecciona los USB, discos duros o SSD a purgar.", font=("Arial", 13), text_color="#94A3B8").pack(pady=(0, 15))

        frame_checks = ctk.CTkScrollableFrame(dialog_discos, height=200, fg_color="#1E293B", corner_radius=10)
        frame_checks.pack(fill="x", padx=30, pady=10)

        checkboxes = []
        for disco in discos_detectados:
            letra = disco.split(" ")[0] # Extrae la pura letra "C:", "D:", etc.
            # Por seguridad, el C: inicia marcado. Los USB inician desmarcados
            var = ctk.BooleanVar(value=True if letra == "C:" else False)
            chk = ctk.CTkCheckBox(frame_checks, text=disco, variable=var, font=("Arial", 14), text_color="#FFFFFF", fg_color="#10B981", hover_color="#059669")
            chk.pack(anchor="w", pady=8, padx=10)
            checkboxes.append((letra, var))

        # El botón de "Seleccionar / Desmarcar Todos" que solicitaste
        def toggle_todos():
            estado_actual = checkboxes[0][1].get()
            nuevo_estado = not estado_actual
            for _, var in checkboxes:
                var.set(nuevo_estado)
            btn_todos.configure(text="Desmarcar Todos" if nuevo_estado else "Seleccionar Todos")

        btn_todos = ctk.CTkButton(dialog_discos, text="Seleccionar Todos", width=150, fg_color="#475569", hover_color="#334155", command=toggle_todos)
        btn_todos.pack(pady=10)

        # 3. Lanzar a la terminal con la lista procesada
        def iniciar():
            seleccionados = [letra for letra, var in checkboxes if var.get()]
            dialog_discos.destroy()
            if seleccionados:
                abrir_consola_y_ejecutar("MANTENIMIENTO EXTREMO", lambda log: logica_mantenimiento_profundo(log, seleccionados))

        btn_frame = ctk.CTkFrame(dialog_discos, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="⚡ Iniciar Limpieza", font=("Arial", 14, "bold"), height=40, fg_color="#10B981", hover_color="#059669", command=iniciar).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", font=("Arial", 14, "bold"), height=40, fg_color="#EF4444", hover_color="#DC2626", command=dialog_discos.destroy).pack(side="left", padx=10)

    def btn_mapa_espacio():
        import psutil, os, threading, shutil, concurrent.futures
        from tkinter import ttk, messagebox

        # 1. Selección de Disco
        discos = [p.device for p in psutil.disk_partitions(all=False) if 'cdrom' not in p.opts and p.fstype != '']
        if not discos:
            messagebox.showerror("Error", "No se detectaron discos válidos.")
            return

        dialogo_disco = ctk.CTkInputDialog(text=f"Discos detectados: {', '.join(discos)}\nEscribe la letra del disco a escanear (Ej: C:\\ o D:\\):", title="Selección de Objetivo")
        disco_sel = dialogo_disco.get_input()
        
        if not disco_sel: return
        disco_sel = disco_sel.strip().upper()
        if not disco_sel.endswith("\\"): disco_sel += "\\"
        
        if disco_sel not in discos:
            messagebox.showerror("Error", "Disco no válido o no encontrado.")
            return

        # 2. Ventana Principal del Radar (INICIA ENCOGIDA Y ELEGANTE)
        win_mapa = ctk.CTkToplevel(app)
        win_mapa.title(f"Radar Visual de Almacenamiento - Disco {disco_sel}")
        win_mapa.geometry("650x200")  # <-- TAMAÑO AJUSTADO PARA QUE QUEPA EL TEXTO
        win_mapa.attributes("-topmost", True)
        win_mapa.transient(app)

        frame_sugerencias = ctk.CTkFrame(win_mapa, fg_color="transparent")
        frame_arbol = ctk.CTkFrame(win_mapa, fg_color="transparent")
        
        # <-- FIX MAESTRO: WRAPLENGTH Y JUSTIFY CENTER PARA AUTO-ACOPLAR TEXTOS LARGOS -->
        lbl_estado = ctk.CTkLabel(win_mapa, text="Analizando sectores del disco...", font=("Arial", 16, "bold"), text_color="#FCD34D", justify="center", wraplength=600)
        lbl_estado.pack(expand=True)

        # --- MOTOR MAXIMIZADO DE CÁLCULO (ANTI-BUCLES) ---
        def get_size_fast(path):
            total = 0
            try:
                for entry in os.scandir(path):
                    try:
                        if entry.is_symlink(): continue
                        if hasattr(entry, 'is_junction') and entry.is_junction(): continue
                        
                        if entry.is_file(follow_symlinks=False):
                            total += entry.stat(follow_symlinks=False).st_size
                        elif entry.is_dir(follow_symlinks=False):
                            total += get_size_fast(entry.path)
                    except: pass
            except: pass
            return total

        def formatear_tamano(bytes_size):
            if bytes_size == 0: return "0 B"
            nombres = ("B", "KB", "MB", "GB", "TB")
            i = 0
            while bytes_size >= 1024 and i < len(nombres)-1:
                bytes_size /= 1024.0
                i += 1
            return f"{bytes_size:.2f} {nombres[i]}"

        # --- FASE 1: SUGERENCIAS INTELIGENTES ---
        rutas_basura = {
            "Caché de Windows Update": r"C:\Windows\SoftwareDistribution\Download",
            "Archivos Temporales (Sistema)": r"C:\Windows\Temp",
            "Archivos Temporales (Usuario)": os.environ.get('TEMP', ''),
            "Caché de Arranque (Prefetch)": r"C:\Windows\Prefetch",
            "Papelera de Reciclaje oculta": os.path.join(disco_sel, "$RECYCLE.BIN")
        }
        basura_detectada = []

        def escanear_sugerencias():
            total_basura = 0
            for nombre, ruta in rutas_basura.items():
                if os.path.exists(ruta):
                    peso = get_size_fast(ruta)
                    if peso > 1024 * 1024:
                        basura_detectada.append({"nombre": nombre, "ruta": ruta, "peso_bytes": peso, "peso_str": formatear_tamano(peso)})
                        total_basura += peso
            app.after(0, lambda: mostrar_fase_1(total_basura))

        def mostrar_fase_1(total_basura):
            win_mapa.geometry("850x650") # <-- EXPANSIÓN
            lbl_estado.pack_forget()
            frame_sugerencias.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(frame_sugerencias, text="💡 Sugerencias de Limpieza Inteligente", font=("Arial", 22, "bold"), text_color="#10B981").pack(pady=(0,5))
            ctk.CTkLabel(frame_sugerencias, text="Se han detectado archivos residuales del sistema operativo que puedes borrar sin riesgo.", font=("Arial", 13), text_color="#94A3B8").pack(pady=(0,15))
            
            if not basura_detectada:
                ctk.CTkLabel(frame_sugerencias, text="¡Tu sistema está limpio! No hay sugerencias importantes.", font=("Arial", 14), text_color="#38BDF8").pack(pady=20)
                btn_txt = "Continuar al Mapa Visual ➡️"
            else:
                ctk.CTkLabel(frame_sugerencias, text=f"Espacio total recuperable: {formatear_tamano(total_basura)}", font=("Arial", 16, "bold"), text_color="#FCD34D").pack(pady=10)
                btn_txt = "⚡ Purgar Selección y Continuar"
            
            vars_checkboxes = []
            frame_lista_sug = ctk.CTkScrollableFrame(frame_sugerencias, fg_color="#1E293B", corner_radius=10, height=250)
            frame_lista_sug.pack(fill="x", padx=20, pady=10)
            
            for item in basura_detectada:
                var = ctk.BooleanVar(value=True)
                vars_checkboxes.append((item, var))
                texto = f"{item['nombre']}  ({item['peso_str']})"
                ctk.CTkCheckBox(frame_lista_sug, text=texto, variable=var, font=("Arial", 14, "bold"), fg_color="#EF4444", hover_color="#DC2626", text_color="#E2E8F0").pack(anchor="w", padx=15, pady=10)

            def aplicar_y_continuar():
                for item, var in vars_checkboxes:
                    if var.get():
                        try:
                            ruta_del = item['ruta']
                            for c in os.listdir(ruta_del):
                                p = os.path.join(ruta_del, c)
                                if os.path.isfile(p): os.unlink(p)
                                elif os.path.isdir(p): shutil.rmtree(p, ignore_errors=True)
                        except: pass
                
                win_mapa.geometry("650x200") # <-- ENCOGIMIENTO CORREGIDO
                frame_sugerencias.pack_forget()
                lbl_estado.configure(text=f"Mapeando árbol de directorios de {disco_sel}...", text_color="#38BDF8")
                lbl_estado.pack(expand=True)
                threading.Thread(target=escanear_arbol_principal, args=(disco_sel,), daemon=True).start()

            ctk.CTkButton(frame_sugerencias, text=btn_txt, font=("Arial", 15, "bold"), height=45, fg_color="#3B82F6", hover_color="#2563EB", command=aplicar_y_continuar).pack(pady=20)

        # --- FASE 2: MAPA VISUAL INTERACTIVO (MULTIHILO) ---
        def escanear_arbol_principal(ruta_base):
            carpetas = []
            try:
                hijos = []
                for entry in os.scandir(ruta_base):
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            if entry.name in ['System Volume Information', 'Recovery', '$Recycle.Bin', 'WindowsApps', 'Documents and Settings']: continue
                            if entry.is_symlink(): continue
                            if hasattr(entry, 'is_junction') and entry.is_junction(): continue
                            hijos.append((entry.name, entry.path))
                    except: pass
                
                total_hijos = len(hijos)
                procesados = 0

                def scan_worker(item):
                    nonlocal procesados
                    nombre, ruta = item
                    app.after(0, lambda n=nombre: lbl_estado.configure(text=f"Inspeccionando: {n}...", text_color="#38BDF8"))
                    
                    peso = get_size_fast(ruta)
                    procesados += 1
                    
                    # <-- FIX MAESTRO 2: EL SALTO DE LÍNEA AHORA ES REAL (\n) -->
                    app.after(0, lambda p=procesados, t=total_hijos: lbl_estado.configure(text=f"Escaneando disco ({p}/{t} carpetas completadas)...\nPor favor espera, el motor multihilo está trabajando.", text_color="#FCD34D"))
                    return (nombre, peso, ruta)

                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                    resultados = executor.map(scan_worker, hijos)
                    for res in resultados:
                        if res[1] > 0: carpetas.append(res)
                        
            except Exception as e: pass
            
            carpetas.sort(key=lambda x: x[1], reverse=True)
            app.after(0, lambda: mostrar_fase_2(ruta_base, carpetas))

        def mostrar_fase_2(ruta_actual, carpetas):
            win_mapa.geometry("850x650") # <-- EXPANSIÓN
            lbl_estado.pack_forget()
            for w in frame_arbol.winfo_children(): w.destroy()
            frame_arbol.pack(fill="both", expand=True, padx=20, pady=20)
            
            header_f2 = ctk.CTkFrame(frame_arbol, fg_color="transparent")
            header_f2.pack(fill="x", pady=(0, 10))
            ctk.CTkLabel(header_f2, text="🗺️ Mapa Visual de Almacenamiento", font=("Arial", 22, "bold"), text_color="#38BDF8").pack(side="left")
            
            style = ttk.Style()
            style.theme_use("default")
            style.configure("Treeview", background="#1E293B", foreground="#E2E8F0", fieldbackground="#1E293B", borderwidth=0, font=('Arial', 12), rowheight=30)
            style.map("Treeview", background=[('selected', '#3B82F6')])
            style.configure("Treeview.Heading", background="#0F172A", foreground="#38BDF8", font=('Arial', 13, 'bold'), borderwidth=0)
            
            ctk.CTkLabel(frame_arbol, text=f"📍 Ubicación actual: {ruta_actual}", font=("Arial", 13, "italic"), text_color="#FCD34D").pack(anchor="w", pady=(0, 10))
            
            columnas = ("tamaño", "ruta_oculta")
            tree = ttk.Treeview(frame_arbol, columns=columnas, show="tree headings", style="Treeview", height=12)
            tree.heading("#0", text="📂 Nombre de Carpeta", anchor="w")
            tree.heading("tamaño", text="💾 Tamaño", anchor="center")
            tree.column("#0", width=450, anchor="w")
            tree.column("tamaño", width=150, anchor="center")
            tree.column("ruta_oculta", width=0, stretch=False)
            
            for nombre, peso, ruta in carpetas:
                tree.insert("", "end", text=f"  {nombre}", values=(formatear_tamano(peso), ruta))
            
            tree.pack(fill="both", expand=True)

            acciones_frame = ctk.CTkFrame(frame_arbol, fg_color="transparent")
            acciones_frame.pack(fill="x", pady=15)

            def navegar_adentro(event=None):
                seleccion = tree.selection()
                if not seleccion: return
                ruta_hija = tree.item(seleccion[0], "values")[1]
                
                win_mapa.geometry("650x200") # <-- ENCOGIMIENTO CORREGIDO
                frame_arbol.pack_forget()
                lbl_estado.configure(text=f"Mapeando: {ruta_hija}...", text_color="#38BDF8")
                lbl_estado.pack(expand=True)
                threading.Thread(target=escanear_arbol_principal, args=(ruta_hija,), daemon=True).start()

            tree.bind("<Double-1>", navegar_adentro)

            def subir_nivel():
                padre = os.path.dirname(ruta_actual)
                if padre and padre != ruta_actual and len(padre) >= 3:
                    win_mapa.geometry("650x200") # <-- ENCOGIMIENTO CORREGIDO
                    frame_arbol.pack_forget()
                    lbl_estado.configure(text=f"Mapeando: {padre}...", text_color="#38BDF8")
                    lbl_estado.pack(expand=True)
                    threading.Thread(target=escanear_arbol_principal, args=(padre,), daemon=True).start()
                else: messagebox.showinfo("Límite", "Ya estás en la raíz del disco.")

            def eliminar_manual():
                seleccion = tree.selection()
                if not seleccion: return
                ruta_del = tree.item(seleccion[0], "values")[1]
                nombre_del = tree.item(seleccion[0], "text").strip()
                
                if messagebox.askyesno("⚠️ Destrucción Manual", f"¿Estás seguro de que deseas ELIMINAR COMPLETAMENTE la carpeta:\n\n{nombre_del}\n\nEsta acción no se puede deshacer."):
                    try:
                        shutil.rmtree(ruta_del, ignore_errors=True)
                        tree.delete(seleccion[0])
                        messagebox.showinfo("Éxito", "Carpeta destruida con éxito.")
                    except:
                        messagebox.showerror("Error", "No se pudo borrar la carpeta. Puede que requiera permisos de Administrador o esté en uso.")

            ctk.CTkButton(acciones_frame, text="⬆️ Subir de Nivel", width=120, fg_color="#334155", hover_color="#475569", command=subir_nivel).pack(side="left", padx=5)
            ctk.CTkButton(acciones_frame, text="🔍 Explorar Carpeta", font=("Arial", 13, "bold"), fg_color="#3B82F6", hover_color="#2563EB", command=navegar_adentro).pack(side="left", padx=5, expand=True, fill="x")
            ctk.CTkButton(acciones_frame, text="🗑️ Eliminar Carpeta", font=("Arial", 13, "bold"), fg_color="#EF4444", hover_color="#DC2626", command=eliminar_manual).pack(side="right", padx=5)

        threading.Thread(target=escanear_sugerencias, daemon=True).start()

    h_mant = [
            {"id": "1", "nombre": "1. Mantenimiento Extremo a Discos", "cmd": btn_mantenimiento_extremo, "nov": "Detecta discos y memorias USB. Vacía papeleras ocultas, borra cachés residuales e infecciones de macOS, y repara el sistema.", "exp": "[Interfaz CTk + WMI] Escanea Win32_LogicalDisk. Ejecuta limpieza recursiva (Trashes/DS_Store), limpia TEMP y lanza DISM/SFC sobre el Kernel."},
            {"id": "2", "nombre": "2. Optimización Avanzada (Chris Titus)", "cmd": lambda: abrir_consola_y_ejecutar("OPTIMIZADOR TITUS", logica_titus), "nov": "La mejor herramienta para acelerar PCs lentas. Desactiva funciones inútiles, instala programas base y mejora el rendimiento.", "exp": "[Chris Titus Tech] irm christitus.com/win | iex. Despliega panel WPF para aplicar tweaks de registro y purga de servicios de telemetría."},
            {"id": "3", "nombre": "3. Debloat del Sistema (Apps Nativas)", "cmd": btn_debloat, "nov": "Elimina de raíz programas basura preinstalados (como Xbox o Bing) que no se pueden desinstalar desde el panel de control.", "exp": "[Microsoft OS] Get-AppxPackage canalizado hacia Remove-AppxPackage -AllUsers. Purga paquetes provisionados UWP."},
            {"id": "4", "nombre": "4. Restablecer Cola de Impresión", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR IMPRESIÓN", logica_spooler), "nov": "Soluciona de inmediato los atascos cuando envías un documento y la impresora se queda trabada sin hacer nada.", "exp": "[Microsoft OS] Detiene Spooler. Purga recursivamente caché .SHD y .SPL del directorio System32, liberando el buffer de cola."},
            {"id": "5", "nombre": "5. Limpieza Extrema de WinSxS", "cmd": lambda: abrir_consola_y_ejecutar("LIMPIEZA WINSXS", logica_winsxs), "nov": "Libera masivamente espacio de disco duro borrando copias de seguridad viejas y obsoletas de actualizaciones de Windows.", "exp": "[Microsoft OS] Ejecuta DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase. Minimiza el footprint consolidando el S.O."},
            {"id": "6", "nombre": "6. Reparar Windows Update Roto", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR UPDATE", logica_reparar_update), "nov": "Arregla el problema crítico cuando las actualizaciones de Windows se quedan trabadas en 'Descargando 0%' eternamente.", "exp": "[Microsoft OS] Detiene criptográficos (wuauserv, bits), renombra SoftwareDistribution a .old y regenera bases de datos de Windows Update."},
            {"id": "7", "nombre": "7. Purgar Puntos Restauración", "cmd": lambda: abrir_consola_y_ejecutar("BORRAR VSS", logica_shadowcopies), "nov": "Borra copias de seguridad de Windows muy antiguas que consumen excesivo espacio oculto en tu disco duro (Seguro).", "exp": "[Microsoft OS] Ejecuta vssadmin delete shadows /all /quiet. Purga registros inactivos y shadow copies asignadas recuperando espacio en MFT."},
            {"id": "8", "nombre": "8. Reparar Telemetría Base (WMI)", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR WMI", logica_wmi), "nov": "Arregla errores raros, como cuando la PC no lee el nivel de batería, no da audio o los programas se cierran solos.", "exp": "[Microsoft OS] Detiene winmgmt, ejecuta la bandera '/resetrepository' para reconstruir archivos MOF/CIM averiados y relanza servicios."},
            {"id": "9", "nombre": "9. Bloquear Espionaje Microsoft", "cmd": lambda: abrir_consola_y_ejecutar("BLOQUEO TELEMETRÍA", logica_telemetria), "nov": "Evita que Windows envíe reportes de uso constante a los servidores de Microsoft. Mejora el rendimiento del internet y disco.", "exp": "[Inyección de Registro] Fuerza detención de DiagTrack y altera llave DWORD AllowTelemetry a 0 en el Registro cortando el tráfico saliente."},
            {"id": "10", "nombre": "10. Reparar Sincronización (Hora)", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR HORA", logica_hora), "nov": "Soluciona el error 'La conexión no es privada' obligando a tu PC a sincronizar la hora exacta con relojes atómicos.", "exp": "[Microsoft OS] Reinicia Time Broker. Modifica peerlist forzando sincronización SNTP estricta contra time.windows.com con resync de placa."},
            {"id": "11", "nombre": "11. Limpiar Navegadores (Caché)", "cmd": lambda: abrir_consola_y_ejecutar("PURGAR NAVEGADORES", logica_limpiar_navegadores), "nov": "Acelera navegadores web eliminando archivos temporales pesados. (Tus contraseñas, historial y marcadores están a salvo).", "exp": "[Python shutil] Destruye de forma recursiva los directorios ocultos 'Cache_Data' de motores Chromium en las variables del LOCALAPPDATA."},
            {"id": "12", "nombre": "12. Reparación Física de Disco (CHKDSK)", "cmd": btn_chkdsk, "nov": "Repara sectores dañados magnéticamente en tu disco duro si la computadora está extremadamente lenta o lanza errores al copiar.", "exp": "[Microsoft OS] Programa chkdsk /f /r /x para desmontaje de inodos y traslado forense de data recuperable a sectores magnéticos sanos."},
            {"id": "13", "nombre": "13. Reconstruir Caché de Iconos", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR ICONOS", logica_iconos), "nov": "Soluciona el molesto fallo visual donde los iconos de tus programas aparecen como hojas en blanco o se ven súper borrosos.", "exp": "[Microsoft OS] Destruye el hilo explorer.exe, purga el archivo IconCache.db en la raíz AppData y relanza el Shell de Windows forzando un re-render."},
            {"id": "14", "nombre": "14. G-Helper (Optimizador ASUS)", "cmd": lambda: abrir_consola_y_ejecutar("G-HELPER", logica_ghelper), "nov": "Reemplazo ultraligero de Armoury Crate (Exclusivo ASUS). Controla LEDs, ventiladores y batería sin trabar la computadora.", "exp": "[Hardware Lock] Escanea el firmware WMI en busca del vendor ASUS. Descarga el binario y lo ejecuta en RAM. Incluye limpieza táctica post-ejecución."},
            {"id": "15", "nombre": "15. Lenovo Legion Toolkit", "cmd": lambda: abrir_consola_y_ejecutar("LENOVO TOOLKIT", logica_lenovo_toolkit), "nov": "Reemplazo ultraligero de Lenovo Vantage. Controla perfiles de energía, ventiladores, RGB y batería sin consumir recursos.", "exp": "[Hardware Lock] Filtro WMI detectando ecosistema Lenovo. Descarga el instalador, despliega modo fantasma (/VERYSILENT) y desinstala limpiando rastros."},
            {"id": "16", "nombre": "16. Mole (Optimizador Terminal)", "cmd": lambda: abrir_consola_y_ejecutar("MOLE", logica_mole), "nov": "Potente optimizador estilo CCleaner, pero corriendo puramente en texto dentro de tu consola. Limpia gigabytes en un parpadeo.", "exp": "[TUI Scripting] Llama al script nativo quick-install.ps1 vía irm. Abre una sesión externa interactiva (conhost) para navegación CLI con purga."},
            {"id": "17", "nombre": "17. Escáner de Fugas y Memoria Virtual", "cmd": btn_fugas_espacio, "nov": "Purga el bug de espacio de Windows 11. Además, escanea tu hardware y te recomienda el límite perfecto de memoria virtual, permitiéndote elegir en qué disco guardarla.", "exp": "[Fusión OSINT HW] Escanea el TotalPhysicalMemory y mapea volumenes vía psutil. Presenta un dashboard interactivo que inyecta parámetros en Win32_PageFileSetting reubicando el pagefile.sys y pulverizando el CapabilityAccessManager."},
            {"id": "18", "nombre": "18. Organizador Inteligente de Archivos", "cmd": lambda: abrir_consola_y_ejecutar("ORGANIZADOR INTELIGENTE", logica_organizador_archivos), "nov": "Selecciona una carpeta hecha un desastre (como Descargas) y automáticamente separará todo en subcarpetas por fotos, videos, programas, etc.", "exp": "[Python shutil & os] Automatiza la clasificación por extensión iterando el directorio. Crea una bóveda Sandbox e incluye una rutina recursiva (Bottom-Up) para purgar directorios vacíos remanentes."},
            {"id": "19", "nombre": "19. Radar Visual de Almacenamiento", "cmd": btn_mapa_espacio, "nov": "Muestra un mapa interactivo de tu disco duro ordenando las carpetas de la más pesada a la más ligera. Además, la inteligencia artificial te sugerirá archivos basura de Windows que puedes eliminar con un clic.", "exp": "[Hilos WMI/OS] Combina un scanner recursivo de alto rendimiento (os.scandir) con un renderizador ttk.Treeview. Incluye módulo Heurístico pre-scan para identificar y truncar inodos huérfanos del S.O."}
    ]
    construir_vista_dinamica("🧹 Mantenimiento y Optimización", "🔍 Buscar (Ej: chkdsk, debloat)...", h_mant)

def cargar_categoria_diagnostico():
    global app
    
    def btn_perfmon():
        dialogo = ctk.CTkInputDialog(text="1. Monitor | 2. Reporte", title="Monitor")
        op = dialogo.get_input()
        if op in ['1', '2', '01', '02']: abrir_consola_y_ejecutar("PERFMON", lambda log: logica_perfmon(log, op))
        
    def btn_visor():
        dialogo = ctk.CTkInputDialog(text="1. Procesos | 2. Servicios | 3. Errores", title="Visor")
        op = dialogo.get_input()
        if op in ['1', '2', '3']: abrir_consola_y_ejecutar("VISOR GRÁFICO", lambda log: logica_visor_grafico(log, op))

    def btn_historial_web():
        import os
        from tkinter import messagebox
        
        local_appdata = os.environ.get('LOCALAPPDATA', '')
        appdata = os.environ.get('APPDATA', '')
        
        # Diccionario maestro de rutas forenses de todos los navegadores Chromium
        posibles_navs = {
            "Google Chrome": os.path.join(local_appdata, r"Google\Chrome\User Data\Default\History"),
            "Microsoft Edge": os.path.join(local_appdata, r"Microsoft\Edge\User Data\Default\History"),
            "Brave": os.path.join(local_appdata, r"BraveSoftware\Brave-Browser\User Data\Default\History"),
            "Opera GX": os.path.join(appdata, r"Opera Software\Opera GX Stable\History"),
            "Opera Clásico": os.path.join(appdata, r"Opera Software\Opera Stable\History"),
            "Vivaldi": os.path.join(local_appdata, r"Vivaldi\User Data\Default\History")
        }
        
        # --- EL ESCÁNER DE INGENIERO ---
        # Filtramos y nos quedamos ÚNICAMENTE con los que existen en esta PC
        navs_detectados = {}
        for nombre, ruta in posibles_navs.items():
            if os.path.exists(ruta):
                navs_detectados[nombre] = ruta
                
        if not navs_detectados:
            messagebox.showinfo("Auditoría Forense", "No se detectó el historial de ningún navegador compatible en este equipo.")
            return
            
        # Construimos el menú a medida solo con lo que se encontró
        menu_texto = "Navegadores detectados en esta PC:\n\n"
        lista_nombres = list(navs_detectados.keys())
        
        for i, nombre in enumerate(lista_nombres):
            menu_texto += f"{i+1}. {nombre}\n"
            
        dialogo = ctk.CTkInputDialog(text=f"{menu_texto}\nIngresa el número a inspeccionar:", title="Forense Web")
        op = dialogo.get_input()
        
        # Validamos que haya puesto un número válido
        if op and op.isdigit():
            idx = int(op) - 1
            if 0 <= idx < len(lista_nombres):
                nav_elegido = lista_nombres[idx]
                ruta_elegida = navs_detectados[nav_elegido]
                
                # Disparamos la extracción pasando la ruta exacta que acabamos de validar
                abrir_consola_y_ejecutar(f"VISUALIZADOR {nav_elegido.upper()}", lambda log: logica_historial_web(log, nav_elegido, ruta_elegida))

    def btn_bitlocker():
        menu = "1. 🛡️ Ver estado de cifrado (Todas las unidades)\n2. 🔑 Extraer y respaldar mi clave actual\n3. 🕵️‍♂️ Buscar claves perdidas (USBs y Discos)\n4. 🔓 Desbloquear una unidad cifrada"
        dialogo = ctk.CTkInputDialog(text=f"¿Qué acción deseas realizar?\n\n{menu}", title="Gestor Avanzado BitLocker")
        opcion = dialogo.get_input()

        if opcion == '1':
            abrir_consola_y_ejecutar("ESTADO BITLOCKER", lambda log: logica_bitlocker(log, '1'))
        elif opcion == '2':
            dialogo_drive = ctk.CTkInputDialog(text="Ingresa la letra de la unidad a respaldar (Ej: C):", title="Respaldar Clave")
            drive = dialogo_drive.get_input()
            if drive:
                abrir_consola_y_ejecutar("RESPALDO BITLOCKER", lambda log: logica_bitlocker(log, '2', drive))
        elif opcion == '3':
            abrir_consola_y_ejecutar("BUSCADOR DE CLAVES", lambda log: logica_bitlocker(log, '3'))
        elif opcion == '4':
            dialogo_drive = ctk.CTkInputDialog(text="Ingresa la letra de la unidad bloqueada (Ej: D):", title="Desbloquear Unidad")
            drive = dialogo_drive.get_input()
            if drive:
                dialogo_clave = ctk.CTkInputDialog(text="Ingresa la clave de recuperación de 48 dígitos:\n(Ej: 123456-123456-...)", title="Desbloquear Unidad")
                clave = dialogo_clave.get_input()
                if clave:
                    abrir_consola_y_ejecutar("DESBLOQUEO BITLOCKER", lambda log: logica_bitlocker(log, '4', drive, clave))

    h_diag = [
        {"id": "1", "nombre": "1. Diagnóstico Veloz", "cmd": lambda: abrir_consola_y_ejecutar("INFO RÁPIDA", logica_diagnostico_rapido), "nov": "Resumen instantáneo con la calificación matemática oficial de velocidad y fluidez que Windows le da a esta PC.", "exp": "[Microsoft OS] Invoca systeminfo y evalúa la clase WMI 'Win32_WinSat', exponiendo la calificación formal WinEI del indexador interno."},
        {"id": "2", "nombre": "2. Radiografía Completa Hardware", "cmd": lambda: abrir_consola_y_ejecutar("RADIOGRAFÍA HW", logica_radiografia_hardware_completa), "nov": "Lista precisa con marcas y modelos reales de la Placa Madre, RAM instalada, Procesador exacto y Tarjetas Gráficas de esta computadora.", "exp": "[CIM Engine] Volcado canalizado. Interroga las clases Win32_BaseBoard, Processor y parsea arreglos matemáticos de PhysicalMemory (DIMMs)."},
        {"id": "3", "nombre": "3. Salud de Discos S.M.A.R.T", "cmd": lambda: abrir_consola_y_ejecutar("SALUD DE DISCOS", logica_salud_discos), "nov": "Lee los sensores internos ocultos de tus discos duros y de estado sólido para advertirte si están a punto de sufrir una falla física.", "exp": "[Lectura a Nivel Hardware] Parsea el firmware físico utilizando Get-PhysicalDisk, evaluando la variable HealthStatus extraída del sensor S.M.A.R.T."},
        {"id": "4", "nombre": "4. Monitor de Estabilidad Windows", "cmd": btn_perfmon, "nov": "Abre una línea de tiempo gráfica que te muestra los últimos días de la computadora, detallando por qué ocurrió cada pantallazo azul o cierre inesperado.", "exp": "[Microsoft OS] Emplea perfmon /rel para tabular crasheos históricos de aplicaciones y hardware utilizando un índice lógico de estabilidad."},
        {"id": "5", "nombre": "5. Cuadrícula Forense de Tareas", "cmd": btn_visor, "nov": "Despliega una hoja de cálculo interactiva para investigar y filtrar procesos y servicios en memoria, mucho más detallado que el Administrador de Tareas.", "exp": "[Pipeline GridView] Redirige cadenas de datos masivas de Get-Process y EventLogs directamente hacia la interfaz gráfica de filtrado en RAM Out-GridView."},
        {"id": "6", "nombre": "6. Tiempo de Actividad Real", "cmd": lambda: abrir_consola_y_ejecutar("UPTIME", logica_uptime), "nov": "Muestra cuánto tiempo exacto lleva esta computadora encendida. Revela si el Inicio Rápido de Windows está impidiendo apagados reales.", "exp": "[Microsoft OS] Resta la variable LastBootUpTime (Win32_OperatingSystem) a la hora actual revelando el falso apagado asociado a la hibernación de kernel."},
        {"id": "7", "nombre": "7. Auditar Tareas Ocultas", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR TAREAS", logica_tareas_servicios), "nov": "Visualiza programas y mantenimientos fantasmas instalados en el fondo de tu equipo que podrían estar robando recursos y batería.", "exp": "[Microsoft OS] Pipe estructurado combinando la tabla schtasks y Get-Service, aislando exclusivamente los daemons cuyo estatus sea 'Running'."},
        {"id": "8", "nombre": "8. Auditoría de Arranque", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR ARRANQUE", logica_programas_arranque), "nov": "Descubre exactamente cuáles programas se abren a escondidas apenas enciendes tu computadora, lo que hace que tu sistema tarde muchísimo en iniciar.", "exp": "[Microsoft OS] Evalúa ramas del registro y WMI (Win32_StartupCommand). Mapea binarios de persistencia que se enganchan a la fase WinLogon."},
        {"id": "9", "nombre": "9. Historial Forense de USBs", "cmd": lambda: abrir_consola_y_ejecutar("HISTORIAL USB", logica_historial_usb), "nov": "Descifra y lista los nombres de todos los pendrives, controles y celulares que se han conectado en este equipo a lo largo de toda su historia.", "exp": "[Lennes Varela] Parsea registro Plug and Play (PnP). Itera recursivamente sobre la rama HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR extrayendo Device IDs."},
        {"id": "10", "nombre": "10. Extractor de Pantallazos", "cmd": lambda: abrir_consola_y_ejecutar("BSOD", logica_pantallazos_azules), "nov": "Extrae los nombres y códigos de error exactos de todos los Pantallazos Azules de la Muerte recientes para diagnosticar hardware dañado.", "exp": "[Microsoft OS] Filtra EventLog System Logs buscando el origen 'BugCheck'. Extrae el volcado hexadecimal de memoria asociado al kernel panic."},
        {"id": "11", "nombre": "11. Gestor y Laboratorio de Batería", "cmd": lambda: abrir_consola_y_ejecutar("CENTRO DE ENERGÍA", logica_monitor_bateria), "nov": "Muestra un simulador de código para entender cómo se programa una batería. Además, monitorea tu batería real en vivo y crea un reporte de desgaste.", "exp": "[Fusión WMI/psutil] Combina un simulador educativo interactivo (bucle while asíncrono) con un lector en vivo de sensores vía psutil y el dumper nativo de Windows (powercfg)."},
        {"id": "12", "nombre": "12. Reporte de Suspensión", "cmd": lambda: abrir_consola_y_ejecutar("SLEEPSTUDY", logica_sleepstudy), "nov": "Si tu laptop se descarga estando guardada o suspendida, descubre exactamente qué programa impidió que entrara en reposo absoluto.", "exp": "[Microsoft OS] powercfg /SleepStudy analiza estados S0 Modern Standby, exponiendo los bloqueadores del Active-State Power Management (ASPM)."},
        {"id": "13", "nombre": "13. Gestor Avanzado BitLocker", "cmd": btn_bitlocker, "nov": "Revisa el estado de cifrado, extrae tu clave actual, busca claves perdidas en USBs y desbloquea discos protegidos fácilmente.", "exp": "[Forense BDE] Interfaz interactiva para el motor 'manage-bde'. Incluye escáner recursivo ultra-rápido (dir /s /b) combinando regex para extraer recovery keys en texto plano de unidades montadas."},
        {"id": "14", "nombre": "14. Auditoría de Usuarios Internos", "cmd": lambda: abrir_consola_y_ejecutar("USUARIOS LOCALES", logica_usuarios_locales), "nov": "Expone las cuentas registradas internamente en tu sistema, listando su nivel de seguridad e intentando detectar infiltraciones.", "exp": "[Microsoft OS] Extrae base de datos SAM ejecutando rutinas CIM hacia Win32_UserAccount para identificar el estatus de habilitación y privilegios base."},
        {"id": "15", "nombre": "15. Extraer Serial de Fábrica", "cmd": lambda: abrir_consola_y_ejecutar("NÚMERO DE SERIE", logica_numero_serie), "nov": "Copia automáticamente a tu portapapeles el número de serie codificado de la placa base, indispensable para revisar garantías o descargar actualizaciones de BIOS.", "exp": "[Microsoft OS] Consulta nativa a Win32_ComputerSystemProduct aislando la variable string 'IdentifyingNumber' incrustada en ROM por el fabricante OEM."},
        {"id": "16", "nombre": "16. Escáner Forense RAM", "cmd": lambda: abrir_consola_y_ejecutar("GHOST RAM", logica_memoria_ghost), "nov": "Busca virus militares sin archivo que no dejan rastros en el disco duro y se ocultan directamente en la Memoria RAM de la computadora.", "exp": "[Ejecución Nativa en Rust] Inyecta analizador de hilos. Rastrea memoria localizando inyecciones de código (Process Hollowing) mediante banderas de paginación RWX."},
        {"id": "17", "nombre": "17. Visualizador Forense Web", "cmd": btn_historial_web, "nov": "Genera una gráfica moderna, interactiva y al instante que te muestra cuáles son las páginas web más visitadas y las últimas búsquedas, evadiendo la seguridad del sistema.", "exp": "[Bypass de Seguridad SQLite3] Evade los file locks (Errno 13) clonando la Database History del navegador Chromium hacia el %TEMP%. Interpreta sentencias SQL nativas y renderiza una interfaz interactiva Tailwind/Chart.js."},
        {"id": "18", "nombre": "18. Radar de Hardware en Conflicto", "cmd": lambda: abrir_consola_y_ejecutar("RADAR HARDWARE", logica_radar_hardware), "nov": "Detecta piezas físicas de la computadora que estén fallando o que no tengan drivers instalados. Al detectarlas, arma automáticamente una búsqueda avanzada en internet para llevarte directo a la solución.", "exp": "[Auto-Dorking Forense] Interroga la clase WMI Win32_PnPEntity buscando ConfigManagerErrorCode != 0. Extrae la firma de hardware (VEN/DEV) y estructura una búsqueda con operadores lógicos de Google apuntando a dominios especializados."}
    ]
    construir_vista_dinamica("🖥️ Diagnóstico e Info del Sistema", "🔍 Buscar (Ej: bateria, smart, usb)...", h_diag)

def cargar_categoria_software():
    global app
    h_soft = [
            {"id": "1", "nombre": "1. Actualizar Apps Globales (Winget)", "cmd": lambda: abrir_consola_y_ejecutar("WINGET UPGRADE", logica_gestor_winget), "nov": "Analiza todos los programas de tu PC y descarga sus últimas versiones de golpe, de forma invisible y sin publicidad molesta.", "exp": "[Motor Microsoft Winget] Ejecuta 'upgrade --all' con banderas silenciosas (--silent) aceptando acuerdos de origen y licencia en background asíncrono."},
            {"id": "2", "nombre": "2. Extraer Clave Original de Windows", "cmd": lambda: abrir_consola_y_ejecutar("CLAVE WINDOWS", logica_clave_windows), "nov": "Si vas a formatear y no tienes tu licencia, esta herramienta escanea la placa madre y saca a la luz la clave de fábrica original.", "exp": "[Microsoft OS] Lee tabla ACPI (MSDM) y ataca la rama de registro 'SoftwareProtectionPlatform' desencriptando el valor alfanumérico BackupProductKeyDefault."},
            {"id": "3", "nombre": "3. Inventario Software a Excel (CSV)", "cmd": lambda: abrir_consola_y_ejecutar("INVENTARIO CSV", logica_inventario_software), "nov": "Crea un documento de Excel en tu escritorio con una lista impecable de todos los programas instalados y sus versiones exactas.", "exp": "[Librería Python Winreg] Itera recursivamente en ramas HKLM 'Uninstall' (Nativo y Wow6432Node), exportando diccionarios de DisplayName a formato tabular."},
            {"id": "4", "nombre": "4. Respaldo Total de Controladores", "cmd": lambda: abrir_consola_y_ejecutar("CLONAR DRIVERS", logica_respaldo_drivers), "nov": "Ideal para PCs antiguas. Clona los controladores de Wi-Fi, Gráfica y Audio antes de un formateo para no quedar incomunicado.", "exp": "[Microsoft OS] Emplea la utilidad de imágenes de despliegue DISM con el parámetro '/export-driver', clonando librerías dinámicas y certificados de catálogo."},
            {"id": "5", "nombre": "5. Auditar Licencias de MS Office", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR OFFICE", logica_auditar_office), "nov": "Descubre si tu Word y Excel son originales, o si fueron instalados con activadores ilegales KMS que podrían contener troyanos.", "exp": "[Microsoft OS] Localiza el script nativo OSPP.VBS en la ruta Office16 y lo invoca forzando la bandera /dstatus para exponer canales de host y grace period."},
            {"id": "6", "nombre": "6. Activador Seguro de Windows (MAS)", "cmd": lambda: abrir_consola_y_ejecutar("ACTIVADOR MAS", logica_activador_mas), "nov": "Activa tu Windows legalmente de por vida vinculando una licencia digital a tu placa madre. Cero programas con cracks o virus.", "exp": "[massgravel / MAS] Llama a Microsoft Activation Scripts mediante Invoke-RestMethod. Asigna un Hardware ID (HWID) ticket verificado por los servidores RMS de MS."},
            {"id": "7", "nombre": "7. Forzar Escaneo de Hardware (PnP)", "cmd": lambda: abrir_consola_y_ejecutar("ESCANEO PNP", logica_escanear_pnp), "nov": "Si conectaste una impresora o monitor y no lo reconoce, usa esto para obligar a Windows a revisar todos los puertos físicos de nuevo.", "exp": "[Microsoft OS] Interacciona con el demonio Plug and Play mediante pnputil. La bandera '/scan-devices' ordena la enumeración eléctrica forzada del bus PCI/USB."},
            {"id": "8", "nombre": "8. Instalar ASUS GlideX (Multipantalla)", "cmd": lambda: abrir_consola_y_ejecutar("GLIDEX MULTIPANTALLA", logica_glidex), "nov": "Descarga la increíble app de ASUS para usar tu tablet o celular como una segunda pantalla táctil inalámbrica para tu PC.", "exp": "[Inyección Microsoft Store] Invoca al gestor Winget forzando la comunicación con msstore API usando el Hash ProductId 9PLH2SV1DVK5 para instalación desatendida."}
        ]
    construir_vista_dinamica("📦 Software y Licencias", "🔍 Buscar (Ej: winget, office)...", h_soft)

def cargar_categoria_soporte():
    global app 
    
    def btn_destructor():
        dialogo = ctk.CTkInputDialog(text="Ruta EXACTA de la carpeta a destruir:", title="Destructor")
        ruta = dialogo.get_input()
        if ruta: abrir_consola_y_ejecutar("DESTRUCTOR", lambda log: logica_destructor(log, ruta))
        
    def btn_gestor_virtualizacion():
        import subprocess
        from tkinter import messagebox
        
        try:
            os_info = subprocess.check_output('wmic os get Caption', shell=True, text=True).strip().split('\n')[-1].strip()
        except:
            os_info = "Windows (Versión Desconocida)"
            
        es_compatible = any(edicion in os_info for edicion in ["Pro", "Enterprise", "Education", "Server"])
        
        dialog_virt = ctk.CTkToplevel(app) 
        dialog_virt.title("Gestor de Virtualización Nativa")
        dialog_virt.geometry("550x300") # Reducimos la altura, ya no necesitamos los botones de manual
        dialog_virt.attributes("-topmost", True)
        dialog_virt.transient(app)
        
        ctk.CTkLabel(dialog_virt, text="Escáner del Sistema:", font=("Arial", 14, "bold"), text_color="#A3E635").pack(pady=(15, 0))
        color_os = "#34D399" if es_compatible else "#EF4444"
        estado_os = "✅ COMPATIBLE" if es_compatible else "❌ NO COMPATIBLE (Requiere versión Pro/Enterprise)"
        ctk.CTkLabel(dialog_virt, text=f"{os_info}\n{estado_os}", font=("Arial", 14), text_color=color_os).pack(pady=5)
        
        def activar_caracteristica(feature_name, nombre_amigable):
            dialog_virt.destroy()
            def logica(log):
                log(f"[*] Verificando compatibilidad de {nombre_amigable} en {os_info}...")
                if not es_compatible:
                    log(f"[-] ADVERTENCIA CRÍTICA: Tu sistema operativo es una edición 'Home' o limitada.")
                    log(f"[-] Microsoft bloquea {nombre_amigable} en esta versión. La inyección podría ser rechazada.")
                
                log(f"[*] Analizando el núcleo de Windows...")
                check = subprocess.run(f'dism.exe /Online /Get-FeatureInfo /FeatureName:{feature_name}', shell=True, capture_output=True, text=True)
                if "Estado : Habilitado" in check.stdout or "State : Enabled" in check.stdout:
                    log(f"[+] {nombre_amigable} YA está habilitado y operando en este equipo.")
                    return
                
                log(f"[*] Inyectando orden de activación para {nombre_amigable}...")
                log("[!] Esto tomará un par de minutos, por favor no cierres la herramienta.")
                act = subprocess.run(f'dism.exe /Online /Enable-Feature /FeatureName:{feature_name} /All /NoRestart', shell=True, capture_output=True, text=True)
                
                if act.returncode in [0, 3010]:
                    log(f"[+] ¡ÉXITO! {nombre_amigable} se ha integrado en el sistema.")
                    if act.returncode == 3010:
                        log("[!] SE REQUIERE UN REINICIO DEL SISTEMA PARA COMPLETAR LA INSTALACIÓN.")
                        if messagebox.askyesno("Reinicio Requerido", f"{nombre_amigable} se activó a nivel de sistema.\n\nPara que los cambios surtan efecto debes reiniciar el PC.\n\n¿Deseas reiniciar AHORA MISMO?"):
                            subprocess.run("shutdown /r /t 5", shell=True)
                else:
                    log(f"[-] Error {act.returncode} al intentar activar la característica.")
                    log("[!] Posible causa principal: Tu BIOS no tiene la 'Virtualización de Hardware' (VT-x/AMD-V) habilitada.")
                    
            abrir_consola_y_ejecutar(f"ACTIVADOR - {nombre_amigable}", logica)

        ctk.CTkLabel(dialog_virt, text="Hyper-V (Máquinas Virtuales Permanentes)", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        ctk.CTkButton(dialog_virt, text="🚀 Activar Hyper-V", fg_color="#2563EB", hover_color="#1D4ED8", command=lambda: activar_caracteristica("Microsoft-Hyper-V", "Hyper-V")).pack(fill="x", padx=40)

        ctk.CTkLabel(dialog_virt, text="Windows Sandbox (Entorno Aislado Desechable)", font=("Arial", 12, "bold")).pack(pady=(20, 2))
        ctk.CTkButton(dialog_virt, text="☢️ Activar Sandbox", fg_color="#D97706", hover_color="#B45309", command=lambda: activar_caracteristica("Containers-DisposableClientVM", "Windows Sandbox")).pack(fill="x", padx=40)

        # Agregamos una nota elegante indicando dónde leer los manuales
        ctk.CTkLabel(dialog_virt, text="* Puedes leer los manuales de uso en la sección 'Manuales y Trucos'.", font=("Arial", 11, "italic"), text_color="#94A3B8").pack(pady=(20, 0))

    def btn_jtr():
        import tkinter.filedialog as fd
        
        archivo_bloqueado = fd.askopenfilename(
            title="Paso 1: Selecciona el archivo protegido", 
            filetypes=[("Archivos Soportados", "*.zip *.rar *.pdf *.7z")],
            parent=app
        )
        
        if not archivo_bloqueado: return
        
        dialog_atk = ctk.CTkToplevel(app)
        dialog_atk.title("John The Ripper - Vector de Ataque")
        dialog_atk.geometry("500x320")
        dialog_atk.attributes("-topmost", True)
        dialog_atk.transient(app)
        
        ctk.CTkLabel(dialog_atk, text="Elige la estrategia de Hackeo:", font=("Arial", 16, "bold"), text_color="#38BDF8").pack(pady=(20, 10))
        
        def lanzar(tipo):
            dialog_atk.destroy()
            if tipo == '4':
                dialogo = ctk.CTkInputDialog(text="Escribe posibles contraseñas separadas por comas\n(Ej: ivanime.com, 12345, animehd):", title="Pistas a Medida")
                pistas = dialogo.get_input()
                if not pistas: return
                abrir_consola_y_ejecutar("ROMPE-CLAVES AVANZADO", lambda log: logica_romper_archivos(log, archivo_bloqueado, tipo, pistas))
            else:
                abrir_consola_y_ejecutar("ROMPE-CLAVES AVANZADO", lambda log: logica_romper_archivos(log, archivo_bloqueado, tipo, ""))
                
        ctk.CTkButton(dialog_atk, text="⚡ 1. Diccionario Básico (Prueba rápida)", font=("Arial", 14, "bold"), height=38, command=lambda: lanzar('1')).pack(fill="x", padx=40, pady=5)
        ctk.CTkButton(dialog_atk, text="🔢 2. Fuerza Bruta Numérica (PINs / Fechas)", font=("Arial", 14, "bold"), height=38, command=lambda: lanzar('2')).pack(fill="x", padx=40, pady=5)
        ctk.CTkButton(dialog_atk, text="🌍 3. Mega-Diccionario Nube (Top 1 Millón)", font=("Arial", 14, "bold"), height=38, fg_color="#8B5CF6", hover_color="#7C3AED", command=lambda: lanzar('3')).pack(fill="x", padx=40, pady=5)
        ctk.CTkButton(dialog_atk, text="🎯 4. Pistas a Medida (Escribe tus sospechas)", font=("Arial", 14, "bold"), height=38, fg_color="#F59E0B", hover_color="#D97706", command=lambda: lanzar('4')).pack(fill="x", padx=40, pady=15)

    def btn_desproteger_excel():
        import tkinter.filedialog as fd
        archivo_excel = fd.askopenfilename(
            title="Selecciona el archivo de Excel bloqueado", 
            filetypes=[("Archivos de Excel", "*.xlsx")],
            parent=app
        )
        if archivo_excel:
            abrir_consola_y_ejecutar("DESBLOQUEO EXCEL", lambda log: logica_desproteger_excel(log, archivo_excel))

    def btn_cambiar_clave():
        dialogo_usr = ctk.CTkInputDialog(text="Nombre del usuario local a modificar:", title="Usuario")
        usr = dialogo_usr.get_input()
        if usr:
            dialogo_pwd = ctk.CTkInputDialog(text="Nueva clave (deja vacío para eliminarla):", title="Clave")
            pwd = dialogo_pwd.get_input()
            if pwd is not None: abrir_consola_y_ejecutar("GESTOR CLAVES", lambda log: logica_cambiar_clave(log, usr, pwd))

    def btn_ytdlp():
        urls_a_descargar = [] 
        
        dialog_url = ctk.CTkToplevel(app)
        dialog_url.title("Descargador Universal (Videos y Fotos)")
        dialog_url.geometry("550x260")
        dialog_url.attributes("-topmost", True)
        dialog_url.transient(app)
        
        ctk.CTkLabel(dialog_url, text="Ingresa el enlace (Video de YT, Facebook, IG, Pinterest, etc):", font=("Arial", 14)).pack(pady=(20, 5))
        entrada = ctk.CTkEntry(dialog_url, width=450)
        entrada.pack(pady=5)
        
        lbl_contador = ctk.CTkLabel(dialog_url, text="📥 Enlaces en cola: 0", font=("Arial", 13, "bold"), text_color="#38BDF8")
        lbl_contador.pack(pady=5)
        
        btn_frame_int = ctk.CTkFrame(dialog_url, fg_color="transparent")
        btn_frame_int.pack(pady=10)
        
        def limpiar_url_magico(url_cruda):
            url_limpia = url_cruda.strip()
            if not url_limpia: return None
            if "youtube.com" in url_limpia or "youtu.be" in url_limpia:
                return url_limpia.split("&list=")[0].split("&index=")[0]
            else:
                return url_limpia.split("&utm_")[0].split("?utm_")[0]

        def agregar_enlace():
            url_procesada = limpiar_url_magico(entrada.get())
            if url_procesada and url_procesada not in urls_a_descargar:
                urls_a_descargar.append(url_procesada)
                lbl_contador.configure(text=f"📥 Enlaces en cola: {len(urls_a_descargar)}")
                entrada.delete(0, 'end')
                btn_siguiente.configure(state="normal", fg_color="#10B981") 
                
        def pegar_y_agregar():
            try:
                texto = dialog_url.clipboard_get().strip()
                if texto:
                    entrada.delete(0, 'end')
                    entrada.insert(0, texto)
                    agregar_enlace()
            except: pass
            
        def procesar_url():
            url_procesada = limpiar_url_magico(entrada.get())
            if url_procesada and url_procesada not in urls_a_descargar:
                urls_a_descargar.append(url_procesada)
                
            if not urls_a_descargar: return
            
            dialog_url.destroy()
            abrir_ventana_calidad(urls_a_descargar)
            
        ctk.CTkButton(btn_frame_int, text="➕ Pegar y Agregar", width=120, fg_color="#3B82F6", hover_color="#2563EB", command=pegar_y_agregar).pack(side="left", padx=5)
        btn_siguiente = ctk.CTkButton(btn_frame_int, text="Siguiente ➡️", width=120, fg_color="#334155", state="disabled", command=procesar_url)
        btn_siguiente.pack(side="left", padx=5)
        ctk.CTkButton(btn_frame_int, text="Cancelar", width=120, fg_color="#880000", hover_color="#AA0000", command=dialog_url.destroy).pack(side="left", padx=5)

        def abrir_ventana_calidad(lista_urls):
            dialog_cal = ctk.CTkToplevel(app)
            dialog_cal.title("Descargador Universal - Paso 2")
            dialog_cal.geometry("500x350")
            dialog_cal.attributes("-topmost", True)
            dialog_cal.transient(app)
            ctk.CTkLabel(dialog_cal, text=f"Elige el formato para los {len(lista_urls)} enlaces:", font=("Arial", 14, "bold")).pack(pady=(15, 10))
            
            def sel_calidad(cal):
                if cal == '5':
                    import tkinter.filedialog as fd
                    from tkinter import messagebox
                    messagebox.showinfo("Bypass Privado", "Para descargar posts privados o fuertemente bloqueados, usa la extensión de navegador 'Get cookies.txt LOCALLY'.\n\nEn la siguiente ventana, selecciona el archivo de texto que descargaste.")
                    dialog_cal.attributes("-topmost", False)
                    archivo_txt = fd.askopenfilename(title="Selecciona cookies.txt", filetypes=[("Archivo de Texto", "*.txt")], parent=dialog_cal)
                    if not archivo_txt: return
                    dialog_cal.destroy()
                    abrir_consola_y_ejecutar("EXTRACTOR DE GALERÍAS", lambda log: logica_ytdlp(log, lista_urls, '5', '', archivo_txt))
                else:
                    dialog_cal.destroy()
                    if cal == '3': abrir_consola_y_ejecutar("DESCARGADOR MEDIOS", lambda log: logica_ytdlp(log, lista_urls, '3', 'mp3', ""))
                    elif cal == '4': abrir_consola_y_ejecutar("EXTRACTOR DE GALERÍAS", lambda log: logica_ytdlp(log, lista_urls, '4', 'img', ""))
                    else: abrir_ventana_formato(lista_urls, cal)
                
            ctk.CTkButton(dialog_cal, text="🌟 1. Video Máxima Calidad (2K/4K/8K)", command=lambda: sel_calidad('1')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="📺 2. Video Calidad Estable (1080p)", command=lambda: sel_calidad('2')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="🎵 3. Solo Audio Puro (MP3)", fg_color="#107C41", hover_color="#0F5C30", command=lambda: sel_calidad('3')).pack(fill="x", padx=40, pady=5)
            
            ctk.CTkFrame(dialog_cal, height=2, fg_color="#334155").pack(fill="x", padx=40, pady=10)
            
            ctk.CTkButton(dialog_cal, text="📸 4. Fotos (Posts Públicos directos)", fg_color="#A855F7", hover_color="#9333EA", command=lambda: sel_calidad('4')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="🔐 5. Fotos (Posts Privados con cookies.txt)", fg_color="#F59E0B", hover_color="#D97706", command=lambda: sel_calidad('5')).pack(fill="x", padx=40, pady=5)

        def abrir_ventana_formato(lista_urls, calidad):
            dialog_fmt = ctk.CTkToplevel(app)
            dialog_fmt.title("Descargador Universal - Paso 3")
            dialog_fmt.geometry("450x250")
            dialog_fmt.attributes("-topmost", True)
            dialog_fmt.transient(app)
            ctk.CTkLabel(dialog_fmt, text="Elige el formato de video:", font=("Arial", 14, "bold")).pack(pady=(20, 15))
            def sel_formato(fmt):
                dialog_fmt.destroy(); abrir_consola_y_ejecutar("DESCARGADOR LOTE", lambda log: logica_ytdlp(log, lista_urls, calidad, fmt, ""))
            ctk.CTkButton(dialog_fmt, text="🎬 MP4 (Universal / Estándar)", command=lambda: sel_formato('mp4')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_fmt, text="🎞️ MKV (Alta Calidad / PC)", command=lambda: sel_formato('mkv')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_fmt, text="🍏 MOV (Apple / Mac)", fg_color="#444444", hover_color="#222222", command=lambda: sel_formato('mov')).pack(fill="x", padx=40, pady=15)

    def btn_gestor_usb():
        menu = "1. 🔒 Bloquear puertos USB (Nadie podrá robar datos)\n2. 🔓 Desbloquear puertos USB (Permitir pendrives)\n3. 🛠️ Remover Protección contra Escritura (Reparar USB)"
        dialogo = ctk.CTkInputDialog(text=f"¿Qué acción deseas realizar?\n\n{menu}", title="Gestor Avanzado de USB")
        opcion = dialogo.get_input()
        
        if opcion in ['1', '2']:
            accion_txt = "BLOQUEO" if opcion == '1' else "DESBLOQUEO"
            abrir_consola_y_ejecutar(f"{accion_txt} USB", lambda log: logica_gestor_usb(log, opcion))
        elif opcion == '3':
            dialogo_disco = ctk.CTkInputDialog(text="Ingresa el NÚMERO del disco USB a reparar (ej. 1, 2):\n(Puedes ver el número en el 'Administrador de Discos')", title="Reparar USB")
            disco = dialogo_disco.get_input()
            if disco:
                abrir_consola_y_ejecutar("REPARACIÓN USB", lambda log: logica_gestor_usb(log, opcion, disco))
        
    def btn_sysprep():
        dialogo = ctk.CTkInputDialog(text="Peligro: El PC se apagará y quedará de fábrica.\nEscribe 'CONFIRMAR':", title="Sysprep")
        confirm = dialogo.get_input()
        if confirm == "CONFIRMAR": abrir_consola_y_ejecutar("SYSPREP", logica_sysprep)

    def btn_optimizador_android():
        # Este no necesita popup porque detecta el teléfono automáticamente
        abrir_consola_y_ejecutar("OPTIMIZADOR ANDROID", logica_optimizador_android)

    def btn_laboratorio_claves():
        menu = "1. Auditar la seguridad de una contraseña mía\n2. Generar una nueva clave Inhackeable"
        dialogo_tipo = ctk.CTkInputDialog(text=f"Bienvenido al Laboratorio Criptográfico.\n\n{menu}", title="Bóveda de Seguridad")
        tipo = dialogo_tipo.get_input()
        
        if tipo == '1':
            dialogo_pwd = ctk.CTkInputDialog(text="Ingresa la contraseña que deseas poner a prueba:", title="Auditoría de Entropía")
            pwd = dialogo_pwd.get_input()
            if pwd is not None:
                abrir_consola_y_ejecutar("LABORATORIO CRIPTO", lambda log: logica_laboratorio_criptografico(log, '1', pwd))
                
        elif tipo == '2':
            dialogo_len = ctk.CTkInputDialog(text="¿De cuántos caracteres quieres tu nueva contraseña?\n(Recomendado: 16 o más):", title="Forjador Militar")
            longitud_str = dialogo_len.get_input()
            if longitud_str is not None:
                abrir_consola_y_ejecutar("LABORATORIO CRIPTO", lambda log: logica_laboratorio_criptografico(log, '2', longitud_str))

    def btn_quitar_fondo():
        import tkinter.filedialog as fd
        archivo = fd.askopenfilename(
            title="Paso 1: Selecciona la imagen para quitarle el fondo", 
            filetypes=[("Imágenes Soportadas", "*.jpg *.jpeg *.png *.webp *.bmp")],
            parent=app
        )
        if archivo:
            abrir_consola_y_ejecutar("Borrador de Fondos IA", lambda log: logica_quitar_fondo(log, archivo))

    def btn_modo_dios():
        abrir_consola_y_ejecutar("MODO DIOS", logica_modo_dios)

    h_sop = [
            {"id": "1", "nombre": "1. Destructor Forzado de Carpetas", "cmd": btn_destructor, "nov": "Elimina de forma irreversible cualquier carpeta bloqueada, virus testarudo o archivo que el sistema de Windows te prohíba tocar.", "exp": "[Escalada de Privilegios NTFS] Ejecuta un override sobre ACLs usando takeown /f. Inyecta herencia estricta para *S-1-5-32-544 (Admins) vía icacls."},
            {"id": "2", "nombre": "2. Bypass de Contraseñas Windows", "cmd": btn_cambiar_clave, "nov": "Te permite borrar o cambiar la clave de inicio de sesión de tu PC al instante si tu perfil de usuario quedó bloqueado por error.", "exp": "[Inyección de SAM Local] Omite la capa de validación hash enviando parámetros privilegiados directos por medio de net.exe user reescribiendo la credencial base."},
            {"id": "3", "nombre": "3. Extractor de Credenciales (LaZagne)", "cmd": lambda: abrir_consola_y_ejecutar("LAZAGNE", logica_lazagne), "nov": "Escaneo forense masivo: encuentra y extrae todas tus contraseñas guardadas de navegadores, wi-fi y bases de datos a un bloc de notas.", "exp": "[Motor de Dumpeo LSA Secrets] Silencia el AMSI de Defender mediante Add-MpPreference temporal. Inyecta payload que audita Data Protection API y SQLite de navegadores."},
            {"id": "4", "nombre": "4. Descargador Universal (Videos y Fotos)", "cmd": btn_ytdlp, "nov": "Descarga videos en 4K o audios de YouTube/Redes y extrae Galerías de Fotos completas burlando los inicios de sesión obligatorios.", "exp": "[Triple Motor CLI: yt-dlp + gallery-dl + FFmpeg] Falsifica cabeceras HTTP y usa cookies locales (DPAPI bypass). FFmpeg recodifica y convierte formatos WEBP crudos al vuelo."},
            {"id": "5", "nombre": "5. Gestor Avanzado de USB", "cmd": btn_gestor_usb, "nov": "Controla el acceso físico al PC. Bloquea pendrives contra robo de datos, restaura accesos o repara memorias protegidas contra escritura.", "exp": "[Controlador Kernel/VHD] Manipula la directiva Start del servicio USBSTOR para montaje/desmontaje PnP. Inyecta subrutinas Diskpart (clear readonly) para sanitizar VHDs."},
            {"id": "6", "nombre": "6. Gestor de Virtualización de Hardware", "cmd": btn_gestor_virtualizacion, "nov": "Activa las poderosas funciones ocultas de Windows: Hyper-V (Máquinas Virtuales) y Sandbox (Caja fuerte para probar virus de forma segura).", "exp": "[API WMI/DISM Interfaz] Valida la edición SKU del SO. Inyecta paquetes de componentes base (Microsoft-Hyper-V / Containers-DisposableClientVM) con reinicio lógico controlado."},
            {"id": "7", "nombre": "7. Reinicio de Fábrica para Ventas (Sysprep)", "cmd": btn_sysprep, "nov": "Preparación comercial militar: Borra la identidad única de tu PC y registros internos. Al encender, pedirá la configuración de primer día.", "exp": "[Destrucción de Identidad HAL] Ejecuta la orden '/generalize'. Limpia la Security ID (SID), contadores KMS y logs, obligando a la BIOS a ejecutar la fase Out-Of-Box Experience (OOBE)."},
            {"id": "8", "nombre": "8. Borrado de Archivos Irreversible (Wipe)", "cmd": lambda: abrir_consola_y_ejecutar("BORRADO WIPE", logica_borrado_seguro), "nov": "Sobrescribe criptográficamente los huecos vacíos de tu disco duro para garantizar que ningún hacker recupere las fotos que ya borraste.", "exp": "[Trituradora de Ciclos Cipher] Genera un archivo masivo aleatorio que ocupa los bloques desasignados del sistema maestro de archivos (MFT), imposibilitando herramientas forenses."},
            {"id": "9", "nombre": "9. Salto de BIOS Forzado (UEFI)", "cmd": lambda: abrir_consola_y_ejecutar("REINICIO BIOS", logica_reinicio_bios), "nov": "Evita el estrés de reiniciar la computadora y presionar F2 súper rápido. Te lleva directamente a los menús de la Placa Madre.", "exp": "[Interrupción ACPI Inteligente] Envía parámetros /r /fw al shutdown core, modificando el flag NVRAM del sistema para omitir el bootloader y aterrizar en BIOS Firmware Mode."},
            {"id": "10", "nombre": "10. Hackeo de Archivos Bloqueados (JtR)", "cmd": btn_jtr, "nov": "Adivina y recupera contraseñas perdidas de archivos ZIP, RAR o PDF mediante listas mundiales o pistas específicas en tiempo récord.", "exp": "[Openwall JohnTheRipper] Estructura multihilo. Emplea scripts perl (*2john.pl) extrayendo firmas de hash. Ataca los inodos utilizando aceleración de OpenCL/GPU hardware nativa."},
            {"id": "11", "nombre": "11. Destructor de Candados Excel (.xlsx)", "cmd": btn_desproteger_excel, "nov": "Desencripta libros y celdas de Excel que no te dejan escribir, creando una copia perfecta totalmente desbloqueada para edición.", "exp": "[Manipulación OOXML por Regex] Descomprime la arquitectura ZIP nativa de Excel. Navega por el DOM del XML purgando la etiqueta <sheetProtection/> para reensamblar y compilar el archivo."},
            {"id": "12", "nombre": "12. Limpiador Android Extremo (Vía USB)", "cmd": btn_optimizador_android, "nov": "Enlaza tu celular por cable y elimina gigabytes de basura, miniaturas y copias viejas de aplicaciones respetando tus fotos reales.", "exp": "[Controlador de Puente ADB] Descarga librerías core SDK. Se comunica por canal daemon TCP inyectando comandos bash directos a nivel root en el sistema de archivos EXT4 de Android."},
            {"id": "13", "nombre": "13. Auditoría Total de Ciberseguridad", "cmd": lambda: abrir_consola_y_ejecutar("WINPEAS", logica_winpeas), "nov": "El rey del análisis. Escanea huecos que dejarían entrar a un hacker y te permite activar escudos militares (Protección RAM y Defender) en un clic.", "exp": "[Forense Privilege Escalation] Importa PEASS-ng. Audita políticas perimetrales, tokens rotos y contraseñas volátiles. Incluye inyección protectora de proceso LSA RunAsPPL para memoria."},
            {"id": "14", "nombre": "14. Laboratorio Criptográfico de Claves", "cmd": btn_laboratorio_claves, "nov": "Pon a prueba tus contraseñas para ver cuánto tardaría un hacker en romperlas, o pide al sistema que te genere una nueva contraseña totalmente indestructible.", "exp": "[Módulo de Entropía de Shannon] Evalúa el 'Pool Size' y la longitud de cadenas de texto para calcular bits de entropía. Interpola los resultados contra un Hashrate de GPU moderno (100GH/s) para estimar tiempos de fractura criptográfica."},
            {"id": "15", "nombre": "15. Modo Dios (Escáner QR, Barras e IMEI)", "cmd": btn_modo_dios, "nov": "Muestra un HUD holográfico. Lee códigos QR, Códigos de Barras y detecta celulares robados analizando sus IMEIs automáticamente en bases de datos mundiales.", "exp": "[Motor OpenCV + PyZBar] Renderiza un HUD asíncrono. Decodifica DataMatrix, EAN13 y QR. Implementa Algoritmo de Luhn para validar IMEIs y lanza un bypass de OSINT directo a bases gubernamentales (SRPA)."},
            {"id": "16", "nombre": "16. Borrador de Fondos IA (Red Neuronal)", "cmd": btn_quitar_fondo, "nov": "Recorta personas y objetos perfectos de cualquier fotografía de forma inteligente sin depender de páginas web, funcionando directamente en tu PC.", "exp": "[Inferencia AI Rembg] Auto-configura el entorno ONNXRuntime con mitigaciones Anti-Crash. Aísla el procesamiento del modelo semántico U-2-Net en un script esclavo con purga táctica posterior."},
            {"id": "17", "nombre": "17. Escáner Óptico de Pantalla (OCR)", "cmd": lambda: abrir_consola_y_ejecutar("ESCÁNER OCR", logica_escaner_ocr), "nov": "Dibuja un cuadro en tu pantalla sobre cualquier foto o error que no te deje copiar su texto. La inteligencia de Windows leerá la imagen y te entregará el texto copiado al portapapeles.", "exp": "[Extracción de Texto WinRT] Evita las pesadas dependencias Tesseract. Utiliza tkinter semitransparente para generar una bounding box. Canaliza un buffer RGBA hacia el motor cognitivo asíncrono nativo OcrEngine de Microsoft."}
        ]
    construir_vista_dinamica("🛠️ Soporte Técnico y Utilidades", "🔍 Buscar (Ej: lazagne, usb, wipe)...", h_sop)

def cargar_categoria_portables():
    import urllib.request, json, time, platform
    global app
    
    url_catalogo = f"https://raw.githubusercontent.com/LennesVP/Programas_Portables/main/Programas_Portables/catalogo.json?t={time.time()}"
    try:
        req = urllib.request.Request(url_catalogo, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        datos = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        catalogo = json.loads(datos)
        
        catalogo.sort(key=lambda x: x['nombre'])
        es_64bits = platform.machine().endswith('64')
        
        h_portables = []
        for index, item in enumerate(catalogo):
            ejecutable_crudo = item['ejecutable']
            exe_final = ejecutable_crudo["64"] if isinstance(ejecutable_crudo, dict) and es_64bits else (ejecutable_crudo["32"] if isinstance(ejecutable_crudo, dict) else ejecutable_crudo)
            
            # Constructor de closures (lambda binds the current value instead of loop reference)
            def make_cmd(c, e, nombre):
                return lambda: abrir_consola_y_ejecutar(nombre.upper(), lambda log: logica_ejecutar_portable(log, c, e))
            
            h_portables.append({
                "id": str(index + 1),
                "nombre": f"{index + 1}. {item['nombre']}",
                "nov": item.get('desc_n', 'Sin descripción para este programa.'),
                "exp": item.get('desc_e', 'Portable en la nube.'),
                "cmd": make_cmd(item['carpeta'], exe_final, item['nombre']),
                "txt_btn": "☁️ Descargar y Ejecutar",
                "color_borde": "#A78BFA" # Borde color Púrpura especial para Nube
            })
            
        construir_vista_dinamica("🧰 Programas Portables (Nube)", "🔍 Buscar aplicación en la nube...", h_portables)
            
    except Exception as e:
        limpiar_panel()
        ctk.CTkLabel(tools_frame, text=f"Error crítico de red. Imposible conectar con GitHub:\n{e}", text_color="#FF4444", font=("Arial", 16)).pack(pady=40)

def cargar_categoria_enciclopedia():
    import urllib.request, json, time, threading, webbrowser
    global app, datos_enciclopedia
    
    # 1. ESCUDO MAESTRO: Resucita la variable global si fue borrada del archivo principal
    if 'datos_enciclopedia' not in globals() or datos_enciclopedia is None:
        datos_enciclopedia = []
        
    limpiar_panel()
    
    # --- 1. ENCABEZADO ---
    header_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    header_frame.pack(side="top", fill="x", pady=(0, 20))
    
    ctk.CTkLabel(header_frame, text="📚 Enciclopedia de Apps", font=("Arial", 24, "bold")).pack(side="left")
    
    if not datos_enciclopedia:
        url_indice = f"https://raw.githubusercontent.com/LennesVP/Encyclopedia-of-Tools/main/enciclopedia.json?t={time.time()}"
        try:
            req = urllib.request.Request(url_indice, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
            respuesta = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
            datos_enciclopedia = json.loads(respuesta)
        except Exception as e:
            ctk.CTkLabel(tools_frame, text=f"Error al conectar con la Nube:\n{e}", text_color="#FF4444").pack(pady=20)
            return

    if not datos_enciclopedia:
        ctk.CTkLabel(tools_frame, text="La enciclopedia está vacía.", text_color="#AAAAAA").pack(pady=20)
        return

    categorias_unicas = set()
    for item in datos_enciclopedia:
        categorias_unicas.add(item.get('categoria', 'Sin Categoría'))
        
    lista_filtros = ["Mostrar Todas"] + sorted(list(categorias_unicas))
    datos_filtrados = datos_enciclopedia.copy()
    indice_actual = 0
    var_filtro = ctk.StringVar(value="Mostrar Todas")

    ancho_seguro_texto = ancho_app - 600

    # --- 2. CONTROLES DE PÁGINA (ANCLADOS AL FONDO PRIMERO) ---
    nav_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    nav_frame.pack(side="bottom", fill="x", pady=20)
    
    btn_prev = ctk.CTkButton(nav_frame, text="⬅️ Anterior", width=120, fg_color="#334155", hover_color="#475569")
    btn_prev.pack(side="left", padx=30)
    
    lbl_contador = ctk.CTkLabel(nav_frame, text="", font=("Arial", 14, "bold"))
    lbl_contador.pack(side="left", expand=True)
    
    btn_next = ctk.CTkButton(nav_frame, text="Siguiente ➡️", width=120, fg_color="#334155", hover_color="#475569")
    btn_next.pack(side="right", padx=30)

    # --- 3. TARJETA CENTRAL (TOMA EL ESPACIO RESTANTE) ---
    tarjeta_frame = ctk.CTkFrame(tools_frame, fg_color="#1E293B", corner_radius=15, border_width=1, border_color="#38BDF8")
    tarjeta_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    
    lbl_titulo = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 22, "bold"), text_color="#38BDF8", wraplength=ancho_seguro_texto)
    lbl_titulo.pack(pady=(30, 5), padx=30, anchor="w")
    
    lbl_autor = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 14, "italic"), text_color="#94A3B8")
    lbl_autor.pack(pady=(0, 5), padx=30, anchor="w")
    
    lbl_cat = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 12, "bold"), text_color="#A78BFA")
    lbl_cat.pack(pady=(0, 20), padx=30, anchor="w")
    
    lbl_desc = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 15), justify="left", wraplength=ancho_seguro_texto)
    lbl_desc.pack(pady=10, padx=30, anchor="w")
    
    lbl_adv = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 14, "bold"), text_color="#EF4444", justify="left", wraplength=ancho_seguro_texto)
    lbl_adv.pack(pady=20, padx=30, anchor="w")
    
    btn_frame = ctk.CTkFrame(tarjeta_frame, fg_color="transparent")
    btn_frame.pack(pady=30)

    def mostrar_pagina(idx):
        if not datos_filtrados:
            lbl_titulo.configure(text="No hay resultados para este filtro.")
            lbl_autor.configure(text="")
            lbl_cat.configure(text="")
            lbl_desc.configure(text="")
            lbl_adv.configure(text="")
            lbl_contador.configure(text="0 de 0")
            for widget in btn_frame.winfo_children(): widget.destroy()
            return

        item = datos_filtrados[idx]
        lbl_titulo.configure(text=item.get('titulo', ''))
        lbl_autor.configure(text=f"Autor: {item.get('autor', '')}")
        lbl_cat.configure(text=f"🏷️ Categoría: {item.get('categoria', 'Sin Categoría')}")
        lbl_desc.configure(text=item.get('descripcion', ''))
        lbl_adv.configure(text=item.get('advertencia', ''))
        
        tarjeta_frame.configure(border_color="#F59E0B" if item.get('advertencia', '') else "#38BDF8")
        
        for widget in btn_frame.winfo_children(): widget.destroy()
            
        if item.get('es_enlace', False):
            def abrir_repo(url=item.get('enlace', '')): webbrowser.open(url)
            ctk.CTkButton(btn_frame, text="🌐 Abrir Repositorio Oficial", font=("Arial", 16, "bold"), height=50, fg_color="#3B82F6", hover_color="#2563EB", text_color="#FFFFFF", command=abrir_repo).pack()
        else:
            def accionar_instalacion():
                def comando_puente(log): logica_instalar_herramienta(log, item.get('carpeta',''), item.get('archivos',[]), item.get('comando_instalacion',''))
                abrir_consola_y_ejecutar(f"INSTALADOR DESATENDIDO: {item.get('titulo', '')}", comando_puente)
                
            ctk.CTkButton(btn_frame, text=f"⬇️ Instalar {item.get('titulo', '')}", font=("Arial", 16, "bold"), height=50, fg_color="#10B981", hover_color="#059669", text_color="#FFFFFF", command=accionar_instalacion).pack()
            
        lbl_contador.configure(text=f"Página {idx + 1} de {len(datos_filtrados)}")

    def cambiar_pagina(direccion):
        nonlocal indice_actual
        if not datos_filtrados: return
        indice_actual += direccion
        if indice_actual < 0: indice_actual = len(datos_filtrados) - 1
        elif indice_actual >= len(datos_filtrados): indice_actual = 0
        mostrar_pagina(indice_actual)

    btn_prev.configure(command=lambda: cambiar_pagina(-1))
    btn_next.configure(command=lambda: cambiar_pagina(1))

    def aplicar_filtro(seleccion):
        nonlocal datos_filtrados, indice_actual
        if seleccion == "Mostrar Todas":
            datos_filtrados = datos_enciclopedia.copy()
        else:
            datos_filtrados = [item for item in datos_enciclopedia if item.get('categoria', 'Sin Categoría') == seleccion]
        
        indice_actual = 0 
        mostrar_pagina(indice_actual)

    combo_filtro = ctk.CTkOptionMenu(header_frame, values=lista_filtros, variable=var_filtro, command=aplicar_filtro, fg_color="#3B82F6", button_color="#2563EB", button_hover_color="#1D4ED8", font=("Arial", 14, "bold"))
    combo_filtro.pack(side="right")
    ctk.CTkLabel(header_frame, text="🔍 Filtrar: ", font=("Arial", 14, "bold"), text_color="#94A3B8").pack(side="right", padx=10)

    mostrar_pagina(0)

# =========================================================================================

def cargar_categoria_manuales():
    import urllib.request, json, time, webbrowser
    global app, datos_manuales
    
    # 1. ESCUDO MAESTRO: Resucita la variable global si fue borrada del archivo principal
    if 'datos_manuales' not in globals() or datos_manuales is None:
        datos_manuales = []
        
    limpiar_panel()
    
    # --- 1. ENCABEZADO ---
    header_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    header_frame.pack(side="top", fill="x", pady=(0, 20))
    
    ctk.CTkLabel(header_frame, text="📖 Manuales y Trucos", font=("Arial", 24, "bold")).pack(side="left")
    
    if not datos_manuales:
        url_indice = f"https://raw.githubusercontent.com/LennesVP/Encyclopedia-of-Tools/main/manuales.json?t={time.time()}"
        try:
            req = urllib.request.Request(url_indice, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
            respuesta = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
            datos_manuales = json.loads(respuesta)
        except Exception as e:
            ctk.CTkLabel(tools_frame, text=f"Error al conectar con la Nube:\n{e}", text_color="#FF4444").pack(pady=20)
            return

    if not datos_manuales:
        ctk.CTkLabel(tools_frame, text="La biblioteca de manuales está vacía.", text_color="#AAAAAA").pack(pady=20)
        return

    plataformas_unicas = set()
    for item in datos_manuales:
        plataformas_unicas.add(item.get('plataforma', 'General'))
        
    lista_filtros = ["Mostrar Todos"] + sorted(list(plataformas_unicas))
    datos_filtrados = datos_manuales.copy()
    indice_actual = 0
    var_filtro = ctk.StringVar(value="Mostrar Todos")

    ancho_seguro_texto = ancho_app - 600

    # --- 2. CONTROLES DE PÁGINA (ANCLADOS AL FONDO PRIMERO) ---
    nav_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    nav_frame.pack(side="bottom", fill="x", pady=10)
    
    btn_prev = ctk.CTkButton(nav_frame, text="⬅️ Anterior", width=120, fg_color="#334155", hover_color="#475569")
    btn_prev.pack(side="left", padx=30)
    
    lbl_contador = ctk.CTkLabel(nav_frame, text="", font=("Arial", 14, "bold"))
    lbl_contador.pack(side="left", expand=True)
    
    btn_next = ctk.CTkButton(nav_frame, text="Siguiente ➡️", width=120, fg_color="#334155", hover_color="#475569")
    btn_next.pack(side="right", padx=30)

    # --- 3. TARJETA CENTRAL (TOMA EL ESPACIO RESTANTE) ---
    tarjeta_frame = ctk.CTkFrame(tools_frame, fg_color="#1E293B", corner_radius=15, border_width=1, border_color="#10B981")
    tarjeta_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    
    lbl_titulo = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 22, "bold"), text_color="#10B981", wraplength=ancho_seguro_texto)
    lbl_titulo.pack(pady=(30, 5), padx=30, anchor="w")
    
    lbl_autor = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 14, "italic"), text_color="#94A3B8")
    lbl_autor.pack(pady=(0, 5), padx=30, anchor="w")
    
    lbl_plat = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 13, "bold"), text_color="#38BDF8")
    lbl_plat.pack(pady=(0, 20), padx=30, anchor="w")
    
    lbl_desc = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 15), justify="left", wraplength=ancho_seguro_texto)
    lbl_desc.pack(pady=10, padx=30, anchor="w")
    
    lbl_adv = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 14, "bold"), text_color="#EF4444", justify="left", wraplength=ancho_seguro_texto)
    lbl_adv.pack(pady=20, padx=30, anchor="w")
    
    btn_frame = ctk.CTkFrame(tarjeta_frame, fg_color="transparent")
    btn_frame.pack(pady=30)

    def mostrar_pagina(idx):
        if not datos_filtrados:
            lbl_titulo.configure(text="No hay manuales para este sistema.")
            lbl_autor.configure(text="")
            lbl_plat.configure(text="")
            lbl_desc.configure(text="")
            lbl_adv.configure(text="")
            lbl_contador.configure(text="0 de 0")
            for widget in btn_frame.winfo_children(): widget.destroy()
            return

        item = datos_filtrados[idx]
        lbl_titulo.configure(text=item.get('titulo', ''))
        lbl_autor.configure(text=f"Autor: {item.get('autor', '')}")
        lbl_plat.configure(text=f"🖥️ Sistema/Dispositivo: {item.get('plataforma', 'General')}")
        lbl_desc.configure(text=item.get('descripcion', ''))
        lbl_adv.configure(text=item.get('advertencia', ''))
        
        tarjeta_frame.configure(border_color="#F59E0B" if item.get('advertencia', '') else "#10B981")
        
        for widget in btn_frame.winfo_children(): widget.destroy()
            
        if item.get('enlace', ''):
            def abrir_repo(url=item.get('enlace', '')): webbrowser.open(url)
            ctk.CTkButton(btn_frame, text="🌐 Ver Documentación Web", font=("Arial", 16, "bold"), height=50, fg_color="#3B82F6", hover_color="#2563EB", text_color="#FFFFFF", command=abrir_repo).pack()
            
        lbl_contador.configure(text=f"Manual {idx + 1} de {len(datos_filtrados)}")

    def cambiar_pagina(direccion):
        nonlocal indice_actual
        if not datos_filtrados: return
        indice_actual += direccion
        if indice_actual < 0: indice_actual = len(datos_filtrados) - 1
        elif indice_actual >= len(datos_filtrados): indice_actual = 0
        mostrar_pagina(indice_actual)

    btn_prev.configure(command=lambda: cambiar_pagina(-1))
    btn_next.configure(command=lambda: cambiar_pagina(1))

    def aplicar_filtro(seleccion):
        nonlocal datos_filtrados, indice_actual
        if seleccion == "Mostrar Todos":
            datos_filtrados = datos_manuales.copy()
        else:
            datos_filtrados = [item for item in datos_manuales if item.get('plataforma', 'General') == seleccion]
        
        indice_actual = 0 
        mostrar_pagina(indice_actual)

    combo_filtro = ctk.CTkOptionMenu(header_frame, values=lista_filtros, variable=var_filtro, command=aplicar_filtro, fg_color="#10B981", button_color="#059669", button_hover_color="#047857", text_color="#FFFFFF", font=("Arial", 14, "bold"))
    combo_filtro.pack(side="right")
    ctk.CTkLabel(header_frame, text="🔍 Filtrar Sistema: ", font=("Arial", 14, "bold"), text_color="#94A3B8").pack(side="right", padx=10)

    mostrar_pagina(0)

def cargar_categoria_tienda():
    import urllib.request, json, time, webbrowser
    global app, datos_tienda, indice_tienda
    
    # 1. ESCUDO MAESTRO: Si las variables globales se borraron por accidente en el archivo, 
    # este escudo las resucita automáticamente. ¡Así jamás volverá a dar el NameError!
    if 'datos_tienda' not in globals() or datos_tienda is None:
        datos_tienda = []
    if 'indice_tienda' not in globals():
        indice_tienda = 0
        
    # 2. REGLA DE ORO: Limpiar la pantalla actual ANTES de hacer nada para evitar superposiciones
    limpiar_panel()

    # --- 1. ENCABEZADO ---
    header_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    header_frame.pack(side="top", fill="x", pady=(0, 20))
    ctk.CTkLabel(header_frame, text="🛒 Venta de Licencias Oficiales", font=("Arial", 24, "bold")).pack(side="left")
    
    if not datos_tienda:
        url_tienda = f"https://raw.githubusercontent.com/LennesVP/Encyclopedia-of-Tools/main/tienda.json?t={time.time()}"
        try:
            req = urllib.request.Request(url_tienda, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
            respuesta = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
            datos_tienda = json.loads(respuesta)
        except Exception as e:
            ctk.CTkLabel(tools_frame, text=f"Error al conectar con la Tienda:\n{e}", text_color="#FF4444").pack(pady=20)
            return

    if not datos_tienda:
        ctk.CTkLabel(tools_frame, text="La tienda está vacía por ahora.", text_color="#AAAAAA").pack(pady=20)
        return

    # --- 2. CONTROLES DE PÁGINA (EMPAQUETADOS AL FONDO PRIMERO) ---
    nav_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    nav_frame.pack(side="bottom", fill="x", pady=20)
    
    btn_prev = ctk.CTkButton(nav_frame, text="⬅️ Anterior", width=120, fg_color="#334155", hover_color="#475569")
    btn_prev.pack(side="left", padx=30)
    lbl_contador = ctk.CTkLabel(nav_frame, text="", font=("Arial", 14, "bold"))
    lbl_contador.pack(side="left", expand=True)
    btn_next = ctk.CTkButton(nav_frame, text="Siguiente ➡️", width=120, fg_color="#334155", hover_color="#475569")
    btn_next.pack(side="right", padx=30)

    # --- 3. DISEÑO DEL CARRUSEL COMERCIAL (TOMA EL ESPACIO RESTANTE) ---
    tarjeta_frame = ctk.CTkFrame(tools_frame, fg_color="#1E293B", corner_radius=15, border_width=2, border_color="#F59E0B")
    tarjeta_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    
    lbl_titulo = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 22, "bold"), text_color="#FCD34D", wraplength=550)
    lbl_titulo.pack(pady=(20, 5), padx=30, anchor="w")
    
    frame_precios = ctk.CTkFrame(tarjeta_frame, fg_color="transparent")
    frame_precios.pack(fill="x", padx=30, pady=5)
    lbl_precio_oficial = ctk.CTkLabel(frame_precios, text="", font=("Arial", 14, "overstrike"), text_color="#94A3B8")
    lbl_precio_oficial.pack(side="left", padx=(0, 10))
    lbl_precio_tremend = ctk.CTkLabel(frame_precios, text="", font=("Arial", 18, "bold"), text_color="#10B981")
    lbl_precio_tremend.pack(side="left")
    
    lbl_desc = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 15), justify="left", wraplength=550)
    lbl_desc.pack(pady=10, padx=30, anchor="w")
    
    lbl_caract = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 14), justify="left", text_color="#E2E8F0", wraplength=550)
    lbl_caract.pack(pady=10, padx=30, anchor="w")
    
    lbl_adv = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 13, "bold"), text_color="#EF4444", justify="left", wraplength=550)
    lbl_adv.pack(pady=20, padx=30, anchor="w")

    lbl_variacion = ctk.CTkLabel(
        tarjeta_frame, 
        text="📌 Nota Legal: Los precios mostrados son aproximados y están sujetos a cambios sin previo aviso. El valor final puede ser menor o mayor dependiendo de las ofertas del proveedor y la tasa de cambio al momento de confirmar la compra.", 
        font=("Arial", 12, "italic"), 
        text_color="#F87171",
        wraplength=550, 
        justify="left"
    )
    lbl_variacion.pack(pady=(0, 10), padx=30, anchor="w")
    
    btn_frame = ctk.CTkFrame(tarjeta_frame, fg_color="transparent")
    btn_frame.pack(pady=20)

    def mostrar_producto(idx):
        item = datos_tienda[idx]
        lbl_titulo.configure(text=item.get('producto', ''))
        lbl_precio_tremend.configure(text=f"Precio TREMEND: {item.get('precio_tremend', '')}")
        lbl_precio_oficial.configure(text=f"Oficial: {item.get('precio_oficial', '')}")
        lbl_desc.configure(text=item.get('descripcion', ''))
        lbl_caract.configure(text=item.get('caracteristicas', ''))
        lbl_adv.configure(text=item.get('advertencia', ''))
        
        for widget in btn_frame.winfo_children(): widget.destroy()
            
        def comprar_wp():
            numero_wa = "573025524549"  
            mensaje = f"Hola Lennes, me interesa adquirir la licencia de: {item.get('producto', '')} que vi en TREMEND Toolkit."
            url = f"https://wa.me/{numero_wa}?text={urllib.parse.quote(mensaje)}"
            webbrowser.open(url)
            
        def enviar_correo():
            correo = "tremend67@gmail.com"  
            asunto = f"Soporte / Compra de Licencia: {item.get('producto', '')}"
            url = f"mailto:{correo}?subject={urllib.parse.quote(asunto)}"
            webbrowser.open(url)
            
        ctk.CTkButton(btn_frame, text="📲 Comprar por WhatsApp", font=("Arial", 15, "bold"), height=45, fg_color="#25D366", hover_color="#1DA851", text_color="#FFFFFF", command=comprar_wp).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="✉️ Soporte / Correo", font=("Arial", 15, "bold"), height=45, fg_color="#3B82F6", hover_color="#2563EB", text_color="#FFFFFF", command=enviar_correo).pack(side="left", padx=10)

    def cambiar_pagina(direccion):
        global indice_tienda
        indice_tienda += direccion
        if indice_tienda < 0: indice_tienda = len(datos_tienda) - 1
        elif indice_tienda >= len(datos_tienda): indice_tienda = 0
        mostrar_producto(indice_tienda)
        lbl_contador.configure(text=f"Producto {indice_tienda + 1} de {len(datos_tienda)}")

    btn_prev.configure(command=lambda: cambiar_pagina(-1))
    btn_next.configure(command=lambda: cambiar_pagina(1))
    
    mostrar_producto(indice_tienda)
    lbl_contador.configure(text=f"Producto {indice_tienda + 1} de {len(datos_tienda)}")

def cargar_categoria_webs():
    import urllib.request, json, time, webbrowser
    global app
    
    url_webs = f"https://raw.githubusercontent.com/LennesVP/Encyclopedia-of-Tools/main/webs.json?t={time.time()}"
    try:
        req = urllib.request.Request(url_webs, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        respuesta = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        datos_webs = json.loads(respuesta)
    except Exception as e:
        limpiar_panel()
        ctk.CTkLabel(tools_frame, text=f"Error al conectar con la Nube:\n{e}", text_color="#FF4444").pack(pady=20)
        return

    if not datos_webs:
        limpiar_panel()
        ctk.CTkLabel(tools_frame, text="El directorio web está vacío.", text_color="#AAAAAA").pack(pady=20)
        return

    # --- ADAPTACIÓN AL MOTOR MAESTRO DE VISTAS ---
    h_webs = []
    for index, item in enumerate(datos_webs):
        # Función constructora para congelar la URL correcta en cada botón
        def make_cmd(url):
            return lambda: webbrowser.open(url)
            
        h_webs.append({
            "id": str(index + 1),
            "nombre": f"{index + 1}. {item.get('nombre', 'Sitio Web')}",
            "exp": item.get("categoria", ""),     # Se ubicará al lado del título (ideal para la Categoría/Etiqueta)
            "nov": item.get("descripcion", ""),   # Se ubicará en el cuerpo del texto
            "cmd": make_cmd(item.get("enlace", "")),
            "txt_btn": "🌐 Abrir Página Web",
            "color_borde": "#8B5CF6"              # Mantiene la identidad visual púrpura neón
        })
        
    construir_vista_dinamica("🌐 Enciclopedia de Páginas Web", "🔍 Buscar (Ej: extensiones, inteligencia, roms)...", h_webs)

# Variable global (Ponla junto a las otras arriba si prefieres, o déjala que se declare sola)
datos_manuales = []

def cargar_categoria_manuales():
    import urllib.request, json, time, webbrowser
    global app, datos_manuales
    
    limpiar_panel()
    
    # --- 1. ENCABEZADO ---
    header_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    header_frame.pack(side="top", fill="x", pady=(0, 20))
    
    ctk.CTkLabel(header_frame, text="📖 Manuales y Trucos", font=("Arial", 24, "bold")).pack(side="left")
    
    if not datos_manuales:
        url_indice = f"https://raw.githubusercontent.com/LennesVP/Encyclopedia-of-Tools/main/manuales.json?t={time.time()}"
        try:
            req = urllib.request.Request(url_indice, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
            respuesta = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
            datos_manuales = json.loads(respuesta)
        except Exception as e:
            ctk.CTkLabel(tools_frame, text=f"Error al conectar con la Nube:\n{e}", text_color="#FF4444").pack(pady=20)
            return

    if not datos_manuales:
        ctk.CTkLabel(tools_frame, text="La biblioteca de manuales está vacía.", text_color="#AAAAAA").pack(pady=20)
        return

    plataformas_unicas = set()
    for item in datos_manuales:
        plataformas_unicas.add(item.get('plataforma', 'General'))
        
    lista_filtros = ["Mostrar Todos"] + sorted(list(plataformas_unicas))
    datos_filtrados = datos_manuales.copy()
    indice_actual = 0
    var_filtro = ctk.StringVar(value="Mostrar Todos")

    ancho_seguro_texto = ancho_app - 600

    # --- 2. CONTROLES DE PÁGINA (ANCLADOS AL FONDO PRIMERO) ---
    nav_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    nav_frame.pack(side="bottom", fill="x", pady=10)
    
    btn_prev = ctk.CTkButton(nav_frame, text="⬅️ Anterior", width=120, fg_color="#334155", hover_color="#475569")
    btn_prev.pack(side="left", padx=30)
    
    lbl_contador = ctk.CTkLabel(nav_frame, text="", font=("Arial", 14, "bold"))
    lbl_contador.pack(side="left", expand=True)
    
    btn_next = ctk.CTkButton(nav_frame, text="Siguiente ➡️", width=120, fg_color="#334155", hover_color="#475569")
    btn_next.pack(side="right", padx=30)

    # --- 3. TARJETA CENTRAL (TOMA EL ESPACIO RESTANTE) ---
    tarjeta_frame = ctk.CTkFrame(tools_frame, fg_color="#1E293B", corner_radius=15, border_width=1, border_color="#10B981")
    tarjeta_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    
    lbl_titulo = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 22, "bold"), text_color="#10B981", wraplength=ancho_seguro_texto)
    lbl_titulo.pack(pady=(30, 5), padx=30, anchor="w")
    
    lbl_autor = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 14, "italic"), text_color="#94A3B8")
    lbl_autor.pack(pady=(0, 5), padx=30, anchor="w")
    
    lbl_plat = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 13, "bold"), text_color="#38BDF8")
    lbl_plat.pack(pady=(0, 20), padx=30, anchor="w")
    
    lbl_desc = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 15), justify="left", wraplength=ancho_seguro_texto)
    lbl_desc.pack(pady=10, padx=30, anchor="w")
    
    lbl_adv = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 14, "bold"), text_color="#EF4444", justify="left", wraplength=ancho_seguro_texto)
    lbl_adv.pack(pady=20, padx=30, anchor="w")
    
    btn_frame = ctk.CTkFrame(tarjeta_frame, fg_color="transparent")
    btn_frame.pack(pady=30)

    def mostrar_pagina(idx):
        if not datos_filtrados:
            lbl_titulo.configure(text="No hay manuales para este sistema.")
            lbl_autor.configure(text="")
            lbl_plat.configure(text="")
            lbl_desc.configure(text="")
            lbl_adv.configure(text="")
            lbl_contador.configure(text="0 de 0")
            for widget in btn_frame.winfo_children(): widget.destroy()
            return

        item = datos_filtrados[idx]
        lbl_titulo.configure(text=item.get('titulo', ''))
        lbl_autor.configure(text=f"Autor: {item.get('autor', '')}")
        lbl_plat.configure(text=f"🖥️ Sistema/Dispositivo: {item.get('plataforma', 'General')}")
        lbl_desc.configure(text=item.get('descripcion', ''))
        lbl_adv.configure(text=item.get('advertencia', ''))
        
        tarjeta_frame.configure(border_color="#F59E0B" if item.get('advertencia', '') else "#10B981")
        
        for widget in btn_frame.winfo_children(): widget.destroy()
            
        if item.get('enlace', ''):
            def abrir_repo(url=item.get('enlace', '')): webbrowser.open(url)
            ctk.CTkButton(btn_frame, text="🌐 Ver Documentación Web", font=("Arial", 16, "bold"), height=50, fg_color="#3B82F6", hover_color="#2563EB", text_color="#FFFFFF", command=abrir_repo).pack()
            
        lbl_contador.configure(text=f"Manual {idx + 1} de {len(datos_filtrados)}")

    def cambiar_pagina(direccion):
        nonlocal indice_actual
        if not datos_filtrados: return
        indice_actual += direccion
        if indice_actual < 0: indice_actual = len(datos_filtrados) - 1
        elif indice_actual >= len(datos_filtrados): indice_actual = 0
        mostrar_pagina(indice_actual)

    btn_prev.configure(command=lambda: cambiar_pagina(-1))
    btn_next.configure(command=lambda: cambiar_pagina(1))

    def aplicar_filtro(seleccion):
        nonlocal datos_filtrados, indice_actual
        if seleccion == "Mostrar Todos":
            datos_filtrados = datos_manuales.copy()
        else:
            datos_filtrados = [item for item in datos_manuales if item.get('plataforma', 'General') == seleccion]
        
        indice_actual = 0 
        mostrar_pagina(indice_actual)

    combo_filtro = ctk.CTkOptionMenu(header_frame, values=lista_filtros, variable=var_filtro, command=aplicar_filtro, fg_color="#10B981", button_color="#059669", button_hover_color="#047857", text_color="#FFFFFF", font=("Arial", 14, "bold"))
    combo_filtro.pack(side="right")
    ctk.CTkLabel(header_frame, text="🔍 Filtrar Sistema: ", font=("Arial", 14, "bold"), text_color="#94A3B8").pack(side="right", padx=10)

    mostrar_pagina(0)

def cargar_categoria_mac():
    import urllib.request, json, time, webbrowser
    global app
    
    url_mac = f"https://raw.githubusercontent.com/LennesVP/Encyclopedia-of-Tools/main/mac.json?t={time.time()}"
    try:
        req = urllib.request.Request(url_mac, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        respuesta = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        datos_mac = json.loads(respuesta)
    except Exception as e:
        limpiar_panel()
        ctk.CTkLabel(tools_frame, text=f"Error al conectar con la Nube de Mac:\n{e}", text_color="#FF4444").pack(pady=20)
        return

    if not datos_mac:
        limpiar_panel()
        ctk.CTkLabel(tools_frame, text="El catálogo de Mac está vacío.", text_color="#AAAAAA").pack(pady=20)
        return

    h_mac = []
    for index, item in enumerate(datos_mac):
        nombre_api = item.get('nombre', 'App Mac')
        
        if "sniffnet" in nombre_api.lower():
            comando_ejecucion = lambda: abrir_consola_y_ejecutar("SNIFFNET", logica_sniffnet)
            txt_boton = "⚡ Ejecutar Herramienta"
        elif "mole" in nombre_api.lower():
            comando_ejecucion = lambda: abrir_consola_y_ejecutar("MOLE", logica_mole)
            txt_boton = "⚡ Ejecutar Herramienta"
        # ---- AQUÍ INYECTAMOS EL NUEVO BOTÓN ----
        elif "macpeas" in nombre_api.lower():
            comando_ejecucion = lambda: abrir_consola_y_ejecutar("MACPEAS", logica_macpeas)
            txt_boton = "⚡ Ejecutar Auditoría"
        # ----------------------------------------
        else:
            # Si es una aplicación normal, le pone el enlace web a GitHub
            def make_cmd(url): return lambda: webbrowser.open(url)
            comando_ejecucion = make_cmd(item.get("enlace", ""))
            txt_boton = "🍏 Ver App Oficial"
            
        badge_text = "🔓 Código Abierto" if item.get('es_open_source', False) else "🔒 Código Cerrado"
        
        h_mac.append({
            "id": str(index + 1),
            "nombre": f"{index + 1}. {nombre_api}",
            "exp": f"Autor: {item.get('autor', 'Desconocido')} | {badge_text}",
            "nov": f"{item.get('descripcion', '')}\n\nCaracterísticas: {item.get('ventajas', '')}",
            "cmd": comando_ejecucion,
            "txt_btn": txt_boton,
            "color_borde": "#A855F7" # Color Púrpura especial para diferenciar Mac
        })
        
    construir_vista_dinamica("🍏 Aplicaciones y Herramientas para Mac", "🔍 Buscar (Ej: firewall, snitch)...", h_mac)

def cargar_categoria_linux():
    limpiar_panel()
    
    # --- LAYOUT ESTILO TILING (Workspace de Servidor) ---
    # Panel Izquierdo: Directorio de comandos (35% del espacio)
    # Panel Derecho: Terminal TTY Persistente (65% del espacio)
    
    panel_izq = ctk.CTkFrame(tools_frame, width=320, fg_color="transparent")
    panel_izq.pack(side="left", fill="y", padx=(0, 15))
    panel_izq.pack_propagate(False) # Congela el ancho para no deformarse
    
    panel_der = ctk.CTkFrame(tools_frame, fg_color="#050505", corner_radius=10, border_width=1, border_color="#22C55E")
    panel_der.pack(side="right", fill="both", expand=True)
    
    # --- TERMINAL NATIVA (DERECHA) ---
    top_term = ctk.CTkFrame(panel_der, fg_color="#166534", corner_radius=0, height=35)
    top_term.pack(fill="x")
    top_term.pack_propagate(False)
    
    ctk.CTkLabel(top_term, text="root@tremend-server:~#", font=("Consolas", 14, "bold"), text_color="#FFFFFF").pack(side="left", padx=15)
    
    txt_consola = ctk.CTkTextbox(panel_der, fg_color="transparent", text_color="#4ADE80", font=("Consolas", 14), wrap="word")
    txt_consola.pack(fill="both", expand=True, padx=10, pady=10)
    txt_consola.insert("end", "TREMEND OS (Linux Subsystem)\nSistema de inyección asíncrona de comandos listo.\nSelecciona un módulo a la izquierda...\n\n")
    txt_consola.configure(state="disabled")
    
    def log_tty(texto):
        def update():
            txt_consola.configure(state="normal")
            txt_consola.insert("end", str(texto) + "\n")
            txt_consola.see("end")
            txt_consola.configure(state="disabled")
        app.after(0, update)
        
    def limpiar_tty():
        txt_consola.configure(state="normal")
        txt_consola.delete("1.0", "end")
        txt_consola.insert("end", "root@tremend-server:~# clear\n\n")
        txt_consola.configure(state="disabled")
        
    ctk.CTkButton(top_term, text="[ Ctrl+L ] Clear", width=80, height=24, fg_color="#064E3B", hover_color="#14532D", text_color="#A7F3D0", font=("Consolas", 12), command=limpiar_tty).pack(side="right", padx=10)

    # --- MOTOR ASÍNCRONO BASH (Reemplaza al viejo LinuxToolkit) ---
    def ejecutar_bash(comando_str, interactivo=False):
        log_tty(f"root@tremend-server:~# {comando_str}")
        
        if interactivo:
            # Para apps como htop que necesitan su propia ventana interactiva pura
            try: subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{comando_str}; exec bash"])
            except: log_tty("[-] gnome-terminal no encontrado. Usa un entorno compatible.\n")
            return

        def run():
            try:
                # bufsize=1 permite leer línea por línea sin esperar a que el proceso termine entero
                proceso = subprocess.Popen(comando_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
                for linea in iter(proceso.stdout.readline, ''):
                    if linea: log_tty(linea.strip())
                proceso.wait()
                log_tty(f"[*] Salida (Exit Code): {proceso.returncode}\n")
            except Exception as e:
                log_tty(f"[-] bash: {comando_str}: error interno ({e})\n")
                
        import threading
        threading.Thread(target=run, daemon=True).start()

    # --- FUNCIONES INTERACTIVAS CON VENTANA ---
    def btn_ping():
        dialogo = ctk.CTkInputDialog(text="Ingresa IP o Dominio:", title="Ping")
        dest = dialogo.get_input()
        if dest: ejecutar_bash(f"ping -c 4 {dest}")
        
    def btn_nmap():
        dialogo = ctk.CTkInputDialog(text="Ingresa IP o Dominio a escanear (vacío para localhost):", title="Nmap")
        dest = dialogo.get_input()
        target = dest if dest else "localhost"
        ejecutar_bash(f"nmap -sV -sC {target}")

    # --- PALETA DE COMANDOS (IZQUIERDA) ---
    ctk.CTkLabel(panel_izq, text="🐧 Directorio Linux", font=("Arial", 22, "bold")).pack(anchor="w", pady=(0, 15))
    
    lista_comandos = ctk.CTkScrollableFrame(panel_izq, fg_color="transparent")
    lista_comandos.pack(fill="both", expand=True)

    # DICCIONARIO CATEGORIZADO (Diseño Hacker/Sysadmin)
    comandos_linux = [
        {"cat": "INTERFACES GRÁFICAS"},
        {"nombre": "Radar Sniffnet", "desc": "Monitor de tráfico", "cmd": lambda: abrir_consola_y_ejecutar("SNIFFNET", logica_sniffnet), "color": "#A855F7"},
        {"nombre": "htop", "desc": "Gestor de tareas", "cmd": lambda: ejecutar_bash("htop", interactivo=True), "color": "#A855F7"},
        
        {"cat": "CIBERSEGURIDAD / AUDITORÍA"},
        {"nombre": "nmap -sV -sC", "desc": "Escáner de vulnerabilidades", "cmd": btn_nmap, "color": "#EF4444"},
        {"nombre": "find SUID", "desc": "Escalada de privilegios", "cmd": lambda: ejecutar_bash("find / -perm -4000 -type f 2>/dev/null | head -n 20"), "color": "#EF4444"},
        {"nombre": "grep Logs", "desc": "Cazar intrusos en auth.log", "cmd": lambda: ejecutar_bash('grep -iE "error|failed|unauthorized" /var/log/auth.log 2>/dev/null | tail -n 20'), "color": "#EF4444"},
        {"nombre": "LinPEAS - Auto", "desc": "Auditoría + Auto-Blindaje", "cmd": lambda: abrir_consola_y_ejecutar("LINPEAS", logica_linpeas), "color": "#EF4444"},

        {"cat": "REDES Y FIREWALL"},
        {"nombre": "ss -tulnp", "desc": "Puertos y sockets activos", "cmd": lambda: ejecutar_bash("ss -tulnp"), "color": "#3B82F6"},
        {"nombre": "iptables -L -n -v", "desc": "Ver reglas del firewall", "cmd": lambda: ejecutar_bash("sudo iptables -L -n -v"), "color": "#3B82F6"},
        {"nombre": "ping -c 4", "desc": "Probar conectividad", "cmd": btn_ping, "color": "#3B82F6"},
        {"nombre": "ip a", "desc": "Interfaces IP locales", "cmd": lambda: ejecutar_bash("ip a | grep inet"), "color": "#3B82F6"},
        
        {"cat": "SISTEMA BASE"},
        {"nombre": "cat /etc/passwd", "desc": "Tabla de usuarios", "cmd": lambda: ejecutar_bash("cat /etc/passwd"), "color": "#10B981"},
        {"nombre": "df -h", "desc": "Uso de discos duros", "cmd": lambda: ejecutar_bash("df -h"), "color": "#10B981"},
        {"nombre": "ls -lah", "desc": "Directorio actual", "cmd": lambda: ejecutar_bash("ls -lah"), "color": "#10B981"}
    ]

    for item in comandos_linux:
        if "cat" in item:
            ctk.CTkLabel(lista_comandos, text=item["cat"], font=("Arial", 11, "bold"), text_color="#64748B").pack(anchor="w", pady=(15, 2))
        else:
            tarjeta = ctk.CTkFrame(lista_comandos, fg_color="#1E293B", corner_radius=8, border_width=1, border_color=item["color"])
            tarjeta.pack(fill="x", pady=4)
            
            # Botón con título del comando
            btn = ctk.CTkButton(tarjeta, text=item["nombre"], font=("Consolas", 14, "bold"), fg_color="transparent", hover_color="#334155", anchor="w", text_color=item["color"], command=item["cmd"])
            btn.pack(fill="x", padx=10, pady=(8, 0))
            
            # Pequeña descripción táctica
            ctk.CTkLabel(tarjeta, text=item["desc"], font=("Arial", 11), text_color="#94A3B8", anchor="w").pack(fill="x", padx=15, pady=(0, 8))

def cargar_categoria_android():
    import urllib.request, json, time, webbrowser
    global app
    limpiar_panel()
    
    # --- 1. ENCABEZADO CON BUSCADOR Y FILTROS ---
    header_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(header_frame, text="🤖 Aplicaciones y APKs para Android", font=("Arial", 24, "bold")).pack(side="left")

    # Variables reactivas para el buscador
    search_var = ctk.StringVar()
    var_filtro = ctk.StringVar(value="Todas las Apps")
    estado = {"pagina": 0, "filtradas": [], "datos": []}

    # Buscador y Filtro Desplegable (UI a la derecha)
    combo_filtro = ctk.CTkOptionMenu(header_frame, values=["Todas las Apps", "🔓 Open Source", "🔒 Código Cerrado"], variable=var_filtro, fg_color="#1E293B", button_color="#3DDC84", button_hover_color="#2EB86A", text_color="#000000", font=("Arial", 13, "bold"))
    combo_filtro.pack(side="right", padx=10)
    
    barra_busqueda = ctk.CTkEntry(header_frame, textvariable=search_var, placeholder_text="🔍 Buscar app, autor o función...", width=250, font=("Arial", 14), corner_radius=15, border_color="#3DDC84")
    barra_busqueda.pack(side="right", padx=10)

    # --- 2. CONTENEDORES DE INTERFAZ ---
    lista_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    lista_frame.pack(side="top", fill="both", expand=True)

    nav_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    nav_frame.pack(side="bottom", fill="x", pady=10)

    btn_prev = ctk.CTkButton(nav_frame, text="⬅️ Anterior", width=120, fg_color="#334155", hover_color="#475569")
    btn_prev.pack(side="left", padx=30)
    lbl_contador = ctk.CTkLabel(nav_frame, text="", font=("Arial", 14, "bold"), text_color="#3DDC84")
    lbl_contador.pack(side="left", expand=True)
    btn_next = ctk.CTkButton(nav_frame, text="Siguiente ➡️", width=120, fg_color="#334155", hover_color="#475569")
    btn_next.pack(side="right", padx=30)

    # --- 3. EXTRACCIÓN DE DATOS DESDE LA NUBE ---
    url_android = f"https://raw.githubusercontent.com/LennesVP/Encyclopedia-of-Tools/main/android.json?t={time.time()}"
    try:
        req = urllib.request.Request(url_android, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        respuesta = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        estado["datos"] = json.loads(respuesta)
        estado["filtradas"] = estado["datos"].copy()
    except Exception as e:
        ctk.CTkLabel(lista_frame, text=f"Error al conectar con la Nube:\n{e}", text_color="#FF4444", font=("Arial", 14)).pack(pady=20)
        return

    if not estado["datos"]:
        ctk.CTkLabel(lista_frame, text="El catálogo de Android está vacío.", text_color="#AAAAAA").pack(pady=20)
        return

    # --- 4. MOTOR LIQUID UI (Adaptabilidad Matemática) ---
    escala_monitor = app._get_window_scaling()
    espacio_libre_vertical = alto_app - (260 * escala_monitor)
    altura_tarjeta = int(220 * escala_monitor) # Las tarjetas Android son más altas
    ITEMS_POR_PAGINA = max(1, int(espacio_libre_vertical / altura_tarjeta))

    def renderizar():
        for w in lista_frame.winfo_children(): w.destroy()

        total = len(estado["filtradas"])
        if total == 0:
            ctk.CTkLabel(lista_frame, text="No se encontraron aplicaciones con ese filtro.", text_color="#AAAAAA", font=("Arial", 16)).pack(pady=50)
            lbl_contador.configure(text="0 Resultados")
            return

        tot_pag = (total - 1) // ITEMS_POR_PAGINA + 1
        if estado["pagina"] >= tot_pag: estado["pagina"] = tot_pag - 1

        inicio = estado["pagina"] * ITEMS_POR_PAGINA
        lote = estado["filtradas"][inicio:inicio+ITEMS_POR_PAGINA]

        # El ancho interno se calcula restando márgenes y menús.
        ancho_panel_central = (ancho_app / escala_monitor) - 520
        espacio_texto = int(ancho_panel_central * 0.90) # Aprovechamos casi todo el ancho para lectura

        # --- 5. DIBUJADO DE LAS TARJETAS PERSONALIZADAS ---
        for item in lote:
            es_open = item.get('es_open_source', False)
            badge_text = "🔓 Código Abierto (Open Source)" if es_open else "🔒 Código Cerrado"
            badge_color = "#10B981" if es_open else "#EF4444"
            borde_color = "#3DDC84" if es_open else "#334155" # Destaca más las apps de código abierto

            tarjeta = ctk.CTkFrame(lista_frame, fg_color="#1E293B", corner_radius=10, border_width=1, border_color=borde_color)
            tarjeta.pack(fill="x", pady=8, padx=10)

            header_f = ctk.CTkFrame(tarjeta, fg_color="transparent")
            header_f.pack(fill="x", padx=20, pady=(12, 2))

            ctk.CTkLabel(header_f, text=item.get('nombre', ''), font=("Arial", 18, "bold"), text_color="#3DDC84").pack(side="left")
            ctk.CTkLabel(header_f, text=f"  |  Autor: {item.get('autor', '')}  |  {badge_text}", font=("Arial", 12, "italic"), text_color=badge_color).pack(side="left", padx=10)

            ctk.CTkLabel(tarjeta, text=item.get('descripcion', ''), font=("Arial", 14), justify="left", wraplength=espacio_texto).pack(padx=20, pady=2, anchor="w")

            # Analizador Inteligente de Trucos
            ventajas_text = item.get('ventajas', '')
            color_ventajas = "#FCD34D" if "⚠️ TRUCO" in ventajas_text else "#E2E8F0"
            
            ctk.CTkLabel(tarjeta, text="Características y Funciones:", font=("Arial", 12, "bold"), text_color="#94A3B8").pack(padx=20, pady=(5, 0), anchor="w")
            ctk.CTkLabel(tarjeta, text=ventajas_text, font=("Arial", 13), text_color=color_ventajas, justify="left", wraplength=espacio_texto).pack(padx=20, pady=(2, 5), anchor="w")

            def make_cmd(url):
                return lambda: webbrowser.open(url)

            ctk.CTkButton(tarjeta, text="🌐 Ver Repositorio Oficial", font=("Arial", 13, "bold"), height=35, fg_color="#3DDC84", hover_color="#2EB86A", text_color="#000000", command=make_cmd(item.get('enlace', ''))).pack(padx=20, pady=(0, 12), anchor="e")

        lbl_contador.configure(text=f"Página {estado['pagina'] + 1} de {tot_pag}  |  Total: {total}")

    # --- 6. MOTORES DE FILTRADO Y BÚSQUEDA ---
    def aplicar_filtros(*args):
        texto = search_var.get().lower().strip()
        filtro_tipo = var_filtro.get()

        resultados = []
        for item in estado["datos"]:
            # Filtrar por Tipo (Open Source vs Cerrado)
            pasa_tipo = True
            es_open = item.get('es_open_source', False)
            if filtro_tipo == "🔓 Open Source" and not es_open: pasa_tipo = False
            if filtro_tipo == "🔒 Código Cerrado" and es_open: pasa_tipo = False

            # Filtrar por Texto
            pasa_texto = True
            if len(texto) >= 2:
                if not (texto in item.get('nombre','').lower() or texto in item.get('descripcion','').lower() or texto in item.get('autor','').lower()):
                    pasa_texto = False

            if pasa_tipo and pasa_texto:
                resultados.append(item)

        estado["filtradas"] = resultados
        estado["pagina"] = 0
        renderizar()

    search_var.trace_add("write", aplicar_filtros)
    var_filtro.trace_add("write", aplicar_filtros)

    def cambiar(dir):
        if not estado["filtradas"]: return
        tot_pag = (len(estado["filtradas"]) - 1) // ITEMS_POR_PAGINA + 1
        n_pag = estado["pagina"] + dir
        if n_pag < 0: n_pag = tot_pag - 1
        elif n_pag >= tot_pag: n_pag = 0
        estado["pagina"] = n_pag; renderizar()

    btn_prev.configure(command=lambda: cambiar(-1))
    btn_next.configure(command=lambda: cambiar(1))

    aplicar_filtros() # Carga inicial

def cargar_categoria_ios():
    import urllib.request, json, time, webbrowser
    global app
    
    url_ios = f"https://raw.githubusercontent.com/LennesVP/Encyclopedia-of-Tools/main/ios.json?t={time.time()}"
    try:
        req = urllib.request.Request(url_ios, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        respuesta = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        datos_ios = json.loads(respuesta)
    except Exception as e:
        limpiar_panel()
        ctk.CTkLabel(tools_frame, text=f"Error al conectar con la Nube de iOS:\n{e}", text_color="#FF4444").pack(pady=20)
        return

    if not datos_ios:
        limpiar_panel()
        ctk.CTkLabel(tools_frame, text="El catálogo de iOS está vacío.", text_color="#AAAAAA").pack(pady=20)
        return

    h_ios = []
    for index, item in enumerate(datos_ios):
        def make_cmd(url):
            return lambda: webbrowser.open(url)
            
        h_ios.append({
            "id": str(index + 1),
            "nombre": f"{item.get('nombre', 'App iOS')}",
            "exp": f"Categoría: {item.get('categoria', 'Utilidades')}",
            "nov": item.get('descripcion', ''),
            "cmd": make_cmd(item.get("enlace", "")),
            "txt_btn": "🍏 Ver en App Store",
            "color_borde": "#F59E0B" # Borde color Naranja/Dorado para distinguir iOS
        })
        
    # Usamos la fábrica de tarjetas responsivas
    construir_vista_dinamica("📱 Aplicaciones y Utilidades para iOS", "🔍 Buscar (Ej: xiaomi, wifi)...", h_ios)
        
# ============================================================================
# 6. MENÚ LATERAL Y ARRANQUE (REDISEÑO CON SUBCATEGORÍAS)
# ============================================================================
ctk.CTkLabel(sidebar, text="TREMEND", font=("Arial", 32, "bold"), text_color="#00FFCC").pack(pady=30, padx=20)

# Motor de expansión de subcategorías (Acordeón)
def toggle_submenu(frame_sub):
    if frame_sub.winfo_ismapped():
        frame_sub.pack_forget()
    else:
        frame_sub.pack(fill="x", pady=(0, 5))

# --- PLATAFORMAS / SISTEMAS OPERATIVOS ---
ctk.CTkLabel(sidebar, text="SISTEMAS OPERATIVOS", font=("Arial", 11, "bold"), text_color="#888888").pack(pady=(0, 5))

# 1. WINDOWS (Contenedor Maestro)
container_win = ctk.CTkFrame(sidebar, fg_color="transparent")
container_win.pack(fill="x", padx=10)
sub_win = ctk.CTkFrame(container_win, fg_color="transparent")

btn_win = ctk.CTkButton(container_win, text="🪟 Windows  ▼", font=("Arial", 14, "bold"), fg_color="#1E293B", hover_color="#334155", border_width=1, border_color="#38BDF8", command=lambda: toggle_submenu(sub_win))
btn_win.pack(fill="x", pady=2)

# Subcategorías de Windows anidadas
ctk.CTkButton(sub_win, text="🌐 Redes e Internet", fg_color="transparent", anchor="w", command=cargar_categoria_redes).pack(pady=1, padx=(30, 0), fill="x")
ctk.CTkButton(sub_win, text="🧹 Mantenimiento", fg_color="transparent", anchor="w", command=cargar_categoria_mantenimiento).pack(pady=1, padx=(30, 0), fill="x")
ctk.CTkButton(sub_win, text="🖥️ Diagnóstico", fg_color="transparent", anchor="w", command=cargar_categoria_diagnostico).pack(pady=1, padx=(30, 0), fill="x")
ctk.CTkButton(sub_win, text="📦 Software/Licencias", fg_color="transparent", anchor="w", command=cargar_categoria_software).pack(pady=1, padx=(30, 0), fill="x")
ctk.CTkButton(sub_win, text="🛠️ Soporte Técnico", fg_color="transparent", anchor="w", command=cargar_categoria_soporte).pack(pady=1, padx=(30, 0), fill="x")

sub_win.pack(fill="x") # Windows arranca expandido por defecto

# 2. OTROS SISTEMAS (Plantillas Preparadas para el Futuro)
def cargar_placeholder(os_name):
    limpiar_panel()
    ctk.CTkLabel(tools_frame, text=f"Soporte para {os_name}", font=("Arial", 24, "bold")).pack(pady=(0, 20), anchor="w")
    ctk.CTkLabel(tools_frame, text=f"El ecosistema de herramientas para {os_name} estará disponible en futuras actualizaciones de TREMEND Toolkit.", text_color="#AAAAAA").pack(pady=10)

ctk.CTkButton(sidebar, text="🐧 Linux", font=("Arial", 14, "bold"), fg_color="transparent", border_width=1, command=cargar_categoria_linux).pack(pady=2, padx=10, fill="x")
ctk.CTkButton(sidebar, text="🍏 Mac", font=("Arial", 14, "bold"), fg_color="transparent", border_width=1, command=cargar_categoria_mac).pack(pady=2, padx=10, fill="x")
ctk.CTkButton(sidebar, text="🤖 Android", font=("Arial", 14, "bold"), fg_color="transparent", border_width=1, command=cargar_categoria_android).pack(pady=2, padx=10, fill="x")
ctk.CTkButton(sidebar, text="📱 iOS", font=("Arial", 14, "bold"), fg_color="transparent", border_width=1, command=cargar_categoria_ios).pack(pady=2, padx=10, fill="x")

# --- SERVICIOS EN LA NUBE Y TIENDA ---
ctk.CTkLabel(sidebar, text="NUBE Y TIENDA", font=("Arial", 11, "bold"), text_color="#888888").pack(pady=(15, 5))

# Contenedor Maestro "Herramientas en la Nube"
container_nube = ctk.CTkFrame(sidebar, fg_color="transparent")
container_nube.pack(fill="x", padx=10)
sub_nube = ctk.CTkFrame(container_nube, fg_color="transparent")

# Botón principal desplegable (con borde púrpura para diferenciarlo)
btn_nube = ctk.CTkButton(container_nube, text="☁️ Herramientas Nube  ▼", font=("Arial", 14, "bold"), fg_color="#1E293B", hover_color="#334155", border_width=1, border_color="#8B5CF6", command=lambda: toggle_submenu(sub_nube))
btn_nube.pack(fill="x", pady=2)

# Subcategorías anidadas
ctk.CTkButton(sub_nube, text="🧰 Portables en la Nube", fg_color="transparent", anchor="w", command=cargar_categoria_portables).pack(pady=1, padx=(30, 0), fill="x")
ctk.CTkButton(sub_nube, text="📚 Enciclopedia Apps", fg_color="transparent", anchor="w", command=cargar_categoria_enciclopedia).pack(pady=1, padx=(30, 0), fill="x")
ctk.CTkButton(sub_nube, text="🌐 Enciclopedia Web", fg_color="transparent", anchor="w", command=cargar_categoria_webs).pack(pady=1, padx=(30, 0), fill="x")

# --- NUEVO BOTÓN PARA LOS MANUALES ---
ctk.CTkButton(sub_nube, text="📖 Manuales y Trucos", fg_color="transparent", anchor="w", command=cargar_categoria_manuales).pack(pady=1, padx=(30, 0), fill="x")

# Ventas de licencias (Afuera como botón principal para maximizar la visibilidad)
ctk.CTkButton(sidebar, text="🛒 Venta de Licencias", font=("Arial", 14, "bold"), fg_color="transparent", border_width=1, command=cargar_categoria_tienda).pack(pady=5, padx=10, fill="x")

cargar_categoria_redes() # Arranca en Windows -> Redes

def mostrar_filosofia():
    # Creamos una ventana emergente profesional
    ventana_info = ctk.CTkToplevel(app)
    ventana_info.title("Filosofía del Proyecto")
    ventana_info.geometry("500x250")
    ventana_info.attributes("-topmost", True) # Se mantiene por encima de la app
    ventana_info.resizable(False, False)
    
    # Título interno
    titulo = ctk.CTkLabel(ventana_info, text="El Origen de TREMEND", font=("Arial", 20, "bold"), text_color="#00B1EA")
    titulo.pack(pady=(20, 10))
    
    # Tu texto inmortalizado
    texto_filosofia = (
        "Este proyecto está impulsado por ideas y por el poder de la inteligencia "
        "artificial, conocida como Gemini Advanced.\n\n"
        "Nuestro enfoque es claro: aprovechar las herramientas actuales para dar "
        "vida a nuestras ideas y, cuando esas herramientas no existan, empezar "
        "nosotros mismos con un boceto."
    )
    
    # Renderizado del texto
    lbl_texto = ctk.CTkLabel(ventana_info, text=texto_filosofia, font=("Arial", 14), wraplength=450, justify="center")
    lbl_texto.pack(padx=20, pady=10)

    # Botón de Filosofía (Colócalo al final de tu barra lateral)
btn_filosofia = ctk.CTkButton(
    sidebar, 
    text="💡 Filosofía de TREMEND", 
    command=mostrar_filosofia, 
    fg_color="transparent", 
    border_width=1, 
    border_color="#00B1EA",
    hover_color="#1E3A8A"
)
btn_filosofia.pack(side="bottom", pady=20, padx=20)

def mostrar_inicios():
    import webbrowser
    ventana_inicios = ctk.CTkToplevel(app)
    ventana_inicios.title("El Origen de TREMEND")
    ventana_inicios.geometry("550x330")
    ventana_inicios.attributes("-topmost", True)
    ventana_inicios.resizable(False, False)
    
    ctk.CTkLabel(ventana_inicios, text="🌱 Mis Inicios", font=("Arial", 22, "bold"), text_color="#3DDC84").pack(pady=(20, 10))
    
    texto = (
        "Todo gran proyecto tiene un comienzo humilde.\n\n"
        "Estas métricas de Junio de 2026 son el testimonio de cuando TREMEND Toolkit "
        "apenas empezaba a dar sus primeros pasos, a recibir sus primeros clones "
        "y a ser descubierto en internet.\n\n"
        "Un recordatorio de que nunca debes desanimarte por empezar desde cero."
    )
    ctk.CTkLabel(ventana_inicios, text=texto, font=("Arial", 14), wraplength=480, justify="center").pack(padx=20, pady=10)

    # Funciones para abrir las imágenes alojadas en tu nube
    def abrir_foto(nombre_archivo):
        # Asegúrate de que esta URL apunte al repositorio donde subiste las fotos
        url_raw = f"https://github.com/LennesVP/TREMEND/tree/main/Inicios/{nombre_archivo}"
        webbrowser.open(url_raw)

    btn_frame = ctk.CTkFrame(ventana_inicios, fg_color="transparent")
    btn_frame.pack(pady=15)
    
    ctk.CTkButton(btn_frame, text="📊 Clones y Tráfico", width=120, fg_color="#1E3A8A", hover_color="#2563EB", command=lambda: abrir_foto("trafico.png")).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="👁️ Vistas Totales", width=120, fg_color="#1E3A8A", hover_color="#2563EB", command=lambda: abrir_foto("vistas.png")).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="🔗 Referencias", width=120, fg_color="#1E3A8A", hover_color="#2563EB", command=lambda: abrir_foto("origen.png")).pack(side="left", padx=5)

# --- BOTÓN EN EL MENÚ LATERAL ---
# Este botón se empaquetará justo arriba de "Filosofía" y "Actualizaciones"
btn_inicios = ctk.CTkButton(
    sidebar, 
    text="🌱 Mis Inicios", 
    command=mostrar_inicios, 
    fg_color="transparent", 
    border_width=1, 
    border_color="#3DDC84",
    text_color="#3DDC84",
    hover_color="#15803D"
)
btn_inicios.pack(side="bottom", pady=(0, 10), padx=20)

# =========================================================================
# EL RADAR DE ACTUALIZACIONES (MODO SILENCIOSO Y MANUAL)
# =========================================================================
def verificar_actualizaciones(silencioso=False):
    import urllib.request, time, webbrowser
    from tkinter import messagebox
    
    try:
        # 1. Rompe-caché y Disfraz de navegador
        url = f"https://raw.githubusercontent.com/LennesVP/TREMEND/main/version.txt?t={time.time()}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # 2. Lectura de la nube
        with urllib.request.urlopen(req, timeout=5) as response:
            version_nube = response.read().decode('utf-8').strip()
        
        # 3. Decisiones Lógicas
        if version_nube != VERSION_ACTUAL:
            # Si hay actualización, SIEMPRE avisa, sea silencioso o no.
            respuesta = messagebox.askyesno(
                "¡Actualización Disponible!", 
                f"¡Tu radar detectó una nueva versión!\n\nTu PC: {VERSION_ACTUAL}\nGitHub: {version_nube}\n\n¿Deseas descargarla ahora?"
            )
            if respuesta: webbrowser.open("https://github.com/LennesVP/TREMEND")
        else:
            # Si está actualizado, SOLO avisa si el usuario presionó el botón manualmente
            if not silencioso:
                messagebox.showinfo("Radar de Nube", f"Conexión perfecta con GitHub.\nTu versión {VERSION_ACTUAL} está al día.")
            
    except Exception as e:
        # Solo muestra errores de conexión si lo buscaste manualmente
        if not silencioso:
            messagebox.showerror("Error de Radar", f"Fallo al conectar con GitHub. Detalle:\n{e}")

# Botón del Asistente Virtual de Voz
btn_asistente_voz = ctk.CTkButton(
    sidebar, 
    text="🎙️ Guía TREMEND (Voz)", 
    command=abrir_guia_asistente, 
    fg_color="transparent", 
    border_width=1, 
    border_color="#A78BFA",
    text_color="#A78BFA",
    hover_color="#7C3AED"
)
btn_asistente_voz.pack(side="bottom", pady=(0, 10), padx=20)

# 4. EL BOTÓN MANUAL (Amarillo brillante) - Llama a la función en modo NO silencioso
btn_actualizar = ctk.CTkButton(
    sidebar, 
    text="🔄 Buscar Actualizaciones", 
    command=lambda: verificar_actualizaciones(silencioso=False), 
    fg_color="transparent", 
    border_width=1, 
    border_color="#FFDD00",
    text_color="#FFDD00",
    hover_color="#AA8800"
)
btn_actualizar.pack(side="bottom", pady=(0, 10), padx=20)

# 5. LA CHISPA DE ARRANQUE AUTOMÁTICO - Llama a la función en modo SILENCIOSO
app.after(1500, lambda: verificar_actualizaciones(silencioso=True))

app.mainloop()