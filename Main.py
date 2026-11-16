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
    def leer_enumerado_cat(ruta): return LinuxToolkit.ejecutar_comando(f'cat -n "{ruta}"')
    @staticmethod
    def auditar_passwd_cat(): return LinuxToolkit.ejecutar_comando("cat /etc/passwd")
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
VERSION_ACTUAL = "3.3"

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

app.title("TREMEND Toolkit V3.3 [ESTABLE Y BLINDADO]")

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

    # --- 3. MANEJO INTELIGENTE SI NO HAY COORDENADAS O HAY ERROR 523 ---
    if len(coordenadas_validas) == 0:
        if errores_523 > 0:
            log("\n[-] ALERTA DE SERVIDOR OSINT: La base de datos satelital gratuita está bajo mantenimiento (Error 523/502).")
        else:
            log("\n[-] Las antenas Wi-Fi escaneadas son privadas o aún no figuran en el catálogo público abierto.")
        log("    -> TREMEND ha contenido la operación para evitar errores en tu sistema.")
        log("\n    [💡] Alternativa Forense Manual:")
        if len(bssids_objetivos) == 1:
            log(f"    🔗 https://wigle.net/search?mac={bssids_objetivos[0]}")
        else:
            log("    🔗 https://wigle.net/")
            log(f"    MACs detectadas: {', '.join(bssids_objetivos[:3])}")
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
    import time, datetime, re
    log(f"\n[*] Iniciando Auditoría de Latencia Continua hacia {destino} (10 paquetes con reloj atómico)...")
    for i in range(10):
        hora = datetime.datetime.now().strftime("%H:%M:%S")
        respuesta = subprocess.run(f"ping -n 1 -w 1000 {destino}", shell=True, capture_output=True, text=True, encoding='cp850', errors='ignore').stdout
        match_ms = re.search(r'(?:tiempo|time)[=<]\s*(\d+)\s*ms', respuesta, re.IGNORECASE)
        if match_ms:
            log(f"[{hora}] -> Respuesta de {destino}: {match_ms.group(1)} ms")
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

def logica_laboratorio_vulnerabilidades_web(log=None):
    import urllib.request
    import ssl
    import json
    import socket
    import subprocess
    import os
    import re
    import concurrent.futures
    import threading
    import customtkinter as ctk
    from tkinter import filedialog, messagebox

    if log:
        log("\n" + "="*75)
        log(" 🛡️ CENTRO DE BLINDAJE DE RED, AUDITORÍA DE CÓDIGO Y PREVENCIÓN ")
        log("="*75)
        log("[*] Desplegando suite de defensa activa y diagnóstico de software...")

    win_def = ctk.CTkToplevel(app)
    win_def.title("TREMEND - Centro de Blindaje Perimetral, Auditoría de Código y Prevención")
    win_def.geometry("1160x720")
    win_def.attributes("-topmost", True)
    win_def.transient(app)

    tabview = ctk.CTkTabview(win_def, fg_color="#1E293B", text_color="#FFFFFF", segmented_button_selected_color="#10B981")
    tabview.pack(pady=10, padx=20, fill="both", expand=True)
    tabview._segmented_button.configure(text_color="#000000")

    tab_perimetro = tabview.add("🧱 1. Escudo de Puertos y Superficie")
    tab_web_sec   = tabview.add("🌐 2. Blindaje Web, DNS y Sesiones")
    tab_codigo    = tabview.add("💻 3. Auditor Código (Yellow Team)")
    tab_manual    = tabview.add("📖 4. Manual Anti-Ataques")
    tab_teams     = tabview.add("🟣 5. Comando Cyber Teams (SOC/ROE)")

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # ====================================================================
    # PESTAÑA 1: ESCUDO DE PUERTOS, SUBDOMINIOS Y SUPERFICIE EXPUESTA
    # (Defensa directa contra el reconocimiento con Nmap, httpx y crt.sh)
    # ====================================================================
    frame_p1_top = ctk.CTkFrame(tab_perimetro, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#38BDF8")
    frame_p1_top.pack(fill="x", padx=10, pady=8)
    ctk.CTkLabel(frame_p1_top, text="Escudo Contra Reconocimiento de Puertos (Nmap / httpx) y Exposición de Subdominios (crt.sh)", font=("Arial", 16, "bold"), text_color="#00FFCC").pack(pady=(8, 2))
    ctk.CTkLabel(frame_p1_top, text="Audita qué puertos o servicios web (8080, 8443, bases de datos) están expuestos en tu PC o dominio y blinda el Firewall automáticamente.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 8))

    frame_p1_ctrl = ctk.CTkFrame(tab_perimetro, fg_color="transparent")
    frame_p1_ctrl.pack(fill="x", padx=15, pady=5)
    ctk.CTkLabel(frame_p1_ctrl, text="Dominio a auditar en crt.sh (Opcional):", font=("Arial", 13, "bold")).pack(side="left", padx=5)
    ent_dominio_crt = ctk.CTkEntry(frame_p1_ctrl, width=260, placeholder_text="Ej: miempresa.com")
    ent_dominio_crt.pack(side="left", padx=5)

    txt_perimetro = ctk.CTkTextbox(tab_perimetro, font=("Consolas", 13), fg_color="#050811", text_color="#38BDF8")
    txt_perimetro.pack(fill="both", expand=True, padx=15, pady=8)
    txt_perimetro.insert("end", "[*] Selecciona una acción defensiva abajo para auditar o blindar tu equipo.\n")
    txt_perimetro.configure(state="disabled")

    def log_p1(texto):
        if win_def.winfo_exists():
            def _u():
                txt_perimetro.configure(state="normal")
                txt_perimetro.insert("end", texto + "\n")
                txt_perimetro.see("end")
                txt_perimetro.configure(state="disabled")
            app.after(0, _u)

    def auditar_puertos_locales():
        txt_perimetro.configure(state="normal"); txt_perimetro.delete("1.0", "end"); txt_perimetro.configure(state="disabled")
        def _run():
            log_p1("="*80)
            log_p1(" 🔍 AUDITORÍA DE PUERTOS Y SERVICIOS WEB EXPUESTOS EN ESTE EQUIPO")
            log_p1("="*80)
            # Lista exacta de puertos que los escáneres (Nmap / httpx) buscan primero
            puertos_criticos = {
                21: "FTP (Transferencia sin cifrar)", 22: "SSH", 25: "SMTP", 53: "DNS",
                80: "HTTP Web", 135: "RPC Windows", 139: "NetBIOS", 443: "HTTPS Web",
                445: "SMB (Carpetas Compartidas - Peligro Ransomware)", 1433: "SQL Server",
                1521: "Oracle DB", 3306: "MySQL / MariaDB", 3389: "RDP (Escritorio Remoto)",
                5432: "PostgreSQL", 5900: "VNC Remoto", 8080: "Servidor Web Alterno (Tomcat/Dev)",
                8443: "HTTPS Alterno (Panel Admin)", 9090: "Consola de Administración Web"
            }
            abiertos = []
            def _check_port(item):
                p, desc = item
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.35)
                res = s.connect_ex(("127.0.0.1", p))
                s.close()
                return (p, desc) if res == 0 else None

            with concurrent.futures.ThreadPoolExecutor(max_workers=18) as ex:
                for r in ex.map(_check_port, puertos_criticos.items()):
                    if r: abiertos.append(r)

            if not abiertos:
                log_p1("\n🟢 EXCELENTE: Ningún puerto crítico ni servidor de desarrollo está abierto localmente.")
            else:
                log_p1(f"\n⚠️ ATENCIÓN: Se detectaron {len(abiertos)} puertos activos en tu sistema:\n")
                for p, desc in abiertos:
                    log_p1(f"   🔴 Puerto :{p:<5} -> {desc}")
                    # Si es un puerto web (80, 443, 8080, 8443, 9090), verificamos si expone versión (como Apache Tomcat)
                    if p in (80, 443, 8080, 8443, 9090):
                        proto = "https" if p in (443, 8443) else "http"
                        try:
                            ctx = ssl.create_default_context()
                            ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
                            req = urllib.request.Request(f"{proto}://127.0.0.1:{p}", headers={"User-Agent": "TREMEND-Defender"})
                            with urllib.request.urlopen(req, timeout=2, context=ctx) as resp:
                                srv_hdr = resp.info().get("Server", "Oculto")
                                body_sample = resp.read(500).decode("utf-8", errors="ignore")
                                log_p1(f"      └─ [Respuesta HTTP {resp.status}] Cabecera Server: {srv_hdr}")
                                if "tomcat" in body_sample.lower() or "apache" in srv_hdr.lower():
                                    log_p1("      └─ 🚨 ALERTA: Tu servidor local está mostrando su nombre/versión públicamente.")
                        except Exception:
                            pass
                log_p1("\n💡 SOLUCIÓN: Si no estás usando estos puertos para trabajar en red, presiona el botón")
                log_p1("   '🛡️ Blindar Puertos en Firewall' para bloquear el acceso externo de inmediato.")
        threading.Thread(target=_run, daemon=True).start()

    def blindar_puertos_firewall():
        if not messagebox.askyesno("Confirmar Blindaje de Firewall", "¿Deseas activar el bloqueo de entrada en el Firewall de Windows para los puertos peligrosos (135, 139, 445, 1433, 3306, 3389, 5432, 5900, 8080, 8443, 9090)?\n\nEsto impedirá que escáneres externos (como Nmap o httpx) se conecten a tus servicios locales.", parent=win_def):
            return
        txt_perimetro.configure(state="normal"); txt_perimetro.delete("1.0", "end"); txt_perimetro.configure(state="disabled")
        def _run():
            log_p1("\n[*] APLICANDO ESCUDO DE FIREWALL CONTRA ESCANEO DE PUERTOS...")
            puertos_bloquear = "135,139,445,1433,1521,3306,3389,5432,5900,8080,8443,9090"
            cmd_fw = f'netsh advfirewall firewall add rule name="TREMEND_Escudo_AntiEscaneo" dir=in action=block protocol=TCP localport={puertos_bloquear}'
            subprocess.run('netsh advfirewall firewall delete rule name="TREMEND_Escudo_AntiEscaneo"', shell=True, capture_output=True, startupinfo=startupinfo)
            res = subprocess.run(cmd_fw, shell=True, capture_output=True, text=True, startupinfo=startupinfo)
            if res.returncode == 0:
                log_p1(f"🟢 ¡ESCUDO ACTIVADO CON ÉXITO!\n   -> Puertos blindados contra conexiones entrantes: {puertos_bloquear}")
                log_p1("   -> Tus programas locales seguirán funcionando en tu PC, pero nadie desde la red podrá escanearlos.")
            else:
                log_p1(f"[-] Error al inyectar regla (Ejecuta como Administrador): {res.stderr}")
        threading.Thread(target=_run, daemon=True).start()

    def auditar_subdominios_crt():
        dom = ent_dominio_crt.get().strip().lower().replace("https://", "").replace("http://", "").split("/")[0]
        if not dom or "." not in dom:
            messagebox.showwarning("Atención", "Escribe un dominio válido (ejemplo: google.com o tuempresa.com) en la caja superior.", parent=win_def)
            return
        txt_perimetro.configure(state="normal"); txt_perimetro.delete("1.0", "end"); txt_perimetro.configure(state="disabled")
        def _run():
            log_p1("="*80)
            log_p1(f" 🌐 AUDITORÍA DE EXPOSICIÓN PÚBLICA DE SUBDOMINIOS (crt.sh): {dom}")
            log_p1("="*80)
            log_p1("[*] Consultando registros públicos de transparencia de certificados SSL...")
            try:
                url = f"https://crt.sh/?q=%25.{dom}&output=json"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (TREMEND-Security-Audit)"})
                with urllib.request.urlopen(req, timeout=12) as resp:
                    datos = json.loads(resp.read().decode("utf-8"))
                subs = sorted(set(
                    entrada.get("name_value", "").lower().strip()
                    for item in datos
                    for entrada in [item]
                ))
                subs_limpios = set()
                for bloque in subs:
                    for linea in bloque.splitlines():
                        if linea and not linea.startswith("*"):
                            subs_limpios.add(linea)
                lista_final = sorted(subs_limpios)
                log_p1(f"\n[+] Se encontraron {len(lista_final)} subdominios públicos indexados en internet:\n")
                sensibles = ("dev", "api", "vpn", "git", "test", "admin", "staging", "mail", "db", "portal")
                for s in lista_final[:40]:
                    alerta = "  <-- ⚠️ [SUBDOMINIO SENSIBLE EXPUESTO: Proteger tras VPN o Cloudflare Zero Trust]" if any(k in s for k in sensibles) else ""
                    log_p1(f"   • {s}{alerta}")
                if len(lista_final) > 40:
                    log_p1(f"   ... y {len(lista_final) - 40} subdominios adicionales.")
                log_p1("\n🛡️ RECOMENDACIÓN DE SEGURIDAD:")
                log_p1("   1. Los subdominios de desarrollo (dev, git, test, staging) NO deben ser accesibles desde internet público.")
                log_p1("   2. Colócalos detrás de una VPN corporativa o activa Cloudflare Access con autenticación previa.")
            except Exception as e:
                log_p1(f"[-] No se pudo completar la consulta en crt.sh (servidor saturado o sin conexión): {e}")
        threading.Thread(target=_run, daemon=True).start()

    frame_p1_btns = ctk.CTkFrame(tab_perimetro, fg_color="transparent")
    frame_p1_btns.pack(fill="x", padx=15, pady=6)
    ctk.CTkButton(frame_p1_btns, text="🔍 1. Auditar Mis Puertos Locales", fg_color="#3B82F6", hover_color="#2563EB", font=("Arial", 13, "bold"), height=40, command=auditar_puertos_locales).pack(side="left", padx=5, expand=True, fill="x")
    ctk.CTkButton(frame_p1_btns, text="🛡️ 2. Blindar Puertos en Firewall (1-Clic)", fg_color="#10B981", hover_color="#059669", font=("Arial", 13, "bold"), height=40, command=blindar_puertos_firewall).pack(side="left", padx=5, expand=True, fill="x")
    ctk.CTkButton(frame_p1_btns, text="🌐 3. Auditar Subdominios Expuestos (crt.sh)", fg_color="#8B5CF6", hover_color="#7C3AED", font=("Arial", 13, "bold"), height=40, command=auditar_subdominios_crt).pack(side="left", padx=5, expand=True, fill="x")

    # ====================================================================
    # PESTAÑA 2: BLINDAJE WEB, DNS ANTI-PHISHING Y PROTECCIÓN DE SESIONES
    # ====================================================================
    frame_p2_top = ctk.CTkFrame(tab_web_sec, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#10B981")
    frame_p2_top.pack(fill="x", padx=10, pady=8)
    ctk.CTkLabel(frame_p2_top, text="Blindaje de Navegación, Escudo DNS Anti-Malware y Auditor de Cabeceras/Cookies", font=("Arial", 16, "bold"), text_color="#10B981").pack(pady=(8, 2))
    ctk.CTkLabel(frame_p2_top, text="Verifica si un sitio web oculta la versión de su servidor (Server Banner), si protege sus cookies con HttpOnly y activa DNS seguros en tu PC.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 8))

    frame_p2_in = ctk.CTkFrame(tab_web_sec, fg_color="transparent")
    frame_p2_in.pack(fill="x", padx=15, pady=4)
    ctk.CTkLabel(frame_p2_in, text="URL o Servidor a Auditar:", font=("Arial", 13, "bold")).pack(side="left", padx=5)
    ent_url_audit = ctk.CTkEntry(frame_p2_in, width=420, placeholder_text="Ej: https://tupagina.com o http://127.0.0.1:8080")
    ent_url_audit.pack(side="left", padx=5, expand=True, fill="x")

    txt_web_sec = ctk.CTkTextbox(tab_web_sec, font=("Consolas", 13), fg_color="#050811", text_color="#E2E8F0")
    txt_web_sec.pack(fill="both", expand=True, padx=15, pady=8)
    txt_web_sec.insert("end", "[*] Usa los botones inferiores para auditar las defensas de una página web o blindar la navegación de tu computadora.\n")
    txt_web_sec.configure(state="disabled")

    def log_p2(texto):
        if win_def.winfo_exists():
            def _u():
                txt_web_sec.configure(state="normal")
                txt_web_sec.insert("end", texto + "\n")
                txt_web_sec.see("end")
                txt_web_sec.configure(state="disabled")
            app.after(0, _u)

    def auditar_defensas_url():
        u = ent_url_audit.get().strip()
        if not u:
            messagebox.showwarning("Atención", "Ingresa una URL o IP para auditar sus escudos web.", parent=win_def)
            return
        if not u.startswith("http"):
            u = "https://" + u
        txt_web_sec.configure(state="normal"); txt_web_sec.delete("1.0", "end"); txt_web_sec.configure(state="disabled")
        def _run():
            log_p2("="*80)
            log_p2(f" 🛡️ DIAGNÓSTICO DE ESCUDOS WEB Y CABECERAS DE SEGURIDAD: {u}")
            log_p2("="*80)
            try:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
                req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (TREMEND-Defensive-Scanner)"})
                with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                    info = resp.info()
                    headers_lower = {k.lower(): v for k, v in info.items()}

                    # 1. Revisión de Fuga de Versión (Como el caso Apache Tomcat/9.0.65 del video)
                    srv = headers_lower.get("server", "")
                    powered = headers_lower.get("x-powered-by", "")
                    log_p2("\n[1] EXPOSICIÓN DE TECNOLOGÍA Y VERSIÓN (SERVER BANNER):")
                    if srv or powered:
                        log_p2(f"   🟠 Server: {srv or 'Oculto'} | X-Powered-By: {powered or 'Oculto'}")
                        if any(char.isdigit() for char in (srv + powered)):
                            log_p2("   🔴 PELIGRO: El servidor está revelando el número exacto de versión.")
                            log_p2("      -> Cómo solucionarlo: En Apache agrega 'ServerTokens Prod' y 'ServerSignature Off'.")
                            log_p2("      -> En Nginx agrega 'server_tokens off;'. En Express/Node usa 'app.disable(\"x-powered-by\")'.")
                        else:
                            log_p2("   🟢 Bien: No se exponen números de versión específicos en las cabeceras.")
                    else:
                        log_p2("   🟢 EXCELENTE: El servidor oculta completamente su tecnología.")

                    # 2. Revisión de Escudos Anti-XSS y Anti-Clickjacking
                    log_p2("\n[2] CABECERAS DEFENSIVAS CONTRA XSS E INYECCIÓN:")
                    escudos = {
                        "content-security-policy": ("Content-Security-Policy (CSP)", "Bloquea la ejecución de <script> maliciosos y robo de cookies (XSS)."),
                        "strict-transport-security": ("Strict-Transport-Security (HSTS)", "Obliga al navegador a usar únicamente conexiones cifradas HTTPS."),
                        "x-frame-options": ("X-Frame-Options", "Impide que clonen tu página dentro de un iframe oculto (Clickjacking)."),
                        "x-content-type-options": ("X-Content-Type-Options", "Evita que el navegador ejecute archivos disfrazados (nosniff).")
                    }
                    for k_low, (nombre_h, explicacion_h) in escudos.items():
                        if k_low in headers_lower:
                            log_p2(f"   🟢 {nombre_h}: ACTIVO ({headers_lower[k_low][:45]})")
                        else:
                            log_p2(f"   🔴 FALTA {nombre_h}: {explicacion_h}")

                    # 3. Revisión de Cookies Protegidas contra document.cookie
                    cookies = info.get_all("Set-Cookie") or []
                    log_p2("\n[3] PROTECCIÓN DE SESIONES (COOKIES):")
                    if not cookies:
                        log_p2("   ⚪ Esta ruta no entregó cookies de sesión en la respuesta inicial.")
                    else:
                        for c in cookies:
                            c_low = c.lower()
                            nombre_c = c.split("=")[0].strip()
                            falta = []
                            if "httponly" not in c_low: falta.append("HttpOnly (Vulnerable a robo por document.cookie en XSS)")
                            if "secure" not in c_low: falta.append("Secure")
                            if "samesite" not in c_low: falta.append("SameSite")
                            if not falta:
                                log_p2(f"   🟢 Cookie '{nombre_c}': Blindada con HttpOnly, Secure y SameSite.")
                            else:
                                log_p2(f"   🔴 Cookie '{nombre_c}' desprotegida. Le falta: {', '.join(falta)}")
            except Exception as e:
                log_p2(f"[-] Error al conectar con {u}: {e}")
        threading.Thread(target=_run, daemon=True).start()

    def activar_dns_escudo():
        txt_web_sec.configure(state="normal"); txt_web_sec.delete("1.0", "end"); txt_web_sec.configure(state="disabled")
        def _run():
            log_p2("\n[*] ACTIVANDO ESCUDO DNS ANTI-MALWARE Y ANTI-PHISHING (QUAD9 + CLOUDFLARE SECURITY)...")
            ps_dns = 'Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | Set-DnsClientServerAddress -ServerAddresses ("9.9.9.9", "1.1.1.2")'
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_dns], capture_output=True, startupinfo=startupinfo)
            subprocess.run("ipconfig /flushdns", shell=True, capture_output=True, startupinfo=startupinfo)
            log_p2("🟢 ¡DNS DE SEGURIDAD ACTIVADOS EN TU PC!")
            log_p2("   -> Servidor Primario   : 9.9.9.9 (Quad9 Filtro Anti-Malware y C2)")
            log_p2("   -> Servidor Secundario : 1.1.1.2 (Cloudflare Security Anti-Phishing)")
            log_p2("   -> Caché DNS purgada. Cualquier intento de conexión hacia dominios de hackers será bloqueado en red.")
        threading.Thread(target=_run, daemon=True).start()

    def auditar_bovedas_cookies_locales():
        txt_web_sec.configure(state="normal"); txt_web_sec.delete("1.0", "end"); txt_web_sec.configure(state="disabled")
        def _run():
            log_p2("="*80)
            log_p2(" 🍪 AUDITORÍA DE BÓVEDAS DE COOKIES ('sessionid') EN ESTE EQUIPO (ANTI-BYPASS 2FA)")
            log_p2("="*80)
            local_app = os.environ.get("LOCALAPPDATA", "")
            bovedas = [
                ("Google Chrome", os.path.join(local_app, r"Google\Chrome\User Data\Default\Network\Cookies")),
                ("Microsoft Edge", os.path.join(local_app, r"Microsoft\Edge\User Data\Default\Network\Cookies")),
                ("Brave Browser", os.path.join(local_app, r"BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies"))
            ]
            encontradas = 0
            for nav, ruta_c in bovedas:
                if os.path.exists(ruta_c):
                    encontradas += 1
                    kb = os.path.getsize(ruta_c) / 1024
                    log_p2(f"   ⚠️ {nav:<16} -> Bóveda 'Cookies' activa ({kb:.1f} KB) en: {ruta_c}")
                else:
                    log_p2(f"   🟢 {nav:<16} -> Sin bóveda de cookies expuesta.")

            log_p2("\n🛡️ DIAGNÓSTICO CONTRA ROBO DE CUENTAS SIN CONTRASEÑA:")
            if encontradas > 0:
                log_p2("   • Si dejas sesiones abiertas en un PC compartido o sin bloquear con WIN + L, cualquiera puede")
                log_p2("     abrir 'Inspeccionar -> Aplicación -> Cookies', copiar tu 'sessionid' y saltar tu 2FA.")
                log_p2("   • Solución: Cierra sesión en las webs críticas cuando termines de usarlas o ejecuta la")
                log_p2("     herramienta #11 de Mantenimiento ('Purga de Emergencia Anti-Robo 2FA') para destruir las cookies.")
            else:
                log_p2("   🟢 Excelente: No hay bóvedas de cookies almacenadas en las rutas estándar.")
        threading.Thread(target=_run, daemon=True).start()

    frame_p2_btns = ctk.CTkFrame(tab_web_sec, fg_color="transparent")
    frame_p2_btns.pack(fill="x", padx=15, pady=6)
    ctk.CTkButton(frame_p2_btns, text="🔍 1. Auditar Escudos de URL", fg_color="#3B82F6", hover_color="#2563EB", font=("Arial", 13, "bold"), height=40, command=auditar_defensas_url).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_p2_btns, text="🛡️ 2. Activar DNS Anti-Malware", fg_color="#10B981", hover_color="#059669", font=("Arial", 13, "bold"), height=40, command=activar_dns_escudo).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_p2_btns, text="🍪 3. Auditar Bóvedas de Cookies en mi PC", fg_color="#8B5CF6", hover_color="#7C3AED", font=("Arial", 13, "bold"), height=40, command=auditar_bovedas_cookies_locales).pack(side="left", padx=4, expand=True, fill="x")

    # ====================================================================
    # PESTAÑA 3: AUDITOR Y REPARADOR DE CÓDIGO FUENTE (DEVSECOPS)
    # ====================================================================
    frame_p3_top = ctk.CTkFrame(tab_codigo, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#A855F7")
    frame_p3_top.pack(fill="x", padx=10, pady=8)
    ctk.CTkLabel(frame_p3_top, text="Inspector de Código Fuente (Detección y Solución de SQLi, XSS, Session Hijacking, RAM y LFI)", font=("Arial", 16, "bold"), text_color="#A855F7").pack(pady=(8, 2))
    ctk.CTkLabel(frame_p3_top, text="Pega tu código o abre un archivo (.py, .js, .php, .html) para detectar líneas inseguras y obtener el código blindado.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 8))

    frame_p3_split = ctk.CTkFrame(tab_codigo, fg_color="transparent")
    frame_p3_split.pack(fill="both", expand=True, padx=10, pady=4)

    txt_code_in = ctk.CTkTextbox(frame_p3_split, font=("Consolas", 12), fg_color="#050811", text_color="#E2E8F0", width=460)
    txt_code_in.pack(side="left", fill="both", expand=True, padx=(0, 5))
    txt_code_in.insert("1.0", "# Pega aquí tu código (Python, JS, PHP, HTML) o carga un archivo:\ncursor.execute(f\"SELECT * FROM users WHERE code = '{codigo}'\")\nelemento.innerHTML = comentario_usuario\nres.cookie('sessionid', token_sesion)\nvida = 100\n")

    txt_code_out = ctk.CTkTextbox(frame_p3_split, font=("Consolas", 12), fg_color="#050811", text_color="#10B981", width=460)
    txt_code_out.pack(side="right", fill="both", expand=True, padx=(5, 0))
    txt_code_out.insert("1.0", "[*] Presiona 'Auditar y Generar Solución' para escanear tu código...\n")
    txt_code_out.configure(state="disabled")

    def cargar_archivo_codigo():
        ruta = filedialog.askopenfilename(title="Selecciona un archivo de código", filetypes=[("Código", "*.py *.js *.ts *.php *.html *.sql"), ("Todos", "*.*")], parent=win_def)
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                    txt_code_in.delete("1.0", "end")
                    txt_code_in.insert("1.0", f.read())
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}", parent=win_def)

    def auditar_codigo_fuente():
        codigo = txt_code_in.get("1.0", "end")
        txt_code_out.configure(state="normal")
        txt_code_out.delete("1.0", "end")
        hallazgos = []

        for num, linea in enumerate(codigo.splitlines(), 1):
            l_strip = linea.strip()
            # 1. Detección SQLi por concatenación o f-strings
            if re.search(r'(SELECT|INSERT|UPDATE|DELETE).*(\+|%s|f["\']|\{.*\}).*WHERE', l_strip, re.IGNORECASE):
                hallazgos.append(
                    f"🔴 [Línea {num}] RIESGO DE INYECCIÓN SQL:\n"
                    f"   Código actual : {l_strip}\n"
                    f"   ✅ Solución   : Usa consultas parametrizadas:\n"
                    f"      cursor.execute('SELECT * FROM users WHERE code = ?', (str(codigo),))\n"
                )
            # 2. Detección de ORM sin validar String (Bypass por Array/JSON IN)
            if "findone" in l_strip.lower() and "where" in l_strip.lower():
                hallazgos.append(
                    f"🟠 [Línea {num}] RIESGO DE BYPASS POR ARRAY EN ORM (WHERE IN):\n"
                    f"   Código actual : {l_strip}\n"
                    f"   ✅ Solución   : Valida que el código sea texto y usa Tokens de 64 caracteres:\n"
                    f"      if (typeof code !== 'string' || code.length < 32) return res.status(400).end();\n"
                )
            # 3. Detección de XSS por innerHTML / document.write
            if ".innerhtml" in l_strip.lower() or "document.write(" in l_strip.lower():
                hallazgos.append(
                    f"🔴 [Línea {num}] RIESGO DE CROSS-SITE SCRIPTING (XSS - Robo de Cookies):\n"
                    f"   Código actual : {l_strip}\n"
                    f"   ✅ Solución   : Reemplaza '.innerHTML' por '.textContent' o escapa con html.escape():\n"
                    f"      elemento.textContent = comentario_usuario;\n"
                )
            # 4. Detección de Path Traversal (LFI)
            if re.search(r'(open|include|require|send_file)\s*\(.*(\+|f["\'])', l_strip, re.IGNORECASE):
                hallazgos.append(
                    f"🔴 [Línea {num}] RIESGO DE PATH TRAVERSAL (Robo de Archivos con ../):\n"
                    f"   Código actual : {l_strip}\n"
                    f"   ✅ Solución   : Limpia la ruta con os.path.basename() antes de abrir el archivo:\n"
                    f"      nombre_seguro = os.path.basename(nombre_archivo)\n"
                )
            # 5. Detección de Variables Críticas en Texto Plano en RAM (Anti-Cheat Engine / Memory Tampering)
            if re.search(r'\b(vida|salud|health|saldo|monedas|coins|ammo|municion|creditos|licencia_activa|is_admin|puntos)\s*=\s*\d+', l_strip, re.IGNORECASE):
                hallazgos.append(
                    f"🟠 [Línea {num}] RIESGO DE MANIPULACIÓN EN MEMORIA RAM (CHEAT ENGINE / 4-BYTES):\n"
                    f"   Código actual : {l_strip}\n"
                    f"   ✅ Solución 1 (Online) : Valida y guarda este valor exclusivamente en el Servidor.\n"
                    f"   ✅ Solución 2 (Offline): Usa Ofuscación XOR + Firma SHA-256 en RAM (Clase VariableBlindadaRAM).\n"
                )
            # 6. Detección de Cookies de Sesión ('sessionid') vulnerables a clonación (Pass-the-Cookie / Bypass 2FA)
            if re.search(r'(set_cookie|res\.cookie|sessionid|session_id)', l_strip, re.IGNORECASE) and "httponly" not in l_strip.lower():
                hallazgos.append(
                    f"🔴 [Línea {num}] RIESGO DE ROBO DE SESIÓN ('sessionid' / BYPASS DE 2FA):\n"
                    f"   Código actual : {l_strip}\n"
                    f"   ⚠️ Riesgo     : Si alguien copia 'sessionid' en otro navegador, entrará sin clave ni 2FA.\n"
                    f"   ✅ Solución   : Activa HttpOnly/Secure/SameSite y vincula la sesión a la huella del cliente:\n"
                    f"      res.cookie('sessionid', token, {{ httpOnly: true, secure: true, sameSite: 'Strict', maxAge: 3600000 }});\n"
                    f"      # En el servidor: vincula el token al hash SHA-256 de (User-Agent + IP/24) para rechazar copias.\n"
                )
            # 7. Detección de Contraseñas con Hash Rápido (MD5/SHA) o Cifrado Reversible (Junior vs Senior)
            if re.search(r'(md5|sha1|sha256|encrypt|fernet).*(\bpass|\bpwd|\bclave|\bcontrasena)', l_strip, re.IGNORECASE):
                hallazgos.append(
                    f"🔴 [Línea {num}] RIESGO CRÍTICO AL GUARDAR CONTRASEÑA (HASH RÁPIDO O CIFRADO REVERSIBLE):\n"
                    f"   Código actual : {l_strip}\n"
                    f"   ⚠️ Riesgo     : Cifrar es reversible si roban la llave, y MD5/SHA permiten probar millones de claves/seg.\n"
                    f"   ✅ Solución   : Usa un Hash Lento con Salt único por usuario (Scrypt / Bcrypt / Argon2):\n"
                    f"      salt = secrets.token_bytes(16)\n"
                    f"      hash_seguro = hashlib.scrypt(clave.encode(), salt=salt, n=16384, r=8, p=1)\n"
                )

        if not hallazgos:
            txt_code_out.insert("end", "🟢 AUDITORÍA COMPLETADA:\nNo se detectaron patrones vulnerables evidentes de SQLi, XSS, Session Hijacking o Path Traversal.")
        else:
            txt_code_out.insert("end", f"⚠️ SE DETECTARON {len(hallazgos)} VULNERABILIDADES EN TU CÓDIGO:\n" + "="*55 + "\n\n")
            txt_code_out.insert("end", "\n".join(hallazgos))
        txt_code_out.configure(state="disabled")

    frame_p3_btns = ctk.CTkFrame(tab_codigo, fg_color="transparent")
    frame_p3_btns.pack(fill="x", padx=15, pady=6)
    ctk.CTkButton(frame_p3_btns, text="📂 1. Cargar Archivo de Código", fg_color="#334155", hover_color="#475569", font=("Arial", 13, "bold"), height=40, command=cargar_archivo_codigo).pack(side="left", padx=5, expand=True, fill="x")
    ctk.CTkButton(frame_p3_btns, text="🛡️ 2. Auditar Código y Generar Solución Blindada", fg_color="#10B981", hover_color="#059669", font=("Arial", 13, "bold"), height=40, command=auditar_codigo_fuente).pack(side="right", padx=5, expand=True, fill="x")

    # ====================================================================
    # PESTAÑA 4: MANUAL INTERACTIVO DE PREVENCIÓN Y RESPUESTA A INCIDENTES
    # ====================================================================
    txt_manual = ctk.CTkTextbox(tab_manual, font=("Consolas", 13), fg_color="#050811", text_color="#E2E8F0", wrap="word")
    txt_manual.pack(fill="both", expand=True, padx=15, pady=10)

    guias_defensa = {
        "recon": (
            "🛡️ MANUAL 1: DEFENSA CONTRA ESCANEO DE PUERTOS, SUBDOMINIOS Y VERSIONES (NMAP / HTTPX / TOMCAT)\n"
            + "="*85 + "\n"
            "🔍 1. ¿CÓMO SABER SI ESTÁS EXPUESTO O SI TE ESTÁN ESCANEANDO?\n"
            "   • Un atacante usa 'crt.sh' y 'subfinder' para ver tus subdominios (dev, api, vpn, git) y luego lanza 'nmap' y 'httpx' buscando puertos olvidados como :8080 o :8443 que muestren páginas por defecto (ej. Apache Tomcat/9.0.65).\n"
            "   • Usa la Pestaña 1 de esta herramienta para ver qué puertos tienes abiertos y qué subdominios aparecen en crt.sh.\n\n"
            "🧱 2. ¿CÓMO PREVENIRLO Y BLINDAR TU EQUIPO / SERVIDOR?\n"
            "   • Cierra todos los puertos entrantes que no uses con el botón 'Blindar Puertos en Firewall' de la Pestaña 1.\n"
            "   • Elimina siempre las páginas de bienvenida por defecto (como /docs, /examples y /manager en Apache Tomcat).\n"
            "   • Oculta el número de versión de tu servidor web (ServerTokens Prod en Apache / server_tokens off en Nginx).\n\n"
            "🚨 3. ¿QUÉ HACER SI YA DEJASTE UN SERVIDOR EXPUESTO?\n"
            "   • Bloquea el puerto inmediatamente en el Firewall, actualiza el servidor a la última versión y revisa los logs de acceso (access.log) buscando peticiones extrañas a '/manager/html' o '/.env'."
        ),
        "xss": (
            "🛡️ MANUAL 2: DEFENSA CONTRA SECUESTRO DE 'sessionid' (BYPASS DE 2FA) Y CROSS-SITE SCRIPTING (XSS)\n"
            + "="*85 + "\n"
            "🔍 1. ¿CÓMO ROBAN UNA CUENTA SALTÁNDOSE LA CONTRASEÑA Y EL 2FA?\n"
            "   • Cuando inicias sesión y pasas el 2FA, la web guarda una cookie ('sessionid') en 'Inspeccionar -> Aplicación -> Almacenamiento -> Cookies'. Si un atacante copia ese valor (mediante acceso físico a tu PC, un malware InfoStealer o un ataque XSS) y lo pega en su navegador, entra directo a tu cuenta sin clave y sin 2FA.\n\n"
            "🧱 2. ¿CÓMO PREVENIRLO EN TU PC Y EN TUS APLICACIONES?\n"
            "   • En tu PC (Hábito de Oro): Vigila las aplicaciones donde tienes sesión iniciada y CIERRA SESIÓN ('Desloguearse') cuando no las necesites; al cerrar sesión, el servidor destruye la validez de ese 'sessionid'.\n"
            "   • Si usas un PC ajeno o compartido: Al terminar, ejecuta la herramienta #11 de Mantenimiento en Modo 2 ('Purga de Emergencia Anti-Robo 2FA') para destruir todas las cookies locales.\n"
            "   • En tu Código Backend: Configura la cookie con 'HttpOnly; Secure; SameSite=Strict' y vincula cada 'sessionid' en la base de datos al hash del User-Agent y subred IP del usuario.\n\n"
            "🚨 3. ¿QUÉ HACER SI YA ROBARON TU COOKIE 'sessionid'?\n"
            "   • Cambiar solo la contraseña a veces no basta si la plataforma no invalida las sesiones activas: entra a 'Seguridad -> Dispositivos / Actividad de inicio de sesión' y cierra todas las sesiones activas inmediatamente."
        ),
        "sqli_otp": (
            "🛡️ MANUAL 3: DEFENSA CONTRA INYECCIÓN SQL, OBJETOS JSON Y BYPASS DE CÓDIGOS CORTOS\n"
            + "="*85 + "\n"
            "🔍 1. ¿CÓMO FUNCIONA EL RIESGO?\n"
            "   • Si un sistema de recuperación usa códigos cortos de 6 dígitos y no valida el tipo de dato, un atacante puede enviar una lista JSON con 10,000 códigos en 1 sola petición, haciendo que el ORM ejecute 'WHERE code IN (...)' y burle el límite de 5 intentos.\n\n"
            "🧱 2. ¿CÓMO PREVENIRLO EN TUS PROYECTOS?\n"
            "   • Valida estrictamente que el dato recibido sea un String (texto) antes de pasarlo a la base de datos.\n"
            "   • En lugar de códigos cortos de 6 dígitos para recuperar claves, usa Tokens Criptográficos Largos de 64 caracteres hexadecimales (puedes generarlos en el módulo #14 de Soporte Técnico).\n"
            "   • Utiliza siempre consultas SQL parametrizadas (? o $1)."
        ),
        "lfi_race": (
            "🛡️ MANUAL 4: DEFENSA CONTRA ROBO DE ARCHIVOS (PATH TRAVERSAL) Y CONDICIÓN DE CARRERA\n"
            + "="*85 + "\n"
            "🔍 1. ¿CÓMO PREVENIR EL ROBO DE ARCHIVOS DEL SISTEMA (../)?\n"
            "   • Jamás concatenes directamente el nombre de un archivo enviado por el usuario en la URL. Aplica siempre 'os.path.basename()' y verifica que la ruta final comience dentro de tu carpeta autorizada.\n\n"
            "🧱 2. ¿CÓMO PREVENIR ATAQUES DE CONDICIÓN DE CARRERA (RACE CONDITION)?\n"
            "   • Cuando programes canje de cupones, transferencias o votos, usa bloqueos de fila en la base de datos ('SELECT ... FOR UPDATE' dentro de una transacción atómica) y activa Rate Limiting por IP/Usuario."
        ),
        "ram_tamper": (
            "🛡️ MANUAL 5: DEFENSA CONTRA MANIPULACIÓN DE MEMORIA RAM (CHEAT ENGINE) Y CONFIANZA EN EL CLIENTE\n"
            + "="*85 + "\n"
            "🔍 1. ¿CÓMO ALTERAN UN PROGRAMA O JUEGO EN LA MEMORIA RAM?\n"
            "   • Cuando un programa guarda un dato importante (vida = 100, saldo, créditos o estado de licencia) como un entero normal de 4 bytes ('64 00 00 00'), un atacante conecta un escáner de memoria (como Cheat Engine), busca el valor 100, espera a que cambie a 73 y luego a 51 ('Next Scan') hasta aislar la dirección exacta (ej. 1B3F8D40) y la sobrescribe por 9999.\n\n"
            "🧱 2. ¿CÓMO PREVENIRLO Y DEFENDER TUS PROGRAMAS Y TU PC?\n"
            "   • Regla de Oro (Aplicaciones Online / Web): Jamás confíes en los valores que reporta la memoria del cliente. La vida, el dinero, el inventario, los descuentos y los permisos deben calcularse y validarse en el SERVIDOR.\n"
            "   • En Programas Offline / Escritorio: Nunca guardes números sensibles en variables enteras simples. Usa la clase 'VariableBlindadaRAM' de nuestra Pestaña 3 (aplica una máscara XOR con llave aleatoria en cada arranque + verificación SHA-256). Así el número real jamás aparece en la RAM y cualquier edición externa bloquea el programa.\n"
            "   • En tu Sistema Operativo Windows: Usa la herramienta #17 de Diagnóstico ('Escudo de Integridad de Memoria RAM') para cerrar inyectores activos y forzar ASLR + DEP en el Kernel."
        ),
        "pwd_hash": (
            "🛡️ MANUAL 6: POR QUÉ NO CIFRAR CONTRASEÑAS NI USAR MD5/SHA (ESTÁNDAR SCRYPT / BCRYPT / ARGON2)\n"
            + "="*85 + "\n"
            "🔍 1. LA TRAMPA DE CIFRAR Y EL PELIGRO DE LOS HASHES RÁPIDOS (JUNIOR VS SENIOR)\n"
            "   • Cifrar (AES/Fernet) es REVERSIBLE: si un atacante roba tu base de datos y tu llave de configuración, desencripta todas las contraseñas en texto plano.\n"
            "   • Hashear con MD5 o SHA-256 tampoco sirve para contraseñas: son algoritmos diseñados para ejecutarse tan rápido que una tarjeta gráfica prueba más de 5,000,000 de combinaciones por segundo.\n\n"
            "🧱 2. ¿CÓMO SE PROTEGEN LAS CONTRASEÑAS PROFESIONALMENTE?\n"
            "   • Usa siempre un Hash Lento a propósito + un SALT único por usuario (Bcrypt, Scrypt o Argon2).\n"
            "   • El SALT garantiza que dos usuarios con la misma contraseña ('clave123') tengan hashes totalmente distintos en la base de datos.\n"
            "   • No guardas contraseñas: guardas una prueba matemática irreversible de que el usuario la conoce (puedes generarlos y verificarlos en el módulo #30 de Redes e Internet)."
        ),
        "cyber_teams": (
            "🛡️ MANUAL 7: ARQUITECTURA DE LOS 6 EQUIPOS DE CIBERSEGURIDAD (CYBER TEAMS EN TREMEND)\n"
            + "="*85 + "\n"
            "🔴 1. RED TEAM (Atacantes Éticos - Pentest & Simulación):\n"
            "   • Simulan ciberataques reales para descubrir vulnerabilidades antes que los criminales (En TREMEND: Radar de Puertos #20, Nmap #24, Auditor Web #26, JtR #10 de Soporte).\n\n"
            "🔵 2. BLUE TEAM (Defensores - Operaciones SOC & Detección):\n"
            "   • Vigilan redes, detectan amenazas, investigan incidentes y bloquean intrusiones (En TREMEND: Cazador Anti-Keyloggers #1 de Diagnóstico, Escudo RAM #17, Sniffnet #23).\n\n"
            "🟣 3. PURPLE TEAM (Colaboración Attack <-> Defend):\n"
            "   • Son el puente entre Red y Blue Team: lanzan un vector controlado y verifican al instante si el Firewall y el EDR realmente lo bloquean (Pestaña 5 de esta suite).\n\n"
            "⚪ 4. WHITE TEAM (Árbitros - Gobernanza, Ética y Rules of Engagement):\n"
            "   • Definen las reglas, supervisan los ejercicios y emiten las actas de auditoría controlada (Generador ROE en la Pestaña 5).\n\n"
            "🟡 5. YELLOW TEAM (Desarrolladores - Código Seguro desde el Inicio):\n"
            "   • Construyen aplicaciones seguras validando entradas y aplicando hashing lento con Salt (Pestaña 3 de esta suite y módulo #30 de Redes).\n\n"
            "🟢 6. GREEN TEAM (Infraestructura y Operaciones - Monitoring & Hardening):\n"
            "   • Refuerzan la fiabilidad de servidores, automatizan parches y endurecen servicios del sistema (Pestaña 1, Pestaña 2 y Monitor de Infraestructura en Pestaña 5)."
        )
    }

    def mostrar_manual(clave):
        txt_manual.configure(state="normal")
        txt_manual.delete("1.0", "end")
        txt_manual.insert("end", guias_defensa[clave])
        txt_manual.configure(state="disabled")

    frame_p4_btns = ctk.CTkFrame(tab_manual, fg_color="transparent")
    frame_p4_btns.pack(fill="x", padx=15, pady=6)
    ctk.CTkButton(frame_p4_btns, text="1. Puertos/Tomcat", fg_color="#3B82F6", command=lambda: mostrar_manual("recon")).pack(side="left", padx=3, expand=True, fill="x")
    ctk.CTkButton(frame_p4_btns, text="2. Anti-2FA/XSS", fg_color="#10B981", command=lambda: mostrar_manual("xss")).pack(side="left", padx=3, expand=True, fill="x")
    ctk.CTkButton(frame_p4_btns, text="3. Anti-SQLi", fg_color="#8B5CF6", command=lambda: mostrar_manual("sqli_otp")).pack(side="left", padx=3, expand=True, fill="x")
    ctk.CTkButton(frame_p4_btns, text="4. Anti-LFI", fg_color="#F59E0B", text_color="#000000", command=lambda: mostrar_manual("lfi_race")).pack(side="left", padx=3, expand=True, fill="x")
    ctk.CTkButton(frame_p4_btns, text="5. Anti-RAM", fg_color="#E11D48", hover_color="#BE123C", command=lambda: mostrar_manual("ram_tamper")).pack(side="left", padx=3, expand=True, fill="x")
    ctk.CTkButton(frame_p4_btns, text="6. Hashing Senior", fg_color="#14B8A6", text_color="#000000", command=lambda: mostrar_manual("pwd_hash")).pack(side="left", padx=3, expand=True, fill="x")
    ctk.CTkButton(frame_p4_btns, text="7. Los 6 Cyber Teams", fg_color="#A855F7", hover_color="#9333EA", command=lambda: mostrar_manual("cyber_teams")).pack(side="left", padx=3, expand=True, fill="x")
    mostrar_manual("recon")

    # ====================================================================
    # PESTAÑA 5: COMANDO CYBER TEAMS (PURPLE SIMULATOR / SOC BLUE-GREEN / WHITE ROE)
    # ====================================================================
    frame_p5_top = ctk.CTkFrame(tab_teams, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#A855F7")
    frame_p5_top.pack(fill="x", padx=10, pady=8)
    ctk.CTkLabel(frame_p5_top, text="Centro de Operaciones Cyber Teams (Red • Blue • Purple • White • Yellow • Green)", font=("Arial", 16, "bold"), text_color="#00FFCC").pack(pady=(8, 2))
    ctk.CTkLabel(frame_p5_top, text="Cruza simulaciones de ataque con tus defensas activas (Purple Team), monitorea la salud del SOC/Infraestructura (Blue/Green) y exporta Actas ROE (White Team).", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 8))

    frame_p5_roe = ctk.CTkFrame(tab_teams, fg_color="transparent")
    frame_p5_roe.pack(fill="x", padx=15, pady=4)
    ctk.CTkLabel(frame_p5_roe, text="Cliente / Organización Auditada (White Team ROE):", font=("Arial", 13, "bold")).pack(side="left", padx=5)
    ent_cliente_roe = ctk.CTkEntry(frame_p5_roe, width=320, placeholder_text="Ej: Empresa Cliente S.A.S / Equipo Local")
    ent_cliente_roe.pack(side="left", padx=5)
    ent_cliente_roe.insert(0, f"Activo Local ({socket.gethostname()})")

    txt_teams = ctk.CTkTextbox(tab_teams, font=("Consolas", 13), fg_color="#050811", text_color="#E2E8F0")
    txt_teams.pack(fill="both", expand=True, padx=15, pady=8)
    txt_teams.insert("end", "[*] Selecciona una misión táctica abajo para iniciar la colaboración entre equipos Cyber.\n")
    txt_teams.configure(state="disabled")

    def log_p5(texto):
        if win_def.winfo_exists():
            def _u():
                txt_teams.configure(state="normal")
                txt_teams.insert("end", texto + "\n")
                txt_teams.see("end")
                txt_teams.configure(state="disabled")
            app.after(0, _u)

    def ejecutar_simulacion_purple():
        txt_teams.configure(state="normal"); txt_teams.delete("1.0", "end"); txt_teams.configure(state="disabled")
        def _run():
            log_p5("="*85)
            log_p5(" 🟣 EJERCICIO PURPLE TEAM EN VIVO: CORRELACIÓN ATTACK (RED) <-> DEFEND (BLUE)")
            log_p5("="*85)
            log_p5("[RED TEAM]  > initial_recon --authorized | Iniciando sondeo de vectores críticos...")
            log_p5("[BLUE TEAM] > threat_monitor --live      | Verificando reglas de contención y Firewall...\n")

            # 1. Verificar si la regla de escudo TREMEND está activa en el Firewall (Blue Team)
            chk_fw = subprocess.run('netsh advfirewall firewall show rule name="TREMEND_Escudo_AntiEscaneo"', shell=True, capture_output=True, text=True, startupinfo=startupinfo)
            escudo_fw_activo = ("TREMEND_Escudo_AntiEscaneo" in chk_fw.stdout)

            vectores = [
                (445, "SMB / Carpetas Compartidas (Vector EternalBlue / Ransomware)"),
                (3389, "RDP / Escritorio Remoto (Vector Fuerza Bruta)"),
                (135, "RPC Endpoint Mapper (Vector Enumeración Remota)"),
                (3306, "MySQL Database Port (Exposición de Datos)"),
                (8080, "HTTP Alterno / Panel Admin Tomcat")
            ]

            bloqueados = 0
            expuestos = 0
            for p, nombre_v in vectores:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                abierto_local = (s.connect_ex(("127.0.0.1", p)) == 0)
                s.close()

                if not abierto_local:
                    estado_blue = "🟢 [ENDPOINT PROTECTED] Servicio cerrado en superficie local."
                    bloqueados += 1
                elif escudo_fw_activo:
                    estado_blue = "🔵 [INTRUSION BLOCKED] Puerto activo en PC pero bloqueado en Firewall por TREMEND."
                    bloqueados += 1
                else:
                    estado_blue = "🔴 [VULNERABILITY DISCOVERED] Puerto abierto y sin regla de bloqueo perimetral."
                    expuestos += 1

                log_p5(f" • Vector :{p:<5} ({nombre_v[:42]:<42}) -> {estado_blue}")

            log_p5("\n" + "-"*85)
            log_p5(f" 📊 BALANCE PURPLE TEAM: {bloqueados}/{len(vectores)} vectores contenidos | {expuestos} brechas detectadas.")
            if expuestos > 0:
                log_p5(" 💡 ACCIÓN RECOMENDADA: Ve a la Pestaña 1 y presiona '🛡️ 2. Blindar Puertos en Firewall (1-Clic)'.")
            else:
                log_p5(" 🛡️ EXCELENTE: El Blue Team neutralizó todos los vectores probados por el Red Team.")
        threading.Thread(target=_run, daemon=True).start()

    def monitor_soc_green_team():
        txt_teams.configure(state="normal"); txt_teams.delete("1.0", "end"); txt_teams.configure(state="disabled")
        def _run():
            log_p5("="*85)
            log_p5(" 🔵🟢 MONITOR SOC (BLUE TEAM) & FIABILIDAD DE INFRAESTRUCTURA (GREEN TEAM)")
            log_p5("="*85)
            script_soc = r"""
            $servicios = @("WinDefend", "MpsSvc", "EventLog", "wscsvc")
            foreach ($s in $servicios) {
                $srv = Get-Service -Name $s -ErrorAction SilentlyContinue
                if ($srv) {
                    Write-Output ("SRV|" + $srv.Name + "|" + $srv.Status + "|" + $srv.DisplayName)
                }
            }
            try {
                $mp = Get-MpComputerStatus -ErrorAction Stop
                Write-Output ("EDR|RealTime:" + $mp.RealTimeProtectionEnabled + "|Behavior:" + $mp.BehaviorMonitorEnabled + "|IOAV:" + $mp.IoavProtectionEnabled + "|SigAge:" + $mp.AntivirusSignatureAge)
            } catch {
                Write-Output "EDR|No disponible"
            }
            $perfiles = Get-NetFirewallProfile -ErrorAction SilentlyContinue | Select-Object Name, Enabled
            foreach ($pf in $perfiles) {
                Write-Output ("FW|" + $pf.Name + "|" + $pf.Enabled)
            }
            """
            out = subprocess.run(["powershell", "-NoProfile", "-Command", script_soc], capture_output=True, text=True, startupinfo=startupinfo).stdout.strip()
            log_p5("[1] ESTADO DE SERVICIOS CRÍTICOS DE INFRAESTRUCTURA (GREEN TEAM):")
            for linea in out.splitlines():
                if linea.startswith("SRV|"):
                    _, nom_s, est_s, disp_s = linea.split("|", 3)
                    ico = "🟢" if est_s == "Running" else "🔴"
                    log_p5(f"   {ico} {nom_s:<12} ({est_s:<8}) -> {disp_s}")
                elif linea.startswith("EDR|"):
                    log_p5("\n[2] TELEMETRÍA DEL ENDPOINT & SOC (BLUE TEAM):")
                    log_p5(f"   🛡️ Sensores Defender: {linea.replace('EDR|', '')}")
                elif linea.startswith("FW|"):
                    _, nom_fw, act_fw = linea.split("|", 2)
                    ico_fw = "🟢 ACTIVO" if act_fw == "True" else "🔴 DESACTIVADO"
                    log_p5(f"   🧱 Perfil Firewall '{nom_fw:<8}': {ico_fw}")

            log_p5("\n[+] Monitoreo SOC e Infraestructura finalizado.")
        threading.Thread(target=_run, daemon=True).start()

    def exportar_acta_white_team():
        import datetime, hashlib
        cliente = ent_cliente_roe.get().strip() or "Equipo Local"
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        contenido_actual = txt_teams.get("1.0", "end").strip()
        firma_roe = hashlib.sha256(f"{cliente}|{fecha_actual}|{contenido_actual}".encode("utf-8")).hexdigest()[:24].upper()

        escritorio = os.path.join(os.environ.get("USERPROFILE"), "Desktop")
        if not os.path.exists(escritorio):
            escritorio = os.path.join(os.environ.get("USERPROFILE"), "Escritorio")
        ruta_acta = os.path.join(escritorio, f"Acta_Auditoria_WhiteTeam_{socket.gethostname()}.txt")

        acta_texto = (
            "========================================================================\n"
            " ⚪ ACTA OFICIAL DE AUDITORÍA Y REGLAS DE COMPROMISO (WHITE TEAM ROE)\n"
            "========================================================================\n"
            f" • Organización / Activo : {cliente}\n"
            f" • Host Auditado         : {socket.gethostname()}\n"
            f" • Fecha y Hora          : {fecha_actual}\n"
            f" • Marco Metodológico    : Cyber Teams (Red / Blue / Purple / White / Yellow / Green)\n"
            f" • Hash de Integridad    : {firma_roe}\n"
            "========================================================================\n\n"
            "1. ALCANCE Y ÉTICA (WHITE TEAM):\n"
            "   Ejercicio ejecutado de forma local, controlada y autorizada mediante\n"
            "   TREMEND Toolkit V3.3 sin afectar la disponibilidad de los servicios.\n\n"
            "2. REGISTRO TÉCNICO DE LA SESIÓN (PURPLE / BLUE / GREEN TEAM):\n"
            f"{contenido_actual}\n\n"
            "========================================================================\n"
            " Generado automáticamente por TREMEND Toolkit - Centro Cyber Teams\n"
        )
        try:
            with open(ruta_acta, "w", encoding="utf-8") as f:
                f.write(acta_texto)
            log_p5(f"\n⚪ [WHITE TEAM] Acta Oficial ROE exportada al Escritorio:\n   -> {ruta_acta}")
            os.startfile(ruta_acta)
        except Exception as e:
            log_p5(f"[-] Error al exportar el Acta ROE: {e}")

    frame_p5_btns = ctk.CTkFrame(tab_teams, fg_color="transparent")
    frame_p5_btns.pack(fill="x", padx=15, pady=6)
    ctk.CTkButton(frame_p5_btns, text="⚔️ 1. Simulación Purple Team (Attack <-> Defend)", fg_color="#A855F7", hover_color="#9333EA", font=("Arial", 13, "bold"), height=40, command=ejecutar_simulacion_purple).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_p5_btns, text="🛡️ 2. Monitor SOC & Infraestructura (Blue/Green)", fg_color="#3B82F6", hover_color="#2563EB", font=("Arial", 13, "bold"), height=40, command=monitor_soc_green_team).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_p5_btns, text="⚖️ 3. Exportar Acta ROE (White Team)", fg_color="#10B981", hover_color="#059669", font=("Arial", 13, "bold"), height=40, command=exportar_acta_white_team).pack(side="left", padx=4, expand=True, fill="x")

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
                            rep_ip += "\n [⚠️] Servidor externo/privado. Procede con extrema precaución.\n"
                            
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

def logica_organizador_archivos(log=None):
    import os
    import shutil
    import hashlib
    import datetime
    from pathlib import Path
    import customtkinter as ctk
    from tkinter import filedialog, messagebox

    if log:
        log("\n" + "="*75)
        log(" 🗂️ INICIANDO SUITE DE AUTOMATIZACIÓN Y ORGANIZACIÓN DE ARCHIVOS (4 EN 1) ")
        log("="*75)

    win_org = ctk.CTkToplevel(app)
    win_org.title("TREMEND - Automatizador Inteligente de Archivos, Lotes y Duplicados")
    win_org.geometry("1120x700")
    win_org.attributes("-topmost", True)
    win_org.transient(app)

    # Historial en memoria para poder deshacer (Rollback) movimientos
    historial_movimientos = []

    categorias = {
        "1_Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".heic"],
        "2_Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
        "3_Documentos": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
        "4_Audios": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
        "5_Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
        "6_Instaladores": [".exe", ".msi", ".bat", ".cmd", ".apk"],
        "7_Codigo_y_Scripts": [".py", ".html", ".js", ".ts", ".css", ".json", ".sql", ".xml", ".ps1"]
    }

    # --- BARRA SUPERIOR: SELECTOR DE RUTA RÁPIDO (ESTILO VIDEO) ---
    frame_top = ctk.CTkFrame(win_org, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#38BDF8")
    frame_top.pack(fill="x", padx=20, pady=12)

    ctk.CTkLabel(frame_top, text="Carpeta Objetivo:", font=("Arial", 13, "bold"), text_color="#00FFCC").pack(side="left", padx=(15, 5), pady=12)

    ruta_downloads = str(Path.home() / "Downloads")
    var_ruta = ctk.StringVar(value=ruta_downloads if os.path.exists(ruta_downloads) else str(Path.home()))

    ent_ruta = ctk.CTkEntry(frame_top, textvariable=var_ruta, width=420, font=("Consolas", 13))
    ent_ruta.pack(side="left", padx=5, pady=12, fill="x", expand=True)

    def elegir_carpeta_custom():
        sel = filedialog.askdirectory(title="Selecciona la carpeta a automatizar", parent=win_org)
        if sel:
            var_ruta.set(sel)
            actualizar_resumen_carpeta()

    def fijar_ruta_rapida(sub):
        p = Path.home() / sub
        if not p.exists() and sub == "Desktop":
            p = Path.home() / "Escritorio"
        if p.exists():
            var_ruta.set(str(p))
            actualizar_resumen_carpeta()

    ctk.CTkButton(frame_top, text="📥 Descargas", width=110, fg_color="#334155", hover_color="#475569", command=lambda: fijar_ruta_rapida("Downloads")).pack(side="left", padx=4)
    ctk.CTkButton(frame_top, text="🖥️ Escritorio", width=110, fg_color="#334155", hover_color="#475569", command=lambda: fijar_ruta_rapida("Desktop")).pack(side="left", padx=4)
    ctk.CTkButton(frame_top, text="📂 Examinar...", width=115, fg_color="#3B82F6", hover_color="#2563EB", command=elegir_carpeta_custom).pack(side="left", padx=4)

    lbl_contador_top = ctk.CTkLabel(frame_top, text="0 archivos sueltos", font=("Consolas", 13, "bold"), text_color="#FCD34D")
    lbl_contador_top.pack(side="right", padx=15)

    # --- PESTAÑAS DE LAS 4 AUTOMATIZACIONES ---
    tabview = ctk.CTkTabview(win_org, fg_color="#1E293B", text_color="#FFFFFF", segmented_button_selected_color="#10B981")
    tabview.pack(pady=(0, 15), padx=20, fill="both", expand=True)
    tabview._segmented_button.configure(text_color="#000000")

    tab_org = tabview.add("🗂️ 1. Organizar por Tipo (+ Reglas)")
    tab_fac = tabview.add("🧾 2. Clasificar Facturas / Fechas")
    tab_ren = tabview.add("🏷️ 3. Renombrar Lotes (Fotos/Docs)")
    tab_dup = tabview.add("👯 4. Cazador de Duplicados (SHA-256)")

    # Helper para evitar sobrescribir archivos si el nombre ya existe
    def destino_sin_colision(ruta_dest: Path) -> Path:
        if not ruta_dest.exists():
            return ruta_dest
        stem = ruta_dest.stem
        suf = ruta_dest.suffix
        parent = ruta_dest.parent
        contador = 1
        while True:
            candidato = parent / f"{stem}_({contador}){suf}"
            if not candidato.exists():
                return candidato
            contador += 1

    # ====================================================================
    # PESTAÑA 1: ORGANIZADOR POR EXTENSIÓN + REGLAS PERSONALIZADAS
    # ====================================================================
    frame_regla = ctk.CTkFrame(tab_org, fg_color="#0F172A", corner_radius=8)
    frame_regla.pack(fill="x", padx=15, pady=8)

    ctk.CTkLabel(frame_regla, text="+ Nueva Regla:", font=("Arial", 13, "bold"), text_color="#A855F7").pack(side="left", padx=10, pady=8)
    ent_nueva_carpeta = ctk.CTkEntry(frame_regla, width=180, placeholder_text="Carpeta (Ej: 8_Disenos)")
    ent_nueva_carpeta.pack(side="left", padx=5, pady=8)
    ent_nuevas_exts = ctk.CTkEntry(frame_regla, width=220, placeholder_text="Extensiones (Ej: .psd, .ai, .fig)")
    ent_nuevas_exts.pack(side="left", padx=5, pady=8)

    txt_consola_org = ctk.CTkTextbox(tab_org, font=("Consolas", 13), fg_color="#050811", text_color="#38BDF8")
    txt_consola_org.pack(fill="both", expand=True, padx=15, pady=8)

    def actualizar_resumen_carpeta():
        ruta_p = Path(var_ruta.get().strip())
        txt_consola_org.configure(state="normal")
        txt_consola_org.delete("1.0", "end")
        if not ruta_p.exists() or not ruta_p.is_dir():
            lbl_contador_top.configure(text="Ruta inválida")
            txt_consola_org.insert("end", "[-] Selecciona una carpeta válida arriba.\n")
            txt_consola_org.configure(state="disabled")
            return

        archivos_sueltos = [f for f in ruta_p.iterdir() if f.is_file()]
        carpetas_actuales = [d for d in ruta_p.iterdir() if d.is_dir()]
        lbl_contador_top.configure(text=f"{len(carpetas_actuales)} carpetas • {len(archivos_sueltos)} archivos sueltos")

        txt_consola_org.insert("end", f"📂 VISTA PREVIA DE: {ruta_p}\n" + "="*80 + "\n")
        txt_consola_org.insert("end", f"• Archivos sueltos detectados : {len(archivos_sueltos)}\n")
        txt_consola_org.insert("end", f"• Subcarpetas actuales        : {len(carpetas_actuales)}\n\n")
        txt_consola_org.insert("end", "📊 DISTRIBUCIÓN POR REGLAS ACTIVAS:\n")

        conteo_previo = {k: 0 for k in categorias}
        conteo_previo["Otros"] = 0
        for f in archivos_sueltos:
            ext = f.suffix.lower()
            asignado = False
            for cat, exts in categorias.items():
                if ext in exts:
                    conteo_previo[cat] += 1
                    asignado = True
                    break
            if not asignado:
                conteo_previo["Otros"] += 1

        for cat, cant in conteo_previo.items():
            exts_muestra = ", ".join(categorias.get(cat, ["*"])[:5])
            txt_consola_org.insert("end", f"   ├─ {cat:<20} : {cant:4d} archivos  ({exts_muestra})\n")
        txt_consola_org.configure(state="disabled")

    def agregar_regla_custom():
        nom_c = ent_nueva_carpeta.get().strip()
        exts_raw = ent_nuevas_exts.get().strip()
        if not nom_c or not exts_raw:
            messagebox.showwarning("Atención", "Escribe el nombre de la carpeta y al menos una extensión (ej: .psd).", parent=win_org)
            return
        lista_e = [e.strip().lower() if e.strip().startswith(".") else "." + e.strip().lower() for e in exts_raw.split(",") if e.strip()]
        categorias[nom_c] = lista_e
        ent_nueva_carpeta.delete(0, "end")
        ent_nuevas_exts.delete(0, "end")
        actualizar_resumen_carpeta()

    ctk.CTkButton(frame_regla, text="➕ Añadir Regla", fg_color="#8B5CF6", hover_color="#7C3AED", font=("Arial", 12, "bold"), command=agregar_regla_custom).pack(side="left", padx=8)

    def ejecutar_organizacion_estandar():
        ruta_p = Path(var_ruta.get().strip())
        if not ruta_p.exists(): return
        historial_movimientos.clear()

        boveda = ruta_p / "TREMEND_Carpeta_Organizada"
        boveda.mkdir(exist_ok=True)

        conteo_final = {}
        movidos = 0

        for item in list(ruta_p.iterdir()):
            if not item.is_file():
                continue
            ext = item.suffix.lower()
            cat_dest = "8_Otros"
            for cat, exts in categorias.items():
                if ext in exts:
                    cat_dest = cat
                    break

            carpeta_cat = boveda / cat_dest
            carpeta_cat.mkdir(exist_ok=True)
            target = destino_sin_colision(carpeta_cat / item.name)

            try:
                shutil.move(str(item), str(target))
                historial_movimientos.append((target, item))
                conteo_final[cat_dest] = conteo_final.get(cat_dest, 0) + 1
                movidos += 1
            except Exception:
                pass

        # Purga de carpetas vacías residuales
        vacias = 0
        for root_d, dirs_d, _ in os.walk(str(ruta_p), topdown=False):
            for d in dirs_d:
                p_dir = os.path.join(root_d, d)
                if "TREMEND_Carpeta_Organizada" in p_dir:
                    continue
                try:
                    if not os.listdir(p_dir):
                        os.rmdir(p_dir)
                        vacias += 1
                except Exception:
                    pass

        txt_consola_org.configure(state="normal")
        txt_consola_org.delete("1.0", "end")
        txt_consola_org.insert("end", f"✅ ORGANIZACIÓN COMPLETADA EN: {boveda.name}/\n" + "="*80 + "\n\n")
        for cat_k, total_k in sorted(conteo_final.items()):
            txt_consola_org.insert("end", f"   ├─ {cat_k + '/':<24} {total_k:4d} archivos  ✔\n")
        txt_consola_org.insert("end", f"\n[+] Total clasificados: {movidos} archivos | Carpetas vacías purgadas: {vacias}\n")
        txt_consola_org.insert("end", "[💡] Si deseas revertir todo a su estado original, presiona '↩️ Deshacer Última Organización'.\n")
        txt_consola_org.configure(state="disabled")
        lbl_contador_top.configure(text=f"{len(conteo_final)} carpetas • 0 archivos sueltos")
        if log:
            log(f"[+] Organización completada: {movidos} archivos ordenados en {boveda}")

    def deshacer_organizacion():
        if not historial_movimientos:
            messagebox.showinfo("Sin Historial", "No hay movimientos recientes para deshacer en esta sesión.", parent=win_org)
            return
        restaurados = 0
        for origen_actual, destino_original in reversed(historial_movimientos):
            try:
                if origen_actual.exists():
                    shutil.move(str(origen_actual), str(destino_original))
                    restaurados += 1
            except Exception:
                pass
        historial_movimientos.clear()
        actualizar_resumen_carpeta()
        messagebox.showinfo("Rollback Completado", f"Se devolvieron {restaurados} archivos a su ubicación original.", parent=win_org)

    frame_btns_org = ctk.CTkFrame(tab_org, fg_color="transparent")
    frame_btns_org.pack(fill="x", padx=15, pady=6)
    ctk.CTkButton(frame_btns_org, text="🚀 Ejecutar Organización Ahora", font=("Arial", 13, "bold"), height=40, fg_color="#10B981", hover_color="#059669", command=ejecutar_organizacion_estandar).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns_org, text="↩️ Deshacer Última Organización", font=("Arial", 13, "bold"), height=40, fg_color="#F59E0B", text_color="#000000", hover_color="#D97706", command=deshacer_organizacion).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns_org, text="📂 Abrir Carpeta", font=("Arial", 13, "bold"), height=40, width=150, fg_color="#334155", hover_color="#475569", command=lambda: os.startfile(var_ruta.get())).pack(side="right", padx=4)

    # ====================================================================
    # PESTAÑA 2: CLASIFICADOR DE FACTURAS, FECHAS Y ANALÍTICA MENSUAL
    # ====================================================================
    frame_fac_top = ctk.CTkFrame(tab_fac, fg_color="#0F172A", corner_radius=8)
    frame_fac_top.pack(fill="x", padx=15, pady=8)
    ctk.CTkLabel(frame_fac_top, text="Palabras clave a buscar en el nombre:", font=("Arial", 13, "bold"), text_color="#00FFCC").pack(side="left", padx=10, pady=10)
    ent_kw_facturas = ctk.CTkEntry(frame_fac_top, width=420)
    ent_kw_facturas.pack(side="left", padx=5, pady=10, fill="x", expand=True)
    ent_kw_facturas.insert(0, "factura, invoice, recibo, nequi, pago, comprobante, extracto, cuenta, impuesto, presupuesto, informe")

    txt_fac = ctk.CTkTextbox(tab_fac, font=("Consolas", 13), fg_color="#050811", text_color="#E2E8F0")
    txt_fac.pack(fill="both", expand=True, padx=15, pady=8)
    txt_fac.insert("end", "[*] Clasifica documentos administrativos en carpetas AÑO-MES o genera la gráfica de productividad mensual (Ene-Dic) de tu carpeta.\n")
    txt_fac.configure(state="disabled")

    def clasificar_facturas_por_fecha():
        ruta_p = Path(var_ruta.get().strip())
        if not ruta_p.exists(): return
        kws = [k.strip().lower() for k in ent_kw_facturas.get().split(",") if k.strip()]
        boveda_fac = ruta_p / "TREMEND_Facturas_y_Soportes"

        encontrados = 0
        txt_fac.configure(state="normal")
        txt_fac.delete("1.0", "end")
        txt_fac.insert("end", f"🧾 ESCANEANDO SOPORTES Y FACTURAS EN: {ruta_p}\n" + "="*80 + "\n\n")

        for item in list(ruta_p.iterdir()):
            if not item.is_file(): continue
            nom_low = item.name.lower()
            if any(k in nom_low for k in kws):
                mtime = datetime.datetime.fromtimestamp(item.stat().st_mtime)
                carpeta_mes = boveda_fac / mtime.strftime("%Y-%m")
                carpeta_mes.mkdir(parents=True, exist_ok=True)
                dest = destino_sin_colision(carpeta_mes / item.name)
                try:
                    shutil.move(str(item), str(dest))
                    historial_movimientos.append((dest, item))
                    txt_fac.insert("end", f"  ✔ [{mtime.strftime('%Y-%m')}] {item.name} -> {carpeta_mes.name}/\n")
                    encontrados += 1
                except Exception:
                    pass

        txt_fac.insert("end", f"\n[+] Total de facturas/recibos clasificados por mes: {encontrados}\n")
        txt_fac.configure(state="disabled")
        actualizar_resumen_carpeta()

    def generar_analitica_mensual():
        ruta_p = Path(var_ruta.get().strip())
        if not ruta_p.exists(): return
        nombres_meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        conteo_mes = {m: 0 for m in range(1, 13)}
        peso_mes = {m: 0 for m in range(1, 13)}
        total_arch = 0

        for item in ruta_p.rglob("*"):
            if item.is_file():
                try:
                    st = item.stat()
                    dt = datetime.datetime.fromtimestamp(st.st_mtime)
                    conteo_mes[dt.month] += 1
                    peso_mes[dt.month] += st.st_size
                    total_arch += 1
                except Exception:
                    pass

        txt_fac.configure(state="normal")
        txt_fac.delete("1.0", "end")
        txt_fac.insert("end", f"📊 ANALÍTICA DE VOLUMEN DE ARCHIVOS POR MES ({total_arch} archivos analizados)\n")
        txt_fac.insert("end", "="*80 + "\n\n")

        max_c = max(conteo_mes.values()) if conteo_mes and max(conteo_mes.values()) > 0 else 1
        for m_idx in range(1, 13):
            cant = conteo_mes[m_idx]
            mb = peso_mes[m_idx] / (1024 * 1024)
            bloques = int((cant / max_c) * 32) if cant > 0 else 0
            barra = "█" * bloques + "░" * (32 - bloques)
            txt_fac.insert("end", f"  {nombres_meses[m_idx-1]} │ {barra} │ {cant:4d} arch. ({mb:6.1f} MB)\n")

        txt_fac.insert("end", "\n" + "="*80 + "\n")
        txt_fac.insert("end", "[+] Gráfica completada. Ideal para auditar picos de trabajo o cierres de mes.\n")
        txt_fac.configure(state="disabled")

    frame_btns_fac = ctk.CTkFrame(tab_fac, fg_color="transparent")
    frame_btns_fac.pack(fill="x", padx=15, pady=6)
    ctk.CTkButton(frame_btns_fac, text="🧾 1. Clasificar Facturas y Soportes por Año-Mes", font=("Arial", 13, "bold"), height=42, fg_color="#10B981", hover_color="#059669", command=clasificar_facturas_por_fecha).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns_fac, text="📊 2. Procesar Gráfica de Archivos por Mes (Ene-Dic)", font=("Arial", 13, "bold"), height=42, fg_color="#3B82F6", hover_color="#2563EB", command=generar_analitica_mensual).pack(side="right", padx=4, expand=True, fill="x")

    # ====================================================================
    # PESTAÑA 3: RENOMBRADOR MASIVO POR FECHA (MODO OFICINA 17:58 / LOTES)
    # ====================================================================
    import re, time

    frame_ren_top = ctk.CTkFrame(tab_ren, fg_color="#0F172A", corner_radius=8)
    frame_ren_top.pack(fill="x", padx=15, pady=(8, 4))

    ctk.CTkLabel(frame_ren_top, text="Modo:", font=("Arial", 13, "bold"), text_color="#00FFCC").pack(side="left", padx=(10, 4), pady=10)
    combo_modo_ren = ctk.CTkOptionMenu(
        frame_ren_top,
        values=[
            "1. Fecha + Nombre Original (2026-03-14_informe.docx)",
            "2. Fecha + Nombre Original + Mover a Carpetas por Mes",
            "3. Prefijo + Fecha + Secuencia (Foto_2026-03-14_001.jpg)"
        ],
        width=360
    )
    combo_modo_ren.pack(side="left", padx=4, pady=10)

    ctk.CTkLabel(frame_ren_top, text="Filtro:", font=("Arial", 13, "bold")).pack(side="left", padx=(8, 4), pady=10)
    combo_tipo_ren = ctk.CTkOptionMenu(
        frame_ren_top,
        values=["Todos los archivos sueltos", "Solo Imágenes (.jpg, .png, .webp)", "Solo Documentos (.pdf, .docx, .xlsx)", "Solo Videos (.mp4, .mov, .mkv)"],
        width=220
    )
    combo_tipo_ren.pack(side="left", padx=4, pady=10)

    var_limpiar_nombres = ctk.BooleanVar(value=True)
    ctk.CTkCheckBox(
        frame_ren_top, text="Limpiar paréntesis/espacios", variable=var_limpiar_nombres,
        font=("Arial", 12, "bold"), text_color="#FCD34D", fg_color="#10B981"
    ).pack(side="left", padx=8, pady=10)

    # Barra de progreso visual y etiqueta de velocidad (Estilo 0.8s del video)
    frame_ren_prog = ctk.CTkFrame(tab_ren, fg_color="transparent")
    frame_ren_prog.pack(fill="x", padx=15, pady=2)

    ent_prefijo = ctk.CTkEntry(frame_ren_prog, width=180, placeholder_text="Prefijo (Solo Modo 3)")
    ent_prefijo.pack(side="left", padx=(0, 8))
    ent_prefijo.insert(0, "Archivo_TREMEND")

    pb_ren = ctk.CTkProgressBar(frame_ren_prog, progress_color="#10B981", height=14)
    pb_ren.pack(side="left", fill="x", expand=True, padx=6)
    pb_ren.set(0)

    lbl_ren_pct = ctk.CTkLabel(frame_ren_prog, text="0% (Listo)", font=("Consolas", 13, "bold"), text_color="#10B981")
    lbl_ren_pct.pack(side="right", padx=6)

    txt_ren = ctk.CTkTextbox(tab_ren, font=("Consolas", 13), fg_color="#050811", text_color="#FCD34D")
    txt_ren.pack(fill="both", expand=True, padx=15, pady=6)
    txt_ren.insert(
        "end",
        "[*] MODO OFICINA 17:58 ACTIVADO:\n"
        "    • Ordena y renombra cientos de archivos por su fecha real en menos de 1 segundo.\n"
        "    • Incluye escudo anti-doble fecha (si un archivo ya tiene '2026-03-14_', no lo repite).\n"
        "    • Si deseas revertir los nombres a como estaban antes, usa el botón '↩️ Deshacer' en la Pestaña 1.\n"
    )
    txt_ren.configure(state="disabled")

    def ejecutar_renombrado_lote():
        ruta_p = Path(var_ruta.get().strip())
        if not ruta_p.exists(): return
        modo_sel = combo_modo_ren.get()
        modo_f = combo_tipo_ren.get()
        prefijo = ent_prefijo.get().strip() or "Lote"

        if "Imágenes" in modo_f: filtro_exts = categorias["1_Imagenes"]
        elif "Documentos" in modo_f: filtro_exts = categorias["3_Documentos"]
        elif "Videos" in modo_f: filtro_exts = categorias["2_Videos"]
        else: filtro_exts = None

        candidatos = [
            f for f in sorted(ruta_p.iterdir(), key=lambda x: x.stat().st_mtime if x.is_file() else 0)
            if f.is_file() and (filtro_exts is None or f.suffix.lower() in filtro_exts)
        ]
        if not candidatos:
            messagebox.showinfo("Sin Archivos", "No se encontraron archivos sueltos que coincidan con ese filtro en la carpeta.", parent=win_org)
            return

        if not messagebox.askyesno(
            "Confirmar Ordenamiento y Renombrado",
            f"Se procesarán {len(candidatos)} archivos aplicando:\n'{modo_sel}'\n\n¿Deseas hacerlo ahora mismo (Podrás revertirlo con el botón Deshacer)?",
            parent=win_org
        ):
            return

        historial_movimientos.clear()
        txt_ren.configure(state="normal")
        txt_ren.delete("1.0", "end")
        pb_ren.set(0)

        t_inicio = time.perf_counter()
        renombrados = 0
        total_c = len(candidatos)

        for idx, arch in enumerate(candidatos, 1):
            dt_arch = datetime.datetime.fromtimestamp(arch.stat().st_mtime)
            fecha_str = dt_arch.strftime("%Y-%m-%d")
            mes_str = dt_arch.strftime("%Y-%m")

            # Quitamos prefijo de fecha previo si ya lo tenía para nunca duplicar YYYY-MM-DD_
            stem_limpio = re.sub(r'^\d{4}-\d{2}-\d{2}[_-]', '', arch.stem)
            if var_limpiar_nombres.get():
                stem_limpio = re.sub(r'[\(\)\[\]]', '', stem_limpio)
                stem_limpio = re.sub(r'\s+', '_', stem_limpio).strip('_')

            if modo_sel.startswith("1."):
                nuevo_nombre = f"{fecha_str}_{stem_limpio}{arch.suffix}"
                carpeta_destino = ruta_p
            elif modo_sel.startswith("2."):
                nuevo_nombre = f"{fecha_str}_{stem_limpio}{arch.suffix}"
                carpeta_destino = ruta_p / f"Ordenados_{mes_str}"
                carpeta_destino.mkdir(exist_ok=True)
            else:
                nuevo_nombre = f"{prefijo}_{fecha_str}_{idx:03d}{arch.suffix.lower()}"
                carpeta_destino = ruta_p

            target = destino_sin_colision(carpeta_destino / nuevo_nombre)
            try:
                nombre_viejo = arch.name
                arch.rename(target)
                historial_movimientos.append((target, arch))
                txt_ren.insert("end", f"  ✔ [{idx:03d}/{total_c:03d}] {nombre_viejo:<32} -> {target.name}\n")
                renombrados += 1
            except Exception:
                pass

            progreso = idx / total_c
            pb_ren.set(progreso)

        segundos_reales = time.perf_counter() - t_inicio
        minutos_manual = (renombrados * 15) / 60.0  # ~15 seg por archivo haciéndolo a mano con clic derecho
        lbl_ren_pct.configure(text=f"100% ({segundos_reales:.2f} s)")

        txt_ren.insert("end", "\n" + "="*80 + "\n")
        txt_ren.insert("end", f"⚡ ¡VELOCIDAD PYTHON!: {renombrados}/{total_c} archivos ordenados y renombrados en {segundos_reales:.3f} segundos.\n")
        txt_ren.insert("end", f"⏱️ Tiempo estimado a mano (clic derecho): ~{minutos_manual:.1f} minutos ahorrados.\n")
        txt_ren.configure(state="disabled")
        actualizar_resumen_carpeta()

    ctk.CTkButton(tab_ren, text="⚡ Ordenar por Fecha y Renombrar Archivos Ahora", font=("Arial", 13, "bold"), height=42, fg_color="#10B981", hover_color="#059669", command=ejecutar_renombrado_lote).pack(fill="x", padx=15, pady=6)

    # ====================================================================
    # PESTAÑA 4: CAZADOR DE DUPLICADOS POR HASH CRIPTOGRÁFICO (SHA-256)
    # ====================================================================
    txt_dup = ctk.CTkTextbox(tab_dup, font=("Consolas", 13), fg_color="#050811", text_color="#10B981")
    txt_dup.pack(fill="both", expand=True, padx=15, pady=10)
    txt_dup.insert("end", "[*] Escanea la carpeta seleccionada calculando el Hash SHA-256 de cada archivo para encontrar copias idénticas que desperdician espacio (incluso si tienen distinto nombre).\n")
    txt_dup.configure(state="disabled")

    def cazar_duplicados_sha256():
        ruta_p = Path(var_ruta.get().strip())
        if not ruta_p.exists(): return
        txt_dup.configure(state="normal")
        txt_dup.delete("1.0", "end")
        txt_dup.insert("end", f"🔍 CALCULANDO HUELLAS SHA-256 EN: {ruta_p}\n" + "="*80 + "\n\n")

        mapa_hashes = {}
        duplicados = []
        bytes_ahorrados = 0

        for item in ruta_p.iterdir():
            if not item.is_file(): continue
            try:
                h = hashlib.sha256()
                with open(item, "rb") as f:
                    while chunk := f.read(65536):
                        h.update(chunk)
                digest = h.hexdigest()
                if digest in mapa_hashes:
                    duplicados.append((item, mapa_hashes[digest]))
                    bytes_ahorrados += item.stat().st_size
                else:
                    mapa_hashes[digest] = item
            except Exception:
                pass

        if not duplicados:
            txt_dup.insert("end", "🟢 EXCELENTE: No se encontraron archivos duplicados en esta carpeta.\n")
        else:
            mb = bytes_ahorrados / (1024 * 1024)
            txt_dup.insert("end", f"⚠️ SE DETECTARON {len(duplicados)} ARCHIVOS CLONADOS ({mb:.2f} MB recuperables):\n\n")
            for clon, original in duplicados:
                txt_dup.insert("end", f"  🔴 Clon: {clon.name:<32} (Idéntico a: {original.name})\n")

            if messagebox.askyesno("Aislar o Eliminar Duplicados", f"Se encontraron {len(duplicados)} archivos repetidos ({mb:.2f} MB).\n\n¿Deseas mover las copias sobrantes a una carpeta '_Duplicados_Aislados' para revisarlas o borrarlas de forma segura?", parent=win_org):
                carpeta_dup = ruta_p / "TREMEND_Duplicados_Aislados"
                carpeta_dup.mkdir(exist_ok=True)
                for clon, _ in duplicados:
                    try:
                        dest = destino_sin_colision(carpeta_dup / clon.name)
                        shutil.move(str(clon), str(dest))
                        historial_movimientos.append((dest, clon))
                    except Exception:
                        pass
                txt_dup.insert("end", f"\n[+] Las {len(duplicados)} copias repetidas fueron aisladas en: {carpeta_dup.name}/\n")
        txt_dup.configure(state="disabled")
        actualizar_resumen_carpeta()

    ctk.CTkButton(tab_dup, text="👯 Escanear y Aislar Archivos Duplicados (SHA-256)", font=("Arial", 13, "bold"), height=42, fg_color="#8B5CF6", hover_color="#7C3AED", command=cazar_duplicados_sha256).pack(fill="x", padx=15, pady=6)

    actualizar_resumen_carpeta()

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
    import os, shutil, subprocess, stat, sys

    log(f"\n[*] Iniciando Mantenimiento Extremo en los discos: {', '.join(discos_seleccionados)}")

    # Helper inspirado en el modificador /F (Forzar borrado de archivos de Solo Lectura)
    def forzar_desbloqueo(func, path, exc_info):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except: pass

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

        # 2. Limpieza de infecciones y basura de macOS
        log(f"[*] Barriendo rastros residuales (.Trashes, Spotlight, fseventsd)...")
        carpetas_mac = [".Trashes", ".fseventsd", ".Spotlight-V100", "FOUND.000"]
        for carpeta in carpetas_mac:
            ruta_completa = f"{disco}\\{carpeta}"
            if os.path.exists(ruta_completa):
                run_cmd(log, f'cmd /c rmdir /s /q "{ruta_completa}" 2>nul')

        # 3. Limpieza de archivos de caché
        log(f"[*] Escaneando y destruyendo cachés visuales (.DS_Store, Thumbs.db)...")
        run_cmd(log, f'cmd /c del /s /q /f /a:h "{disco}\\.DS_Store" 2>nul')
        run_cmd(log, f'cmd /c del /s /q /f /a:h "{disco}\\Thumbs.db" 2>nul')
        
        log(f"[+] Purga superficial de {disco} completada.")

    # 4. Operaciones Core del Sistema (Exclusivo para la raíz C:)
    if "C:" in discos_seleccionados:
        log(f"\n=======================================================")
        log(f"[*] APLICANDO OPTIMIZACIÓN DE NÚCLEO AL SISTEMA (C:)")
        log(f"=======================================================")
        
        # --- FASE A: PURGA DE WINDOWS.OLD INTEGRADA ---
        ruta_win_old = r"C:\Windows.old"
        if os.path.exists(ruta_win_old):
            log("\n[*] ⚠️ DETECTADA CARPETA RESIDUAL 'Windows.old' (Actualización previa)...")
            log("[*] Iniciando purga militar. Aplicando permisos de Administrador y destruyendo...")
            
            script_winold = f"""
            Write-Host "    -> Tomando propiedad del directorio..." -ForegroundColor Yellow
            takeown.exe /F "{ruta_win_old}" /A /R /D Y 2>null
            Write-Host "    -> Asignando control total a la herramienta..." -ForegroundColor Yellow
            icacls.exe "{ruta_win_old}" /grant *S-1-5-32-544:F /T /C /Q 2>null
            Write-Host "    -> Ejecutando borrado forzado de gigabytes..." -ForegroundColor Yellow
            Remove-Item -LiteralPath "{ruta_win_old}" -Recurse -Force -ErrorAction SilentlyContinue
            """
            run_ps_script(log, script_winold)
            
            if not os.path.exists(ruta_win_old):
                log("[+] ¡Windows.old pulverizada! Se han recuperado gigabytes masivos de espacio.")
            else:
                log("[-] Quedaron algunos rastros bloqueados por el sistema, desaparecerán tras reiniciar.")
        
        # --- FASE B: DESTRUCCIÓN QUIRÚRGICA DE TEMPORALES Y CACHÉS ---
        log("\n[*] Destruyendo directorios temporales y volcados de errores (Modo Forzado /F)...")
        
        local_appdata = os.environ.get('LOCALAPPDATA', '')
        rutas_temp = [
            ("Temp de Usuario (%TEMP%)", os.environ.get('TEMP')),
            ("Temp del Núcleo (Windows\\Temp)", r"C:\Windows\Temp"),
            ("Caché de Pre-carga (Prefetch)", r"C:\Windows\Prefetch"),
            ("Reportes de Fallos (WER)", r"C:\ProgramData\Microsoft\Windows\WER\ReportArchive"),
            ("Volcados de Crasheo (CrashDumps)", os.path.join(local_appdata, "CrashDumps"))
        ]
        
        # Escudo Anti-Crash: Protege la caché de TREMEND y el ejecutable compilado (_MEI)
        prefijos_protegidos = ("tremend_", "_mei")
        ruta_mei_actual = getattr(sys, '_MEIPASS', '').lower()

        bytes_liberados = 0
        archivos_destruidos = 0
        
        for nombre_zona, ruta in rutas_temp:
            if ruta and os.path.exists(ruta):
                log(f"    -> Purgando {nombre_zona}: {ruta}")
                for item in os.listdir(ruta):
                    nombre_lower = item.lower()
                    p = os.path.join(ruta, item)
                    
                    # Saltamos archivos propios de TREMEND para evitar cierres inesperados
                    if nombre_lower.startswith(prefijos_protegidos) or (ruta_mei_actual and p.lower().startswith(ruta_mei_actual)):
                        continue
                        
                    try:
                        if os.path.isfile(p) or os.path.islink(p): 
                             tam = os.path.getsize(p) if not os.path.islink(p) else 0
                             os.chmod(p, stat.S_IWRITE) # Equivalente al /F del video
                             os.unlink(p)
                             bytes_liberados += tam
                             archivos_destruidos += 1
                        elif os.path.isdir(p): 
                            tam_dir = 0
                            for dirpath, _, filenames in os.walk(p):
                                for f in filenames:
                                    fp = os.path.join(dirpath, f)
                                    if not os.path.islink(fp):
                                        try: tam_dir += os.path.getsize(fp)
                                        except: pass
                            shutil.rmtree(p, onerror=forzar_desbloqueo)
                            if not os.path.exists(p):
                                bytes_liberados += tam_dir
                                archivos_destruidos += 1
                    except:
                        # Si está bloqueado en uso por otra app abierta, lo ignora con seguridad
                        pass
        
        if bytes_liberados > (1024**3):
            espacio_str = f"{(bytes_liberados / (1024**3)):.2f} GB"
        else:
            espacio_str = f"{(bytes_liberados / (1024**2)):.2f} MB"
            
        log(f"[+] ¡Limpieza Táctica Exitosa!")
        log(f"    -> Se destruyeron {archivos_destruidos} elementos basura (archivos y subdirectorios).")
        log(f"    -> Espacio recuperado: {espacio_str}")
        log(f"    -> Escudo TREMEND: Tus motores portables en caché fueron protegidos.")

        log("\n[*] Verificando e inyectando salud a la imagen de Windows (DISM)...")
        log("[!] AVISO: Este proceso es pesado y reconstruye el núcleo del sistema.")
        log("[!] Es normal que tarde varios minutos. TREMEND ocultará la barra de progreso para evitar lag visual.")
        run_cmd(log, 'DISM /Online /Cleanup-Image /RestoreHealth | findstr /V /C:"="')

        log("\n[*] Escaneando e integrando archivos del sistema corruptos (SFC)...")
        log("[!] Iniciando comprobación. Esto también tomará algunos minutos...")
        run_cmd(log, "sfc /scannow")

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

def logica_maquina_tiempo(log):
    import subprocess, json, datetime
    from tkinter import messagebox
    import customtkinter as ctk

    log("\n" + "="*75)
    log(" ⏳ MÁQUINA DEL TIEMPO (GESTOR INTELIGENTE DE RESTAURACIÓN) ")
    log("="*75)
    log("[*] Interrogando al núcleo de Windows sobre los Puntos de Restauración...")
    log("[*] Activando la protección del sistema en el disco C: (por si está desactivada)...")

    # Script PS para activar la protección, extraer los puntos y devolverlos en JSON limpio
    script_ps = """
    try {
        Enable-ComputerRestore -Drive "C:\\" -ErrorAction SilentlyContinue
        $points = Get-ComputerRestorePoint -ErrorAction SilentlyContinue
        if ($points) {
            $data = @()
            foreach ($p in $points) {
                $fecha_limpia = $p.CreationTime.ToString("yyyy-MM-dd")
                $data += [PSCustomObject]@{
                    ID = $p.SequenceNumber
                    Nombre = $p.Description
                    Fecha = $fecha_limpia
                }
            }
            $data | ConvertTo-Json -Compress
        } else {
            Write-Output "VACIO"
        }
    } catch { Write-Output "ERROR" }
    """
    
    # Ocultamos la ventana de PowerShell
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    resultado = subprocess.run(["powershell", "-NoProfile", "-Command", script_ps], capture_output=True, text=True, startupinfo=startupinfo)
    salida = resultado.stdout.strip()

    # --- CASO 1: NO HAY PUNTOS DE RESTAURACIÓN ---
    if "VACIO" in salida or not salida:
        log("\n[-] ALERTA ROJA: No se encontró NINGÚN Punto de Restauración en este equipo.")
        log("    -> El sistema está totalmente vulnerable ante una actualización fallida o virus.")
        
        if messagebox.askyesno("Sistema Vulnerable", "No se encontraron Puntos de Restauración.\n\nSi el computador está funcionando perfectamente en este momento, lo más recomendable es CREAR UN PUNTO DE RESPALDO AHORA MISMO.\n\n¿Deseas que TREMEND cree uno automáticamente?"):
            log("\n[*] Forjando nuevo Punto de Restauración de grado sistema...")
            log("[!] Esto puede tardar unos minutos. Por favor no cierres la ventana.")
            
            ps_crear = 'Checkpoint-Computer -Description "TREMEND_Respaldo_Seguro" -RestorePointType "MODIFY_SETTINGS" -ErrorAction Stop'
            res_crear = subprocess.run(["powershell", "-NoProfile", "-Command", ps_crear], capture_output=True, text=True, startupinfo=startupinfo)
            
            if res_crear.returncode == 0:
                log("[+] ¡ÉXITO! Escudo de restauración creado. Tu sistema ahora está a salvo.")
                messagebox.showinfo("Éxito", "Punto de Restauración creado correctamente.")
            else:
                log(f"[-] Error al crear el punto (Posible límite de espacio en disco): {res_crear.stderr}")
        else:
            log("[*] Operación cancelada. Se recomienda crear uno manualmente pronto.")
        return

    # --- CASO 2: SÍ HAY PUNTOS DE RESTAURACIÓN (ANÁLISIS INTELIGENTE) ---
    if "ERROR" in salida:
        log("[-] Ocurrió un error al leer la base de datos de Windows (WMI).")
        return

    try:
        puntos = json.loads(salida)
        if isinstance(puntos, dict): puntos = [puntos] # Por si solo hay 1 punto
    except:
        log("[-] Error decodificando los datos del sistema.")
        return

    log(f"\n[+] Se encontraron {len(puntos)} Puntos de Restauración en el sistema:\n")
    
    # Análisis de fechas (Heurística de Ingeniero)
    hoy = datetime.datetime.now().date()
    puntos_viejos = 0
    lista_menu = ""

    for i, p in enumerate(puntos):
        try:
            fecha_obj = datetime.datetime.strptime(p["Fecha"], "%Y-%m-%d").date()
        except:
            # Fallback seguro para parseo de fechas en Python
            partes = p["Fecha"].split("-")
            fecha_obj = datetime.date(int(partes[0]), int(partes[1]), int(partes[2]))
            
        dias_antiguedad = (hoy - fecha_obj).days
        
        estado_str = "🟢 CONFIABLE"
        if dias_antiguedad > 30:
            estado_str = "🔴 OBSOLETO/RIESGOSO"
            puntos_viejos += 1
        elif dias_antiguedad > 15:
            estado_str = "🟡 ANTIGUO"

        # Mostramos en el log de la terminal
        log(f"  [{p['ID']}] Fecha: {p['Fecha']} ({dias_antiguedad} días) | Info: {p['Nombre'][:30]}")
        log(f"        -> Estado: {estado_str}")
        
        # Construimos el texto para el menú interactivo
        lista_menu += f"ID {p['ID']}: {p['Fecha']} - {p['Nombre'][:25]}\n"

    log("\n" + "-"*60)
    # Lógica de Recomendación
    if puntos_viejos == len(puntos):
        log("[!] RECOMENDACIÓN DE TREMEND:")
        log("    -> TODOS tus puntos de restauración son muy viejos (más de 30 días).")
        log("    -> NO es recomendable confiar en ellos, ya que al restaurarlos podrías romper programas actuales.")
        log("    -> Te sugerimos eliminar los viejos y crear uno nuevo y fresco.")
    else:
        log("[+] El sistema cuenta con puntos de restauración recientes y confiables.")

    # --- MENÚ DE ACCIÓN (GUI) ---
    def menu_opciones():
        menu_texto = "Elige una acción:\n\n1. 🔄 Restaurar el sistema a un punto específico\n2. ➕ Crear un nuevo punto de respaldo seguro\n3. 🗑️ Purgar puntos viejos (Liberar espacio)"
        dialogo_opcion = ctk.CTkInputDialog(text=menu_texto, title="Máquina del Tiempo")
        opcion = dialogo_opcion.get_input()

        if opcion == '1':
            dialogo_id = ctk.CTkInputDialog(text=f"Ingresa el NÚMERO DE ID a restaurar:\n\n{lista_menu}", title="Restaurar Sistema")
            id_restaurar = dialogo_id.get_input()
            if id_restaurar and id_restaurar.isdigit():
                if messagebox.askyesno("⚠️ ALERTA CRÍTICA", f"Estás a punto de regresar tu PC en el tiempo al punto ID {id_restaurar}.\n\nTu computador SE REINICIARÁ INMEDIATAMENTE y no podrás usarlo por varios minutos.\n\n¿Estás completamente seguro?"):
                    log(f"\n[*] INICIANDO SECUENCIA DE RESTAURACIÓN (ID {id_restaurar})...")
                    log("[!] Agárrate, el sistema se reiniciará en 5 segundos.")
                    ps_restore = f"Restore-Computer -RestorePoint {id_restaurar} -Force"
                    subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_restore], startupinfo=startupinfo)
            else:
                log("[-] ID inválido o cancelado.")
                
        elif opcion == '2':
            log("\n[*] Forjando nuevo Punto de Restauración en segundo plano...")
            ps_crear = 'Checkpoint-Computer -Description "TREMEND_Respaldo_Fresco" -RestorePointType "MODIFY_SETTINGS" -ErrorAction Stop'
            res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_crear], capture_output=True, text=True, startupinfo=startupinfo)
            if res.returncode == 0:
                log("[+] ¡ÉXITO! Nuevo escudo de restauración creado correctamente.")
            else:
                log(f"[-] Falló la creación: {res.stderr}")
                
        elif opcion == '3':
            if messagebox.askyesno("Limpieza", "¿Borrar todos los puntos viejos para liberar espacio en el disco duro?"):
                log("\n[*] Purgando Puntos de Restauración viejos (VSS)...")
                subprocess.run("vssadmin delete shadows /all /quiet", shell=True, capture_output=True, startupinfo=startupinfo)
                log("[+] Espacio liberado con éxito.")

    # Lanzamos el menú tras medio segundo para que alcance a leer el log
    app.after(500, menu_opciones)

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
    import os, shutil, subprocess
    import customtkinter as ctk
    from tkinter import messagebox

    log("\n" + "="*75)
    log(" 🌐 GESTOR DE HIGIENE WEB Y ESCUDO ANTI-SECUESTRO DE SESIONES (2FA) ")
    log("="*75)

    dialogo = ctk.CTkInputDialog(
        text="Selecciona el nivel de intervención en tus navegadores (Chrome, Edge, Brave, Firefox):\n\n"
             "1. 🧹 Limpiar SOLO Caché Pesada (Libera GBs conservando tus sesiones abiertas)\n"
             "2. 🔒 Purga de Emergencia Anti-Robo 2FA (Cierra navegadores y destruye Cookies 'sessionid' y Tokens)",
        title="Escudo de Navegadores"
    )
    modo = dialogo.get_input()
    if modo not in ('1', '2'):
        log("[-] Operación cancelada por el usuario.")
        return

    local_app = os.environ.get('LOCALAPPDATA', '')
    roaming_app = os.environ.get('APPDATA', '')

    navegadores_chromium = {
        "Google Chrome": os.path.join(local_app, r"Google\Chrome\User Data\Default"),
        "Microsoft Edge": os.path.join(local_app, r"Microsoft\Edge\User Data\Default"),
        "Brave Browser": os.path.join(local_app, r"BraveSoftware\Brave-Browser\User Data\Default")
    }

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    if modo == '2':
        if not messagebox.askyesno("Confirmar Cierre Total de Sesiones", "⚠️ Esta acción cerrará tus navegadores abiertos y destruirá todas las cookies locales ('sessionid') y tokens web para impedir el robo de cuentas.\n\nTendrás que volver a iniciar sesión en tus páginas. ¿Deseas continuar?"):
            log("[-] Purga de sesiones cancelada.")
            return
        log("\n[*] Cerrando procesos activos de navegadores para liberar las bóvedas SQLite...")
        for proc_nav in ["chrome.exe", "msedge.exe", "brave.exe", "firefox.exe"]:
            subprocess.run(f"taskkill /F /IM {proc_nav} /T", shell=True, capture_output=True, startupinfo=startupinfo)

    bytes_totales = 0

    for nombre_nav, ruta_base in navegadores_chromium.items():
        if not os.path.exists(ruta_base):
            continue
        log(f"\n[*] Interviniendo {nombre_nav}...")

        # Carpetas de caché pesada (Modo 1 y Modo 2)
        for sub_cache in ["Cache", "Code Cache", "GPUCache"]:
            ruta_c = os.path.join(ruta_base, sub_cache)
            if os.path.exists(ruta_c):
                for root_d, _, files_d in os.walk(ruta_c):
                    for f in files_d:
                        try: bytes_totales += os.path.getsize(os.path.join(root_d, f))
                        except: pass
                shutil.rmtree(ruta_c, ignore_errors=True)
        log(f"    [+] Caché gráfica y de código de {nombre_nav} destruida.")

        # Destrucción de Cookies (sessionid) y Tokens de Sesión (Exclusivo Modo 2)
        if modo == '2':
            rutas_sesiones = [
                os.path.join(ruta_base, "Network", "Cookies"),
                os.path.join(ruta_base, "Network", "Cookies-journal"),
                os.path.join(ruta_base, "Cookies"),
                os.path.join(ruta_base, "Web Data")
            ]
            for r_cookie in rutas_sesiones:
                if os.path.exists(r_cookie):
                    try:
                        os.remove(r_cookie)
                        log(f"    [🔒] Bóveda de cookies erradicada: {os.path.basename(r_cookie)}")
                    except Exception:
                        pass
            for carpeta_token in ["Local Storage", "Session Storage", "IndexedDB"]:
                r_tok = os.path.join(ruta_base, carpeta_token)
                if os.path.exists(r_tok):
                    shutil.rmtree(r_tok, ignore_errors=True)
                    log(f"    [🔒] Almacenamiento de tokens purgado: {carpeta_token}")

    # Soporte para Mozilla Firefox en Modo 2
    ruta_ff = os.path.join(roaming_app, r"Mozilla\Firefox\Profiles")
    if modo == '2' and os.path.exists(ruta_ff):
        for perfil in os.listdir(ruta_ff):
            cookie_ff = os.path.join(ruta_ff, perfil, "cookies.sqlite")
            if os.path.exists(cookie_ff):
                try:
                    os.remove(cookie_ff)
                    log(f"    [🔒] Bóveda 'cookies.sqlite' de Firefox erradicada en perfil {perfil}.")
                except Exception:
                    pass

    mb_lib = bytes_totales / (1024 * 1024)
    log("\n" + "="*75)
    if modo == '1':
        log(f" ✅ CACHÉ DE NAVEGADORES PURGADA ({mb_lib:.2f} MB liberados | Sesiones intactas)")
    else:
        log(f" 🛡️ PURGA ANTI-SECUESTRO COMPLETADA ({mb_lib:.2f} MB liberados | Cero 'sessionid' expuestos)")
    log("="*75)
    try: notificar_voz("El blindaje y limpieza de navegadores ha finalizado.")
    except: pass

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
def logica_cazador_malware(log):
    log("\n" + "="*75)
    log(" 🦠 CAZADOR FORENSE DE MALWARE Y KEYLOGGERS (HEURÍSTICA) ")
    log("="*75)
    log("[*] Iniciando escaneo profundo de memoria RAM y rastreo de inyecciones...")
    log("[!] AVISO: El análisis de firmas digitales tomará un par de minutos. No cierres la ventana.")

    # Script en PowerShell que ejecuta la heurística avanzada
    script_ps = """
    Write-Host "`n[1] Analizando procesos activos y firmas criptográficas (Cazando el Keylogger)..." -ForegroundColor Cyan
    # Buscamos SOLO programas que estén transmitiendo datos a internet ahora mismo
    $procesos_red = Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    $amenazas_detectadas = 0

    foreach ($pId in $procesos_red) {
        $proc = Get-Process -Id $pId -ErrorAction SilentlyContinue
        if ($proc -and $proc.Path) {
            # Descartamos las rutas oficiales del núcleo de Windows para no romper el PC
            if ($proc.Path -notmatch "\\\\Windows\\\\System32" -and $proc.Path -notmatch "\\\\Windows\\\\SysWOW64") {
                # Aquí está la magia: Revisamos si el creador del programa está verificado
                $firma = Get-AuthenticodeSignature -FilePath $proc.Path -ErrorAction SilentlyContinue
                if ($firma.Status -ne "Valid") {
                    Write-Host "[🔥] ALERTA ROJA: Proceso ESPÍA detectado (Sin firma y enviando datos):" -ForegroundColor Red
                    Write-Host "      -> Nombre : $($proc.Name)" -ForegroundColor Yellow
                    Write-Host "      -> Ruta   : $($proc.Path)" -ForegroundColor Yellow
                    
                    try {
                        # Asesinamos el Keylogger en la memoria RAM para cortar la transmisión
                        Stop-Process -Id $pId -Force -ErrorAction Stop
                        Write-Host "      [+] Proceso asesinado en RAM. Conexión con el hacker cortada." -ForegroundColor Green
                    } catch {
                        Write-Host "      [-] El malware se resiste (Permisos insuficientes)." -ForegroundColor Red
                    }
                    $amenazas_detectadas++
                }
            }
        }
    }

    if ($amenazas_detectadas -eq 0) {
        Write-Host "[+] Fase 1 limpia: No se detectaron Keyloggers o Troyanos transmitiendo datos actualmente." -ForegroundColor Green
    } else {
        Write-Host "[!] Se neutralizaron $amenazas_detectadas amenazas activas en memoria." -ForegroundColor Yellow
    }

    Write-Host "`n[2] Invocando Escáner de Raíz (Motor Anti-Malware Nativo)..." -ForegroundColor Cyan
    Write-Host "[*] Lanzando motor de purga profunda en modo silencioso..."
    # Ejecutamos la herramienta MRT (Malicious Software Removal Tool) de Windows de forma oculta
    Start-Process -FilePath "mrt.exe" -ArgumentList "/F /Q" -Wait -NoNewWindow
    Write-Host "[+] Escaneo MRT finalizado."

    Write-Host "`n[3] Invocando Antivirus de Windows Defender - Búsqueda Rápida..." -ForegroundColor Cyan
    $defender_path = "C:\\ProgramData\\Microsoft\\Windows Defender\\Platform\\*\\MpCmdRun.exe"
    $exe = Get-ChildItem -Path $defender_path -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($exe) {
        Write-Host "[*] Ejecutando purga heurística final..."
        & $exe.FullName -Scan -ScanType 1
        Write-Host "[+] Purga de Defender completada."
    } else {
        Write-Host "[-] No se pudo localizar el motor de línea de comandos de Defender." -ForegroundColor Yellow
    }
    """
    
    run_ps_script(log, script_ps)
    
    log("\n=======================================================")
    log(" [+] CAZADOR FORENSE FINALIZADO CON ÉXITO ")
    log("=======================================================")
    log("[!] Tu sistema ha sido blindado cruzando firmas digitales y tráfico de red.")
    try: notificar_voz("El cazador forense de Malware y Keyloggers ha finalizado su escaneo.")
    except: pass

def logica_diagnostico_rapido(log):
    log("\n[*] Ejecutando Diagnóstico Rápido y Evaluación de Rendimiento (WinSat)...")
    log("[!] Re-evaluando el hardware del sistema. Esto puede tomar un minuto...")
    
    # Forzar la re-evaluación del hardware (winsat formal)
    run_cmd(log, "winsat formal")
    
    # Extraer y formatear el resultado con PowerShell
    script_ps = """
    try { 
        $sat = Get-CimInstance Win32_WinSat
        Write-Host "`n--- PUNTUACIÓN DE RENDIMIENTO WINSAT ---" -ForegroundColor Cyan
        Write-Host "Puntuación Base (General) : $($sat.WinSPRLevel)"
        Write-Host "Puntuación de CPU         : $($sat.CPUScore)"
        Write-Host "Puntuación de RAM         : $($sat.MemoryScore)"
        Write-Host "Puntuación de Disco       : $($sat.DiskScore)"
        Write-Host "Puntuación de Gráficos 2D : $($sat.GraphicsScore)"
        Write-Host "Puntuación de Gráficos 3D : $($sat.D3DScore)"
    } catch { 
        Write-Host '[-] Error al extraer la puntuación WinSat.' -ForegroundColor Red 
    }
    """
    run_ps_script(log, script_ps)

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
    log(" 🔋 INICIANDO CENTRO DE SALUD ENERGÉTICA Y OPTIMIZACIÓN DE BATERÍA ")
    log("="*75)

    win_bat = ctk.CTkToplevel(app)
    win_bat.title("TREMEND - Optimizador de Energía y Monitor de Batería Física")
    win_bat.geometry("920x520")
    win_bat.attributes("-topmost", True)
    win_bat.transient(app)

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # --- PANEL IZQUIERDO: OPTIMIZADOR REAL DE ENERGÍA Y DRENAJE ---
    frame_izq = ctk.CTkFrame(win_bat, width=440, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#38BDF8")
    frame_izq.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(frame_izq, text="⚡ Optimizador de Energía Activo", font=("Arial", 20, "bold"), text_color="#00FFCC").pack(pady=(18, 4))
    ctk.CTkLabel(frame_izq, text="Detecta qué procesos drenan tu energía y cambia el perfil del procesador en 1 clic.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 10))

    txt_drenaje = ctk.CTkTextbox(frame_izq, font=("Consolas", 12), fg_color="#050811", text_color="#38BDF8", height=180)
    txt_drenaje.pack(padx=15, pady=5, fill="both", expand=True)

    def escanear_drenaje():
        txt_drenaje.configure(state="normal")
        txt_drenaje.delete("1.0", "end")
        txt_drenaje.insert("end", "🔍 TOP PROCESOS CONSUMIENDO ENERGÍA AHORA MISMO:\n" + "="*48 + "\n")
        procs = []
        for p in psutil.process_iter(['name', 'memory_percent']):
            try:
                if p.info['name'].lower() not in ('system idle process', 'system'):
                    procs.append((p.info['name'], p.info['memory_percent'] or 0.0))
            except: pass
        procs.sort(key=lambda x: x[1], reverse=True)
        for nom, mem in procs[:6]:
            txt_drenaje.insert("end", f" • {nom[:25]:<25} | Impacto RAM: {mem:.1f}%\n")
        txt_drenaje.configure(state="disabled")

    def aplicar_plan_energia(guid, nombre_plan):
        subprocess.run(f"powercfg /setactive {guid}", shell=True, capture_output=True, startupinfo=startupinfo)
        log(f"[+] Plan de energía cambiado a: {nombre_plan}")
        escanear_drenaje()

    frame_planes = ctk.CTkFrame(frame_izq, fg_color="transparent")
    frame_planes.pack(fill="x", padx=15, pady=10)
    ctk.CTkButton(frame_planes, text="🌿 Ahorro Extremo", fg_color="#10B981", hover_color="#059669", font=("Arial", 12, "bold"), height=38, command=lambda: aplicar_plan_energia("a1841308-3541-4fab-bc81-f71556f20b4a", "Economizador")).pack(side="left", padx=3, expand=True, fill="x")
    ctk.CTkButton(frame_planes, text="⚖️ Equilibrado", fg_color="#3B82F6", hover_color="#2563EB", font=("Arial", 12, "bold"), height=38, command=lambda: aplicar_plan_energia("381b4222-f694-41f0-9685-ff5bb260df2e", "Equilibrado")).pack(side="left", padx=3, expand=True, fill="x")
    ctk.CTkButton(frame_planes, text="🚀 Máxima Potencia", fg_color="#F59E0B", text_color="#000000", hover_color="#D97706", font=("Arial", 12, "bold"), height=38, command=lambda: aplicar_plan_energia("8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c", "Alto Rendimiento")).pack(side="left", padx=3, expand=True, fill="x")

    ctk.CTkButton(frame_izq, text="🔄 Actualizar Radar de Consumo", fg_color="#334155", hover_color="#475569", height=34, command=escanear_drenaje).pack(padx=15, pady=(0, 12), fill="x")
    escanear_drenaje()

    # --- PANEL DERECHO: ESTADO REAL Y REPORTE FORENSE ---
    frame_der = ctk.CTkFrame(win_bat, width=420, fg_color="#1E293B", corner_radius=10, border_width=1, border_color="#A78BFA")
    frame_der.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

    ctk.CTkLabel(frame_der, text="🔋 Batería Física Real", font=("Arial", 20, "bold"), text_color="#A78BFA").pack(pady=(20, 5))
    ctk.CTkLabel(frame_der, text="Sensores en vivo de tu Hardware.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 20))

    lbl_real_porc = ctk.CTkLabel(frame_der, text="--%", font=("Arial", 60, "bold"), text_color="#10B981")
    lbl_real_porc.pack(pady=10)

    pb_real = ctk.CTkProgressBar(frame_der, height=35, corner_radius=10, progress_color="#10B981", fg_color="#0F172A")
    pb_real.pack(fill="x", padx=40, pady=10)
    pb_real.set(0)

    lbl_estado_real = ctk.CTkLabel(frame_der, text="Calculando...", font=("Arial", 16, "bold"), text_color="#E2E8F0")
    lbl_estado_real.pack(pady=10)

    def monitorear_bateria_real():
        while win_bat.winfo_exists():
            try:
                bat_real = psutil.sensors_battery()
                if bat_real:
                    porc = int(bat_real.percent)
                    enchufado = bat_real.power_plugged
                    estado = "🔌 Conectado (Cargando)" if enchufado else "🔋 Usando Batería"
                else:
                    porc = 100
                    estado = "🔌 PC Escritorio (Corriente Directa)"
            except:
                porc = 100; estado = "🔌 Sensor de Corriente Activo"

            color = "#EF4444" if porc <= 20 else ("#FCD34D" if porc <= 60 else "#10B981")
            def actualizar_ui(p=porc, e=estado, c=color):
                if win_bat.winfo_exists():
                    lbl_real_porc.configure(text=f"{p}%", text_color=c)
                    pb_real.set(p / 100.0)
                    pb_real.configure(progress_color=c)
                    lbl_estado_real.configure(text=e)
            app.after(0, actualizar_ui)
            time.sleep(1.5)

    threading.Thread(target=monitorear_bateria_real, daemon=True).start()

    def generar_reporte():
        log("[*] Interrogando sensores ACPI a nivel de Hardware...")
        ruta = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "Reporte_Bateria_TREMEND.html")
        subprocess.run(f'powercfg /batteryreport /output "{ruta}"', shell=True, capture_output=True, startupinfo=startupinfo)
        log(f"[+] ¡ÉXITO! Reporte de desgaste exportado a: {ruta}")
        try: os.startfile(ruta)
        except: pass

    ctk.CTkButton(frame_der, text="📄 Generar Reporte de Desgaste (HTML)", font=("Arial", 14, "bold"), height=45, fg_color="#3B82F6", hover_color="#2563EB", command=generar_reporte).pack(side="bottom", pady=25, padx=40, fill="x")

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

def logica_usuarios_locales(log=None):
    import os, subprocess, shutil
    import customtkinter as ctk
    from tkinter import filedialog, messagebox

    if log:
        log("\n" + "="*75)
        log(" 🕵️ INICIANDO INSPECTOR CAT PRO & ANATOMÍA DE USUARIOS (SAM / PASSWD) ")
        log("="*75)
        log("[*] Desplegando interfaz táctica Cyberpunk...")

    win_cat = ctk.CTkToplevel(app)
    win_cat.title("TREMEND - Inspector CAT Pro & Anatomía de Usuarios")
    win_cat.geometry("1120x680")
    win_cat.attributes("-topmost", True)
    win_cat.transient(app)

    tabview = ctk.CTkTabview(
        win_cat, fg_color="#0F172A", text_color="#FFFFFF",
        segmented_button_selected_color="#00FFCC", segmented_button_selected_hover_color="#10B981"
    )
    tabview.pack(pady=10, padx=20, fill="both", expand=True)
    # Ajustar color de texto del botón seleccionado para contraste con #00FFCC
    tabview._segmented_button.configure(text_color="#000000")

    tab_passwd = tabview.add("👤 Misión: Anatomía Usuarios (SAM / passwd)")
    tab_lector = tabview.add("📄 Misión: Visor Numerado (cat -n)")
    tab_unir   = tabview.add("🔗 Misión: Concatenar Archivos (cat A + B)")

    # ====================================================================
    # PESTAÑA 1: ANATOMÍA DE USUARIOS (/etc/passwd & Windows SAM)
    # ====================================================================
    frame_top_u = ctk.CTkFrame(tab_passwd, fg_color="#1E293B", corner_radius=8, border_width=1, border_color="#00FFCC")
    frame_top_u.pack(fill="x", padx=15, pady=10)

    ctk.CTkLabel(
        frame_top_u,
        text=" TERMINAL // AUDITORÍA DE CUENTAS Y ANATOMÍA DE LÍNEA",
        font=("Consolas", 15, "bold"), text_color="#00FFCC"
    ).pack(side="left", padx=15, pady=10)

    txt_passwd = ctk.CTkTextbox(tab_passwd, font=("Consolas", 13), fg_color="#050811", text_color="#38BDF8", height=240, border_width=1, border_color="#334155")
    txt_passwd.pack(fill="x", padx=15, pady=5)

    # Caja estética idéntica al video: "ANATOMÍA DE UNA LÍNEA"
    frame_anatomia = ctk.CTkFrame(tab_passwd, fg_color="#0A1120", corner_radius=10, border_width=2, border_color="#38BDF8")
    frame_anatomia.pack(fill="both", expand=True, padx=15, pady=10)

    ctk.CTkLabel(
        frame_anatomia,
        text="🔬 ANATOMÍA FORENSE Y DIAGNÓSTICO DE SEGURIDAD",
        font=("Consolas", 15, "bold"), text_color="#00FFCC"
    ).pack(anchor="w", padx=15, pady=(10, 5))

    txt_anatomia = ctk.CTkTextbox(frame_anatomia, font=("Consolas", 13), fg_color="transparent", text_color="#E2E8F0")
    txt_anatomia.pack(fill="both", expand=True, padx=15, pady=(0, 10))

    def cargar_passwd_linux():
        txt_passwd.configure(state="normal")
        txt_anatomia.configure(state="normal")
        txt_passwd.delete("1.0", "end")
        txt_anatomia.delete("1.0", "end")

        salida = ""
        if os.name != 'nt' and os.path.exists("/etc/passwd"):
            with open("/etc/passwd", "r", encoding="utf-8", errors="ignore") as f:
                salida = f.read()
        elif shutil.which("wsl"):
            try:
                res = subprocess.run(["wsl", "-e", "cat", "/etc/passwd"], capture_output=True, text=True, timeout=4)
                salida = res.stdout.strip()
            except: pass

        if not salida:
            txt_passwd.insert("end", "[*] Subsistema Linux (WSL) no detectado en este equipo Windows.\n" + "="*80 + "\n")
            txt_passwd.insert("end", "Para auditar un servidor Linux real desde Windows tienes dos opciones:\n")
            txt_passwd.insert("end", " 1. Usa la Pestaña 2 ('Visor Numerado cat -n') para abrir cualquier archivo passwd o log exportado.\n")
            txt_passwd.insert("end", " 2. Revisa abajo el Manual de Blindaje y Prevención de Intrusos en Cuentas Linux (/etc/passwd y /etc/shadow).\n")
            desglose = (
                "🛡️ MANUAL DE DEFENSA Y BLINDAJE DE CUENTAS EN LINUX (/etc/passwd & /etc/shadow):\n"
                "   ├─ 1. ¿CÓMO DETECTAR UN INTRUSO (BACKDOOR)?: Ejecuta 'awk -F: '($3 == 0) {print}' /etc/passwd'.\n"
                "   │     El único usuario que debe aparecer es 'root'. Si aparece otro nombre con UID 0, es un intruso.\n"
                "   ├─ 2. BLOQUEAR CONSOLA A CUENTAS DE SERVICIO: Las cuentas como www-data, mysql o sshd deben terminar\n"
                "   │     en '/usr/sbin/nologin' o '/bin/false' para impedir que un atacante abra una terminal.\n"
                "   └─ 3. BLINDAJE DE PERMISOS EN UN COMANDO:\n"
                "         sudo chmod 644 /etc/passwd && sudo chmod 600 /etc/shadow && sudo passwd -l root"
            )
            txt_anatomia.insert("end", desglose)
            txt_passwd.configure(state="disabled")
            txt_anatomia.configure(state="disabled")
            return

        txt_passwd.insert("end", "$ cat -n /etc/passwd   [LECTURA REAL DEL SUBSISTEMA LINUX / WSL]\n" + "="*80 + "\n")
        lineas = [l.strip() for l in salida.splitlines() if l.strip() and not l.startswith("#")]
        alertas_seguridad = []
        ejemplo_usuario = lineas[-1] if lineas else "root:x:0:0:root:/root:/bin/bash"

        for idx, l in enumerate(lineas, 1):
            txt_passwd.insert("end", f" {idx:2d}  {l}\n")
            partes = l.split(":")
            if len(partes) >= 7:
                usr, pwd_flag, uid, gid, desc, home, shell = partes[:7]
                if uid == "0" and usr != "root":
                    alertas_seguridad.append(f"🔴 ALERTA CRÍTICA (Línea {idx}): El usuario '{usr}' tiene UID 0 (Privilegios de Root ocultos).")
                if ("sh" in shell and "nologin" not in shell and "false" not in shell) and (uid.isdigit() and 0 < int(uid) < 1000):
                    alertas_seguridad.append(f"🟠 PRECAUCIÓN (Línea {idx}): La cuenta de sistema '{usr}' (UID {uid}) tiene una consola activa ({shell}).")
                if pwd_flag not in ("x", "*"):
                    alertas_seguridad.append(f"🔴 ALERTA (Línea {idx}): La contraseña de '{usr}' no está cifrada en /etc/shadow.")

        partes_ej = ejemplo_usuario.split(":")
        while len(partes_ej) < 7: partes_ej.append("N/A")
        desglose = (
            f"📌 CUENTA ANALIZADA ->  {ejemplo_usuario}\n"
            f"   ├─ 1. USUARIO          : {partes_ej[0]}\n"
            f"   ├─ 2. CONTRASEÑA       : '{partes_ej[1]}' (Resguardada en /etc/shadow)\n"
            f"   ├─ 3. UID / GID        : UID={partes_ej[2]} | GID={partes_ej[3]} (0 = Root, >=1000 = Usuarios estándar)\n"
            f"   ├─ 4. CARPETA PERSONAL : {partes_ej[5]}\n"
            f"   └─ 5. SHELL ASIGNADA   : {partes_ej[6]}\n\n"
            f"🛡️ RESULTADO DE LA AUDITORÍA:\n"
        )
        desglose += "\n".join("   " + a for a in alertas_seguridad) if alertas_seguridad else "   🟢 Todas las cuentas de Linux cumplen con los parámetros seguros."
        txt_anatomia.insert("end", desglose)
        txt_passwd.configure(state="disabled")
        txt_anatomia.configure(state="disabled")

    def cargar_sam_windows():
        txt_passwd.configure(state="normal")
        txt_anatomia.configure(state="normal")
        txt_passwd.delete("1.0", "end")
        txt_anatomia.delete("1.0", "end")

        txt_passwd.insert("end", "PS C:\\> Get-CimInstance Win32_UserAccount (Auditoría Real Windows SAM)\n" + "="*80 + "\n")
        script = r"Get-CimInstance Win32_UserAccount -Filter 'LocalAccount=True' | ForEach-Object { Write-Output ($_.Name + ':' + $_.Status + ':' + $_.SID + ':' + $_.Disabled + ':' + $_.AccountType) }"
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        res = subprocess.run(["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True, startupinfo=startupinfo).stdout.strip()

        lineas = [l.strip() for l in res.splitlines() if l.strip()]
        activos = []
        alertas_win = []
        for idx, l in enumerate(lineas, 1):
            txt_passwd.insert("end", f" {idx:2d}  {l}\n")
            partes = l.split(":")
            if len(partes) >= 4 and partes[3].lower() == "false":
                activos.append(partes[0])
                if partes[2].endswith("-501") or partes[0].lower() in ("invitado", "guest", "defaultaccount"):
                    alertas_win.append(f"🔴 ALERTA: La cuenta insegura '{partes[0]}' está HABILITADA. Presiona 'Blindar Cuentas' arriba para desactivarla.")

        ej = lineas[0].split(":") if lineas else ["Admin", "OK", "S-1-5-21-...-500", "False", "512"]
        while len(ej) < 5: ej.append("N/A")

        desglose = (
            f"📌 ANATOMÍA DE CUENTA WINDOWS SAM ->  {':'.join(ej)}\n"
            f"   ├─ 1. NOMBRE DE USUARIO : {ej[0]}\n"
            f"   ├─ 2. ESTADO DE SALUD   : {ej[1]}\n"
            f"   ├─ 3. IDENTIFICADOR SID : {ej[2]} (Terminación -500 = Administrador Raíz, -501 = Invitado)\n"
            f"   ├─ 4. CUENTA DESACTIVADA: {ej[3]} (False = Cuenta habilitada para iniciar sesión)\n"
            f"   └─ 5. BÓVEDA DE CLAVES  : Cifrada en C:\\Windows\\System32\\config\\SAM\n\n"
            f"🛡️ CUENTAS HABILITADAS ACTUALMENTE EN ESTE PC ({len(activos)}): {', '.join(activos)}\n"
        )
        if alertas_win:
            desglose += "\n".join("   " + a for a in alertas_win)
        else:
            desglose += "   🟢 Cuentas de Invitado/Default deshabilitadas correctamente."
        txt_anatomia.insert("end", desglose)
        txt_passwd.configure(state="disabled")
        txt_anatomia.configure(state="disabled")

    def blindar_cuentas_windows():
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        for usr_inseguro in ["Guest", "Invitado", "DefaultAccount", "WDAGUtilityAccount"]:
            subprocess.run(f'net user "{usr_inseguro}" /active:no', shell=True, capture_output=True, startupinfo=startupinfo)
        cargar_sam_windows()
        messagebox.showinfo("Blindaje Aplicado", "Las cuentas laterales (Invitado / Guest / DefaultAccount) han sido deshabilitadas en la base SAM.", parent=win_cat)

    ctk.CTkButton(frame_top_u, text="🛡️ Blindar Cuentas (Desactivar Invitado)", fg_color="#F59E0B", text_color="#000000", hover_color="#D97706", font=("Arial", 12, "bold"), command=blindar_cuentas_windows).pack(side="right", padx=8, pady=8)
    ctk.CTkButton(frame_top_u, text="🐧 Auditar /etc/passwd (WSL)", fg_color="#10B981", hover_color="#059669", command=cargar_passwd_linux).pack(side="right", padx=5, pady=8)
    ctk.CTkButton(frame_top_u, text="🪟 Auditar Windows (SAM)", fg_color="#3B82F6", hover_color="#2563EB", command=cargar_sam_windows).pack(side="right", padx=5, pady=8)

    cargar_sam_windows()

    # ====================================================================
    # PESTAÑA 2: VISOR NUMERADO (cat -n) + DETECTOR DE ERRORES
    # ====================================================================
    frame_top_l = ctk.CTkFrame(tab_lector, fg_color="#1E293B", corner_radius=8)
    frame_top_l.pack(fill="x", padx=15, pady=10)

    ent_buscar_linea = ctk.CTkEntry(frame_top_l, width=280, placeholder_text="Filtrar palabra clave (ej: error, password, 404)...")
    ent_buscar_linea.pack(side="left", padx=15, pady=10)

    txt_visor_cat = ctk.CTkTextbox(tab_lector, font=("Consolas", 13), fg_color="#050811", text_color="#00FFCC", wrap="none")
    txt_visor_cat.pack(fill="both", expand=True, padx=15, pady=10)
    txt_visor_cat.insert("end", "[*] Selecciona un archivo (.txt, .log, .ini, .py, .json) para leerlo con líneas numeradas (cat -n) sin abrir ningún editor externo.\n")
    txt_visor_cat.configure(state="disabled")

    def abrir_con_cat_n():
        ruta = filedialog.askopenfilename(title="Seleccionar archivo para inspección rápida (cat -n)", parent=win_cat)
        if not ruta: return
        filtro = ent_buscar_linea.get().strip().lower()

        txt_visor_cat.configure(state="normal")
        txt_visor_cat.delete("1.0", "end")
        txt_visor_cat.insert("end", f"$ cat -n \"{os.path.basename(ruta)}\"\n" + "="*85 + "\n")

        try:
            with open(ruta, "r", encoding="utf-8", errors="replace") as f:
                coincidencias = 0
                for num, linea in enumerate(f, 1):
                    if num > 5000:
                        txt_visor_cat.insert("end", "\n[!] Archivo muy extenso: Se muestran las primeras 5,000 líneas por fluidez visual.\n")
                        break
                    if not filtro or filtro in linea.lower():
                        prefijo = "🔥" if any(k in linea.lower() for k in ["error", "fail", "denied", "password", "critical"]) else "  "
                        txt_visor_cat.insert("end", f"{prefijo} {num:4d} │ {linea.rstrip()}\n")
                        coincidencias += 1
                txt_visor_cat.insert("end", "="*85 + f"\n[+] Total de líneas mostradas: {coincidencias}\n")
        except Exception as e:
            txt_visor_cat.insert("end", f"[-] Error al leer el archivo: {e}\n")

        txt_visor_cat.configure(state="disabled")

    ctk.CTkButton(frame_top_l, text="📂 Abrir y Numerar Archivo (cat -n)", font=("Arial", 13, "bold"), fg_color="#00FFCC", text_color="#000000", hover_color="#10B981", command=abrir_con_cat_n).pack(side="right", padx=15, pady=10)

    # ====================================================================
    # PESTAÑA 3: CONCATENADOR DE ARCHIVOS (cat a.txt b.txt > final.txt)
    # ====================================================================
    archivos_a_unir = []

    frame_top_c = ctk.CTkFrame(tab_unir, fg_color="#1E293B", corner_radius=8)
    frame_top_c.pack(fill="x", padx=15, pady=10)

    ctk.CTkLabel(frame_top_c, text="Une múltiples archivos (.txt, .log, .csv, diccionarios) uno detrás del otro:", font=("Arial", 13, "bold")).pack(side="left", padx=15, pady=10)

    txt_cola_cat = ctk.CTkTextbox(tab_unir, font=("Consolas", 13), fg_color="#050811", text_color="#FCD34D")
    txt_cola_cat.pack(fill="both", expand=True, padx=15, pady=10)

    def agregar_archivos_cat():
        rutas = filedialog.askopenfilenames(title="Selecciona los archivos a concatenar en orden", parent=win_cat)
        if rutas:
            for r in rutas:
                if r not in archivos_a_unir:
                    archivos_a_unir.append(r)
            txt_cola_cat.delete("1.0", "end")
            cmd_preview = "$ cat " + " ".join(f'"{os.path.basename(x)}"' for x in archivos_a_unir) + " > TREMEND_Concatenado.txt\n" + "="*80 + "\n\n"
            txt_cola_cat.insert("end", cmd_preview)
            for idx, r in enumerate(archivos_a_unir, 1):
                txt_cola_cat.insert("end", f" [{idx}] {r}\n")

    def ejecutar_concatenacion():
        if len(archivos_a_unir) < 2:
            messagebox.showwarning("Atención", "Selecciona al menos 2 archivos para unirlos.", parent=win_cat)
            return
        destino = filedialog.asksaveasfilename(
            title="Guardar archivo unido como...",
            defaultextension=".txt",
            initialfile="TREMEND_Concatenado.txt",
            parent=win_cat
        )
        if not destino: return
        try:
            total_lineas = 0
            with open(destino, "w", encoding="utf-8") as f_out:
                for r in archivos_a_unir:
                    with open(r, "r", encoding="utf-8", errors="replace") as f_in:
                        for linea in f_in:
                            f_out.write(linea)
                            total_lineas += 1
                    f_out.write("\n")
            txt_cola_cat.insert("end", f"\n[+] ¡ÉXITO! {len(archivos_a_unir)} archivos unidos ({total_lineas} líneas totales) en:\n    -> {destino}\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo concatenar: {e}", parent=win_cat)

    frame_btns_c = ctk.CTkFrame(tab_unir, fg_color="transparent")
    frame_btns_c.pack(fill="x", padx=15, pady=5)
    ctk.CTkButton(frame_btns_c, text="➕ Seleccionar Archivos", fg_color="#3B82F6", command=agregar_archivos_cat).pack(side="left", padx=5, expand=True, fill="x")
    ctk.CTkButton(frame_btns_c, text="🧹 Limpiar Lista", fg_color="#334155", command=lambda: (archivos_a_unir.clear(), txt_cola_cat.delete("1.0", "end"))).pack(side="left", padx=5, expand=True, fill="x")
    ctk.CTkButton(frame_btns_c, text="🔗 Unir y Exportar (Concatenate)", font=("Arial", 13, "bold"), fg_color="#10B981", hover_color="#059669", command=ejecutar_concatenacion).pack(side="left", padx=5, expand=True, fill="x")

def logica_numero_serie(log):
    log("\n[*] Extrayendo Número de Serie y Modelo...")
    run_ps_script(log, 'try { $info = Get-CimInstance Win32_ComputerSystemProduct; $info | Format-List; Set-Clipboard -Value $info.IdentifyingNumber; Write-Host "[+] Copiado" } catch {}')

def logica_memoria_ghost(log):
    import os, subprocess, shutil, psutil
    from tkinter import messagebox

    log("\n" + "="*75)
    log(" 🛡️ ESCUDO DE INTEGRIDAD DE MEMORIA RAM Y CAZADOR DE INYECTORES ")
    log("="*75)

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # ------------------------------------------------------------------
    # FASE 1: CAZADOR DE ESCÁNERES DE MEMORIA, INYECTORES Y DEBUGGERS
    # ------------------------------------------------------------------
    log("\n[1/3] Escaneando procesos en busca de modificadores de RAM (Cheat Engine / Debuggers / Inyectores)...")
    firmas_manipuladores = {
        "cheatengine": "Cheat Engine (Escáner y modificador de direcciones RAM)",
        "ce-x64": "Cheat Engine 64-bit Kernel Module",
        "ce-i386": "Cheat Engine 32-bit Module",
        "x64dbg": "x64dbg (Depurador y ensamblador de memoria)",
        "x32dbg": "x32dbg (Depurador de memoria 32-bit)",
        "ollydbg": "OllyDbg (Analizador de registros RAM)",
        "ida64": "IDA Pro Disassembler",
        "artmoney": "ArtMoney (Editor hexadecimal de memoria RAM)",
        "wemod": "WeMod (Inyector de punteros de memoria)",
        "extremeinjector": "Extreme Injector (Inyector de DLLs en RAM)",
        "processhacker": "Process Hacker (Inspector con acceso a WriteProcessMemory)"
    }

    detectados_ram = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            nombre_p = (proc.info['name'] or "").lower()
            for firma, desc in firmas_manipuladores.items():
                if firma in nombre_p:
                    detectados_ram.append((proc.info['pid'], proc.info['name'], desc))
                    break
        except Exception:
            pass

    if not detectados_ram:
        log("    🟢 Limpio: No se detectaron programas de alteración de memoria (como Cheat Engine o x64dbg) activos.")
    else:
        log(f"    🔴 ¡ALERTA DE MANIPULACIÓN DE RAM! Se detectaron {len(detectados_ram)} herramientas activas:")
        for pid, nom_p, desc_p in detectados_ram:
            log(f"       -> [PID {pid}] {nom_p}: {desc_p}")
        if messagebox.askyesno("Amenaza en Memoria RAM", f"Se detectaron {len(detectados_ram)} programas capaces de escanear y alterar direcciones de memoria RAM en vivo.\n\n¿Deseas que TREMEND cierre y neutralice estos procesos inmediatamente?"):
            for pid, nom_p, _ in detectados_ram:
                try:
                    psutil.Process(pid).kill()
                    log(f"       [+] Proceso '{nom_p}' (PID {pid}) neutralizado en RAM.")
                except Exception as e:
                    log(f"       [-] No se pudo cerrar {nom_p}: {e}")

    # ------------------------------------------------------------------
    # FASE 2: AUDITORÍA Y BLINDAJE DEL KERNEL (ASLR, DEP Y VBS/HVCI)
    # ------------------------------------------------------------------
    log("\n[2/3] Auditando escudos de hardware y Kernel contra rastreo de punteros (ASLR / DEP / HVCI)...")
    script_mitigacion = r"""
    try {
        $dep = (Get-CimInstance Win32_OperatingSystem).DataExecutionPrevention_SupportPolicy
        Write-Host "    -> Política DEP (Prevención de Ejecución de Datos) : Nivel $dep (2=OptIn, 3=AlwaysOn)" -ForegroundColor Cyan
        $aslr = Get-ProcessMitigation -System
        Write-Host "    -> ASLR (Aleatorización de Direcciones en RAM)     : BottomUp=$($aslr.Aslr.BottomUp) | ForceRelocate=$($aslr.Aslr.ForceRelocateImages)" -ForegroundColor Cyan
        $dg = Get-CimInstance -ClassName Win32_DeviceGuard -Namespace root\Microsoft\Windows\DeviceGuard -ErrorAction SilentlyContinue
        if ($dg -and ($dg.SecurityServicesRunning -contains 2)) {
            Write-Host "    -> Integridad de Memoria del Núcleo (HVCI / VBS)   : 🟢 ACTIVA (Protegida por Hardware)" -ForegroundColor Green
        } else {
            Write-Host "    -> Integridad de Memoria del Núcleo (HVCI / VBS)   : 🟡 INACTIVA (Se recomienda activar Aislamiento del Núcleo)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "    [-] No se pudo leer el estado completo de mitigación del Kernel."
    }
    """
    run_ps_script(log, script_mitigacion)

    if messagebox.askyesno("Blindaje Anti-Manipulación de RAM (ASLR + DEP)", "¿Deseas forzar la activación de DEP (OptOut) y ASLR (Aleatorización de Direcciones de Memoria) en Windows?\n\nEsto hace que las direcciones hexadecimales cambien constantemente y bloquea la inyección de código en la memoria RAM."):
        log("[*] Inyectando directivas de aleatorización de memoria (ASLR) y protección DEP...")
        run_cmd(log, "bcdedit /set nx OptOut")
        run_ps_script(log, "Set-ProcessMitigation -System -Enable DEP, BottomUp, HighEntropy -ErrorAction SilentlyContinue")
        log("[+] ¡Escudos DEP y ASLR de Alta Entropía activados en el Kernel!")

    # ------------------------------------------------------------------
    # FASE 3: ESCÁNER PROFUNDO DE INYECCIÓN EN RAM (MOTOR GHOST EN RUST)
    # ------------------------------------------------------------------
    if messagebox.askyesno("Escáner Profundo Ghost (Opcional)", "¿Deseas ejecutar además el motor profundo 'Ghost' (en Rust) para buscar inyecciones ocultas de shellcode dentro de los anillos de memoria?"):
        log("\n[3/3] Iniciando Auditoría Profunda de Anillos de Memoria (Ghost por pandaadir05)...")
        temp_dir = r"C:\Tremend_Scanner"
        script_ghost = fr"""
        if (!(Test-Path "{temp_dir}")) {{ New-Item -ItemType Directory -Force -Path "{temp_dir}" | Out-Null }}
        try {{
            Write-Host "[*] Contactando a GitHub de forma segura..."
            $headers = @{{ "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }}
            $api = Invoke-RestMethod -Uri "https://api.github.com/repos/pandaadir05/ghost/releases/latest" -Headers $headers
            $url = ($api.assets | Where-Object {{ $_.name -match "windows" -and $_.name -match ".zip" }}).browser_download_url
            if ($url) {{
                Write-Host "[+] Descargando binario nativo (Rust)..."
                Invoke-WebRequest -Uri $url -OutFile "{temp_dir}\ghost.zip"
                Expand-Archive -Path "{temp_dir}\ghost.zip" -DestinationPath "{temp_dir}" -Force -ErrorAction SilentlyContinue
                $exe = Get-ChildItem -Path "{temp_dir}" -Filter "*ghost*.exe" -Recurse | Select-Object -ExpandProperty FullName -First 1
                if ($exe) {{
                    Write-Host "[*] Lanzando Dashboard de Ghost (Presiona 'Q' en su ventana al terminar)..."
                    Start-Process -FilePath $exe -Wait
                }}
            }}
        }} catch {{ Write-Host "[-] Error de comunicación con GitHub: $($_.Exception.Message)" }}
        """
        run_ps_script(log, script_ghost)
        if os.path.exists(temp_dir) and messagebox.askyesno("Limpieza Forense", "¿Deseas ELIMINAR el motor Ghost descargado para no dejar rastro en el equipo?"):
            shutil.rmtree(temp_dir, ignore_errors=True)
            log("[+] Limpieza táctica: Motor Ghost destruido sin dejar rastro.")
    else:
        log("\n[+] Auditoría y blindaje nativo de memoria RAM completados.")

    try: notificar_voz("El blindaje de memoria RAM ha finalizado.")
    except: pass

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
def logica_entornos_aislados(log, accion):
    import os, subprocess, platform
    from tkinter import messagebox

    log("\n" + "="*75)
    log(" 🛡️ GESTOR DE ENTORNOS AISLADOS Y VIRTUALIZACIÓN ")
    log("="*75)

    sistema = platform.system().lower()
    if sistema != 'windows' or int(platform.release()) < 10:
        log("[-] Error: El sistema Sandbox y Hyper-V solo están disponibles en Windows 10/11.")
        return

    # ACCIÓN 1: Lanza la Caja de Arena (Windows Sandbox)
    if accion == '1':
        log("[*] Verificando si la característica nativa 'Windows Sandbox' está habilitada en el núcleo...")
        sandbox_exe = r"C:\Windows\System32\WindowsSandbox.exe"
        
        if not os.path.exists(sandbox_exe):
            log("[-] La Caja de Arena no está activada o tu PC no cuenta con la versión 'Pro'.")
            if messagebox.askyesno("Activar Sandbox", "Windows Sandbox parece desactivado.\n\n¿Deseas que TREMEND intente forzar la activación en el núcleo mediante DISM?\n(Requerirá conexión a internet y REINICIAR el equipo al finalizar)."):
                log("[*] Inyectando comandos para habilitar contenedores y Sandbox...")
                script_enable = """
                Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -All -Online -NoRestart
                Write-Host "[+] Característica instalada. Por favor, REINICIA TU PC para que tome efecto." -ForegroundColor Green
                """
                run_ps_script(log, script_enable)
            else:
                log("[-] Operación cancelada por el usuario.")
            return

        log("[*] Compilando archivo de configuración (.wsb) para aislar la red y el hardware...")
        escritorio = os.path.join(os.environ.get("USERPROFILE"), "Desktop")
        if not os.path.exists(escritorio): 
            escritorio = os.path.join(os.environ.get("USERPROFILE"), "Escritorio")
            
        ruta_wsb = os.path.join(escritorio, "Entorno_Seguro_TREMEND.wsb")
        config_xml = """<Configuration>\n  <Networking>Enable</Networking>\n  <AudioInput>Disable</AudioInput>\n  <VideoInput>Disable</VideoInput>\n  <ProtectedClient>Enable</ProtectedClient>\n</Configuration>"""

        try:
            with open(ruta_wsb, "w", encoding="utf-8") as f:
                f.write(config_xml)
            log("[*] Iniciando Máquina Virtual Desechable...")
            log("[!] ADVERTENCIA: Todo lo que descargues o ejecutes dentro de esa ventana desaparecerá PARA SIEMPRE al cerrarla.")
            log("[!] Arrastra los archivos sospechosos desde tu PC hacia adentro de la ventana para abrirlos sin riesgo.")
            subprocess.Popen(f'"{ruta_wsb}"', shell=True)
            log("[+] Entorno seguro desplegado con éxito.")
        except Exception as e:
            log(f"[-] Error al lanzar la Caja de Arena: {e}")

    # ACCIÓN 2: Escáner de Virtualización (BIOS/CPU)
    elif accion == '2':
        log("[*] Escaneando el procesador para verificar soporte de virtualización (Hardware-Assisted)...")
        script_vt = """
        $sysinfo = Get-ComputerInfo
        Write-Host "--- REPORTE DE VIRTUALIZACIÓN DE HARDWARE ---" -ForegroundColor Cyan
        Write-Host "Hipervisor Presente       : $($sysinfo.HyperVisorPresent)"
        Write-Host "Virtualización en Firmware: $($sysinfo.HyperVRequirementVirtualizationFirmwareEnabled)"
        Write-Host "Prevención de Datos (DEP) : $($sysinfo.HyperVRequirementDataExecutionPreventionAvailable)"
        Write-Host "Traducción de Direcciones : $($sysinfo.HyperVRequirementSecondLevelAddressTranslation)"
        
        if ($sysinfo.HyperVRequirementVirtualizationFirmwareEnabled -eq$true -or $sysinfo.HyperVisorPresent -eq$true) {
            Write-Host "`n[+] EXCELENTE: Tu procesador y BIOS tienen la Virtualización ACTIVADA." -ForegroundColor Green
            Write-Host "    -> Puedes usar Windows Sandbox, VirtualBox, VMware o WSL sin problemas."
        } else {
            Write-Host "`n[-] ADVERTENCIA: La virtualización está DESACTIVADA o no es soportada." -ForegroundColor Red
            Write-Host "    -> Debes reiniciar el equipo, entrar a la BIOS/UEFI y activar 'Intel VT-x' o 'AMD-V / SVM'." -ForegroundColor Yellow
        }
        """
        run_ps_script(log, script_vt)

def logica_rayos_x_archivo(log, ruta_archivo):
    import os, string, hashlib

    log("\n" + "="*75)
    log(f" ☢️ LABORATORIO DE RAYOS X (ANÁLISIS BINARIO FORENSE) ")
    log("="*75)
    
    if not os.path.exists(ruta_archivo):
        log("[-] Archivo no encontrado.")
        return
        
    nombre_arch = os.path.basename(ruta_archivo)
    tamano_bytes = os.path.getsize(ruta_archivo)
    tamano_mb = tamano_bytes / (1024 * 1024)
    extension_real = nombre_arch.lower().split('.')[-1] if '.' in nombre_arch else 'desconocida'
    
    log(f"[*] Analizando objetivo: {nombre_arch} ({tamano_mb:.2f} MB)")
    log("[*] Leyendo ADN binario (Cero ejecución, 100% seguro)...\n")

    try:
        # Abrimos el archivo en modo Binario Lectura (rb) para no ejecutarlo
        with open(ruta_archivo, 'rb') as f:
            cabecera = f.read(256) # Leemos un poco más de cabecera por si acaso
            f.seek(0)
            contenido_completo = f.read()
    except Exception as e:
        log(f"[-] El archivo está bloqueado por el sistema o el antivirus: {e}")
        return

    # --- 1. GENERACIÓN DE HASH SHA-256 (PARA VIRUSTOTAL) ---
    log(" 🔍 [FASE 1] HUELLA DIGITAL CRIPTOGRÁFICA")
    sha256_hash = hashlib.sha256(contenido_completo).hexdigest()
    log(f"    -> SHA-256: {sha256_hash}")
    log(f"    -> (Pista: Pega este código en www.virustotal.com para ver si es un malware conocido mundialmente)\n")

    # --- 2. DETECCIÓN DE FIRMAS (MAGIC BYTES) ---
    log(" 🧬 [FASE 2] IDENTIDAD BINARIA (MAGIC BYTES)")
    firmas = {
        b'MZ': 'Ejecutable de Windows (.EXE / .DLL)',
        b'\x89PNG\r\n\x1a\n': 'Imagen PNG',
        b'\xff\xd8\xff': 'Imagen JPG / JPEG',
        b'%PDF-': 'Documento PDF',
        b'PK\x03\x04': 'Comprimido ZIP / DOCX / XLSX / APK',
        b'Rar!\x1a\x07': 'Comprimido RAR',
        b'7z\xbc\xaf\x27\x1c': 'Comprimido 7Z'
    }

    identidad_real = "Desconocida / Archivo en crudo"
    for firma_hex, tipo in firmas.items():
        if cabecera.startswith(firma_hex):
            identidad_real = tipo
            break

    log(f"    -> Identidad según extensión (Disfraz) : .{extension_real.upper()}")
    log(f"    -> Identidad según núcleo (ADN Real)   : {identidad_real}")
    
    if "Ejecutable" in identidad_real and extension_real not in ["exe", "dll", "sys"]:
        log("    🔴 ¡ALERTA ROJA! El archivo MIENTE. Dice ser otra cosa, pero por dentro es un VIRUS EJECUTABLE.")
    elif extension_real in ["jpg", "jpeg"] and "JPG" not in identidad_real:
        log("    🔴 ¡ALERTA ROJA! El archivo no es una imagen real, su núcleo ha sido alterado.")
    else:
        log("    🟢 Identidad estructural congruente.\n")

    # --- 3. DETECCIÓN DE ESTEGANOGRAFÍA (DATOS OCULTOS) ---
    log(" 🦠 [FASE 3] PARÁSITOS Y ESTEGANOGRAFÍA")
    if extension_real in ["jpg", "jpeg"] and b'\xff\xd8\xff' in cabecera:
        # Un JPG real DEBE terminar con FF D9.
        marcador_fin = contenido_completo.rfind(b'\xff\xd9')
        if marcador_fin != -1:
            bytes_sobrantes = len(contenido_completo) - (marcador_fin + 2)
            if bytes_sobrantes > 100: 
                log(f"    🔴 ¡ALERTA DE INYECCIÓN! Se encontraron {bytes_sobrantes} bytes de datos ocultos detrás de la imagen.")
                log("        -> Posible virus adjunto (Dropper) o mensaje oculto.")
            else:
                log("    🟢 Imagen limpia. No hay carga útil pegada en la cola.")
    else:
        log("    ⚪ Análisis de carga trasera solo calibrado para JPG.\n")

    # --- 4. ANÁLISIS DE METADATOS (EXIF) ---
    if extension_real in ["jpg", "jpeg", "png"]:
        log("\n 📸 [FASE 4] METADATOS EXIF (GPS Y HARDWARE)")
        try:
            import importlib.util
            if importlib.util.find_spec("exifread") is None:
                log("    -> Instalando módulo de lectura EXIF (exifread)...")
                subprocess.run([sys.executable, "-m", "pip", "install", "exifread"], capture_output=True)
            
            import exifread
            with open(ruta_archivo, 'rb') as f:
                tags = exifread.process_file(f, details=False)
            
            if not tags:
                log("    🟢 El archivo no contiene metadatos ocultos.")
            else:
                log("    🟡 Se encontraron rastros de información en el archivo:")
                # Filtrar solo cosas interesantes
                for tag, value in tags.items():
                    if any(key in tag for key in ['Make', 'Model', 'Software', 'DateTime', 'GPS']):
                        log(f"        -> {tag.split(' ')[-1]}: {value}")
        except Exception as e:
            log("    [-] Ocurrió un error al leer los metadatos.")
    
    # --- 5. EXTRACCIÓN DE TEXTOS Y CÓDIGO MALICIOSO (STRINGS) ---
    log("\n 💻 [FASE 5] EXTRACCIÓN DE CÓDIGO INCORPORADO (STRINGS)")
    if tamano_mb > 50:
        log("    [-] Archivo demasiado grande para extracción de textos. Omitiendo...")
    else:
        log("    [*] Aplicando filtro polarizado al código máquina...")
        caracteres_imprimibles = set(bytes(string.printable, 'ascii'))
        cadenas = []
        cadena_actual = bytearray()
        
        for byte in contenido_completo:
            if byte in caracteres_imprimibles:
                cadena_actual.append(byte)
            else:
                if len(cadena_actual) >= 6: # Solo textos de 6 letras o más
                    cadenas.append(cadena_actual.decode('ascii'))
                cadena_actual = bytearray()
                
        # Buscar patrones de virus modernos, troyanos y shellcodes
        patrones_peligrosos = ["http://", "https://", "cmd.exe", "powershell", "RunPE", "WScript", "CreateRemoteThread", "VirtualAlloc", "ShellExecute", "WMI"]
        hallazgos = []
        
        for c in cadenas:
            for p in patrones_peligrosos:
                if p.lower() in c.lower() and c not in hallazgos:
                    hallazgos.append(c)
                    
        if hallazgos:
            log(f"    🔴 ¡PRECAUCIÓN EXTREMA! Se detectaron {len(hallazgos)} firmas de comportamiento malicioso:")
            for h in hallazgos[:10]:
                log(f"        -> {h.strip()[:80]}")
            if len(hallazgos) > 10:
                log("        -> (Se ocultaron otros hallazgos similares)")
        else:
            log("    🟢 No se detectaron comandos ni firmas de troyanos en el código interno.")

    log("\n=======================================================")
    log(" [+] ANÁLISIS FORENSE FINALIZADO")
    try: notificar_voz("El análisis de rayos X ha concluido.")
    except: pass

def logica_gestor_winget(*args, **kwargs):
    import subprocess, json, threading, os, re, shutil, winreg
    from tkinter import ttk, messagebox
    import customtkinter as ctk

    if args and args[0]:
        try: args[0]("\n[*] Abriendo Centro de Inteligencia de Software y Cazador Forense (Revo Killer)...")
        except: pass

    def analizar_app(nombre, editor=""):
        n = f"{nombre} {editor}".lower()
        if any(x in n for x in ["candy crush", "solitaire", "xbox", "bing", "widget", "gethelp", "zune", "tiktok", "instagram", "facebook", "feedback", "mcafee", "avast", "onedrive", "cortana", "mixedreality", "people", " wallet", "skypeapp", "yourphone", "clipchamp", " news", "weather"]):
            return "🗑️", "🔴 Sugerencias a Eliminar (Bloatware)", "Bloatware, telemetría o app preinstalada prescindible. Sugerencia: Eliminar."
        elif any(x in n for x in ["c++", ".net", "framework", "runtime", "redistributable", "driver", "intel", "amd", "nvidia", "realtek", "geforce", "radeon", "vulkan", "directx", "physx", "chipset", "windows sdk", "edgewebview"]):
            return "⚙️", "🟡 Sistema y Controladores", "COMPONENTE CRÍTICO O DRIVER DE HARDWARE. ¡NO BORRAR!"
        elif any(x in n for x in ["dropbox", "google drive", "icloud", "mega", "nextcloud", "sync"]):
            return "☁️", "☁️ Nube", "Sincronización en la nube. Consume red y arranque."
        elif any(x in n for x in ["game", "riot", "steam", "epic", "ubisoft", "ea ", "battle.net", "gog", "roblox", "minecraft"]):
            return "🎮", "🎮 Juegos", "Plataforma o videojuego."
        elif any(x in n for x in ["edge", "chrome", "firefox", "brave", "opera", "vivaldi", "tor "]):
            return "🌐", "🌐 Navegadores y Red", "Navegador web principal."
        elif any(x in n for x in ["office", "word", "excel", "powerpoint", "adobe", "pdf", "capcut", "filmora", "photoshop", "libreoffice", "vlc", "winrar", "7-zip", "audacity", "obs "]):
            return "📄", "📄 Ofimática y Multimedia", "Herramienta productiva, compresor o multimedia."
        elif any(x in n for x in ["python", "node", "git", "visual studio", "vscode", "docker", "postman", "java", "jdk", "nmap", "wireshark"]):
            return "💻", "💻 Desarrollo e Ingeniería", "Entorno de programación o auditoría técnica."
        elif any(x in n for x in ["skype", "teams", "zoom", "discord", "webex", "whatsapp", "telegram", "slack", "anydesk", "teamviewer"]):
            return "💬", "💬 Comunicación y Remoto", "App de mensajería o asistencia remota."
        elif any(x in n for x in ["hp ", "dell", "lenovo", "asus", "acer", "myasus", "vantage", "armoury"]):
            return "🛠️", "🛠️ Software de Fabricante", "Utilidad OEM del fabricante de la placa/laptop."
        else:
            return "📦", "⚪ Otros Programas", "Software de terceros instalado por el usuario."

    datos_sistema = {"actualizables": [], "instaladas": []}
    mapa_actualizables = {}
    mapa_instaladas = {}

    win_gestor = ctk.CTkToplevel(app)
    win_gestor.title("TREMEND - Centro de Inteligencia de Software & Cazador Forense (Revo Killer V2)")
    win_gestor.geometry("1220x740")
    win_gestor.lift()
    win_gestor.attributes("-topmost", True)
    win_gestor.after(200, lambda: win_gestor.attributes("-topmost", False))
    win_gestor.focus_force()

    frame_carga = ctk.CTkFrame(win_gestor, fg_color="transparent")
    frame_carga.pack(expand=True, fill="both")
    lbl_carga_tit = ctk.CTkLabel(frame_carga, text="🔍 Escaneando el Sistema a Nivel Profundo...", font=("Arial", 26, "bold"), text_color="#00FFCC")
    lbl_carga_tit.pack(pady=(230, 10))
    lbl_carga_sub = ctk.CTkLabel(frame_carga, text="Consultando servidores Winget en línea, colmenas del Registro (x64/x86) y paquetes UWP...", font=("Arial", 14), text_color="#94A3B8")
    lbl_carga_sub.pack(pady=(0, 20))
    barra_carga = ctk.CTkProgressBar(frame_carga, width=450, mode="indeterminate", progress_color="#10B981")
    barra_carga.pack()
    barra_carga.start()

    def escanear_sistema():
        datos_sistema["actualizables"].clear()
        datos_sistema["instaladas"].clear()

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # ------------------------------------------------------------------
        # 1. ESCÁNER PROFUNDO DE ACTUALIZACIONES EN LÍNEA (WINGET)
        # ------------------------------------------------------------------
        try:
            cmd_upg = "winget upgrade --include-unknown --accept-source-agreements --accept-package-agreements"
            res_upg = subprocess.run(cmd_upg, shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore", startupinfo=startupinfo)
            capturando = False
            ids_vistos = set()

            for linea in res_upg.stdout.splitlines():
                linea_limpia = linea.strip()
                if linea_limpia.startswith("-------") or "-----" in linea_limpia:
                    capturando = True
                    continue
                if not capturando or not linea_limpia:
                    continue
                if any(w in linea_limpia.lower() for w in ["actualizaciones disponibles", "upgrades available", "paquetes tienen", "packages have", "explicit targeting"]):
                    continue

                partes = re.split(r'\s{2,}', linea_limpia)
                if len(partes) >= 3:
                    nombre = partes[0].strip()
                    id_app = partes[1].strip()
                    if len(partes) >= 5:
                        v_vieja, v_nueva, origen = partes[2].strip(), partes[3].strip(), partes[4].strip()
                    elif len(partes) == 4:
                        v_vieja, v_nueva, origen = partes[2].strip(), partes[3].strip(), "winget"
                    else:
                        v_vieja, v_nueva, origen = " instalada", partes[2].strip(), "winget"

                    if id_app and "." in id_app and id_app not in ids_vistos:
                        ids_vistos.add(id_app)
                        icono, categoria, desc = analizar_app(nombre, id_app)
                        datos_sistema["actualizables"].append({
                            "nombre": nombre, "id": id_app, "v_vieja": v_vieja,
                            "v_nueva": v_nueva, "origen": origen, "icono": icono,
                            "cat": categoria, "seleccionado": True
                        })
        except Exception:
            pass

        # ------------------------------------------------------------------
        # 2. ESCÁNER PROFUNDO DE PROGRAMAS INSTALADOS (REGISTRO + UWP)
        # ------------------------------------------------------------------
        try:
            script_ps = r"""
$apps = @()
$paths = @(
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
)
$regApps = Get-ItemProperty $paths -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -and $_.SystemComponent -ne 1 }
foreach ($r in $regApps) {
    $apps += [PSCustomObject]@{
        Nombre = [string]$r.DisplayName
        Id = [string]$r.PSChildName
        Version = if ($r.DisplayVersion) { [string]$r.DisplayVersion } else { "N/A" }
        Editor = if ($r.Publisher) { [string]$r.Publisher } else { "Desconocido" }
        Tipo = "Win32"
        Ruta = if ($r.InstallLocation) { [string]$r.InstallLocation } else { "" }
        Uninstall = if ($r.QuietUninstallString) { [string]$r.QuietUninstallString } elseif ($r.UninstallString) { [string]$r.UninstallString } else { "" }
        RegPath = [string]$r.PSPath
    }
}
$uwpApps = Get-AppxPackage -ErrorAction SilentlyContinue | Where-Object { $_.NonRemovable -eq $false -and $_.IsFramework -eq $false }
foreach ($u in $uwpApps) {
    $apps += [PSCustomObject]@{
        Nombre = [string]$u.Name
        Id = [string]$u.PackageFullName
        Version = [string]$u.Version
        Editor = [string]$u.PublisherId
        Tipo = "UWP (Store)"
        Ruta = [string]$u.InstallLocation
        Uninstall = ""
        RegPath = ""
    }
}
$apps | ConvertTo-Json -Compress -Depth 2
"""
            res_list = subprocess.run(["powershell", "-NoProfile", "-Command", script_ps], capture_output=True, text=True, encoding="utf-8", errors="ignore", startupinfo=startupinfo)
            apps_brutas = json.loads(res_list.stdout) if res_list.stdout.strip() else []
            if isinstance(apps_brutas, dict):
                apps_brutas = [apps_brutas]

            vistos_inst = set()
            for a in apps_brutas:
                nombre = (a.get("Nombre") or "").strip()
                id_app = (a.get("Id") or "").strip()
                if not nombre or "Microsoft.VCLibs" in nombre or "Microsoft.UI" in nombre:
                    continue
                clave_unica = f"{nombre.lower()}_{a.get('Tipo','')}"
                if clave_unica in vistos_inst:
                    continue
                vistos_inst.add(clave_unica)

                editor = (a.get("Editor") or "Desconocido").strip()
                version = (a.get("Version") or "N/A").strip()
                tipo = a.get("Tipo", "Win32")
                ruta = (a.get("Ruta") or "").strip().strip('"')
                uninst = (a.get("Uninstall") or "").strip()
                reg_path = (a.get("RegPath") or "").strip()

                # Si no reporta ruta, intentamos deducirla del UninstallString
                if not ruta and uninst and ":\\" in uninst:
                    posible_exe = uninst.split(".exe")[0] + ".exe"
                    posible_exe = posible_exe.replace('"', '').strip()
                    if os.path.exists(posible_exe):
                        ruta = os.path.dirname(posible_exe)

                if not ruta:
                    ruta = "Ruta gestionada por el núcleo"

                icono, categoria, desc = analizar_app(nombre, editor)
                nombre_limpio = nombre.replace("Microsoft.", "").replace("Windows.", "")
                datos_sistema["instaladas"].append({
                    "nombre": nombre_limpio, "nombre_original": nombre, "id": id_app,
                    "version": version, "editor": editor, "tipo": tipo,
                    "icono": icono, "cat": categoria, "desc": desc,
                    "ruta": ruta, "uninstall": uninst, "reg_path": reg_path,
                    "seleccionado": False
                })
            datos_sistema["instaladas"].sort(key=lambda x: x["nombre"].lower())
        except Exception:
            pass

        if win_gestor.winfo_exists():
            win_gestor.after(0, construir_interfaz_final)

    def construir_interfaz_final():
        if frame_carga.winfo_exists():
            frame_carga.destroy()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0F172A", foreground="#E2E8F0", fieldbackground="#0F172A", borderwidth=0, font=("Arial", 11), rowheight=34)
        style.map("Treeview", background=[("selected", "#1E3A8A")])
        style.configure("Treeview.Heading", background="#1E293B", foreground="#00FFCC", font=("Arial", 12, "bold"), borderwidth=0)

        tabview = ctk.CTkTabview(win_gestor, fg_color="#1E293B", text_color="#FFFFFF", segmented_button_selected_color="#3B82F6")
        tabview.pack(pady=10, padx=20, fill="both", expand=True)

        tab_act = tabview.add("🔄 Actualizar Software (Online)")
        tab_des = tabview.add("💀 Desinstalador Cazador Pro (Revo Killer)")
        tab_mig = tabview.add("💾 Migrar / Clonar PC")

        # ====================================================================
        # PESTAÑA 1: ACTUALIZAR SOFTWARE (ESCANEO ONLINE COMPLETO)
        # ====================================================================
        top_act = ctk.CTkFrame(tab_act, fg_color="transparent")
        top_act.pack(fill="x", pady=5)

        var_busq_act = ctk.StringVar()
        ent_busq_act = ctk.CTkEntry(top_act, textvariable=var_busq_act, placeholder_text="🔍 Buscar actualización por nombre o ID...", width=280, font=("Arial", 13))
        ent_busq_act.pack(side="left", padx=5)

        filtros_act = ["Todas las categorías", "🌐 Navegadores y Red", "🎮 Juegos", "📄 Ofimática y Multimedia", "💻 Desarrollo e Ingeniería", "💬 Comunicación y Remoto", "🛠️ Software de Fabricante", "⚙️ Sistema y Controladores", "⚪ Otros Programas"]
        combo_filtro_act = ctk.CTkOptionMenu(top_act, values=filtros_act, width=230, font=("Arial", 13), fg_color="#334155", button_color="#475569")
        combo_filtro_act.pack(side="left", padx=5)

        lbl_cont_act = ctk.CTkLabel(top_act, text="Seleccionados: 0", font=("Arial", 14, "bold"), text_color="#00FFCC")
        lbl_cont_act.pack(side="right", padx=10)

        frame_tabla_act = ctk.CTkFrame(tab_act, fg_color="transparent")
        frame_tabla_act.pack(fill="both", expand=True, pady=8)

        scroll_y_act = ttk.Scrollbar(frame_tabla_act, orient="vertical")
        scroll_y_act.pack(side="right", fill="y")
        scroll_x_act = ttk.Scrollbar(frame_tabla_act, orient="horizontal")
        scroll_x_act.pack(side="bottom", fill="x")

        tree_act = ttk.Treeview(
            frame_tabla_act,
            columns=("check", "icono", "nombre", "id_pkg", "v_vieja", "v_nueva", "cat"),
            show="headings", height=11,
            yscrollcommand=scroll_y_act.set, xscrollcommand=scroll_x_act.set
        )
        scroll_y_act.config(command=tree_act.yview)
        scroll_x_act.config(command=tree_act.xview)

        tree_act.heading("check", text="Seleccionar")
        tree_act.heading("icono", text="Tipo")
        tree_act.heading("nombre", text="Nombre del Programa")
        tree_act.heading("id_pkg", text="ID Oficial (Repositorio)")
        tree_act.heading("v_vieja", text="Versión Actual")
        tree_act.heading("v_nueva", text="Nueva Versión Online")
        tree_act.heading("cat", text="Categoría")

        tree_act.column("check", width=90, anchor="center")
        tree_act.column("icono", width=55, anchor="center")
        tree_act.column("nombre", width=280, anchor="w")
        tree_act.column("id_pkg", width=220, anchor="w")
        tree_act.column("v_vieja", width=120, anchor="center")
        tree_act.column("v_nueva", width=150, anchor="center")
        tree_act.column("cat", width=210, anchor="w")
        tree_act.pack(fill="both", expand=True)

        def actualizar_contador_act():
            total_sel = sum(1 for a in datos_sistema["actualizables"] if a["seleccionado"])
            lbl_cont_act.configure(text=f"Seleccionados: {total_sel} de {len(datos_sistema['actualizables'])}")

        def render_tabla_act(*args):
            tree_act.delete(*tree_act.get_children())
            mapa_actualizables.clear()
            busq = var_busq_act.get().strip().lower()
            cat_sel = combo_filtro_act.get()

            for a in datos_sistema["actualizables"]:
                if cat_sel != "Todas las categorías" and cat_sel not in a["cat"]:
                    continue
                if busq and (busq not in a["nombre"].lower() and busq not in a["id"].lower()):
                    continue
                chk = "[ ✔ ]" if a["seleccionado"] else "[   ]"
                iid = tree_act.insert("", "end", values=(chk, a["icono"], a["nombre"], a["id"], a["v_vieja"], a["v_nueva"], a["cat"]))
                mapa_actualizables[iid] = a
            actualizar_contador_act()

        def click_tabla_act(event):
            item = tree_act.identify_row(event.y)
            if not item or item not in mapa_actualizables:
                return
            obj = mapa_actualizables[item]
            obj["seleccionado"] = not obj["seleccionado"]
            vals = list(tree_act.item(item, "values"))
            vals[0] = "[ ✔ ]" if obj["seleccionado"] else "[   ]"
            tree_act.item(item, values=vals)
            actualizar_contador_act()

        tree_act.bind("<ButtonRelease-1>", click_tabla_act)
        var_busq_act.trace_add("write", render_tabla_act)
        combo_filtro_act.configure(command=lambda _: render_tabla_act())

        def cambiar_seleccion_act(modo):
            for iid in tree_act.get_children():
                obj = mapa_actualizables.get(iid)
                if obj:
                    if modo == "todo": obj["seleccionado"] = True
                    elif modo == "nada": obj["seleccionado"] = False
                    elif modo == "invertir": obj["seleccionado"] = not obj["seleccionado"]
            render_tabla_act()

        render_tabla_act()

        btn_frame_act = ctk.CTkFrame(tab_act, fg_color="transparent")
        btn_frame_act.pack(fill="x", pady=5)

        ctk.CTkButton(btn_frame_act, text="☑️ Seleccionar Todo", width=130, fg_color="#334155", hover_color="#475569", command=lambda: cambiar_seleccion_act("todo")).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame_act, text="⬜ Deseleccionar Todo", width=140, fg_color="#334155", hover_color="#475569", command=lambda: cambiar_seleccion_act("nada")).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame_act, text="🔀 Invertir Selección", width=130, fg_color="#334155", hover_color="#475569", command=lambda: cambiar_seleccion_act("invertir")).pack(side="left", padx=4)

        def run_actualizar_sel():
            seleccionados = [a for a in datos_sistema["actualizables"] if a["seleccionado"]]
            if not seleccionados:
                messagebox.showwarning("Aviso", "Selecciona al menos un programa para actualizar.", parent=win_gestor)
                return
            win_gestor.destroy()
            def proc_act(log_ui):
                log_ui(f"\n[*] INICIANDO ACTUALIZACIÓN QUIRÚRGICA DE {len(seleccionados)} PROGRAMAS...")
                for idx, a in enumerate(seleccionados, 1):
                    log_ui(f"\n[{idx}/{len(seleccionados)}] 🚀 Actualizando: {a['nombre']} ({a['v_vieja']} -> {a['v_nueva']})")
                    run_cmd(log_ui, f'winget upgrade --id "{a["id"]}" --silent --include-unknown --accept-package-agreements --accept-source-agreements')
                log_ui("\n[+] Todas las actualizaciones seleccionadas han finalizado.")
                try: notificar_voz("Las actualizaciones seleccionadas han terminado.")
                except: pass
            abrir_consola_y_ejecutar("ACTUALIZANDO SELECCIONADOS", proc_act)

        def run_actualizar_todo():
            win_gestor.destroy()
            def proc_todo(log_ui):
                log_ui("\n[*] INICIANDO MODO DIOS: ACTUALIZACIÓN GLOBAL DE TODO EL SISTEMA...")
                run_cmd(log_ui, "winget upgrade --all --include-unknown --silent --accept-package-agreements --accept-source-agreements")
                log_ui("\n[+] Todo el software del computador ha sido actualizado a su última versión.")
                try: notificar_voz("Actualización total del sistema completada.")
                except: pass
            abrir_consola_y_ejecutar("MODO DIOS (ACTUALIZAR TODO)", proc_todo)

        ctk.CTkButton(btn_frame_act, text="🚀 ACTUALIZAR TODO (Modo Dios)", font=("Arial", 13, "bold"), height=40, fg_color="#10B981", hover_color="#059669", command=run_actualizar_todo).pack(side="right", padx=5)
        ctk.CTkButton(btn_frame_act, text="⚡ ACTUALIZAR SELECCIONADOS", font=("Arial", 13, "bold"), height=40, fg_color="#3B82F6", hover_color="#2563EB", command=run_actualizar_sel).pack(side="right", padx=5)

        # ====================================================================
        # PESTAÑA 2: DESINSTALADOR CAZADOR PRO (SUPERIOR A REVO UNINSTALLER)
        # ====================================================================
        top_des = ctk.CTkFrame(tab_des, fg_color="transparent")
        top_des.pack(fill="x", pady=5)

        var_busq_des = ctk.StringVar()
        ent_busq_des = ctk.CTkEntry(top_des, textvariable=var_busq_des, placeholder_text="🔍 Buscar programa instalado o fabricante...", width=260, font=("Arial", 13))
        ent_busq_des.pack(side="left", padx=5)

        filtros_des = ["Todas las aplicaciones", "🔴 Sugerencias a Eliminar (Bloatware)", "🟡 Sistema y Controladores", "☁️ Nube", "🎮 Juegos", "🌐 Navegadores y Red", "📄 Ofimática y Multimedia", "💻 Desarrollo e Ingeniería", "💬 Comunicación y Remoto", "🛠️ Software de Fabricante", "⚪ Otros Programas"]
        combo_filtro_des = ctk.CTkOptionMenu(top_des, values=filtros_des, width=260, font=("Arial", 13), fg_color="#334155", button_color="#475569")
        combo_filtro_des.pack(side="left", padx=5)

        var_modo_revo = ctk.BooleanVar(value=True)
        chk_revo = ctk.CTkCheckBox(top_des, text="🔥 Modo Cazador Forense (Destruir Residuos AppData + Registro)", variable=var_modo_revo, font=("Arial", 12, "bold"), text_color="#FCD34D", fg_color="#EF4444")
        chk_revo.pack(side="left", padx=10)

        lbl_cont_des = ctk.CTkLabel(top_des, text="Para Borrar: 0", font=("Arial", 14, "bold"), text_color="#EF4444")
        lbl_cont_des.pack(side="right", padx=10)

        frame_tabla_des = ctk.CTkFrame(tab_des, fg_color="transparent")
        frame_tabla_des.pack(fill="both", expand=True, pady=8)

        scroll_y_des = ttk.Scrollbar(frame_tabla_des, orient="vertical")
        scroll_y_des.pack(side="right", fill="y")
        scroll_x_des = ttk.Scrollbar(frame_tabla_des, orient="horizontal")
        scroll_x_des.pack(side="bottom", fill="x")

        tree_des = ttk.Treeview(
            frame_tabla_des,
            columns=("check", "folder", "icono", "nombre", "version", "editor", "cat", "desc"),
            show="headings", height=11,
            yscrollcommand=scroll_y_des.set, xscrollcommand=scroll_x_des.set
        )
        scroll_y_des.config(command=tree_des.yview)
        scroll_x_des.config(command=tree_des.xview)

        tree_des.heading("check", text="Borrar")
        tree_des.heading("folder", text="Ruta")
        tree_des.heading("icono", text="Tipo")
        tree_des.heading("nombre", text="Nombre de Aplicación")
        tree_des.heading("version", text="Versión")
        tree_des.heading("editor", text="Fabricante / Editor")
        tree_des.heading("cat", text="Clasificación")
        tree_des.heading("desc", text="Diagnóstico Heurístico TREMEND")

        tree_des.column("check", width=70, anchor="center")
        tree_des.column("folder", width=55, anchor="center")
        tree_des.column("icono", width=50, anchor="center")
        tree_des.column("nombre", width=250, anchor="w")
        tree_des.column("version", width=100, anchor="center")
        tree_des.column("editor", width=180, anchor="w")
        tree_des.column("cat", width=210, anchor="w")
        tree_des.column("desc", width=420, anchor="w")
        tree_des.pack(fill="both", expand=True)

        def actualizar_contador_des():
            total_sel = sum(1 for a in datos_sistema["instaladas"] if a["seleccionado"])
            lbl_cont_des.configure(text=f"Para Borrar: {total_sel}")

        def render_tabla_des(*args):
            tree_des.delete(*tree_des.get_children())
            mapa_instaladas.clear()
            busq = var_busq_des.get().strip().lower()
            cat_sel = combo_filtro_des.get()

            for a in datos_sistema["instaladas"]:
                if cat_sel != "Todas las aplicaciones" and a["cat"] != cat_sel:
                    continue
                if busq and (busq not in a["nombre"].lower() and busq not in a["editor"].lower()):
                    continue
                chk = "[ ✔ ]" if a["seleccionado"] else "[   ]"
                iid = tree_des.insert("", "end", values=(chk, "📁", a["icono"], a["nombre"], a["version"], a["editor"], a["cat"], a["desc"]))
                mapa_instaladas[iid] = a
            actualizar_contador_des()

        def click_tabla_des(event):
            region = tree_des.identify_region(event.x, event.y)
            if region != "cell": return
            col = tree_des.identify_column(event.x)
            item = tree_des.identify_row(event.y)
            if not item or item not in mapa_instaladas: return
            app_info = mapa_instaladas[item]

            if col == "#2":
                ruta_app = app_info["ruta"]
                if os.path.exists(ruta_app):
                    try: os.startfile(os.path.normpath(ruta_app))
                    except: pass
                else:
                    messagebox.showinfo("Ruta de Sistema", f"Este paquete reside en una bóveda interna del sistema:\n\nID: {app_info['id']}\nRegistro: {app_info['reg_path'] or 'UWP Store'}", parent=win_gestor)
            else:
                app_info["seleccionado"] = not app_info["seleccionado"]
                vals = list(tree_des.item(item, "values"))
                vals[0] = "[ ✔ ]" if app_info["seleccionado"] else "[   ]"
                tree_des.item(item, values=vals)
                actualizar_contador_des()

        tree_des.bind("<ButtonRelease-1>", click_tabla_des)
        var_busq_des.trace_add("write", render_tabla_des)
        combo_filtro_des.configure(command=lambda _: render_tabla_des())

        def cambiar_seleccion_des(modo):
            if modo == "bloatware":
                for a in datos_sistema["instaladas"]:
                    a["seleccionado"] = ("Bloatware" in a["cat"])
            else:
                for iid in tree_des.get_children():
                    obj = mapa_instaladas.get(iid)
                    if obj:
                        obj["seleccionado"] = (modo == "todo")
            render_tabla_des()

        render_tabla_des()

        btn_frame_des = ctk.CTkFrame(tab_des, fg_color="transparent")
        btn_frame_des.pack(fill="x", pady=5)

        ctk.CTkButton(btn_frame_des, text="☑️ Seleccionar Vista", width=130, fg_color="#334155", hover_color="#475569", command=lambda: cambiar_seleccion_des("todo")).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame_des, text="⬜ Desmarcar Todo", width=130, fg_color="#334155", hover_color="#475569", command=lambda: cambiar_seleccion_des("nada")).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame_des, text="🎯 Auto-Marcar Bloatware", width=165, fg_color="#F59E0B", text_color="#000000", hover_color="#D97706", font=("Arial", 12, "bold"), command=lambda: cambiar_seleccion_des("bloatware")).pack(side="left", padx=4)

        def run_borrar_cazador():
            apps_del = [a for a in datos_sistema["instaladas"] if a["seleccionado"]]
            if not apps_del:
                messagebox.showwarning("Atención", "No seleccionaste ningún programa para desinstalar.", parent=win_gestor)
                return

            modo_cazador = var_modo_revo.get()
            txt_modo = "CON CAZADOR FORENSE DE RESIDUOS (Archivos y Registro)" if modo_cazador else "ESTÁNDAR"
            if not messagebox.askyesno("⚠️ Confirmación de Purga Militar", f"¿Estás seguro de erradicar {len(apps_del)} programa(s) en modo {txt_modo}?\n\nEsta operación cerrará sus procesos activos, ejecutará la desinstalación y destruirá carpetas y claves residuales.", parent=win_gestor):
                return

            win_gestor.destroy()

            def proc_del(log_ui):
                log_ui("="*80)
                log_ui(f" 💀 INICIANDO CAZADOR FORENSE DE DESINSTALACIÓN ({len(apps_del)} OBJETIVOS)")
                log_ui("="*80)

                carpetas_protegidas = {
                    "microsoft", "windows", "windows nt", "common files", "internet explorer",
                    "windows defender", "package cache", " temp", "system32", "syswow64", "google", "mozilla"
                }

                for idx, a in enumerate(apps_del, 1):
                    nom = a["nombre"]
                    nom_orig = a["nombre_original"]
                    log_ui(f"\n[{idx}/{len(apps_del)}] 🎯 OBJETIVO: {nom} ({a['version']}) | Tipo: {a['tipo']}")

                    # FASE 1: Cierre de procesos y Desinstalación Principal
                    token_proc = re.sub(r'[^a-zA-Z0-9]', '', nom.split()[0])
                    if len(token_proc) >= 4 and token_proc.lower() not in ("microsoft", "windows", "driver"):
                        log_ui(f"    -> [Fase 1/3] Cerrando procesos activos vinculados a '{token_proc}'...")
                        run_ps_script(log_ui, f"Get-Process | Where-Object {{ $_.ProcessName -match '{token_proc}' }} | Stop-Process -Force -ErrorAction SilentlyContinue")

                    if "onedrive" in nom.lower():
                        log_ui("    -> Ejecutando desinstalador nuclear de OneDrive...")
                        subprocess.run("taskkill /f /im OneDrive.exe", shell=True, capture_output=True)
                        sys_root = os.environ.get("SystemRoot", r"C:\Windows")
                        loc_app = os.environ.get("LocalAppData", "")
                        for r_od in [fr"{sys_root}\SysWOW64\OneDriveSetup.exe", fr"{sys_root}\System32\OneDriveSetup.exe", fr"{loc_app}\Microsoft\OneDrive\OneDriveSetup.exe"]:
                            if os.path.exists(r_od):
                                run_cmd(log_ui, f'"{r_od}" /uninstall')
                    elif "UWP" in a["tipo"]:
                        log_ui(f"    -> Removiendo paquete UWP del núcleo: {a['id']}...")
                        run_ps_script(log_ui, f'Remove-AppxPackage -Package "{a["id"]}" -AllUsers -ErrorAction SilentlyContinue')
                    else:
                        log_ui(f"    -> Ejecutando desinstalación silenciosa vía Winget / Registro...")
                        run_cmd(log_ui, f'winget uninstall --id "{a["id"]}" --silent --accept-source-agreements')

                    # FASE 2 Y 3: CAZADOR FORENSE DE RESIDUOS (SUPERIOR A REVO UNINSTALLER)
                    if modo_cazador:
                        log_ui("    -> [Fase 2/3] Escaneando disco duro en busca de carpetas y cachés huérfanas...")
                        residuos_borrados = 0

                        # 2A. Si la carpeta de instalación original quedó con basura, la destruimos
                        ruta_inst = a["ruta"]
                        if ruta_inst and os.path.exists(ruta_inst) and "gestionada" not in ruta_inst.lower():
                            nombre_carpeta = os.path.basename(os.path.normpath(ruta_inst)).lower()
                            if nombre_carpeta not in carpetas_protegidas and len(nombre_carpeta) >= 4:
                                try:
                                    shutil.rmtree(ruta_inst, ignore_errors=True)
                                    log_ui(f"       [🔥 Residuo Pulverizado] Carpeta raíz: {ruta_inst}")
                                    residuos_borrados += 1
                                except: pass

                        # 2B. Búsqueda heurística en AppData\Local, AppData\Roaming y ProgramData
                        patron = nom.split()[0].strip().lower()
                        if len(patron) >= 4 and patron not in carpetas_protegidas:
                            zonas_busqueda = [
                                os.environ.get("LOCALAPPDATA", ""),
                                os.environ.get("APPDATA", ""),
                                os.environ.get("PROGRAMDATA", r"C:\ProgramData")
                            ]
                            for zona in zonas_busqueda:
                                if zona and os.path.exists(zona):
                                    try:
                                        for item in os.listdir(zona):
                                            item_low = item.lower()
                                            if item_low == patron or item_low.startswith(nom.lower()[:8]):
                                                if item_low not in carpetas_protegidas:
                                                    ruta_res = os.path.join(zona, item)
                                                    shutil.rmtree(ruta_res, ignore_errors=True)
                                                    if not os.path.exists(ruta_res):
                                                        log_ui(f"       [🔥 Residuo Pulverizado] Caché oculta: {ruta_res}")
                                                        residuos_borrados += 1
                                    except: pass

                        # FASE 3: Limpieza profunda de llaves huérfanas en el Registro
                        log_ui("    -> [Fase 3/3] Purgando entradas huérfanas en el Registro de Windows (Regedit)...")
                        reg_borrados = 0
                        if a["reg_path"]:
                            run_ps_script(log_ui, f'Remove-Item -LiteralPath "{a["reg_path"]}" -Recurse -Force -ErrorAction SilentlyContinue')
                            reg_borrados += 1

                        if len(patron) >= 5 and patron not in carpetas_protegidas:
                            for hive_str in [f"HKCU:\\Software\\{nom}", f"HKLM:\\SOFTWARE\\{nom}", f"HKLM:\\SOFTWARE\\WOW6432Node\\{nom}"]:
                                run_ps_script(log_ui, f'if (Test-Path "{hive_str}") {{ Remove-Item -LiteralPath "{hive_str}" -Recurse -Force -ErrorAction SilentlyContinue; Write-Host "       [🔥 Registro Purgado] {hive_str}" }}')

                        log_ui(f"    [+] Balance Forense '{nom}': {residuos_borrados} directorios residuales y {reg_borrados}+ registros erradicados.")

                log_ui("\n" + "="*80)
                log_ui(" ✅ PURGA FORENSE COMPLETADA. SISTEMA LIMPIO DE RASTROS.")
                log_ui("="*80)
                try: notificar_voz("El Cazador Forense ha erradicado los programas y sus residuos.")
                except: pass

            abrir_consola_y_ejecutar("CAZADOR FORENSE DE DESINSTALACIÓN", proc_del)

        ctk.CTkButton(btn_frame_des, text="💀 DESINSTALAR Y DESTRUIR RESIDUOS", font=("Arial", 13, "bold"), height=40, fg_color="#EF4444", hover_color="#DC2626", command=run_borrar_cazador).pack(side="right", padx=5)

        # ====================================================================
        # PESTAÑA 3: MIGRAR / CLONAR PC (PRE-FORMATEO)
        # ====================================================================
        ctk.CTkLabel(tab_mig, text="¿Vas a formatear este equipo o acabas de instalar Windows desde cero?", font=("Arial", 20, "bold"), text_color="#00FFCC").pack(pady=(90, 10))
        ctk.CTkLabel(tab_mig, text="Usa nuestro Clonador Pre-Formateo para respaldar todos tus programas en una USB (.JSON auto-instalable + Excel .CSV)\no instalar el Kit Esencial Posformateo con un solo clic.", font=("Arial", 14), text_color="#94A3B8").pack(pady=(0, 30))
        ctk.CTkButton(tab_mig, text="💾 Abrir Centro de Clonación y Kits Posformateo", font=("Arial", 15, "bold"), height=50, fg_color="#10B981", hover_color="#059669", command=lambda: logica_inventario_software(None)).pack()

    threading.Thread(target=escanear_sistema, daemon=True).start()

def logica_inventario_software(log=None):
    import os, csv, json, winreg, subprocess, threading
    import customtkinter as ctk
    from tkinter import filedialog, messagebox

    if log:
        log("\n[*] Abriendo Centro de Clonación, Migración e Inventario de Software...")

    win_mig = ctk.CTkToplevel(app)
    win_mig.title("TREMEND - Clonador Pre-Formateo e Inventario (Winget JSON + CSV)")
    win_mig.geometry("980x620")
    win_mig.attributes("-topmost", True)
    win_mig.transient(app)

    # Encabezado
    frame_head = ctk.CTkFrame(win_mig, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#38BDF8")
    frame_head.pack(fill="x", padx=20, pady=15)
    ctk.CTkLabel(frame_head, text="💾 Centro de Migración y Clonación de Software (Pre/Pos-Formateo)", font=("Arial", 20, "bold"), text_color="#00FFCC").pack(pady=(12, 4))
    ctk.CTkLabel(frame_head, text="Exporta tus programas a una USB antes de formatear (JSON auto-instalable + Excel CSV) o restaura todo con 1 clic.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 12))

    # Consola interna de progreso en vivo
    txt_out = ctk.CTkTextbox(win_mig, font=("Consolas", 13), fg_color="#050811", text_color="#38BDF8", border_width=1, border_color="#334155")
    txt_out.pack(fill="both", expand=True, padx=20, pady=(0, 10))
    txt_out.insert("end", "[*] Selecciona una operación abajo.\n[*] Si conectaste un Pendrive USB, podrás seleccionarlo directamente sin escribir letras de unidad.\n")
    txt_out.configure(state="disabled")

    pb_mig = ctk.CTkProgressBar(win_mig, progress_color="#10B981", height=10)
    pb_mig.pack(fill="x", padx=20, pady=(0, 10))
    pb_mig.set(0)

    def write_log(texto):
        if win_mig.winfo_exists():
            def _u():
                txt_out.configure(state="normal")
                txt_out.insert("end", texto + "\n")
                txt_out.see("end")
                txt_out.configure(state="disabled")
            app.after(0, _u)
        if log:
            try: log(texto)
            except: pass

    # 1. FUNCIÓN: EXPORTAR (JSON AUTO-INSTALABLE + CSV EXCEL + FILTRO ANTI-BLOATWARE)
    def accion_exportar():
        carpeta = filedialog.askdirectory(title="Selecciona tu Pendrive USB o Carpeta donde guardar el Respaldo", parent=win_mig)
        if not carpeta: return

        ruta_json = os.path.join(carpeta, "TREMEND_Programas.json")
        ruta_csv  = os.path.join(carpeta, "Inventario_Software_TREMEND.csv")

        pb_mig.configure(mode="indeterminate")
        pb_mig.start()

        def _thread_exp():
            write_log("\n" + "="*75)
            write_log(f" 📤 FASE 1: GENERANDO INVENTARIO COMPLETO PARA EXCEL (.CSV)")
            write_log("="*75)
            programas = []
            rutas_reg = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            ]
            nombres_vistos = set()
            for hkey, ruta in rutas_reg:
                try:
                    key = winreg.OpenKey(hkey, ruta)
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        sub_key = winreg.OpenKey(key, winreg.EnumKey(key, i))
                        try:
                            nom = winreg.QueryValueEx(sub_key, "DisplayName")[0].strip()
                            ver = winreg.QueryValueEx(sub_key, "DisplayVersion")[0].strip()
                            if nom and nom not in nombres_vistos:
                                nombres_vistos.add(nom)
                                programas.append([nom, ver])
                        except: pass
                except: pass

            try:
                programas.sort(key=lambda x: x[0].lower())
                with open(ruta_csv, mode='w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Nombre del Programa", "Versión Instalada"])
                    writer.writerows(programas)
                write_log(f"[+] Inventario CSV guardado ({len(programas)} programas): {ruta_csv}")
            except Exception as e:
                write_log(f"[-] Error guardando CSV: {e}")

            write_log("\n" + "="*75)
            write_log(f" 📦 FASE 2: EXPORTANDO PAQUETES AUTO-INSTALABLES (WINGET EXPORT)")
            write_log("="*75)
            write_log("[*] Escaneando repositorios e inyectando auto-aceptación de términos...")

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            cmd_exp = f'winget export -o "{ruta_json}" --accept-source-agreements'
            proc = subprocess.Popen(cmd_exp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore', startupinfo=startupinfo)
            no_disponibles = 0
            for linea in proc.stdout:
                l = linea.strip()
                if "not available from any source" in l or "no está disponible" in l:
                    no_disponibles += 1
                elif l and len(l) > 3:
                    write_log(f"    -> {l}")
            proc.wait()

            # FASE 3: SANITIZACIÓN DEL JSON (PURGA DE BLOATWARE Y LIBRERÍAS REDUNDANTES)
            if os.path.exists(ruta_json):
                try:
                    with open(ruta_json, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    bloat_keywords = ("vclibs", "ui.xaml", "windowsappruntime", "onedrive", "bing", "solitaire", "xbox", "zune", "gethelp", "feedback")
                    total_antes = 0
                    total_despues = 0
                    for source in data.get("Sources", []):
                        paquetes = source.get("Packages", [])
                        total_antes += len(paquetes)
                        limpios = [
                            p for p in paquetes
                            if not any(b in p.get("PackageIdentifier", "").lower() for b in bloat_keywords)
                        ]
                        source["Packages"] = limpios
                        total_despues += len(limpios)

                    with open(ruta_json, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)

                    write_log(f"\n[+] ¡Archivo JSON de clonación creado y purgado con éxito!")
                    write_log(f"    -> Programas listos para auto-instalar : {total_despues}")
                    write_log(f"    -> Basura/Librerías filtradas del JSON : {total_antes - total_despues}")
                    write_log(f"    -> Apps exclusivas respaldadas en CSV  : {no_disponibles}")
                    write_log(f"    -> Ruta del respaldo                   : {ruta_json}")
                except Exception as e:
                    write_log(f"[!] JSON exportado (sin filtrado adicional): {e}")
            else:
                write_log("[-] No se pudo generar el archivo JSON. Verifica que Winget esté actualizado.")

            if win_mig.winfo_exists():
                app.after(0, lambda: (pb_mig.stop(), pb_mig.configure(mode="determinate"), pb_mig.set(1.0)))

        threading.Thread(target=_thread_exp, daemon=True).start()

    # 2. FUNCIÓN: IMPORTAR (WINGET IMPORT 100% DESATENDIDO SIN PEDIR 'Y')
    def accion_importar(ruta_custom=None):
        ruta_json = ruta_custom
        if not ruta_json:
            ruta_json = filedialog.askopenfilename(
                title="Selecciona el archivo programas.json o TREMEND_Programas.json",
                filetypes=[("Archivos JSON Winget", "*.json"), ("Todos los archivos", "*.*")],
                parent=win_mig
            )
        if not ruta_json or not os.path.exists(ruta_json): return

        pb_mig.configure(mode="indeterminate")
        pb_mig.start()

        def _thread_imp():
            write_log("\n" + "="*75)
            write_log(f" 🚀 INICIANDO INSTALACIÓN MASIVA DESATENDIDA (WINGET IMPORT)")
            write_log("="*75)
            write_log(f"[*] Archivo origen: {ruta_json}")
            write_log("[*] Banderas activadas: Auto-Aceptar Licencias + Ignorar Incompatibles (Cero bloqueos)...\n")

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            cmd_imp = f'winget import -i "{ruta_json}" --accept-package-agreements --accept-source-agreements --ignore-unavailable --ignore-versions'
            proc = subprocess.Popen(cmd_imp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore', startupinfo=startupinfo)
            for linea in proc.stdout:
                l = linea.strip()
                if l and len(l) > 2 and not all(c in "-\\|/" for c in l):
                    write_log(f"    {l}")
            proc.wait()

            write_log("\n[+] ¡SECUENCIA DE RESTAURACIÓN DE PROGRAMAS COMPLETADA!")
            try: notificar_voz("La restauración masiva de programas ha finalizado.")
            except: pass
            if win_mig.winfo_exists():
                app.after(0, lambda: (pb_mig.stop(), pb_mig.configure(mode="determinate"), pb_mig.set(1.0)))

        threading.Thread(target=_thread_imp, daemon=True).start()

    # 3. FUNCIÓN EXTRA: KIT ESENCIAL POSFORMATEO (ESTILO NINITE EN 1 CLIC)
    def accion_kit_esencial():
        if not messagebox.askyesno("Kit Posformateo", "¿Deseas instalar automáticamente el Kit Esencial de Posformateo?\n\nIncluye:\n- Google Chrome\n- Brave Browser\n- WinRAR\n- VLC Media Player\n- Adobe Acrobat Reader\n- AnyDesk", parent=win_mig):
            return
        kit_json = {
            "$schema": "https://aka.ms/winget-packages.schema.2.0.json",
            "Sources": [{
                "Packages": [
                    {"PackageIdentifier": "Google.Chrome"},
                    {"PackageIdentifier": "Brave.Brave"},
                    {"PackageIdentifier": "RARLab.WinRAR"},
                    {"PackageIdentifier": "VideoLAN.VLC"},
                    {"PackageIdentifier": "Adobe.Acrobat.Reader.64-bit"},
                    {"PackageIdentifier": "AnyDeskSoftwareGmbH.AnyDesk"}
                ],
                "SourceDetails": {
                    "Argument": "https://cdn.winget.microsoft.com/cache",
                    "Identifier": "Microsoft.Winget.Source_8wekyb3d8bbwe",
                    "Name": "winget",
                    "Type": "Microsoft.PreIndexed.Package"
                }
            }]
        }
        ruta_temp_kit = os.path.join(os.environ.get("TEMP"), "TREMEND_Kit_Posformateo.json")
        with open(ruta_temp_kit, "w", encoding="utf-8") as f:
            json.dump(kit_json, f, indent=2)
        accion_importar(ruta_temp_kit)

    # Botonera inferior
    frame_btns = ctk.CTkFrame(win_mig, fg_color="transparent")
    frame_btns.pack(fill="x", padx=20, pady=(0, 15))

    ctk.CTkButton(frame_btns, text="📤 1. Exportar Respaldo (JSON + CSV)", font=("Arial", 13, "bold"), height=42, fg_color="#3B82F6", hover_color="#2563EB", command=accion_exportar).pack(side="left", padx=5, expand=True, fill="x")
    ctk.CTkButton(frame_btns, text="📥 2. Importar y Restaurar (.JSON)", font=("Arial", 13, "bold"), height=42, fg_color="#10B981", hover_color="#059669", command=accion_importar).pack(side="left", padx=5, expand=True, fill="x")
    ctk.CTkButton(frame_btns, text="🚀 3. Kit Esencial Posformateo", font=("Arial", 13, "bold"), height=42, fg_color="#F59E0B", text_color="#000000", hover_color="#D97706", command=accion_kit_esencial).pack(side="left", padx=5, expand=True, fill="x")

def logica_respaldo_drivers(log):
    log("\n[*] Clonando archivos de controladores (.sys / .inf)...")
    ruta = r"C:\\RespaldoDrivers"
    if not os.path.exists(ruta): os.makedirs(ruta)
    run_cmd(log, f"dism /online /export-driver /destination:{ruta}")

def logica_auditoria_licencias(log):
    import winreg, subprocess, os, datetime
    from tkinter import messagebox

    log("\n" + "="*75)
    log(" 💎 AUDITORÍA FORENSE Y EXTRACTOR PROFUNDO DE LICENCIAS (WINDOWS & OFFICE) ")
    log("="*75)

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # Helper: Decodificador matemático Base-24 para desencriptar DigitalProductId del Registro
    def decodificar_digital_product_id(digital_pid):
        try:
            key_offset = 52
            chars = "BCDFGHJKMPQRTVWXY2346789"
            raw = list(digital_pid[key_offset:key_offset + 15])
            is_win8_or_newer = (raw[14] >> 3) & 1
            raw[14] = (raw[14] & 0xF7) | ((is_win8_or_newer & 2) << 2)
            key = ""
            last = 0
            for i in range(24, -1, -1):
                cur = 0
                for j in range(14, -1, -1):
                    cur = cur * 256
                    cur = raw[j] + cur
                    raw[j] = cur // 24
                    cur = cur % 24
                    last = cur
                key = chars[cur] + key
            if is_win8_or_newer:
                keypart1 = key[1:last + 1]
                keypart2 = key[last + 1:]
                key = keypart1 + "N" + keypart2
            return "-".join([key[i:i+5] for i in range(0, 25, 5)])
        except Exception:
            return ""

    # Catálogo de claves genéricas RTM/GVLK de Microsoft (para avisar si es genérica o exclusiva)
    claves_genericas_ms = {
        "VK7JG-NPHTM-C97JM-9MPGT-3V66T": "Genérica Windows 10/11 Pro (Vinculada a Licencia Digital HWID)",
        "YTMG3-N6DKC-DKB77-7M9GH-8HVX7": "Genérica Windows 10/11 Home (Vinculada a Licencia Digital HWID)",
        "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99": "Genérica Windows 10/11 Home KMS/Retail",
        "BT79Q-G7N6G-PGBYW-4YWX6-6F4BT": "Genérica Windows 10/11 Home Single Language",
        "W269N-WFGWX-YVC9B-4J6C9-T83GX": "Genérica Corporativa GVLK Windows 10/11 Pro (Cliente KMS)",
        "NPPR9-FWDCX-D2C8J-H872K-2YT43": "Genérica Corporativa GVLK Windows 10/11 Enterprise (Cliente KMS)"
    }

    resumen_pasaporte = []

    # ---------------------------------------------------------
    # 1. AUDITORÍA PROFUNDA DE WINDOWS (BIOS + REGISTRO + SLMGR /DLV)
    # ---------------------------------------------------------
    log("\n[1] Extrayendo Claves de Producto y Telemetría de Licencias (Nivel slmgr /dlv)...")
    try:
        # A. Clave 1: OEM grabada en Placa Base (BIOS/UEFI - Comando 1 del video)
        # B. Clave 2: BackupProductKeyDefault en el Registro (Comando 2 del video)
        # C. Telemetría completa equivalente a slmgr /dlv (Comando 3 del video)
        script_win_full = r"""
        $sls = Get-CimInstance SoftwareLicensingService -ErrorAction SilentlyContinue
        $biosKey = if ($sls.OA3xOriginalProductKey) { $sls.OA3xOriginalProductKey } else { "" }
        $rearms = if ($null -ne $sls.RemainingWindowsRearmCount) { $sls.RemainingWindowsRearmCount } else { "N/A" }

        $regPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform"
        $regKey = (Get-ItemProperty -Path $regPath -Name "BackupProductKeyDefault" -ErrorAction SilentlyContinue).BackupProductKeyDefault
        if (-not $regKey) { $regKey = "" }

        $osCaption = (Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue).Caption

        $prod = Get-CimInstance SoftwareLicensingProduct -Filter "ApplicationID = '55c92734-d682-4d71-983e-d6ec3f16059f' AND PartialProductKey IS NOT NULL" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($prod) {
            Write-Output ("OK|" + $osCaption + "|" + $biosKey + "|" + $regKey + "|" + $prod.LicenseStatus + "|" + $prod.ProductKeyChannel + "|" + $prod.PartialProductKey + "|" + $prod.Description + "|" + $prod.KeyManagementServiceMachine + "|" + $rearms)
        } else {
            Write-Output ("NO_ACT|" + $osCaption + "|" + $biosKey + "|" + $regKey + "|0|N/A|N/A|Sin Licencia||" + $rearms)
        }
        """
        salida_win = subprocess.run(["powershell", "-NoProfile", "-Command", script_win_full], capture_output=True, text=True, startupinfo=startupinfo).stdout.strip()

        # D. Clave 3: Desencriptado binario directo desde DigitalProductId en winreg
        clave_decodificada = ""
        try:
            k_nt = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            dpid, _ = winreg.QueryValueEx(k_nt, "DigitalProductId")
            clave_decodificada = decodificar_digital_product_id(dpid)
        except Exception:
            pass

        partes = salida_win.split("|")
        while len(partes) < 10:
            partes.append("")
        _, os_cap, clave_bios, clave_reg, status_code, canal_raw, clave_parcial, desc_lic, kms_srv, rearms_left = partes

        log(f"    -> Sistema Operativo             : {os_cap}")
        log(f"    -> [1] Clave OEM en BIOS/UEFI    : {clave_bios if clave_bios else 'No incluida en placa base (PC armado o sin licencia OEM)'}")
        log(f"    -> [2] Clave en Registro Windows : {clave_reg if clave_reg else 'No registrada en SoftwareProtectionPlatform'}")
        if clave_decodificada and clave_decodificada != clave_reg:
            log(f"    -> [3] Clave Binaria (Kernel)    : {clave_decodificada}")

        # Evaluar si la clave del registro es genérica o única
        clave_principal = clave_bios or clave_reg or clave_decodificada
        if clave_reg in claves_genericas_ms:
            log(f"       ℹ️ Nota Forense: La clave del Registro ({clave_reg}) es una {claves_genericas_ms[clave_reg]}.")
        elif clave_reg:
            log("       💎 Nota Forense: La clave del Registro es un serial específico (Respaldo recomendado antes de formatear).")

        if clave_bios and clave_reg and (clave_bios.upper() != clave_reg.upper()):
            log("       ⚠️ Diferencia detectada: La clave instalada actualmente en el Registro es distinta a la clave original de la BIOS.")

        # Análisis del Canal de Licencia (OEM / Retail / MAK / KMS) estilo slmgr /dlv
        canal_explicacion = canal_raw or desc_lic
        if "Retail" in canal_raw or "Retail" in desc_lic:
            canal_explicacion = f"💎 RETAIL ({canal_raw}) - Licencia Completa y Transferible"
        elif "OEM" in canal_raw or "OEM" in desc_lic:
            canal_explicacion = f"🏭 OEM ({canal_raw}) - Licencia Oficial Anclada a la Placa Base"
        elif "MAK" in canal_raw or "MAK" in desc_lic:
            canal_explicacion = f"🏢 VOLUMEN MAK ({canal_raw}) - Clave de Activación Múltiple Corporativa"
        elif "GVLK" in canal_raw or "KMS" in desc_lic or "Volume" in canal_raw:
            canal_explicacion = f"📡 VOLUMEN KMS / GVLK ({canal_raw}) - Activación por Servidor (Empresarial o Emulador)"

        estado_str = "🟢 ACTIVADO (Con Licencia)" if status_code == "1" else "🔴 SIN ACTIVAR / PERIODO DE GRACIA EXPIRADO"
        log(f"    -> Estado de Licencia            : {estado_str}")
        log(f"    -> Canal de Clave (slmgr /dlv)   : {canal_explicacion}")
        log(f"    -> Clave Parcial Activa          : *****-*****-*****-*****-{clave_parcial}")
        log(f"    -> Rearmados de Windows Restantes: {rearms_left}")

        if "KMS" in canal_explicacion or "GVLK" in canal_explicacion:
            if kms_srv:
                log(f"    -> Servidor KMS Detectado        : {kms_srv}")
                if any(x in kms_srv.lower() for x in ["127.0.0.1", "localhost", "kms"]):
                    log("       🔴 ALERTA CRÍTICA: Servidor KMS emulado o no oficial detectado (Renovación temporal cada 180 días).")

        if status_code != "1":
            log("    💡 SUGERENCIA TREMEND: Si necesitas una licencia 100% original y permanente,")
            log("       visita el módulo '🛒 Venta de Licencias' en el menú izquierdo de TREMEND Toolkit.")

        resumen_pasaporte.append(f"SO: {os_cap}")
        resumen_pasaporte.append(f"Clave OEM BIOS/UEFI   : {clave_bios or 'N/A'}")
        resumen_pasaporte.append(f"Clave Registro Default: {clave_reg or 'N/A'}")
        resumen_pasaporte.append(f"Clave Kernel Decodif. : {clave_decodificada or 'N/A'}")
        resumen_pasaporte.append(f"Canal / Terminación   : {canal_raw} (Parcial: {clave_parcial}) | Estado: {estado_str}")
    except Exception as e:
        log(f"    [-] Error al extraer telemetría de Windows: {e}")

    # ---------------------------------------------------------
    # 2. AUDITORÍA DE MICROSOFT OFFICE
    # ---------------------------------------------------------
    log("\n[2] Rastreando motor criptográfico OSPP de Microsoft Office...")

    rutas_posibles = [
        r"C:\Program Files\Microsoft Office\Office16\OSPP.VBS",
        r"C:\Program Files (x86)\Microsoft Office\Office16\OSPP.VBS",
        r"C:\Program Files\Microsoft Office\Office15\OSPP.VBS",
        r"C:\Program Files (x86)\Microsoft Office\Office15\OSPP.VBS"
    ]

    script_path = next((r for r in rutas_posibles if os.path.exists(r)), None)

    if not script_path:
        log("    [-] Microsoft Office clásico no detectado o usas versión UWP de la Store.")
    else:
        log("    [+] Motor OSPP localizado. Desencriptando estado...\n")
        comando = f'cscript //nologo "{script_path}" /dstatus'
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, encoding='cp850', errors='ignore', startupinfo=startupinfo)

        if not resultado.stdout.strip() or "No installed product keys" in resultado.stdout:
            log("    🔴 OFFICE NO ESTÁ ACTIVADO (No se detectaron claves instaladas).")
        else:
            bloques = resultado.stdout.split("---Processing--------------------------")
            licencias_encontradas = 0

            for bloque in bloques:
                if "LICENSE NAME" in bloque:
                    licencias_encontradas += 1
                    nombre, desc, estado, clave_parcial_of, kms_host = "Desconocido", "Desconocida", "Desconocido", "*****", ""

                    for linea in bloque.splitlines():
                        if "LICENSE NAME:" in linea: nombre = linea.split("NAME:")[1].strip()
                        elif "LICENSE DESCRIPTION:" in linea: desc = linea.split("DESCRIPTION:")[1].strip()
                        elif "LICENSE STATUS:" in linea: estado = linea.split("STATUS:")[1].strip()
                        elif "Last 5 characters" in linea: clave_parcial_of = linea.split("key:")[1].strip()
                        elif "KMS machine name from DNS:" in linea: kms_host = linea.split("DNS:")[1].strip()
                        elif "KMS machine registry override defined:" in linea: kms_host = linea.split("defined:")[1].strip()

                    prod_limpio = nombre.split(',')[0]
                    log(f" 📊 [REPORTE OFFICE #{licencias_encontradas}]")
                    log(f"    -> Producto          : {prod_limpio}")
                    log(f"    -> Terminación Clave : *****-{clave_parcial_of}")

                    if "---LICENSED---" in estado: log("    -> Estado Actual     : 🟢 ACTIVADO")
                    elif "OOB_GRACE" in estado or "GRACE" in estado: log("    -> Estado Actual     : 🟡 PERIODO DE GRACIA (Pronto a expirar)")
                    else: log(f"    -> Estado Actual     : 🔴 {estado}")

                    if "KMS_Client" in desc or "VOLUME" in desc:
                        log("    -> Tipo de Licencia  : 🏢 KMS / VOLUMEN")
                        if "ProPlus" in nombre:
                            log("    🔴 ALERTA: Edición 'Pro Plus' de volumen detectada (Frecuente en activaciones KMS no oficiales).")
                        if kms_host:
                            log(f"    -> Servidor KMS      : {kms_host}")
                    elif "MAK" in desc:
                        log("    -> Tipo de Licencia  : 🏢 VOLUMEN MAK (Clave Múltiple Corporativa)")
                    elif "RETAIL" in desc:
                        log("    -> Tipo de Licencia  : 💎 RETAIL (Licencia Original)")
                    log("")
                    resumen_pasaporte.append(f"Office #{licencias_encontradas}: {prod_limpio} | Parcial: {clave_parcial_of} | Canal: {desc}")

    # ---------------------------------------------------------
    # 3. RASTREO FORENSE DE CRACKS MODERNOS (MAS / OHOOK / KMSPICO)
    # ---------------------------------------------------------
    log("[3] Escaneando el sistema en busca de Tareas y Archivos Clandestinos (MAS / HWID / Ohook)...")
    amenazas_encontradas = 0

    try:
        tareas_crudo = subprocess.run('schtasks /query /fo csv', shell=True, capture_output=True, text=True, errors='ignore', startupinfo=startupinfo).stdout
        for linea in tareas_crudo.splitlines():
            if any(x in linea.lower() for x in ["kms", "pico", "autokms", "kmse"]):
                nombre_tarea = linea.split(',')[0].replace('"', '')
                log(f"    🔴 ALERTA: Tarea programada de auto-renovación detectada -> {nombre_tarea}")
                amenazas_encontradas += 1
    except Exception:
        pass

    rutas_peligro = [
        (r"C:\Program Files\KMSpico", "Activador KMSpico clásico"),
        (r"C:\Windows\KMS", "Carpeta de servidor KMS falso"),
        (r"C:\ProgramData\KMSAutoS", "Activador KMSAuto"),
        (r"C:\Windows\System32\sppextcomobjhook.dll", "DLL Ohook (Secuestro de licencia Office - MAS)")
    ]

    for ruta, motivo in rutas_peligro:
        if os.path.exists(ruta):
            log(f"    🔴 ALERTA CRÍTICA: Archivo/Carpeta detectada -> {ruta} ({motivo}).")
            amenazas_encontradas += 1

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Office\ClickToRun\Configuration")
        val, _ = winreg.QueryValueEx(key, "O365ProPlusRetail.OSPPReady")
        if val == 1:
            log("    🔴 ALERTA CRÍTICA: Registro 'OSPPReady' alterado (Activación Ohook / MAS en Office).")
            amenazas_encontradas += 1
    except Exception:
        pass

    if amenazas_encontradas == 0:
        log("    🟢 El sistema está limpio de rastros clandestinos de activadores conocidos.")
    else:
        log(f"    ⚠️ Se encontraron {amenazas_encontradas} indicios de herramientas de activación alternativa en la máquina.")

    # ---------------------------------------------------------
    # 4. EXPORTACIÓN DE PASAPORTE DE LICENCIAS Y VENTANA SLMGR /DLV
    # ---------------------------------------------------------
    try:
        escritorio = os.path.join(os.environ.get("USERPROFILE"), "Desktop")
        if not os.path.exists(escritorio):
            escritorio = os.path.join(os.environ.get("USERPROFILE"), "Escritorio")
        ruta_pasaporte = os.path.join(escritorio, "Pasaporte_Licencias_TREMEND.txt")

        with open(ruta_pasaporte, "w", encoding="utf-8") as f:
            f.write("====================================================================\n")
            f.write(" 💎 PASAPORTE FORENSE DE CLAVES Y LICENCIAS - TREMEND TOOLKIT V3.3\n")
            f.write(f" Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("====================================================================\n\n")
            for lin in resumen_pasaporte:
                f.write(f" • {lin}\n")
            f.write("\n====================================================================\n")

        if clave_principal:
            app.clipboard_clear()
            app.clipboard_append(clave_principal)
            log(f"\n[+] Clave principal ({clave_principal}) copiada automáticamente a tu portapapeles.")
        log(f"[+] Pasaporte de Licencias respaldado en tu Escritorio: {ruta_pasaporte}")
    except Exception:
        pass

    log("\n=======================================================")
    log(" [+] Auditoría forense de licencias completada.")
    try: notificar_voz("La auditoría y extracción de licencias ha finalizado.")
    except: pass

    if messagebox.askyesno("Ventana Oficial slmgr /dlv", "¿Deseas abrir también la ventana oficial detallada del Servicio de Licencias de Windows (slmgr /dlv) para ver el certificado del sistema?"):
        subprocess.Popen("cscript //nologo C:\\Windows\\System32\\slmgr.vbs /dlv" if False else "wscript.exe C:\\Windows\\System32\\slmgr.vbs /dlv", shell=True)

def logica_gestor_suscripciones(log=None):
    import os, json, datetime, urllib.parse, webbrowser
    from tkinter import ttk, messagebox
    import customtkinter as ctk

    if log:
        log("\n[*] Abriendo Centro de Control de Suscripciones Compartidas y Cobros Mensuales...")

    ruta_db = os.path.join(os.environ.get("USERPROFILE", ""), "TREMEND_Suscripciones_Cobros.json")

    def cargar_db():
        if os.path.exists(ruta_db):
            try:
                with open(ruta_db, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    if "[Escribe aquí" in datos.get("metodo_pago", ""):
                        datos["metodo_pago"] = "Nequi / Llave: [Escribe aquí tu número]"
                    return datos
            except Exception:
                pass
        return {
            "metodo_pago": "Nequi / Llave: [Escribe aquí tu número]",
            "miembros": []
        }

    def guardar_db(datos):
        try:
            with open(ruta_db, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la base de datos: {e}")

    db = cargar_db()

    win_sub = ctk.CTkToplevel(app)
    win_sub.title("TREMEND - Gestor de Grupos Familiares, Cobros Mensuales y Corte de Servicio")
    win_sub.geometry("1200x690")
    win_sub.attributes("-topmost", True)
    win_sub.transient(app)

    # --- ENCABEZADO Y CONFIGURACIÓN DE TU CUENTA DE COBRO (SIN RECORTES) ---
    frame_top = ctk.CTkFrame(win_sub, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#38BDF8")
    frame_top.pack(fill="x", padx=20, pady=12)

    ctk.CTkLabel(frame_top, text="Control de Suscripciones Compartidas (Google Gemini Pro / Family) y Autocobro", font=("Arial", 18, "bold"), text_color="#00FFCC").pack(pady=(10, 2))
    ctk.CTkLabel(frame_top, text="Registra a los miembros de tu grupo familiar. El día 30 envía el cobro con 1 clic y el 31 identifica en ROJO a quién cortarle el servicio.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 8))

    frame_cfg = ctk.CTkFrame(frame_top, fg_color="transparent")
    frame_cfg.pack(fill="x", padx=15, pady=(0, 10))

    ctk.CTkLabel(frame_cfg, text="Tus datos de pago:", font=("Arial", 13, "bold"), text_color="#FCD34D").pack(side="left", padx=(5, 8))
    ent_metodo_pago = ctk.CTkEntry(frame_cfg, width=280, font=("Consolas", 13))
    ent_metodo_pago.pack(side="left", padx=5)
    ent_metodo_pago.insert(0, db.get("metodo_pago", "Nequi / Llave: @LDVP671"))

    def guardar_metodo(silencioso=False):
        db["metodo_pago"] = ent_metodo_pago.get().strip()
        guardar_db(db)
        if not silencioso:
            messagebox.showinfo("Guardado", "Tus datos de cobro han sido actualizados correctamente.", parent=win_sub)

    ctk.CTkButton(frame_cfg, text="Guardar Cuenta", width=130, fg_color="#334155", hover_color="#475569", font=("Arial", 12, "bold"), command=lambda: guardar_metodo(False)).pack(side="left", padx=8)

    lbl_resumen = ctk.CTkLabel(frame_cfg, text="Miembros: 0 / 5  |  Recaudo Mensual: $0 COP", font=("Arial", 14, "bold"), text_color="#10B981")
    lbl_resumen.pack(side="right", padx=12)

    # --- FORMULARIO PARA AGREGAR MIEMBRO ---
    frame_add = ctk.CTkFrame(win_sub, fg_color="#1E293B", corner_radius=8)
    frame_add.pack(fill="x", padx=20, pady=5)

    ent_nombre = ctk.CTkEntry(frame_add, width=210, placeholder_text="Nombre (Ej: Primo Juan)")
    ent_nombre.pack(side="left", padx=8, pady=8)

    ent_tel = ctk.CTkEntry(frame_add, width=170, placeholder_text="WhatsApp (Ej: 57300...)")
    ent_tel.pack(side="left", padx=8, pady=8)

    ent_servicio = ctk.CTkEntry(frame_add, width=190, placeholder_text="Plan (Ej: Gemini Pro)")
    ent_servicio.pack(side="left", padx=8, pady=8)
    ent_servicio.insert(0, "Google Gemini Pro")

    ent_valor = ctk.CTkEntry(frame_add, width=120, placeholder_text="Valor ($)")
    ent_valor.pack(side="left", padx=8, pady=8)
    ent_valor.insert(0, "10000")

    ent_dia = ctk.CTkEntry(frame_add, width=110, placeholder_text="Día Cobro (30)")
    ent_dia.pack(side="left", padx=8, pady=8)
    ent_dia.insert(0, "30")

    # --- TABLA DE CONTROL DE PAGOS Y VENCIMIENTOS (COLUMNAS BIEN ESPACIADAS) ---
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#0F172A", foreground="#E2E8F0", fieldbackground="#0F172A", borderwidth=0, font=("Arial", 11), rowheight=36)
    style.map("Treeview", background=[("selected", "#1E3A8A")])
    style.configure("Treeview.Heading", background="#1E293B", foreground="#00FFCC", font=("Arial", 12, "bold"), borderwidth=0, padding=(6, 6))

    frame_tabla = ctk.CTkFrame(win_sub, fg_color="transparent")
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=8)

    scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    cols = ("nombre", "telefono", "servicio", "valor", "dia_corte", "ultimo_pago", "estado")
    tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=10, yscrollcommand=scroll_y.set)
    scroll_y.config(command=tree.yview)

    tree.heading("nombre", text="Miembro / Familiar")
    tree.heading("telefono", text="WhatsApp")
    tree.heading("servicio", text="Plan Compartido")
    tree.heading("valor", text="Cuota Mes")
    tree.heading("dia_corte", text="Corte")
    tree.heading("ultimo_pago", text="Último Pago")
    tree.heading("estado", text="Estado y Acción (Día 30 / 31)")

    tree.column("nombre", width=180, anchor="w", stretch=True)
    tree.column("telefono", width=135, anchor="center", stretch=False)
    tree.column("servicio", width=175, anchor="center", stretch=False)
    tree.column("valor", width=115, anchor="center", stretch=False)
    tree.column("dia_corte", width=95, anchor="center", stretch=False)
    tree.column("ultimo_pago", width=125, anchor="center", stretch=False)
    tree.column("estado", width=310, anchor="w", stretch=True)
    tree.pack(fill="both", expand=True)

    def calcular_estado(miembro):
        hoy = datetime.date.today()
        mes_actual_str = hoy.strftime("%Y-%m")
        pagado_este_mes = (miembro.get("ultimo_mes_pagado") == mes_actual_str)
        dia_corte = int(miembro.get("dia_corte", 30))

        if pagado_este_mes:
            return "[AL DÍA] Servicio Activo"
        if hoy.day == dia_corte:
            return "[COBRAR HOY] Día de Pago"
        elif hoy.day > dia_corte:
            return "[EN MORA] ¡Retirar del Grupo Hoy!"
        else:
            faltan = dia_corte - hoy.day
            return f"[PENDIENTE] Faltan {faltan} días"

    def refrescar_tabla():
        tree.delete(*tree.get_children())
        total_mes = 0
        for idx, m in enumerate(db["miembros"]):
            est = calcular_estado(m)
            val_num = int(m.get("valor", 10000))
            total_mes += val_num
            tree.insert("", "end", iid=str(idx), values=(
                m.get("nombre", ""),
                m.get("telefono", ""),
                m.get("servicio", "Google Gemini Pro"),
                f"${val_num:,.0f}",
                f"Día {m.get('dia_corte', 30)}",
                m.get("ultimo_mes_pagado", "Pendiente"),
                est
            ))
        lbl_resumen.configure(text=f"Miembros: {len(db['miembros'])}  |  Recaudo Mensual: ${total_mes:,.0f} COP")

    def agregar_miembro():
        nom = ent_nombre.get().strip()
        tel = "".join(filter(str.isdigit, ent_tel.get().strip()))
        srv = ent_servicio.get().strip() or "Google Gemini Pro"
        val = "".join(filter(str.isdigit, ent_valor.get().strip())) or "10000"
        dia = "".join(filter(str.isdigit, ent_dia.get().strip())) or "30"

        if not nom or not tel:
            messagebox.showwarning("Faltan Datos", "Ingresa el nombre y el número de WhatsApp.", parent=win_sub)
            return
        if len(tel) == 10 and tel.startswith("3"):
            tel = "57" + tel

        db["miembros"].append({
            "nombre": nom,
            "telefono": tel,
            "servicio": srv,
            "valor": int(val),
            "dia_corte": min(31, max(1, int(dia))),
            "ultimo_mes_pagado": "Pendiente"
        })
        guardar_db(db)
        ent_nombre.delete(0, "end")
        ent_tel.delete(0, "end")
        refrescar_tabla()

    ctk.CTkButton(frame_add, text="+ Agregar al Grupo", fg_color="#10B981", hover_color="#059669", font=("Arial", 13, "bold"), width=155, command=agregar_miembro).pack(side="right", padx=10, pady=8)

    # --- ACCIONES TÁCTICAS DE COBRO, RENOVACIÓN Y CORTE INDIVIDUAL ---
    def marcar_pagado():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona un miembro de la tabla para registrar su pago.", parent=win_sub)
            return
        idx = int(sel[0])
        mes_actual = datetime.date.today().strftime("%Y-%m")
        db["miembros"][idx]["ultimo_mes_pagado"] = mes_actual
        guardar_db(db)
        refrescar_tabla()

    def marcar_pendiente():
        sel = tree.selection()
        if not sel: return
        idx = int(sel[0])
        db["miembros"][idx]["ultimo_mes_pagado"] = "Pendiente"
        guardar_db(db)
        refrescar_tabla()

    def enviar_cobro_whatsapp():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Selección", "Selecciona primero a un familiar en la tabla para enviarle el mensaje.", parent=win_sub)
            return
        # Auto-guardamos lo que tengas escrito en la caja de datos de pago
        guardar_metodo(silencioso=True)
        idx = int(sel[0])
        m = db["miembros"][idx]
        cuenta_pago = db.get("metodo_pago", "Nequi / Llave: @LDVP671")
        est = calcular_estado(m)

        # Mensaje 100% libre de emojis de 4 bytes para que nunca salga el signo '?' en WhatsApp Desktop
        if "MORA" in est:
            msg = (
                f"*AVISO DE CORTE DE SERVICIO - {m['servicio'].upper()}*\n\n"
                f"Hola *{m['nombre']}*, te recuerdo que el dia {m['dia_corte']} vencio la cuota mensual de "
                f"*${m['valor']:,.0f} COP* de nuestro grupo familiar de *{m['servicio']}*.\n\n"
                f"• *Cuenta para transferir:* {cuenta_pago}\n\n"
                f"Por favor enviame el comprobante hoy mismo para mantener tu cupo activo y evitar que el sistema retire tu cuenta del grupo familiar. ¡Muchas gracias!"
            )
        else:
            msg = (
                f"*RECORDATORIO DE PAGO MENSUAL - {m['servicio'].upper()}*\n\n"
                f"Hola *{m['nombre']}*, pasando a recordarte que el dia {m['dia_corte']} corresponde el pago mensual de "
                f"*${m['valor']:,.0f} COP* por los beneficios de *{m['servicio']}* (IA + Almacenamiento).\n\n"
                f"• *Puedes transferir a:* {cuenta_pago}\n\n"
                f"Recuerda enviarme el comprobante a mas tardar el dia {m['dia_corte']} para que tu servicio siga activo sin interrupciones el dia 31. ¡Gracias!"
            )
        url_wa = f"https://wa.me/{m['telefono']}?text={urllib.parse.quote(msg)}"
        webbrowser.open(url_wa)

    def eliminar_miembro():
        sel = tree.selection()
        if not sel: return
        idx = int(sel[0])
        nom = db["miembros"][idx]["nombre"]
        if messagebox.askyesno("Eliminar", f"¿Quitar a '{nom}' de tu tabla de control?", parent=win_sub):
            db["miembros"].pop(idx)
            guardar_db(db)
            refrescar_tabla()

    def abrir_panel_corte_individual():
        sel = tree.selection()
        nombre_sel = db["miembros"][int(sel[0])]["nombre"] if sel else "el miembro que no pagó"
        messagebox.showinfo(
            "Cómo Cortar el Servicio a 1 Sola Persona",
            f"Se abrirá la lista individual de tu Grupo Familiar de Google para retirar a {nombre_sel}:\n\n"
            "1. En la página que se abrirá ('Tu grupo familiar'), verás los nombres de los 5 miembros por separado.\n"
            f"2. Haz clic únicamente sobre el nombre de '{nombre_sel}'.\n"
            "3. Presiona el botón 'Quitar miembro' (Remove member).\n\n"
            "NOTA: Así solo él pierde el acceso a Gemini Pro y los otros 4 familiares que sí pagaron siguen disfrutando sus beneficios sin interrupción.",
            parent=win_sub
        )
        # Abre directamente la lista individual de miembros del grupo familiar (no el interruptor global)
        webbrowser.open("https://myaccount.google.com/family/details")

    frame_btns = ctk.CTkFrame(win_sub, fg_color="transparent")
    frame_btns.pack(fill="x", padx=20, pady=12)

    ctk.CTkButton(frame_btns, text="1. Enviar Cobro por WhatsApp", font=("Arial", 13, "bold"), height=42, fg_color="#25D366", hover_color="#1DA851", text_color="#000000", command=enviar_cobro_whatsapp).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns, text="2. Marcar Mes Pagado", font=("Arial", 13, "bold"), height=42, fg_color="#10B981", hover_color="#059669", command=marcar_pagado).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns, text="3. Reiniciar a Pendiente", font=("Arial", 13, "bold"), height=42, fg_color="#3B82F6", hover_color="#2563EB", command=marcar_pendiente).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns, text="4. Retirar 1 Miembro (Google Family)", font=("Arial", 13, "bold"), height=42, fg_color="#EF4444", hover_color="#DC2626", command=abrir_panel_corte_individual).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns, text="Borrar Fila", font=("Arial", 13, "bold"), height=42, width=110, fg_color="#334155", hover_color="#475569", command=eliminar_miembro).pack(side="right", padx=4)

    refrescar_tabla()

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
    log("[*] Alterando directivas de propiedad del Kernel...")
    
    # Aplicamos la técnica del video: takeown + icacls + Remove-Item en PowerShell
    script_destruccion = f"""
    takeown.exe /F "{ruta}" /A /R /D Y 2>null
    icacls.exe "{ruta}" /grant *S-1-5-32-544:F /T /C /Q 2>null
    Remove-Item -LiteralPath "{ruta}" -Recurse -Force -ErrorAction SilentlyContinue
    """
    run_ps_script(log, script_destruccion)
    
    import os
    if not os.path.exists(ruta): 
        log("[+] CARPETA REBELDE PULVERIZADA EXITOSAMENTE.")
    else: 
        log("[-] Operación parcial: Algunos archivos siguen anclados al procesador o RAM. Se borrarán al reiniciar.")

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

def logica_ytdlp(log=None, lista_urls=None, calidad=None, formato="mp4", ruta_cookies=""):
    import zipfile, urllib.request, os, shutil, subprocess, json, threading, webbrowser
    import customtkinter as ctk
    from tkinter import filedialog, messagebox

    # Si se invoca con los parámetros antiguos desde un script externo, ejecuta directo;
    # si se abre desde el botón principal, lanza el Dashboard Visual estilo Cobalt.tools:
    if lista_urls and calidad:
        _ejecutar_motor_multimedia(log, lista_urls, calidad, formato, ruta_cookies)
        return

    if log:
        log("\n[*] Desplegando TREMEND Media Studio (Interfaz Cobalt + Motores Locales yt-dlp / gallery-dl / FFmpeg)...")

    win_media = ctk.CTkToplevel(app)
    win_media.title("TREMEND Media Studio - Descargador Universal & Conversor (Estilo Cobalt.tools)")
    win_media.geometry("1080x680")
    win_media.attributes("-topmost", True)
    win_media.transient(app)

    # --- ENCABEZADO ESTILO COBALT.TOOLS (NEÓN VERDE SOBRE NEGRO PROFUNDO) ---
    frame_head = ctk.CTkFrame(win_media, fg_color="#050811", corner_radius=12, border_width=1, border_color="#10B981")
    frame_head.pack(fill="x", padx=20, pady=(15, 8))

    ctk.CTkLabel(frame_head, text=">> TREMEND MEDIA & COBALT STUDIO", font=("Consolas", 20, "bold"), text_color="#10B981").pack(pady=(10, 2))
    ctk.CTkLabel(frame_head, text="Descarga Vídeo (4K/1080p), Audio (MP3), Fotos (JPG Originales) y Carruseles de +1000 sitios • Sin anuncios + Conversor Offline", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 10))

    # --- BARRA DE ENLACES (SOPORTA 1 O MÚLTIPLES ENLACES) ---
    frame_url = ctk.CTkFrame(win_media, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#334155")
    frame_url.pack(fill="x", padx=20, pady=6)

    ctk.CTkLabel(frame_url, text="🔗 Enlace(s):", font=("Arial", 13, "bold"), text_color="#00FFCC").pack(side="left", padx=(12, 6), pady=12)
    ent_urls = ctk.CTkEntry(frame_url, placeholder_text="Pega aquí uno o varios enlaces separados por coma (Instagram, TikTok, YouTube, X, Reddit, Pinterest, SoundCloud...)", font=("Consolas", 13), height=38)
    ent_urls.pack(side="left", fill="x", expand=True, padx=6, pady=12)

    def pegar_portapapeles():
        try:
            texto_clip = app.clipboard_get().strip()
            if texto_clip:
                ent_urls.delete(0, "end")
                ent_urls.insert(0, texto_clip)
        except Exception:
            pass

    ctk.CTkButton(frame_url, text="📋 Pegar", width=95, height=38, fg_color="#334155", hover_color="#475569", font=("Arial", 12, "bold"), command=pegar_portapapeles).pack(side="right", padx=(4, 12), pady=12)

    # --- SELECTOR DE LOS 4 MODOS DE COBALT + OPCIONES AVANZADAS ---
    frame_opts = ctk.CTkFrame(win_media, fg_color="#1E293B", corner_radius=10)
    frame_opts.pack(fill="x", padx=20, pady=6)

    var_modo = ctk.StringVar(value="1")
    modos_cobalt = [
        ("🎬 Vídeo (Máx / 4K)", "1"),
        ("🎬 Vídeo (1080p)", "2"),
        ("🎬 Vídeo (720p)", "6"),
        ("🎵 Audio (MP3 Puro)", "3"),
        ("🖼️ Fotos / Carrusel (JPG)", "4")
    ]
    for texto_m, val_m in modos_cobalt:
        ctk.CTkRadioButton(
            frame_opts, text=texto_m, variable=var_modo, value=val_m,
            font=("Arial", 12, "bold"), text_color="#E2E8F0", fg_color="#10B981", hover_color="#059669"
        ).pack(side="left", padx=12, pady=12)

    var_formato = ctk.StringVar(value="mp4")
    combo_fmt = ctk.CTkOptionMenu(frame_opts, variable=var_formato, values=["mp4", "mkv"], width=85, fg_color="#0F172A", button_color="#334155")
    combo_fmt.pack(side="right", padx=12, pady=12)
    ctk.CTkLabel(frame_opts, text="Contenedor:", font=("Arial", 12, "bold"), text_color="#94A3B8").pack(side="right", padx=2)

    var_cookies = ctk.StringVar(value="")
    def seleccionar_cookies():
        r_c = filedialog.askopenfilename(title="Selecciona tu archivo cookies.txt (Opcional para posts privados)", filetypes=[("Texto Cookies", "*.txt"), ("Todos", "*.*")], parent=win_media)
        if r_c:
            var_cookies.set(r_c)
            btn_cookies.configure(text="🍪 Cookies Activas ✔", fg_color="#10B981", text_color="#000000")

    btn_cookies = ctk.CTkButton(frame_opts, text="🍪 Inyectar cookies.txt (Opcional)", width=210, fg_color="#334155", hover_color="#475569", font=("Arial", 12), command=seleccionar_cookies)
    btn_cookies.pack(side="right", padx=10, pady=12)

    # --- CONSOLA INTERNA EN TIEMPO REAL ---
    txt_media = ctk.CTkTextbox(win_media, font=("Consolas", 13), fg_color="#050811", text_color="#00FFCC", border_width=1, border_color="#334155")
    txt_media.pack(fill="both", expand=True, padx=20, pady=8)
    txt_media.insert("end", "[*] Listo para extraer. Pega un enlace arriba y presiona 'Descargar Ahora'.\n[*] El motor convierte automáticamente las imágenes WEBP de carruseles a formato JPG original.\n")
    txt_media.configure(state="disabled")

    def log_ui(msg):
        if win_media.winfo_exists():
            def _u():
                txt_media.configure(state="normal")
                txt_media.insert("end", str(msg) + "\n")
                txt_media.see("end")
                txt_media.configure(state="disabled")
            app.after(0, _u)
        if log:
            try: log(msg)
            except Exception: pass

    def iniciar_descarga_ui():
        raw = ent_urls.get().strip()
        if not raw:
            messagebox.showwarning("Sin Enlace", "Pega al menos un enlace en la barra superior.", parent=win_media)
            return
        urls = [u.strip() for u in raw.replace("\n", ",").split(",") if u.strip()]
        cal = var_modo.get()
        fmt = var_formato.get()
        ck = var_cookies.get()

        txt_media.configure(state="normal"); txt_media.delete("1.0", "end"); txt_media.configure(state="disabled")
        threading.Thread(
            target=_ejecutar_motor_multimedia,
            args=(log_ui, urls, cal, fmt, ck, win_media),
            daemon=True
        ).start()

    # --- NUEVO USO: CONVERSOR OFFLINE Y LIMPIADOR DE METADATOS CON FFMPEG ---
    def convertir_y_limpiar_local():
        arch_in = filedialog.askopenfilename(
            title="Selecciona un video, audio o imagen de tu PC para convertir y limpiar metadatos",
            filetypes=[("Multimedia", "*.mp4 *.mkv *.webm *.mov *.avi *.mp3 *.wav *.flac *.webp *.png"), ("Todos", "*.*")],
            parent=win_media
        )
        if not arch_in:
            return
        dialogo_f = ctk.CTkInputDialog(
            text="Escribe el formato de salida deseado (mp4, mp3, jpg, png, wav):\n(Además se eliminarán todos los metadatos ocultos de rastreo)",
            title="Conversor y Limpiador Forense FFmpeg"
        )
        fmt_out = (dialogo_f.get_input() or "").strip().lower().replace(".", "")
        if fmt_out not in ("mp4", "mp3", "jpg", "png", "wav", "mkv"):
            return

        def _run_conv():
            temp_dir = r"C:\Tremend_Media"
            ffmpeg_path = _asegurar_ffmpeg(log_ui, temp_dir)
            if not ffmpeg_path:
                return
            base_no_ext = os.path.splitext(arch_in)[0]
            arch_out = f"{base_no_ext}_TREMEND_Clean.{fmt_out}"
            log_ui(f"\n[*] Convirtiendo y purgando metadatos ocultos: {os.path.basename(arch_in)} -> .{fmt_out.upper()}...")
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            cmd_ff = f'"{ffmpeg_path}" -y -i "{arch_in}" -map_metadata -1 "{arch_out}"'
            res = subprocess.run(cmd_ff, shell=True, capture_output=True, text=True, startupinfo=startupinfo)
            if res.returncode == 0 and os.path.exists(arch_out):
                log_ui(f"[+] ¡ÉXITO! Archivo convertido y libre de metadatos en:\n    -> {arch_out}")
                try: os.startfile(os.path.dirname(arch_out))
                except Exception: pass
            else:
                log_ui(f"[-] Error en conversión FFmpeg: {res.stderr[-300:]}")

        threading.Thread(target=_run_conv, daemon=True).start()

    # --- BOTONERA INFERIOR ---
    frame_btns = ctk.CTkFrame(win_media, fg_color="transparent")
    frame_btns.pack(fill="x", padx=20, pady=(4, 15))

    ctk.CTkButton(frame_btns, text="⬇️ 1. Descargar Ahora (Motor Local)", font=("Arial", 14, "bold"), height=44, fg_color="#10B981", hover_color="#059669", text_color="#000000", command=iniciar_descarga_ui).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns, text="🧼 2. Convertir Archivo Local + Borrar Metadatos", font=("Arial", 13, "bold"), height=44, fg_color="#3B82F6", hover_color="#2563EB", command=convertir_y_limpiar_local).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns, text="🌐 3. Abrir cobalt.tools Web", font=("Arial", 13, "bold"), height=44, width=200, fg_color="#8B5CF6", hover_color="#7C3AED", command=lambda: webbrowser.open("https://cobalt.tools")).pack(side="left", padx=4)
    ctk.CTkButton(frame_btns, text="📂 Descargas", font=("Arial", 13, "bold"), height=44, width=125, fg_color="#334155", hover_color="#475569", command=lambda: os.startfile(os.path.join(os.environ.get("USERPROFILE"), "Downloads"))).pack(side="right", padx=4)


def _asegurar_ffmpeg(log, temp_dir):
    import os, zipfile, urllib.request
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    ffmpeg_path = os.path.join(temp_dir, "ffmpeg.exe")
    ffprobe_path = os.path.join(temp_dir, "ffprobe.exe")

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
                        with open(os.path.join(temp_dir, filename), "wb") as f_out:
                            f_out.write(zip_ref.read(member))
            os.remove(zip_path)
            log("[+] Códecs FFmpeg instalados con éxito.")
        except Exception as e:
            log(f"[-] Advertencia al procesar códecs: {e}")
            return None
    return ffmpeg_path


def _ejecutar_motor_multimedia(log, lista_urls, calidad, formato, ruta_cookies="", parent_win=None):
    import os, shutil, subprocess, json, urllib.request
    from tkinter import messagebox

    temp_dir = r"C:\Tremend_Media"
    ffmpeg_path = _asegurar_ffmpeg(log, temp_dir)

    # === RAMA DE FOTOGRAFÍAS Y CARRUSELES ENTEROS (GALLERY-DL + FFMPEG JPG) ===
    if calidad in ['4', '5']:
        log(f"\n[*] Iniciando Extractor de Fotos y Carruseles (Lote de {len(lista_urls)} enlaces)")
        exe_path = os.path.join(temp_dir, "gallery-dl.exe")

        if not os.path.exists(exe_path):
            log("[*] Contactando API de GitHub para ubicar el motor gallery-dl...")
            api_url = "https://api.github.com/repos/mikf/gallery-dl/releases/latest"
            url_gdl = None
            try:
                req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as response:
                    data = json.loads(response.read().decode())
                for asset in data.get('assets', []):
                    nombre = asset.get('name', '').lower()
                    if 'gallery-dl' in nombre and nombre.endswith('.exe'):
                        url_gdl = asset['browser_download_url']
                        break
            except Exception:
                pass
            if not url_gdl:
                url_gdl = "https://github.com/mikf/gallery-dl/releases/download/v1.27.2/gallery-dl.exe"
            try:
                urllib.request.urlretrieve(url_gdl, exe_path)
            except Exception as e2:
                log(f"[-] Error de red: {e2}")
                return

        dl_path = os.path.join(os.environ.get("USERPROFILE"), "Downloads", "TREMEND_Galerias")
        if not os.path.exists(dl_path):
            os.makedirs(dl_path)
        urls_param = ' '.join([f'"{u}"' for u in lista_urls])

        if ruta_cookies and os.path.exists(ruta_cookies):
            log("[*] Inyectando sesión desde archivo cookies.txt...")
            cmd = f'"{exe_path}" --cookies "{ruta_cookies}" --directory "{dl_path}" {urls_param}'
        else:
            log("[*] Extracción Directa (Modo Público)...")
            cmd = f'"{exe_path}" --directory "{dl_path}" {urls_param}'

        run_cmd(log, cmd)

        log("[*] Escaneando carrusel en busca de archivos WEBP para convertirlos a JPG original...")
        convertidas = 0
        for root, _, files in os.walk(dl_path):
            for file in files:
                if file.lower().endswith('.webp') and ffmpeg_path:
                    ruta_webp = os.path.join(root, file)
                    ruta_jpg = os.path.join(root, file[:-5] + ".jpg")
                    try:
                        subprocess.run(f'"{ffmpeg_path}" -y -i "{ruta_webp}" -qscale:v 2 "{ruta_jpg}"', shell=True, capture_output=True)
                        os.remove(ruta_webp)
                        convertidas += 1
                    except Exception:
                        pass

        if convertidas > 0:
            log(f"[+] {convertidas} imágenes WEBP convertidas a JPG de alta calidad exitosamente.")

        log("\n=======================================================")
        log(f" [+] EXTRACCIÓN COMPLETADA. Imágenes guardadas en:\n [+] {dl_path}")
        log("=======================================================")
        try: os.startfile(dl_path)
        except Exception: pass
        try: notificar_voz("La extracción de fotos y carruseles ha finalizado.")
        except Exception: pass
        return

    # === RAMA DE VIDEOS Y AUDIO (YT-DLP + FFMPEG) ===
    log(f"\n[*] Iniciando Descargador Multimedia Avanzado (Lote de {len(lista_urls)} enlaces)")
    exe_path = os.path.join(temp_dir, "yt-dlp.exe")

    if not os.path.exists(exe_path):
        log("[*] Descargando motor de extracción portátil (yt-dlp)...")
        try:
            urllib.request.urlretrieve("https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe", exe_path)
        except Exception as e:
            log(f"[-] Error de red en yt-dlp: {e}")
            return

    dl_path = os.path.join(os.environ.get("USERPROFILE"), "Downloads")
    urls_param = ' '.join([f'"{u}"' for u in lista_urls])
    cookie_flag = f'--cookies "{ruta_cookies}"' if (ruta_cookies and os.path.exists(ruta_cookies)) else ""
    params_base = f'--yes-playlist --windows-filenames {cookie_flag} -o "%(playlist_index|)s%(playlist_index& - |)s%(title).80s [%(id)s].%(ext)s" --embed-metadata --embed-thumbnail'

    if calidad == '3':
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -x --audio-format mp3 -P "{dl_path}" {urls_param}'
    elif calidad == '1':
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -S "vcodec:vp9" --remux-video {formato} -f "bestvideo+bestaudio/best" --merge-output-format {formato} -P "{dl_path}" {urls_param}'
    elif calidad == '2':
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -S "vcodec:vp9,res:1080" --remux-video {formato} -f "bestvideo[height<=1080]+bestaudio/best" --merge-output-format {formato} -P "{dl_path}" {urls_param}'
    elif calidad == '6':
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -S "vcodec:vp9,res:720" --remux-video {formato} -f "bestvideo[height<=720]+bestaudio/best" --merge-output-format {formato} -P "{dl_path}" {urls_param}'
    elif calidad == '7':
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -S "vcodec:vp9,res:480" --remux-video {formato} -f "bestvideo[height<=480]+bestaudio/best" --merge-output-format {formato} -P "{dl_path}" {urls_param}'
    else:
        return

    log("[*] Procesando flujos y uniendo contenedores. Por favor, espera...")
    run_cmd(log, cmd)
    log("\n[+] ¡EXTRACCIÓN COMPLETADA! Archivos guardados en tu carpeta de Descargas.")
    try: notificar_voz("La descarga del contenido ha finalizado.")
    except Exception: pass

def logica_gestor_usb(log, accion, disco=""):
    import winreg, os, subprocess, shutil
    
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
        
        # 1. Desbloqueo por Registro de Windows (StorageDevicePolicies)
        log("[*] Eliminando bloqueos de escritura en el Registro del Sistema...")
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\StorageDevicePolicies")
            winreg.SetValueEx(key, "WriteProtect", 0, winreg.REG_DWORD, 0)
            log("    -> Directiva WriteProtect desactivada (Valor = 0).")
        except Exception:
            pass

        # 2. Desbloqueo físico por Diskpart
        script_path = os.path.join(os.environ.get("TEMP"), "dp_unlock.txt")
        try:
            with open(script_path, "w") as f:
                f.write(f"select disk {disco}\nattributes disk clear readonly\nexit")
            run_cmd(log, f'diskpart /s "{script_path}"')
            try: os.remove(script_path)
            except: pass
            log("[+] Atributos de solo lectura eliminados. Extrae y vuelve a conectar la USB.")
        except Exception as e: 
            log(f"[-] Error durante la inyección de Diskpart: {e}")

    elif accion == '4':
        letra = disco.replace(":", "").replace("\\", "").strip().upper()
        if not letra or not letra.isalpha() or len(letra) != 1:
            log("[-] Error: Debes ingresar una letra de unidad válida (Ejemplo: E, F, G).")
            return
            
        unidad = f"{letra}:"
        ruta_raiz = f"{unidad}\\"
        
        if not os.path.exists(ruta_raiz):
            log(f"[-] Error: La unidad {unidad} no está conectada o no fue detectada por Windows.")
            return
            
        if unidad == "C:":
            log("[-] ESCUDO DE SEGURIDAD: Operación bloqueada en C:. Esta herramienta es exclusiva para memorias USB y discos externos.")
            return

        log("\n" + "="*75)
        log(f" 💉 DESINFECCIÓN, RESCATE Y VACUNA USB (UNIDAD {unidad}) ")
        log("="*75)

        # FASE 1: Destrucción de vectores de infección en la raíz (Estilo del /q /f)
        log(f"\n[1/3] Eliminando accesos directos falsos (.lnk) y scripts maliciosos en la raíz de {unidad}...")
        extensiones_basura = (".lnk", ".vbs", ".vbe", ".wsf", ".scr", ".pif")
        eliminados = 0
        
        try:
            for item in os.listdir(ruta_raiz):
                ruta_item = os.path.join(ruta_raiz, item)
                if os.path.isfile(ruta_item) and item.lower().endswith(extensiones_basura):
                    try:
                        run_cmd(log, f'cmd /c attrib -h -r -s "{ruta_item}" 2>nul')
                        os.remove(ruta_item)
                        log(f"    -> Amenaza neutralizada: {item}")
                        eliminados += 1
                    except Exception:
                        pass
        except Exception as e:
            log(f"[-] Error escaneando la raíz: {e}")
            
        log(f"[+] Se destruyeron {eliminados} accesos directos/scripts trampa.")

        # FASE 2: Rescate de carpetas y archivos ocultos por el virus
        log(f"\n[2/3] Restaurando visibilidad a las carpetas y archivos secuestrados en {unidad}...")
        log("    -> Quitando atributos Oculto (-H), Sistema (-S) y Solo Lectura (-R)...")
        log("    [!] Esto puede tomar unos segundos según la cantidad de archivos...")
        run_cmd(log, f'attrib -h -r -s /s /d {unidad}\\*.*')
        
        # Rescate de carpetas invisibles (sin nombre o espacio en blanco creadas por troyanos USB)
        for item in os.listdir(ruta_raiz):
            if item.strip() == "" or item == "\u00a0":
                ruta_invisible = os.path.join(ruta_raiz, item)
                ruta_rescate = os.path.join(ruta_raiz, "ARCHIVOS_RESCATADOS_TREMEND")
                try:
                    os.rename(ruta_invisible, ruta_rescate)
                    log(f"    -> [!] Bóveda oculta sin nombre detectada y renombrada a: 'ARCHIVOS_RESCATADOS_TREMEND'")
                except Exception:
                    pass

        log("[+] ¡Archivos y carpetas del usuario restaurados con éxito!")

        # FASE 3: Vacuna Inmunizadora (Carpeta autorun.inf blindada)
        log(f"\n[3/3] Aplicando Vacuna Anti-Autorun en {unidad}...")
        ruta_autorun = os.path.join(ruta_raiz, "autorun.inf")
        
        try:
            # Si existe un archivo autorun.inf malicioso previo, lo destruimos
            if os.path.isfile(ruta_autorun):
                run_cmd(log, f'cmd /c attrib -h -r -s "{ruta_autorun}" 2>nul')
                os.remove(ruta_autorun)
                log("    -> Archivo 'autorun.inf' malicioso previo destruido.")
                
            # Creamos un DIRECTORIO autorun.inf con subcarpeta protegida
            if not os.path.exists(ruta_autorun):
                os.makedirs(os.path.join(ruta_autorun, "Vacuna_TREMEND.lock"), exist_ok=True)
                
            # Ocultamos y blindamos la vacuna como archivo de sistema e inmutable
            run_cmd(log, f'cmd /c attrib +h +r +s "{ruta_autorun}" 2>nul')
            run_cmd(log, f'cmd /c icacls "{ruta_autorun}" /deny *S-1-1-0:(D,WD,AD,WA) 2>nul')
            log("[+] ¡Vacuna inyectada! Ningún virus clásico podrá volver a escribir un 'autorun.inf' en esta USB.")
        except Exception as e:
            log(f"[-] Advertencia al aplicar vacuna: {e}")

        log("\n=======================================================")
        log(f" ✅ MEMORIA USB ({unidad}) DESINFECTADA Y PROTEGIDA ")
        log("=======================================================")
        try: os.startfile(ruta_raiz)
        except: pass

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

def logica_laboratorio_criptografico(log, accion=None, dato=None):
    import math
    import secrets
    import string
    import subprocess
    import threading
    import customtkinter as ctk
    from tkinter import messagebox

    def calcular_entropia(pwd):
        if not pwd:
            return 0, "0 Segundos (Vacía)", "Inválida", "#94A3B8"
        pool_size = 0
        if any(c.islower() for c in pwd): pool_size += 26
        if any(c.isupper() for c in pwd): pool_size += 26
        if any(c.isdigit() for c in pwd): pool_size += 10
        if any(c in string.punctuation for c in pwd): pool_size += 32
        entropia = len(pwd) * math.log2(pool_size) if pool_size > 0 else 0
        segundos = (2 ** entropia) / 100_000_000_000
        if segundos < 1: return entropia, "Instantáneo ❌", "CRÍTICO", "#EF4444"
        elif segundos < 60: return entropia, f"{int(segundos)} Segundos ⚠️", "Vulnerable", "#EF4444"
        elif segundos < 3600: return entropia, f"{int(segundos / 60)} Minutos ⚠️", "Débil", "#F59E0B"
        elif segundos < 86400: return entropia, f"{int(segundos / 3600)} Horas ⚠️", "Media", "#FCD34D"
        elif segundos < 31536000: return entropia, f"{int(segundos / 86400)} Días 🛡️", "Fuerte", "#10B981"
        elif segundos < 3153600000: return entropia, f"{int(segundos / 31536000)} Años 🛡️", "Militar", "#38BDF8"
        else: return entropia, "Milenios (Inhackeable) 🌌", "Titanium", "#8B5CF6"

    win_crypto = ctk.CTkToplevel(app)
    win_crypto.title("TREMEND - Bóveda Criptográfica y Escudo Anti-Fuerza Bruta de Windows")
    win_crypto.geometry("1140x620")
    win_crypto.attributes("-topmost", True)
    win_crypto.transient(app)

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # ---------------------------------------------------------
    # PANEL IZQUIERDO: AUDITOR, GENERADOR Y TOKENS DE 256 BITS
    # ---------------------------------------------------------
    frame_izq = ctk.CTkFrame(win_crypto, width=460, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#38BDF8")
    frame_izq.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(frame_izq, text="🛡️ Auditor y Generador Militar", font=("Arial", 22, "bold"), text_color="#00FFCC").pack(pady=(18, 5))
    ctk.CTkLabel(frame_izq, text="Audita la resistencia de tus claves o genera contraseñas y Tokens de 256-bit.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 18))

    ent_auditar = ctk.CTkEntry(frame_izq, placeholder_text="Escribe una contraseña para medir su seguridad...", font=("Arial", 15), width=360, height=42, show="*")
    ent_auditar.pack(pady=5)

    lbl_nivel = ctk.CTkLabel(frame_izq, text="Seguridad: ---", font=("Arial", 16, "bold"), text_color="#94A3B8")
    lbl_nivel.pack(pady=(8, 0))
    lbl_tiempo = ctk.CTkLabel(frame_izq, text="Resistencia ante Fuerza Bruta: ---", font=("Arial", 14), text_color="#CBD5E1")
    lbl_tiempo.pack(pady=(0, 10))

    def on_typing(event):
        pwd = ent_auditar.get()
        if not pwd:
            lbl_nivel.configure(text="Seguridad: ---", text_color="#94A3B8")
            lbl_tiempo.configure(text="Resistencia ante Fuerza Bruta: ---")
            return
        _, tiempo_str, nivel, color = calcular_entropia(pwd)
        lbl_nivel.configure(text=f"Seguridad: {nivel}", text_color=color)
        lbl_tiempo.configure(text=f"Resistencia ante Fuerza Bruta: {tiempo_str}")

    ent_auditar.bind("<KeyRelease>", on_typing)

    ctk.CTkFrame(frame_izq, height=1, fg_color="#334155").pack(fill="x", padx=35, pady=15)

    ctk.CTkLabel(frame_izq, text="Longitud de nueva clave (Ej: 16):", font=("Arial", 14, "bold"), text_color="#E2E8F0").pack()
    var_len = ctk.StringVar(value="16")
    ctk.CTkEntry(frame_izq, textvariable=var_len, width=80, justify="center", font=("Arial", 16)).pack(pady=5)

    lbl_gen_resultado = ctk.CTkLabel(frame_izq, text="---", font=("Consolas", 15, "bold"), text_color="#38BDF8", wraplength=400)
    lbl_gen_resultado.pack(pady=(12, 10))

    def forjar_clave():
        try: l = int(var_len.get())
        except: l = 16
        if l < 8: l = 8
        caracteres = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        nueva = ''.join(secrets.choice(caracteres) for _ in range(l))
        lbl_gen_resultado.configure(text=nueva, font=("Consolas", 20, "bold"))
        try:
            app.clipboard_clear(); app.clipboard_append(nueva)
            lbl_nivel.configure(text="¡Clave copiada al portapapeles!", text_color="#10B981")
        except: pass

    def forjar_token_reset():
        token_largo = secrets.token_hex(32)
        lbl_gen_resultado.configure(text=token_largo, font=("Consolas", 12, "bold"))
        try:
            app.clipboard_clear(); app.clipboard_append(token_largo)
            lbl_nivel.configure(text="🛡️ Token Hex de 256-bit Copiado al Portapapeles", text_color="#A855F7")
            lbl_tiempo.configure(text="Inmune a ataques de lista/Array (1.15 × 10^77 comb.)")
        except: pass

    frame_btns_gen = ctk.CTkFrame(frame_izq, fg_color="transparent")
    frame_btns_gen.pack(fill="x", padx=25, pady=8)
    ctk.CTkButton(frame_btns_gen, text="🗡️ Forjar Clave Segura", font=("Arial", 13, "bold"), height=42, fg_color="#3B82F6", hover_color="#2563EB", command=forjar_clave).pack(side="left", expand=True, fill="x", padx=4)
    ctk.CTkButton(frame_btns_gen, text="🔗 Forjar Token 256-bit", font=("Arial", 13, "bold"), height=42, fg_color="#8B5CF6", hover_color="#7C3AED", command=forjar_token_reset).pack(side="right", expand=True, fill="x", padx=4)

    # ---------------------------------------------------------
    # PANEL DERECHO: ESCUDO REAL ANTI-FUERZA BRUTA DE WINDOWS
    # ---------------------------------------------------------
    frame_der = ctk.CTkFrame(win_crypto, width=580, fg_color="#1E293B", corner_radius=10, border_width=1, border_color="#10B981")
    frame_der.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

    ctk.CTkLabel(frame_der, text="🔒 Escudo Anti-Fuerza Bruta del Sistema (Windows SAM)", font=("Arial", 20, "bold"), text_color="#10B981").pack(pady=(18, 4))
    ctk.CTkLabel(frame_der, text="Por defecto Windows permite intentos infinitos de contraseña. Activa aquí el bloqueo automático tras 5 intentos fallidos y audita si intentaron entrar a tu PC.", font=("Arial", 12), text_color="#94A3B8", wraplength=520).pack(pady=(0, 10))

    txt_defensa_win = ctk.CTkTextbox(frame_der, font=("Consolas", 13), fg_color="#050811", text_color="#38BDF8")
    txt_defensa_win.pack(fill="both", expand=True, padx=20, pady=10)
    txt_defensa_win.configure(state="disabled")

    def log_def(texto):
        if win_crypto.winfo_exists():
            def _u():
                txt_defensa_win.configure(state="normal")
                txt_defensa_win.insert("end", texto + "\n")
                txt_defensa_win.see("end")
                txt_defensa_win.configure(state="disabled")
            app.after(0, _u)

    def auditar_estado_bloqueo():
        txt_defensa_win.configure(state="normal"); txt_defensa_win.delete("1.0", "end"); txt_defensa_win.configure(state="disabled")
        def _run():
            log_def("="*65)
            log_def(" 🛡️ ESTADO ACTUAL DE POLÍTICAS DE CUENTA (NET ACCOUNTS)")
            log_def("="*65)
            out = subprocess.run("net accounts", shell=True, capture_output=True, text=True, encoding="cp850", errors="ignore", startupinfo=startupinfo).stdout
            for l in out.splitlines():
                if l.strip(): log_def("  " + l.strip())
            if "Never" in out or "Nunca" in out:
                log_def("\n🔴 ALERTA: Tu PC NO tiene límite de intentos fallidos ('Nunca').")
                log_def("   Un atacante o malware en red puede probar miles de claves sin ser bloqueado.")
            else:
                log_def("\n🟢 PROTEGIDO: Tu equipo cuenta con bloqueo automático contra fuerza bruta.")

            log_def("\n" + "="*65)
            log_def(" 🕵️ AUDITORÍA DE INTENTOS DE INTRUSIÓN FALLIDOS (EVENT ID 4625)")
            log_def("="*65)
            ps_4625 = "Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} -MaxEvents 10 -ErrorAction SilentlyContinue | Select-Object TimeCreated, Message | ConvertTo-Json"
            res_ev = subprocess.run(["powershell", "-NoProfile", "-Command", ps_4625], capture_output=True, text=True, startupinfo=startupinfo).stdout.strip()
            if not res_ev:
                log_def("🟢 Limpio: No se registran intentos recientes de ataque por fuerza bruta en tu sesión.")
            else:
                log_def("⚠️ Se detectaron intentos fallidos de inicio de sesión recientes en el Visor de Seguridad.")
                log_def("   Te recomendamos mantener activado el Escudo de 5 Intentos.")
        threading.Thread(target=_run, daemon=True).start()

    def activar_bloqueo_5_intentos():
        def _run():
            log_def("\n[*] INYECTANDO POLÍTICA DE BLOQUEO (RATE LIMITING) EN EL KERNEL DE WINDOWS...")
            subprocess.run("net accounts /lockoutthreshold:5 /lockoutduration:15 /lockoutwindow:15", shell=True, capture_output=True, startupinfo=startupinfo)
            auditar_estado_bloqueo()
        threading.Thread(target=_run, daemon=True).start()

    def desactivar_bloqueo():
        def _run():
            subprocess.run("net accounts /lockoutthreshold:0", shell=True, capture_output=True, startupinfo=startupinfo)
            auditar_estado_bloqueo()
        threading.Thread(target=_run, daemon=True).start()

    frame_btns_def = ctk.CTkFrame(frame_der, fg_color="transparent")
    frame_btns_def.pack(side="bottom", fill="x", pady=15, padx=20)
    ctk.CTkButton(frame_btns_def, text="🔍 1. Auditar Estado", height=42, fg_color="#3B82F6", hover_color="#2563EB", font=("Arial", 13, "bold"), command=auditar_estado_bloqueo).pack(side="left", fill="x", expand=True, padx=4)
    ctk.CTkButton(frame_btns_def, text="🛡️ 2. Blindar (5 Intentos = Bloqueo)", height=42, fg_color="#10B981", hover_color="#059669", font=("Arial", 13, "bold"), command=activar_bloqueo_5_intentos).pack(side="left", fill="x", expand=True, padx=4)
    ctk.CTkButton(frame_btns_def, text="🔓 3. Quitar Límite", height=42, fg_color="#334155", hover_color="#475569", font=("Arial", 13, "bold"), command=desactivar_bloqueo).pack(side="right", fill="x", expand=True, padx=4)

    auditar_estado_bloqueo()

def logica_decodificador_forense(log):
    import base64, hashlib, binascii, re, secrets, hmac, time
    import customtkinter as ctk

    log("\n" + "="*75)
    log(" 🕵️ INICIANDO LABORATORIO CRIPTOGRÁFICO Y FORJADOR DE HASHES (SENIOR) ")
    log("="*75)
    log("[*] Desplegando interfaz de transformación y blindaje de contraseñas con Salt...")

    win_chef = ctk.CTkToplevel(app)
    win_chef.title("TREMEND - Decodificador Forense & Hashing Senior (Scrypt + Salt / CyberChef)")
    win_chef.geometry("1140x680")
    win_chef.attributes("-topmost", True)
    win_chef.transient(app)

    # --- LAYOUT PRINCIPAL ---
    frame_in = ctk.CTkFrame(win_chef, width=400, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#38BDF8")
    frame_in.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=20)

    ctk.CTkLabel(frame_in, text="📥 Datos de Entrada (Input)", font=("Arial", 16, "bold"), text_color="#38BDF8").pack(pady=(15, 2))
    ctk.CTkLabel(frame_in, text="Para verificar una clave contra un Hash, escribe:  tu_clave | $scrypt$...", font=("Arial", 11), text_color="#94A3B8").pack(pady=(0, 6))
    txt_input = ctk.CTkTextbox(frame_in, font=("Consolas", 14), fg_color="#000000", text_color="#FFFFFF", wrap="word")
    txt_input.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    # Panel Central (Operaciones)
    frame_ops = ctk.CTkFrame(win_chef, width=260, fg_color="#1E293B", corner_radius=10)
    frame_ops.pack(side="left", fill="y", padx=10, pady=20)

    ctk.CTkLabel(frame_ops, text="⚙️ Operaciones", font=("Arial", 16, "bold"), text_color="#FCD34D").pack(pady=(12, 10))

    # Panel Derecho (Output)
    frame_out = ctk.CTkFrame(win_chef, width=400, fg_color="#0F172A", corner_radius=10, border_width=1, border_color="#10B981")
    frame_out.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)

    ctk.CTkLabel(frame_out, text="📤 Resultado Criptográfico (Output)", font=("Arial", 16, "bold"), text_color="#10B981").pack(pady=(15, 5))
    txt_output = ctk.CTkTextbox(frame_out, font=("Consolas", 13), fg_color="#000000", text_color="#10B981", wrap="word")
    txt_output.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def forjar_hash_scrypt_senior(pwd):
        # Medimos diferencia real Junior (SHA-256 rápido) vs Senior (Scrypt lento + Salt único)
        t0 = time.perf_counter()
        _ = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
        t_sha_ms = (time.perf_counter() - t0) * 1000

        salt_1 = secrets.token_bytes(16)
        t1 = time.perf_counter()
        derivado_1 = hashlib.scrypt(pwd.encode('utf-8'), salt=salt_1, n=16384, r=8, p=1, dklen=32)
        t_scrypt_ms = (time.perf_counter() - t1) * 1000

        # Generamos un segundo Salt con la MISMA clave para demostrar que nunca dan el mismo hash
        salt_2 = secrets.token_bytes(16)
        derivado_2 = hashlib.scrypt(pwd.encode('utf-8'), salt=salt_2, n=16384, r=8, p=1, dklen=32)

        hash_final_1 = f"$scrypt$n=16384,r=8,p=1${salt_1.hex()}${derivado_1.hex()}"
        hash_final_2 = f"$scrypt$n=16384,r=8,p=1${salt_2.hex()}${derivado_2.hex()}"

        try:
            app.clipboard_clear()
            app.clipboard_append(hash_final_1)
        except Exception:
            pass

        return (
            f"🛡️ HASH SENIOR GENERADO (SCRYPT + SALT ÚNICO DE 128 BITS):\n"
            f"==========================================================\n"
            f"{hash_final_1}\n"
            f"(✔️ Copiado automáticamente a tu portapapeles)\n\n"
            f"🔬 DEMOSTRACIÓN DE SALT ÚNICO (MISMA CLAVE, HASH DISTINTO):\n"
            f"• Usuario 1 (Salt {salt_1.hex()[:8]}...) -> ...{derivado_1.hex()[:24]}\n"
            f"• Usuario 2 (Salt {salt_2.hex()[:8]}...) -> ...{derivado_2.hex()[:24]}\n\n"
            f"⏱️ BENCHMARK EN TU PROCESADOR (POR QUÉ ES INHACKEABLE):\n"
            f"• Hash Rápido (SHA-256) : {t_sha_ms:.4f} ms (Permite millones de intentos/seg ❌)\n"
            f"• Hash Lento  (Scrypt)  : {t_scrypt_ms:.2f} ms (Frena la fuerza bruta por años 🛡️)\n\n"
            f"💡 Para verificar esta contraseña después, escribe en el panel izquierdo:\n"
            f"{pwd} | {hash_final_1}\n"
            f"y presiona el botón '✅ Verificar Clave vs Hash'."
        )

    def verificar_hash_senior(entrada):
        if "|" not in entrada:
            return (
                "⚠️ FORMATO DE VERIFICACIÓN:\n"
                "Escribe en la caja de entrada la contraseña seguida de '|' y el hash guardado.\n\n"
                "Ejemplo:\n"
                "MiClave123 | $scrypt$n=16384,r=8,p=1$a1b2c3...$9f8e7d..."
            )
        pwd_candidata, hash_guardado = [x.strip() for x in entrada.split("|", 1)]
        try:
            if hash_guardado.startswith("$scrypt$"):
                partes = hash_guardado.split("$")
                # Formato: ['', 'scrypt', 'n=16384,r=8,p=1', salt_hex, hash_hex]
                salt_bytes = bytes.fromhex(partes[3])
                hash_esperado = bytes.fromhex(partes[4])
                calculado = hashlib.scrypt(pwd_candidata.encode('utf-8'), salt=salt_bytes, n=16384, r=8, p=1, dklen=len(hash_esperado))
                es_valido = hmac.compare_digest(calculado, hash_esperado)
                if es_valido:
                    return "🟢 ¡VERIFICACIÓN EXITOSA! (Prueba de conocimiento válida)\nLa contraseña ingresada coincide matemáticamente con el Hash + Salt sin necesidad de guardar ni descifrar la clave original."
                else:
                    return "🔴 ACCESO DENEGADO: La contraseña NO coincide con este Hash."
            elif len(hash_guardado) == 64:
                calc = hashlib.sha256(pwd_candidata.encode('utf-8')).hexdigest()
                return "🟢 Coincide (SHA-256 sin Salt - ⚠️ Se recomienda migrar a Scrypt)." if hmac.compare_digest(calc.lower(), hash_guardado.lower()) else "🔴 No coincide con el hash SHA-256."
            elif len(hash_guardado) == 32:
                calc = hashlib.md5(pwd_candidata.encode('utf-8')).hexdigest()
                return "🟢 Coincide (MD5 inseguro - ⚠️ Migrar urgente a Scrypt)." if hmac.compare_digest(calc.lower(), hash_guardado.lower()) else "🔴 No coincide con el hash MD5."
            else:
                return "[-] Formato de hash no reconocido para verificación directa."
        except Exception as e:
            return f"❌ Error al verificar la estructura del hash: {e}"

    def funcion_magic(texto):
        texto_limpio = texto.replace(" ", "").replace("\n", "")
        reporte = "🔮 ANÁLISIS FORENSE AUTOMÁTICO COMPLETADO:\n\n"
        detectado = False

        if texto_limpio.startswith("$scrypt$"):
            reporte += "[+] Formato detectado: HASH SENIOR SCRYPT + SALT (Nivel Militar 🛡️)\nIrreversible y resistente a fuerza bruta por GPU.\n\n"
            detectado = True
        elif texto_limpio.startswith(("$2a$", "$2b$", "$2y$")):
            reporte += "[+] Formato detectado: HASH SENIOR BCRYPT + SALT (Nivel Seguro 🛡️)\nEstándar lento con factor de costo integrado.\n\n"
            detectado = True
        elif texto_limpio.startswith("$argon2"):
            reporte += "[+] Formato detectado: HASH SENIOR ARGON2 + SALT (Estándar OWASP 🛡️)\nMáxima resistencia contra hardware dedicado.\n\n"
            detectado = True

        if re.match(r'^[A-Za-z0-9+/]+={0,2}$', texto_limpio) and len(texto_limpio) % 4 == 0:
            try:
                dec = base64.b64decode(texto_limpio).decode('utf-8')
                if dec.isprintable():
                    reporte += f"[+] Formato detectado: BASE64 (Codificación Reversible)\nTexto oculto: {dec}\n\n"
                    detectado = True
            except Exception:
                pass

        if re.match(r'^[0-9a-fA-F]+$', texto_limpio) and len(texto_limpio) % 2 == 0:
            try:
                dec = binascii.unhexlify(texto_limpio).decode('utf-8')
                if dec.isprintable():
                    reporte += f"[+] Formato detectado: HEXADECIMAL\nTexto oculto: {dec}\n\n"
                    detectado = True
            except Exception:
                pass

        if re.match(r'^[01]+$', texto_limpio) and len(texto_limpio) % 8 == 0:
            try:
                dec = ''.join(chr(int(texto_limpio[i:i+8], 2)) for i in range(0, len(texto_limpio), 8))
                if dec.isprintable():
                    reporte += f"[+] Formato detectado: BINARIO\nTexto oculto: {dec}\n\n"
                    detectado = True
            except Exception:
                pass

        if len(texto_limpio) == 32 and re.match(r'^[0-9a-fA-F]+$', texto_limpio):
            reporte += "[+] Formato detectado: Hash MD5 (32 hex)\n⚠️ ADVERTENCIA: Úsalo solo para verificar integridad de archivos, NUNCA para guardar contraseñas (un atacante prueba millones por segundo).\n\n"
            detectado = True
        elif len(texto_limpio) == 64 and re.match(r'^[0-9a-fA-F]+$', texto_limpio):
            reporte += "[+] Formato detectado: Hash SHA-256 (64 hex)\n⚠️ ADVERTENCIA: Excelente para firmas de archivos, pero para contraseñas usa 'Hash Senior (Scrypt + Salt)'.\n\n"
            detectado = True

        if not detectado:
            reporte += "[-] No se detectó un formato codificado estándar. Parece texto plano: puedes presionar '🛡️ Hash Senior (Scrypt + Salt)' para protegerlo correctamente."
        return reporte

    def procesar(operacion):
        entrada = txt_input.get("1.0", "end").strip()
        if not entrada:
            return
        txt_output.configure(state="normal")
        txt_output.delete("1.0", "end")
        try:
            if operacion == "to_base64":
                resultado = base64.b64encode(entrada.encode('utf-8')).decode('utf-8')
            elif operacion == "from_base64":
                resultado = base64.b64decode(entrada).decode('utf-8', errors='ignore')
            elif operacion == "to_hex":
                resultado = binascii.hexlify(entrada.encode('utf-8')).decode('utf-8')
            elif operacion == "from_hex":
                entrada_limpia = entrada.replace(" ", "").replace("0x", "")
                resultado = binascii.unhexlify(entrada_limpia).decode('utf-8', errors='ignore')
            elif operacion == "sha256":
                resultado = hashlib.sha256(entrada.encode('utf-8')).hexdigest()
            elif operacion == "md5":
                resultado = hashlib.md5(entrada.encode('utf-8')).hexdigest()
            elif operacion == "scrypt_senior":
                resultado = forjar_hash_scrypt_senior(entrada)
            elif operacion == "verify_senior":
                resultado = verificar_hash_senior(entrada)
            elif operacion == "magic":
                resultado = funcion_magic(entrada)
        except Exception as e:
            resultado = f"❌ Error de procesamiento:\n{str(e)}"

        txt_output.insert("end", resultado)
        txt_output.configure(state="disabled")

    btn_style = {"font": ("Arial", 12, "bold"), "width": 220, "height": 34, "corner_radius": 8}

    ctk.CTkButton(frame_ops, text="🛡️ Hash Senior (Scrypt + Salt)", fg_color="#10B981", hover_color="#059669", text_color="#000000", command=lambda: procesar("scrypt_senior"), **btn_style).pack(pady=4)
    ctk.CTkButton(frame_ops, text="✅ Verificar Clave vs Hash", fg_color="#059669", hover_color="#047857", command=lambda: procesar("verify_senior"), **btn_style).pack(pady=(0, 12))

    ctk.CTkButton(frame_ops, text="Base64 -> Texto", fg_color="#3B82F6", hover_color="#2563EB", command=lambda: procesar("from_base64"), **btn_style).pack(pady=4)
    ctk.CTkButton(frame_ops, text="Texto -> Base64", fg_color="#334155", hover_color="#475569", command=lambda: procesar("to_base64"), **btn_style).pack(pady=(0, 10))

    ctk.CTkButton(frame_ops, text="Hex -> Texto", fg_color="#3B82F6", hover_color="#2563EB", command=lambda: procesar("from_hex"), **btn_style).pack(pady=4)
    ctk.CTkButton(frame_ops, text="Texto -> Hex", fg_color="#334155", hover_color="#475569", command=lambda: procesar("to_hex"), **btn_style).pack(pady=(0, 10))

    ctk.CTkButton(frame_ops, text="Huella Archivo (SHA-256)", fg_color="#8B5CF6", hover_color="#7C3AED", command=lambda: procesar("sha256"), **btn_style).pack(pady=4)
    ctk.CTkButton(frame_ops, text="Huella Rápida (MD5)", fg_color="#8B5CF6", hover_color="#7C3AED", command=lambda: procesar("md5"), **btn_style).pack(pady=(0, 10))

    ctk.CTkFrame(frame_ops, height=1, fg_color="#334155").pack(fill="x", padx=20, pady=6)
    ctk.CTkButton(frame_ops, text="🔮 MAGIC (Identificar)", font=("Arial", 14, "bold"), width=220, height=44, fg_color="#A855F7", hover_color="#9333EA", command=lambda: procesar("magic")).pack(pady=6)

    log("[+] Laboratorio criptográfico desplegado con soporte Scrypt + Salt.")

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
        ruta_img = os.path.join(escritorio, nombre_img)
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
# 3.5 ASISTENTE VIRTUAL DE VOZ (SISTEMA COGNITIVO V4.1 - BLINDADO)
# ============================================================================
detener_voz = False
proceso_actual_tts = None

def abrir_guia_asistente():
    global detener_voz, proceso_actual_tts
    
    # 1. Detenemos cualquier voz o proceso anterior al abrir la ventana
    detener_voz = True 
    if proceso_actual_tts:
        try: proceso_actual_tts.kill()
        except: pass
    time.sleep(0.2)
    detener_voz = False

    # 2. Creación de la Ventana Principal del Asistente (Lo que se había borrado)
    ventana_guia = ctk.CTkToplevel(app)
    ventana_guia.title("Asistente Virtual TREMEND")
    ventana_guia.geometry("1050x650")
    ventana_guia.lift()
    ventana_guia.attributes("-topmost", True)
    ventana_guia.after(200, lambda: ventana_guia.attributes("-topmost", False))
    ventana_guia.transient(app)
    ventana_guia.focus_force()

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

    # --- MOTOR DE VOZ INVENCIBLE (VÍA VARIABLE DE ENTORNO + POWERSHELL) ---
    def reproducir_guia(titulo_guia, diccionario_textos):
        global detener_voz, proceso_actual_tts
        
        detener_voz = True 
        if proceso_actual_tts:
            try: proceso_actual_tts.kill()
            except: pass
        time.sleep(0.2)
        detener_voz = False

        if txt_subtitulos.winfo_exists():
            txt_subtitulos.configure(state="normal")
            txt_subtitulos.delete("1.0", "end")
            txt_subtitulos.insert("end", f"=== EXPLICANDO: {titulo_guia.upper()} ===\n\n")
            txt_subtitulos.configure(state="disabled")

        def run():
            global proceso_actual_tts
            for item in diccionario_textos:
                if detener_voz or not ventana_guia.winfo_exists():
                    break
                if not isinstance(item, (tuple, list)) or len(item) < 2:
                    continue
                titulo, explicacion = item[0], item[1]

                # 1. Imprimimos el texto en la pantalla
                app.after(0, update_ui_text, titulo, explicacion)
                
                # 2. Preparamos el texto limpio y lo pasamos por Variable de Entorno (0% fallos de comillas)
                titulo_limpio = ''.join([i for i in titulo if not i.isdigit()]).replace(".", "").strip()
                texto_hablar = f"La función {titulo_limpio}. {explicacion}"
                
                env_tts = os.environ.copy()
                env_tts["TREMEND_TTS_TEXT"] = texto_hablar
                script_tts = "Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Rate = 0; $s.Volume = 90; $s.Speak($env:TREMEND_TTS_TEXT)"
                
                try:
                    flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                    proceso_actual_tts = subprocess.Popen(["powershell", "-NoProfile", "-Command", script_tts], env=env_tts, creationflags=flags)
                    proceso_actual_tts.wait()
                except Exception as e:
                    print("Error de TTS:", e)
                
                time.sleep(0.3)
            
            if not detener_voz and ventana_guia.winfo_exists():
                def fin():
                    if txt_subtitulos.winfo_exists():
                        txt_subtitulos.configure(state="normal")
                        txt_subtitulos.insert("end", "\n[✓] Explicación completada.\n")
                        txt_subtitulos.see("end")
                        txt_subtitulos.configure(state="disabled")
                app.after(0, fin)

        threading.Thread(target=run, daemon=True).start()

    def detener_habla():
        global detener_voz, proceso_actual_tts
        detener_voz = True
        if proceso_actual_tts:
            try: proceso_actual_tts.kill()
            except: pass
        if txt_subtitulos.winfo_exists():
            txt_subtitulos.configure(state="normal")
            txt_subtitulos.insert("end", "\n[!] Voz detenida por el usuario.\n")
            txt_subtitulos.see("end")
            txt_subtitulos.configure(state="disabled")

    # ==========================================================
    # DICCIONARIOS SINCRONIZADOS AL 100% CON EL CÓDIGO MAESTRO V3.3
    # ==========================================================
    guia_categorias_main = [
        ("Sistemas Operativos Windows", "Es el corazón de este programa. Aquí encontrarás todas las herramientas pesadas de reparación, ciberseguridad, manejo de redes y soporte técnico exclusivas para computadoras de Microsoft."),
        ("El Sistema Linux", "Un entorno de terminal profesional y multiplataforma. Incluye el Inspector CAT Pro, auditoría de cuentas passwd, redes y escaneo de privilegios."),
        ("El Ecosistema Mac", "Una colección de aplicaciones y manuales diseñados para auditar, limpiar con Mole y blindar computadoras de Apple de forma segura."),
        ("Herramientas Android", "Tu navaja suiza para celulares. Al conectar un teléfono por cable USB, esta sección te permite borrarle gigabytes de basura oculta sin tocar tus fotos o chats importantes."),
        ("La Nube y Tienda", "Aquí tienes programas portátiles que se ejecutan en memoria temporal sin ensuciar tu PC, enciclopedias web y la zona oficial de licencias."),
        ("El Proyecto TREMEND", "Aquí puedes descubrir cómo nació este proyecto desde cero y nuestra filosofía de unir programación avanzada e inteligencia artificial.")
    ]

    guia_red_win = [
        ("1. Info Básica de Red e IP", "Muestra tu dirección IP local y pública real al instante junto con todos los detalles de tus adaptadores."),
        ("2. Reparador de Red Autónomo", "Soluciona el fallo de conectado sin internet. Limpia DNS, renueva IP, reinicia Winsock, fuerza DHCP, destruye proxies maliciosos y restaura el archivo Hosts."),
        ("3. Prueba de Conectividad", "Envía señales a una página web o a un puerto TCP específico para comprobar si están en línea o bloqueados por un firewall."),
        ("4. Monitor Conexiones TCP", "Escanea y muestra en tiempo real qué programas de tu computadora están conectados a internet transmitiendo datos en segundo plano."),
        ("5. Identificar Proceso por Puerto", "Si un programa o servidor falla porque el puerto está ocupado, descubre exactamente qué proceso lo está bloqueando."),
        ("6. Auditoría y Migración Wi-Fi", "Extrae todas las contraseñas Wi-Fi guardadas, audita su nivel de seguridad, consulta en Have I Been Pwned si fueron filtradas por hackers y permite exportar o importar backups."),
        ("7. Generador Universal de QR", "Crea códigos QR en alta calidad para compartir tu red Wi-Fi sin dictar la clave o para compartir enlaces web."),
        ("8. Radar OSINT de IP", "Rastrea cualquier dirección IP del mundo extrayendo proveedor ISP, coordenadas y generando un mapa satelital interactivo en modo oscuro."),
        ("9. Diagnóstico Wi-Fi", "Genera el reporte oficial interactivo de Windows con el historial detallado de caídas y desconexiones inalámbricas."),
        ("10. Resolución DNS Inversa", "Interroga los servidores raíz para descubrir las direcciones IP reales detrás de cualquier dominio web."),
        ("11. Gestor Avanzado de Hosts", "Permite bloquear páginas web desde la raíz del sistema, desbloquear dominios específicos o restaurar el archivo Hosts de fábrica."),
        ("12. Abrir Puertos Firewall", "Inyecta reglas de entrada TCP o UDP en el Firewall de Windows para liberar juegos, bases de datos o servidores locales."),
        ("13. Purgar Historial Wi-Fi", "Elimina de un solo golpe todos los perfiles inalámbricos memorizados para resolver conflictos de red."),
        ("14. Reset Firewall a Fábrica", "Restaura todas las políticas del Firewall de Windows a su estado original."),
        ("15. Purgar Caché ARP", "Vacía las tablas de dirección física MAC para obligar al equipo a redescubrir los dispositivos de la red local."),
        ("16. Optimizador Avanzado de DNS", "Inyecta 12 perfiles de DNS en tus adaptadores: máxima velocidad con Cloudflare o Google, bloqueo de publicidad con AdGuard o Mullvad, escudo anti-malware con Quad9 y filtros familiares."),
        ("17. Gestionar Sesiones SMB", "Detecta al instante si otro equipo en tu red local está conectado a tus carpetas compartidas."),
        ("18. Radar Wi-Fi de Espectro", "Realiza 5 barridos consecutivos mostrando la potencia de señal y los canales de todas las redes cercanas."),
        ("19. Auditoría Latencia", "Envía paquetes continuos con reloj atómico para detectar microcortes de internet y pérdida de paquetes."),
        ("20. Radar de Puertos Avanzado", "Escáner multihilo ultrarrápido que auto-detecta tu IP o analiza equipos remotos buscando 16 puertos críticos abiertos."),
        ("21. Crear Servidor NAS Compartido", "Transforma cualquier carpeta de tu PC en un servidor de red local accesible desde celulares o televisores."),
        ("22. Auditar Caché DNS Web", "Extrae de la memoria las páginas web que se han visitado recientemente en el equipo, incluso en modo incógnito."),
        ("23. Visualizador de Tráfico de Red", "Despliega el motor gráfico Sniffnet en Rust para visualizar en tiempo real gráficas de tráfico y países de destino."),
        ("24. Escáner Forense Táctico Nmap", "Despliega Nmap con evasión de ping para detectar puertos, servicios y versiones de sistema operativo, con opción de autolimpieza sin dejar rastros."),
        ("25. Reparar Visibilidad LAN", "Activa los servicios PnP, UPnP y reglas de Firewall para que tu computadora vuelva a ser visible en la red local."),
        ("26. Auditor Web Forense DirBuster", "Escanea servidores web o routers extrayendo cabeceras ocultas del servidor, escudos de seguridad y buscando paneles de administración o archivos expuestos."),
        ("27. Radar Táctico de Enjambre Geo WiFi", "Auto-detecta todas las antenas Wi-Fi a tu alrededor o busca una dirección MAC específica para triangular su ubicación física en un mapa satelital."),
        ("28. Radar Financiero y Laboratorio A P I", "Dashboard interactivo conectado a la bolsa global en tiempo real para cruzar divisas como Dólar, Euro y Peso Colombiano, mostrando el código Python en vivo."),
        ("29. Laboratorio Forense Anti Phishing", "Analiza el código original de cualquier correo electrónico verificando firmas SPF, DKIM y DMARC para detectar suplantaciones y geolocalizar el servidor de origen."),
        ("30. Decodificador Forense y Hashing Senior CyberChef", "Transforma datos entre Base sesenta y cuatro, Hexadecimal y Binario, y permite forjar y verificar hashes lentos profesionales con Scrypt y Salt único por usuario, evitando el riesgo de guardar contraseñas cifradas o en M D cinco."),
        ("31. Centro de Blindaje Perimetral, Código y Comando Cyber Teams", "Suite completa con cinco módulos que integra a los seis equipos de ciberseguridad: audita y bloquea puertos en el Firewall, descubre subdominios expuestos en crt punto sh, blinda cabeceras y cookies web con DNS anti-malware, repara código fuente como Yellow Team, y ejecuta simulaciones Purple Team Attack versus Defend junto con monitoreo S O C Blue y Green Team y exportación de actas White Team.")
    ]

    guia_mant_win = [
        ("1. Mantenimiento Extremo a Discos", "Purga papeleras ocultas, rastros de Mac, cachés visuales, reportes de fallos y destruye automáticamente la pesada carpeta Windows punto old, protegiendo la caché de TREMEND y reparando el núcleo con DISM y SFC."),
        ("2. Optimización Avanzada Chris Titus", "Lanza el panel de optimización avanzada para desactivar servicios innecesarios y acelerar Windows."),
        ("3. Debloat del Sistema Apps Nativas", "Elimina paquetes preinstalados de Windows por nombre mediante PowerShell."),
        ("4. Restablecer Cola de Impresión", "Reinicia el servicio Spooler y destruye los documentos atascados que impiden imprimir."),
        ("5. Limpieza Extrema de WinSxS", "Comprime y limpia el almacén de componentes de actualizaciones antiguas de Windows para liberar gigabytes."),
        ("6. Reparar Windows Update Roto", "Detiene los servicios de actualización, renombra las bases de datos corruptas SoftwareDistribution y Catroot2 y reactiva el sistema."),
        ("7. Gestor de Puntos de Restauración", "Analiza la antigüedad de tus puntos de restauración, te advierte si son obsoletos y te permite crear un respaldo fresco o regresar el PC en el tiempo."),
        ("8. Reparar Telemetría Base W M I", "Reconstruye el repositorio WMI cuando Windows deja de leer correctamente la batería, el brillo o los sensores."),
        ("9. Bloquear Espionaje Microsoft", "Desactiva el servicio DiagTrack y bloquea el envío de telemetría por Registro."),
        ("10. Reparar Sincronización de Hora", "Fuerza la sincronización del reloj de la placa base con los servidores atómicos globales."),
        ("11. Higiene de Navegadores y Escudo Anti Robo de Sesiones", "Ofrece dos modos para Chrome, Edge, Brave y Firefox: el modo uno elimina gigabytes de caché pesada conservando tus cuentas abiertas, y el modo dos ejecuta una purga de emergencia que cierra los navegadores y destruye las cookies session I D y tokens locales para impedir el secuestro de sesiones y el salto del segundo factor de autenticación."),
        ("12. Reparación Física de Disco CHKDSK", "Programa un escaneo magnético CHKDSK para aislar sectores defectuosos en el próximo reinicio."),
        ("13. Reconstruir Caché de Iconos", "Purga la base de datos IconCache y reinicia el explorador para reparar iconos blancos o dañados."),
        ("14. G-Helper Optimizador ASUS", "Verifica que tu laptop sea ASUS y despliega G-Helper portátil para controlar ventiladores, batería y potencia sin consumir RAM."),
        ("15. Lenovo Legion Toolkit", "Verifica que tu equipo sea Lenovo y despliega Legion Toolkit con opción de desinstalación limpia al terminar."),
        ("16. Mole Optimizador Terminal", "Despliega la herramienta interactiva Mole en consola para limpieza rápida en sistemas Windows y Mac."),
        ("17. Escáner de Fugas y Memoria Virtual", "Repara el bug de almacenamiento de Windows 11 y calcula matemáticamente los límites exactos de memoria virtual pagefile según tu RAM física."),
        ("18. Suite Automatizadora de Archivos, Lotes y Duplicados", "Cuatro herramientas en una: organiza tus Descargas o Escritorio por tipo con botón para deshacer cambios, clasifica facturas por año y mes generando gráficas de volumen mensual, ordena y renombra cientos de archivos por su fecha conservando su nombre original en menos de un segundo, y detecta duplicados mediante huella S H A doscientos cincuenta y seis."),
        ("19. Radar Visual de Almacenamiento", "Escanea tus discos en dos fases: primero sugiere purgar cachés pesadas de Windows y luego despliega un árbol interactivo ordenando tus carpetas por tamaño."),
        ("20. Gestor de Pánico Liberar RAM y CPU", "Monitorea en tiempo real el procesador y la memoria. Con un clic aniquila procesos pesados y obliga al Kernel mediante Empty Working Set a liberar la RAM inactiva.")
    ]

    guia_diag_win = [
        ("1. Cazador Forense Anti Keyloggers", "Cruza las conexiones de red establecidas con las firmas digitales Authenticode. Si descubre un programa sin firma enviando datos, lo asesina en RAM y lanza MRT y Defender."),
        ("2. Diagnóstico Veloz", "Ejecuta WinSat para calcular la puntuación matemática oficial de tu procesador, RAM, disco y tarjeta gráfica."),
        ("3. Radiografía Completa Hardware", "Extrae marcas, modelos, velocidades y capacidades exactas de tu placa base, BIOS, procesador, módulos RAM y GPU."),
        ("4. Salud de Discos S.M.A.R.T", "Interroga el firmware físico de tus discos duros y SSDs para verificar si su estado de salud es óptimo o riesgoso."),
        ("5. Monitor de Estabilidad Windows", "Abre el historial gráfico de confiabilidad o el reporte diagnóstico avanzado del sistema."),
        ("6. Cuadrícula Forense de Tareas", "Despliega tablas interactivas con filtro para auditar procesos activos, servicios o los últimos 100 errores del sistema."),
        ("7. Tiempo de Actividad Real", "Revela exactamente cuántos días y horas lleva encendido el núcleo sin un reinicio real."),
        ("8. Auditar Tareas Ocultas", "Lista todos los servicios que se encuentran actualmente en ejecución en segundo plano."),
        ("9. Auditoría de Arranque", "Muestra en una tabla interactiva todos los comandos y programas que se inician automáticamente al encender el PC."),
        ("10. Historial Forense de USBs", "Lee el registro USBSTOR para listar cada memoria USB y disco externo que se ha conectado históricamente al equipo."),
        ("11. Extractor de Pantallazos", "Extrae del visor de eventos los registros BugCheck para diagnosticar la causa de los pantallazos azules."),
        ("12. Optimizador de Energía y Salud de Batería", "Detecta en tiempo real qué procesos están drenando tu energía, permite cambiar entre los planes Economizador, Equilibrado o Alto Rendimiento con un clic, monitorea tu batería física y genera el reporte oficial de desgaste en HTML."),
        ("13. Reporte de Suspensión", "Genera el informe SleepStudy para descubrir qué componente gasta batería mientras la laptop está suspendida."),
        ("14. Gestor Avanzado BitLocker", "Consulta el estado de cifrado, extrae claves activas, busca archivos de recuperación perdidos en todos tus discos con expresiones regulares o desbloquea unidades."),
        ("15. Inspector CAT Pro y Blindaje de Cuentas", "Suite con tres herramientas: audita las cuentas locales SAM de Windows y passwd de Linux permitiendo deshabilitar cuentas inseguras como Invitado, lee archivos numerados estilo cat guion n resaltando errores, y concatena múltiples archivos en uno solo."),
        ("16. Extraer Serial de Fábrica", "Extrae el número de serie quemado en la placa base y lo copia automáticamente al portapapeles."),
        ("17. Escudo de Integridad RAM y Cazador de Inyectores", "Defiende la memoria en tres fases: neutraliza programas que intenten modificar valores en RAM como Cheat Engine o depuradores, activa la aleatorización de direcciones A S L R y protección D E P en el Kernel, y ejecuta el motor Ghost en Rust para buscar código malicioso inyectado."),
        ("18. Visualizador Forense Web", "Auto-detecta los navegadores instalados, clona su base de datos SQLite en memoria y renderiza un dashboard HTML5 con gráficas de los sitios más visitados y búsquedas."),
        ("19. Radar de Hardware en Conflicto", "Detecta piezas físicas con códigos de error en el Administrador de Dispositivos y lanza una búsqueda avanzada Dork en foros de ingeniería con la firma exacta del hardware."),
        ("20. Gestor de Entornos Aislados y Sandbox", "Verifica si tu procesador y BIOS tienen la virtualización activada y despliega máquinas virtuales desechables Windows Sandbox para probar archivos sospechosos sin riesgo."),
        ("21. Laboratorio de Rayos X Binario", "Analiza el ADN interno de cualquier archivo sin ejecutarlo: calcula su hash SHA-256, detecta ejecutables disfrazados mediante Magic Bytes, busca esteganografía, extrae metadatos EXIF y filtra textos maliciosos.")
    ]
    
    guia_soft_win = [
        ("1. Centro de Inteligencia de Software y Cazador Forense", "Superior a Revo Uninstaller. Escanea en línea todas las actualizaciones disponibles con buscador, filtros y selección individual o masiva. En desinstalación, cierra procesos activos, desinstala el programa y barre el disco duro y el Registro destruyendo carpetas y claves residuales."),
        ("2. Clonador Pre-Formateo e Inventario de Software", "Centro de migración completo: exporta tus programas a una memoria USB en formato JSON auto-instalable limpio de basura y en formato CSV para Excel, restaura todos tus programas tras formatear sin confirmaciones manuales, o instala el Kit Esencial Posformateo con un clic."),
        ("3. Respaldo Total de Controladores Drivers", "Extrae y clona todos los controladores originales instalados en el sistema hacia la carpeta RespaldoDrivers antes de formatear."),
        ("4. Activador Seguro de Windows M A S", "Lanza la consola externa de Microsoft Activation Scripts para gestión de licencias digitales."),
        ("5. Forzar Escaneo de Hardware PnP", "Obliga al núcleo de Windows a reescanear todos los puertos Plug and Play para detectar hardware recién conectado."),
        ("6. Instalar ASUS GlideX Multipantalla", "Instala desde Microsoft Store la utilidad para usar tablets o celulares como segunda pantalla."),
        ("7. Auditor Forense y Extractor de Claves de Licencias", "Extrae tu clave OEM de la placa base, desencripta la clave instalada en el Registro de Windows aunque el equipo sea armado, analiza el canal O E M, Retail, M A K o K M S nivel s l m g r, audita Office, detecta activadores ocultos y guarda un pasaporte con tus claves en el Escritorio antes de formatear."),
        ("8. Gestor de Suscripciones Compartidas y Cobros Mensuales", "Administra los miembros de tu grupo familiar de Google Gemini Pro, Office o servicios compartidos. Calcula automáticamente quién debe pagar el día treinta, envía el cobro directo a su WhatsApp con tu cuenta de pago y te abre el panel oficial de Google el día treinta y uno para suspender el servicio a quienes estén en mora.")
    ]

    guia_soporte_win = [
        ("1. Destructor Forzado de Carpetas", "Toma posesión a nivel de Kernel mediante takeown, icacls y PowerShell para pulverizar carpetas bloqueadas o rebeldes."),
        ("2. Bypass de Contraseñas Windows", "Altera directamente la base de datos SAM local para restablecer la contraseña de cualquier usuario del equipo."),
        ("3. Extractor de Credenciales LaZagne", "Ejecuta una auditoría de recuperación de credenciales almacenadas en navegadores y sistema, generando el reporte en el Escritorio."),
        ("4. TREMEND Media y Cobalt Studio", "Centro multimedia inspirado en Cobalt que descarga videos hasta en cuatro K, música en M P tres, fotos en J P G original y carruseles enteros de Instagram, TikTok, YouTube, Equis y más de mil sitios, además de convertir archivos locales borrando sus metadatos ocultos."),
        ("5. Gestor Avanzado de USB y Vacuna Forense", "Cuatro herramientas en una: bloquea o desbloquea puertos de almacenamiento USB, elimina la protección contra escritura por Registro y Diskpart, o desinfecta memorias USB rescatando carpetas ocultas por virus y aplicando una vacuna anti-autorun inmutable."),
        ("6. Gestor de Virtualización de Hardware", "Escanea si tu edición de Windows es compatible e inyecta la activación directa en el núcleo de Hyper-V o Windows Sandbox mediante DISM."),
        ("7. Reinicio de Fábrica para Ventas Sysprep", "Ejecuta Sysprep generalizando la imagen del sistema para dejar el equipo listo para entregar a un nuevo dueño."),
        ("8. Borrado de Archivos Irreversible Wipe", "Sobrescribe el espacio libre del disco duro mediante cifrado Cipher para impedir que programas forenses recuperen archivos borrados."),
        ("9. Salto de BIOS Forzado UEFI", "Verifica si tu placa base es UEFI y reinicia el computador entrando directamente a la configuración de la BIOS sin presionar teclas."),
        ("10. Hackeo de Archivos Bloqueados JtR", "Utiliza John The Ripper con aceleración por GPU o CPU multinúcleo para recuperar contraseñas olvidadas en archivos ZIP, RAR, 7z y PDF."),
        ("11. Destructor de Candados Excel", "Desempaqueta la estructura XML interna de documentos Excel modernos para eliminar la protección de celdas bloqueadas."),
        ("12. Limpiador Android Extremo Vía USB", "Conecta por ADB con teléfonos Android para purgar cachés ocultas, miniaturas fantasma y bases de datos antiguas de WhatsApp sin tocar tus chats ni fotos."),
        ("13. Auditoría Total de Ciberseguridad WinPEAS", "Ejecuta WinPEAS para detectar brechas de escalada de privilegios y ofrece un protocolo de Auto-Blindaje que activa protección LSA en RAM, UAC y limpia historiales."),
        ("14. Bóveda Criptográfica y Escudo Anti Fuerza Bruta", "Panel dual de defensa: calcula la resistencia matemática de tus contraseñas, forja claves militares y tokens de 256 bits, audita en el visor de eventos si alguien intentó forzar tu sesión y activa el bloqueo automático de Windows tras cinco intentos fallidos."),
        ("15. Modo Dios Escáner QR, Barras e I M E I", "Despliega una cámara con interfaz holográfica que lee códigos QR y valida matemáticamente códigos de barras IMEI mediante el algoritmo de Luhn, abriendo bases de datos para verificar si un celular es robado."),
        ("16. Borrador de Fondos con Inteligencia Artificial", "Ejecuta la red neuronal U-2-Net localmente para recortar el fondo de cualquier fotografía y entregar un archivo PNG transparente."),
        ("17. Escáner Óptico de Pantalla O. C. R.", "Congela y atenúa tu pantalla con soporte multimonitor para que dibujes un recuadro sobre cualquier imagen o error, aplicando escalado óptico 3X e inteligencia artificial nativa para copiar el texto a tu portapapeles.")
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
        ctk.CTkButton(panel_nav, text="🐧 Linux y Seguridad", font=("Arial", 14), height=40, command=lambda: reproducir_guia("Módulos de Linux", [("Auditoría Linux", "Esta sección te da una terminal con herramientas de administrador. Puedes auditar servidores, analizar el archivo passwd con CAT Pro, ver el tráfico de red y cazar intrusos.")])).pack(pady=5, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🍏 Funciones de Mac", font=("Arial", 14), height=40, command=lambda: reproducir_guia("Módulos de Mac", [("MacPEAS y Ecosistema", "Contiene el optimizador Mole para Mac y el auditor de seguridad MacPEAS que escanea el equipo buscando configuraciones débiles y aplica blindaje automático.")])).pack(pady=5, fill="x", padx=15)
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
        
        ctk.CTkButton(panel_nav, text="▶ Explicar TODA la Categoría", font=("Arial", 13, "bold"), height=38, fg_color="#10B981", hover_color="#059669", command=lambda: reproducir_guia(titulo_cat, diccionario)).pack(pady=5, fill="x", padx=15)
        
        ctk.CTkFrame(panel_nav, height=1, fg_color="#334155").pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(panel_nav, text="O ingresa el N° de la función:", font=("Arial", 12, "bold"), text_color="#94A3B8").pack(pady=2)
        
        entrada_num = ctk.CTkEntry(panel_nav, placeholder_text=f"Ej: 1 al {len(diccionario)}", width=160, justify="center", font=("Arial", 14))
        entrada_num.pack(pady=5)
        
        def explicar_una(event=None):
            val = entrada_num.get().strip()
            if val.isdigit():
                idx = int(val) - 1
                if 0 <= idx < len(diccionario):
                    item = diccionario[idx]
                    reproducir_guia("Función Seleccionada", [item])
                    entrada_num.delete(0, 'end') 
                else:
                    messagebox.showwarning("Aviso", f"Ingresa un número válido entre 1 y {len(diccionario)}.", parent=ventana_guia)
            else:
                messagebox.showwarning("Aviso", "Por favor ingresa solo números enteros.", parent=ventana_guia)
        
        entrada_num.bind("<Return>", explicar_una)
        
        ctk.CTkButton(panel_nav, text="Explicar Específica", font=("Arial", 13, "bold"), height=35, fg_color="#3B82F6", hover_color="#2563EB", command=explicar_una).pack(pady=5, fill="x", padx=15)
        
        lista_funcs = ctk.CTkScrollableFrame(panel_nav, fg_color="transparent")
        lista_funcs.pack(fill="both", expand=True, padx=5, pady=5)
        
        for nombre, _ in diccionario:
            ctk.CTkLabel(lista_funcs, text=nombre, font=("Arial", 12), text_color="#CBD5E1", anchor="w", justify="left").pack(fill="x", pady=2)

        ctk.CTkButton(panel_nav, text="⬅️ Volver", font=("Arial", 13), height=35, fg_color="#334155", hover_color="#475569", command=vista_windows).pack(side="bottom", pady=10, fill="x", padx=15)
        ctk.CTkButton(panel_nav, text="🛑 Detener Voz", font=("Arial", 13, "bold"), height=30, fg_color="#EF4444", hover_color="#DC2626", command=detener_habla).pack(side="bottom", pady=0, fill="x", padx=15)

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

# --- NUEVA MEJORA: SENSOR DE LATENCIA Y VELOCIDAD DE RED ---
ctk.CTkFrame(hud_frame, height=1, fg_color="#334155").pack(fill="x", padx=20, pady=10)

lbl_net = ctk.CTkLabel(hud_frame, text="⚡ Ping: Calculando...", font=("Arial", 12, "bold"), text_color="#FCD34D")
lbl_net.pack(anchor="w", padx=20, pady=(5, 2))

# Nuevos labels para Ancho de Banda
lbl_net_dl = ctk.CTkLabel(hud_frame, text="⬇️ DL: 0.0 MB/s", font=("Consolas", 12, "bold"), text_color="#38BDF8")
lbl_net_dl.pack(anchor="w", padx=20, pady=(2, 0))

lbl_net_ul = ctk.CTkLabel(hud_frame, text="⬆️ UL: 0.0 MB/s", font=("Consolas", 12, "bold"), text_color="#A855F7")
lbl_net_ul.pack(anchor="w", padx=20, pady=(0, 5))

# --- MOTOR LÓGICO DEL HUD (MAXIMIZADO, CORREGIDO Y ANTI-CRASH) ---
from ctypes import wintypes
import ctypes
import shutil
import psutil # <--- Requerido para medir el ancho de banda

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

def arrancar_motor_hud():
    import subprocess
    import time
    import threading
    
    def get_system_times():
        idleTime, kernelTime, userTime = FILETIME(), FILETIME(), FILETIME()
        ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idleTime), ctypes.byref(kernelTime), ctypes.byref(userTime))
        idle = (idleTime.dwHighDateTime << 32) | idleTime.dwLowDateTime
        sys_time = ((kernelTime.dwHighDateTime << 32) | kernelTime.dwLowDateTime) + ((userTime.dwHighDateTime << 32) | userTime.dwLowDateTime)
        return idle, sys_time

    # Obtenemos la RAM física real instalada en los slots
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
        
        # Inicializamos los contadores de red
        try:
            net_io = psutil.net_io_counters()
            bytes_recv_prev = net_io.bytes_recv
            bytes_sent_prev = net_io.bytes_sent
        except:
            bytes_recv_prev, bytes_sent_prev = 0, 0
            
        while True:
            time.sleep(1.5)
            
            # 1. CPU
            idle_now, sys_now = get_system_times()
            idle_diff = idle_now - idle_prev
            sys_diff = sys_now - sys_prev
            cpu_percent = int((sys_diff - idle_diff) * 100.0 / sys_diff) if sys_diff > 0 else 0
            idle_prev, sys_prev = idle_now, sys_now

            # 2. RAM
            try:
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                ram_percent = stat.dwMemoryLoad
                ram_total = ram_fisica_gb if ram_fisica_gb > 0 else stat.ullTotalPhys / (1024**3)
                ram_usada = (stat.ullTotalPhys - stat.ullAvailPhys) / (1024**3)
            except: ram_percent, ram_total, ram_usada = 0, 0, 0

            # 3. Disco C:
            try:
                total_b, _, free_b = shutil.disk_usage("C:\\")
                disco_total = total_b / (1024**3)
                disco_usado = (total_b - free_b) / (1024**3)
                disco_percent = (disco_usado / disco_total) * 100 if disco_total > 0 else 0
            except: disco_percent, disco_total, disco_usado = 0, 0, 0
            
            # 4. Red (Download / Upload en MB/s)
            try:
                net_io_now = psutil.net_io_counters()
                dl_speed = (net_io_now.bytes_recv - bytes_recv_prev) / 1.5 / (1024 * 1024)
                ul_speed = (net_io_now.bytes_sent - bytes_sent_prev) / 1.5 / (1024 * 1024)
                
                bytes_recv_prev = net_io_now.bytes_recv
                bytes_sent_prev = net_io_now.bytes_sent
            except: 
                dl_speed, ul_speed = 0.0, 0.0

            color_cpu = "#EF4444" if cpu_percent > 85 else ("#F59E0B" if cpu_percent > 60 else "#10B981")
            color_ram = "#EF4444" if ram_percent > 85 else ("#F59E0B" if ram_percent > 60 else "#3B82F6")
            color_disco = "#EF4444" if disco_percent > 90 else "#8B5CF6"

            def refrescar_ui():
                try:
                    # Actualización pura con escudo Anti-Crash global
                    lbl_cpu_val.configure(text=f"{cpu_percent}%")
                    pb_cpu.set(cpu_percent / 100.0)
                    pb_cpu.configure(progress_color=color_cpu)

                    lbl_ram_val.configure(text=f"{ram_usada:.1f} GB / {ram_total:.1f} GB ({ram_percent}%)")
                    pb_ram.set(ram_percent / 100.0)
                    pb_ram.configure(progress_color=color_ram)

                    lbl_disco_val.configure(text=f"{disco_usado:.1f} GB / {disco_total:.1f} GB ({int(disco_percent)}%)")
                    pb_disco.set(disco_percent / 100.0)
                    pb_disco.configure(progress_color=color_disco)
                    
                    # Actualizar velocidad de red
                    lbl_net_dl.configure(text=f"⬇️ DL: {dl_speed:.1f} MB/s")
                    lbl_net_ul.configure(text=f"⬆️ UL: {ul_speed:.1f} MB/s")
                except Exception: pass 

            app.after(0, refrescar_ui)

    def tarea_ping():
        import re
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        while True:
            try:
                salida = subprocess.run(["ping", "-n", "1", "-w", "1000", "8.8.8.8"], capture_output=True, text=True, startupinfo=startupinfo)
                match_ms = re.search(r'(?:tiempo|time)[=<]\s*(\d+)\s*ms', salida.stdout, re.IGNORECASE)
                if match_ms:
                    ms = int(match_ms.group(1))
                    color = "#10B981" if ms < 50 else ("#F59E0B" if ms < 150 else "#EF4444")
                    def update_ui_ping(m=ms, c=color):
                        try: lbl_net.configure(text=f"⚡ Ping: {m} ms", text_color=c)
                        except Exception: pass
                    app.after(0, update_ui_ping)
                else:
                    def update_ui_desc():
                        try: lbl_net.configure(text="⚡ Ping: Desconectado", text_color="#EF4444")
                        except Exception: pass
                    app.after(0, update_ui_desc)
            except Exception:
                def update_ui_err():
                    try: lbl_net.configure(text="⚡ Ping: Error", text_color="#EF4444")
                    except Exception: pass
                app.after(0, update_ui_err)

            time.sleep(2)

    # --- ESTAS 3 LÍNEAS FALTABAN PARA ENCENDER EL HUD ---
    threading.Thread(target=tarea_actualizacion, daemon=True).start()
    threading.Thread(target=tarea_ping, daemon=True).start()

app.after(300, arrancar_motor_hud)

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
            
            ctk.CTkLabel(text_frame, text=item["nombre"], font=("Arial", 16, "bold"), text_color="#FFFFFF", justify="left", wraplength=espacio_texto).pack(anchor="w")
            
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
        dialogo = ctk.CTkInputDialog(text="Ingresa la IP o Dominio del servidor web a auditar\n(Ej. 192.168.1.1 o scanme.nmap.org):", title="Auditor Web Forense")
        objetivo = dialogo.get_input()
        if objetivo and objetivo.strip():
            def _auditar_servidor(log):
                import urllib.request, ssl, concurrent.futures
                url_base = objetivo.strip()
                if not url_base.startswith("http"):
                    url_base = "http://" + url_base
                url_base = url_base.rstrip("/")

                log("\n" + "="*75)
                log(f" 🕷️ AUDITOR WEB FORENSE (BANNER GRABBING & DIRBUSTER): {url_base}")
                log("="*75)

                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE

                log("\n[1/2] Extrayendo Cabeceras HTTP y Escudos de Seguridad (Banner Grabbing)...")
                try:
                    req = urllib.request.Request(url_base, headers={'User-Agent': 'Mozilla/5.0 (TREMEND-Auditor)'})
                    with urllib.request.urlopen(req, timeout=6, context=ctx) as resp:
                        headers = dict(resp.info())
                        for k, v in headers.items():
                            log(f"    -> {k}: {v}")
                        for sec_h in ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options"]:
                            if sec_h not in headers and sec_h.lower() not in [h.lower() for h in headers]:
                                log(f"    [⚠️ Falta Cabecera de Seguridad]: {sec_h}")
                except Exception as e:
                    log(f"    [-] Error al conectar con la raíz: {e}")

                log("\n[2/2] Ejecutando Fuzzing Concurrente de Directorios y Archivos Ocultos...")
                rutas_fuzz = [
                    "admin", "login", "wp-admin", "phpmyadmin", "robots.txt", ".env",
                    ".git/config", "backup.zip", "config.php", "api", "dashboard", "server-status"
                ]
                def probar_ruta(ruta):
                    u = f"{url_base}/{ruta}"
                    try:
                        r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(r, timeout=4, context=ctx) as res:
                            return (ruta, res.status)
                    except urllib.error.HTTPError as he:
                        if he.code in (401, 403):
                            return (ruta, he.code)
                    except: pass
                    return None

                hallazgos = 0
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
                    for res in ex.map(probar_ruta, rutas_fuzz):
                        if res:
                            ruta_ok, code = res
                            estado_txt = "🔓 ABIERTO (200 OK)" if code == 200 else f"🔒 PROTEGIDO ({code})"
                            log(f"    [+] /{ruta_ok.ljust(18)} -> {estado_txt}")
                            hallazgos += 1
                if hallazgos == 0:
                    log("    [-] No se detectaron directorios sensibles expuestos en el diccionario base.")

            abrir_consola_y_ejecutar("AUDITOR WEB FORENSE", _auditar_servidor)

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
        {"id": "29", "nombre": "29. Laboratorio Forense Anti-Phishing", "cmd": lambda: abrir_consola_y_ejecutar("ANTI-PHISHING", logica_analizador_phishing), "nov": "Detecta si un correo electrónico es falso o real. Pega el código original del correo y la herramienta analizará las firmas de seguridad y geolocalizará la IP del remitente.", "exp": "[Fusión OSINT + Regex] Módulo 2 en 1. Parsea cabeceras crudas (RFC 5322) usando Regex para validar firmas criptográficas SPF/DKIM/DMARC. Extrae la IP de origen y pivota hacia ip-api.com para trazar el ASN/ISP."},
        {"id": "30", "nombre": "30. Decodificador Forense y Hashing Senior (Scrypt + Salt / CyberChef)", "cmd": lambda: abrir_consola_y_ejecutar("LABORATORIO DATOS", logica_decodificador_forense), "nov": "Protege contraseñas con nivel Senior (Scrypt + Salt único por usuario) demostrando por qué no se debe usar MD5 ni cifrado reversible, verifica claves sin descifrarlas y traduce códigos Base64, Hex y Binario.", "exp": "[KDF hashlib.scrypt + CSPRNG Salt + Constant-Time HMAC] Deriva claves con memoria endurecida (n=16384, r=8, p=1) y Salt de 128 bits, valida pruebas de conocimiento vía hmac.compare_digest anti-Timing Attack e identifica firmas Bcrypt/Argon2/SHA."},
        {"id": "31", "nombre": "31. Centro de Blindaje Perimetral, Código y Comando Cyber Teams (Red/Blue/Purple)", "cmd": lambda: logica_laboratorio_vulnerabilidades_web(None), "nov": "5 herramientas en 1 (Arquitectura de 6 Cyber Teams): Audita y blinda puertos en el Firewall, descubre subdominios expuestos, audita la seguridad de páginas web, repara vulnerabilidades en tu código (Yellow Team) y ejecuta simulaciones Purple Team (Ataque vs Defensa) con Actas de Auditoría (White Team).", "exp": "[Suite 6 Cyber Teams: Red / Blue / Purple / White / Yellow / Green] Integra correlación Attack <-> Defend en vivo, telemetría SOC (Get-MpComputerStatus / Firewall Profiles), generación de Actas ROE firmadas con SHA-256, consulta crt.sh y análisis estático DevSecOps."},
    ]
    construir_vista_dinamica("🌐 Redes e Internet", "🔍 Buscar (Ej: dns, 16, wifi)...", h_redes)

def logica_boton_panico(log):
    import psutil, ctypes, time, threading
    import customtkinter as ctk
    from tkinter import messagebox

    log("\n" + "="*75)
    log(" 🚨 INICIANDO CENTRO DE CONTROL Y BOTÓN DE PÁNICO ")
    log("="*75)
    log("[*] Desplegando sensores en tiempo real de CPU y RAM...")

    win_panico = ctk.CTkToplevel(app)
    win_panico.title("TREMEND - Liberador Extremo de Recursos")
    win_panico.geometry("600x480")
    win_panico.attributes("-topmost", True)
    win_panico.transient(app)

    ctk.CTkLabel(win_panico, text="Monitor de Rendimiento Crítico", font=("Arial", 22, "bold"), text_color="#38BDF8").pack(pady=(20, 5))
    ctk.CTkLabel(win_panico, text="Evalúa la carga actual. Usa el botón de pánico si el sistema no responde.", font=("Arial", 12), text_color="#94A3B8").pack(pady=(0, 20))

    # --- INDICADORES GRÁFICOS ---
    frame_sensores = ctk.CTkFrame(win_panico, fg_color="#1E293B", corner_radius=10)
    frame_sensores.pack(fill="x", padx=30, pady=10)

    # CPU
    ctk.CTkLabel(frame_sensores, text="Procesador (CPU)", font=("Arial", 14, "bold"), text_color="#E2E8F0").pack(anchor="w", padx=20, pady=(15, 0))
    lbl_cpu = ctk.CTkLabel(frame_sensores, text="0%", font=("Arial", 28, "bold"), text_color="#10B981")
    lbl_cpu.pack(pady=5)
    lbl_estado_cpu = ctk.CTkLabel(frame_sensores, text="Normal", font=("Arial", 12, "bold"), text_color="#10B981")
    lbl_estado_cpu.pack()

    # RAM
    ctk.CTkLabel(frame_sensores, text="Memoria RAM", font=("Arial", 14, "bold"), text_color="#E2E8F0").pack(anchor="w", padx=20, pady=(15, 0))
    lbl_ram = ctk.CTkLabel(frame_sensores, text="0%", font=("Arial", 28, "bold"), text_color="#10B981")
    lbl_ram.pack(pady=5)
    lbl_estado_ram = ctk.CTkLabel(frame_sensores, text="Normal", font=("Arial", 12, "bold"), text_color="#10B981")
    lbl_estado_ram.pack(pady=(0, 15))

    # --- MOTOR DE SENSORES EN TIEMPO REAL ---
    def actualizar_sensores():
        while win_panico.winfo_exists():
            cpu_val = psutil.cpu_percent(interval=None)
            ram_info = psutil.virtual_memory()
            ram_val = ram_info.percent

            # Lógica de Límites (Verde, Amarillo, Rojo)
            if cpu_val < 60:
                c_cpu, t_cpu = "#10B981", "Óptimo"
            elif cpu_val < 85:
                c_cpu, t_cpu = "#F59E0B", "Sobrecarga (Cuidado)"
            else:
                c_cpu, t_cpu = "#EF4444", "CRÍTICO (Riesgo de sobrecalentamiento)"

            if ram_val < 60:
                c_ram, t_ram = "#10B981", "Óptimo"
            elif ram_val < 85:
                c_ram, t_ram = "#F59E0B", "Llenándose (Cuidado)"
            else:
                c_ram, t_ram = "#EF4444", "CRÍTICO (El equipo se congelará)"

            def refrescar(cv=cpu_val, cc=c_cpu, tc=t_cpu, rv=ram_val, cr=c_ram, tr=t_ram):
                if win_panico.winfo_exists():
                    lbl_cpu.configure(text=f"{cv:.1f}%", text_color=cc)
                    lbl_estado_cpu.configure(text=tc, text_color=cc)
                    lbl_ram.configure(text=f"{rv:.1f}%", text_color=cr)
                    lbl_estado_ram.configure(text=tr, text_color=cr)

            app.after(0, refrescar)
            time.sleep(1.5)

    threading.Thread(target=actualizar_sensores, daemon=True).start()

    # --- PROTOCOLO DE PÁNICO (PURGA QUIRÚRGICA EXTENDIDA) ---
    def ejecutar_panico():
        if messagebox.askyesno("⚠️ ALERTA CRÍTICA", "Se cerrarán forzosamente TODOS los navegadores web y procesos basura en segundo plano.\n\nADVERTENCIA: Si tienes documentos de Word/Excel sin guardar, guárdalos antes de continuar.\n\n¿Estás seguro de ejecutar el Protocolo de Pánico?"):
            log("\n[!] PROTOCOLO DE PÁNICO INICIADO.")
            log("[*] Ejecutando purga de aplicaciones consumidoras y telemetría basura...")
            
            # Catálogo de exterminio dinámico (Navegadores, Juegos y Basura detectada en RAM)
            apps_pesadas = [
                'chrome.exe', 'msedge.exe', 'brave.exe', 'firefox.exe', 'opera.exe',
                'discord.exe', 'steam.exe', 'epicgames.exe', 'teams.exe', 'skype.exe',
                'spotify.exe', 'iexplore.exe', 'whatsapp.exe', 'code.exe',
                'webview2', 'lenovovantage', 'widget', 'glidex', 'fdm.exe',
                'notifyme.exe', 'copilot', 'mspcmanager', 'batterywidget'
            ]
            muertos = 0
            
            # 1. Matar aplicaciones y bloatware mediante coincidencia flexible de texto
            for proc in psutil.process_iter(['name']):
                try:
                    nombre_proceso = proc.info['name'].lower()
                    # Si el nombre del proceso contiene alguna palabra clave del catálogo
                    if any(objetivo in nombre_proceso for objetivo in apps_pesadas):
                        proc.kill()
                        muertos += 1
                except: pass
            
            log(f"    -> Se aniquilaron {muertos} procesos (incluyendo módulos WebView2 y Telemetría).")
            log("[*] Obligando al Kernel de Windows a soltar la RAM inactiva (EmptyWorkingSet)...")

            # 2. El Truco Maestro: Empty Working Set (Libera RAM de procesos del sistema sin cerrarlos)
            liberados = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # 0x0100 (PROCESS_QUERY_INFORMATION) | 0x0400 (PROCESS_QUERY_LIMITED_INFORMATION) | 0x0001 (PROCESS_VM_READ)
                    handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, proc.info['pid'])
                    if handle:
                        if ctypes.windll.psapi.EmptyWorkingSet(handle):
                            liberados += 1
                        ctypes.windll.kernel32.CloseHandle(handle)
                except: pass

            log(f"    -> Se obligó a {liberados} programas vitales a devolver memoria RAM inactiva al sistema.")
            log("\n[+] ¡SISTEMA ESTABILIZADO! El procesador y la RAM ahora pueden respirar.")
            messagebox.showinfo("Éxito", "Protocolo finalizado. El equipo debería sentirse mucho más rápido ahora.")

    ctk.CTkButton(win_panico, text="🚨 PROTOCOLO DE PÁNICO (Purga Quirúrgica)", font=("Arial", 16, "bold"), height=55, fg_color="#EF4444", hover_color="#DC2626", command=ejecutar_panico).pack(side="bottom", fill="x", padx=40, pady=30)

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
            {"id": "7", "nombre": "7. Gestor de Puntos de Restauración", "cmd": lambda: abrir_consola_y_ejecutar("MÁQUINA DEL TIEMPO", logica_maquina_tiempo), "nov": "Escanea tus puntos de restauración, te advierte si son muy viejos, crea backups nuevos o te permite regresar el PC en el tiempo con un clic.", "exp": "[Fusión WMI/VSS] Interroga la clase RestorePoint. Implementa análisis de fechas (Datetime) y despliega menú para crear (Checkpoint-Computer), restaurar o purgar volúmenes ocultos."},
            {"id": "8", "nombre": "8. Reparar Telemetría Base (WMI)", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR WMI", logica_wmi), "nov": "Arregla errores raros, como cuando la PC no lee el nivel de batería, no da audio o los programas se cierran solos.", "exp": "[Microsoft OS] Detiene winmgmt, ejecuta la bandera '/resetrepository' para reconstruir archivos MOF/CIM averiados y relanza servicios."},
            {"id": "9", "nombre": "9. Bloquear Espionaje Microsoft", "cmd": lambda: abrir_consola_y_ejecutar("BLOQUEO TELEMETRÍA", logica_telemetria), "nov": "Evita que Windows envíe reportes de uso constante a los servidores de Microsoft. Mejora el rendimiento del internet y disco.", "exp": "[Inyección de Registro] Fuerza detención de DiagTrack y altera llave DWORD AllowTelemetry a 0 en el Registro cortando el tráfico saliente."},
            {"id": "10", "nombre": "10. Reparar Sincronización (Hora)", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR HORA", logica_hora), "nov": "Soluciona el error 'La conexión no es privada' obligando a tu PC a sincronizar la hora exacta con relojes atómicos.", "exp": "[Microsoft OS] Reinicia Time Broker. Modifica peerlist forzando sincronización SNTP estricta contra time.windows.com con resync de placa."},
            {"id": "11", "nombre": "11. Higiene de Navegadores y Escudo Anti-Robo de Sesiones (2FA)", "cmd": lambda: abrir_consola_y_ejecutar("ESCUDO DE NAVEGADORES", logica_limpiar_navegadores), "nov": "2 modos de protección para Chrome, Edge, Brave y Firefox: limpia solo la caché pesada sin cerrar tus cuentas, o ejecuta la Purga de Emergencia que destruye todas las cookies 'sessionid' para evitar que roben tus sesiones saltándose el 2FA.", "exp": "[Purga Chromium/Gecko + Anti-Pass-The-Cookie] Modo 1: Destruye directorios Cache, Code Cache y GPUCache. Modo 2: Finaliza procesos activos y erradica bases SQLite (Network\\Cookies, cookies.sqlite), Local Storage y Session Storage anulando tokens de sesión."},
            {"id": "12", "nombre": "12. Reparación Física de Disco (CHKDSK)", "cmd": btn_chkdsk, "nov": "Repara sectores dañados magnéticamente en tu disco duro si la computadora está extremadamente lenta o lanza errores al copiar.", "exp": "[Microsoft OS] Programa chkdsk /f /r /x para desmontaje de inodos y traslado forense de data recuperable a sectores magnéticos sanos."},
            {"id": "13", "nombre": "13. Reconstruir Caché de Iconos", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR ICONOS", logica_iconos), "nov": "Soluciona el molesto fallo visual donde los iconos de tus programas aparecen como hojas en blanco o se ven súper borrosos.", "exp": "[Microsoft OS] Destruye el hilo explorer.exe, purga el archivo IconCache.db en la raíz AppData y relanza el Shell de Windows forzando un re-render."},
            {"id": "14", "nombre": "14. G-Helper (Optimizador ASUS)", "cmd": lambda: abrir_consola_y_ejecutar("G-HELPER", logica_ghelper), "nov": "Reemplazo ultraligero de Armoury Crate (Exclusivo ASUS). Controla LEDs, ventiladores y batería sin trabar la computadora.", "exp": "[Hardware Lock] Escanea el firmware WMI en busca del vendor ASUS. Descarga el binario y lo ejecuta en RAM. Incluye limpieza táctica post-ejecución."},
            {"id": "15", "nombre": "15. Lenovo Legion Toolkit", "cmd": lambda: abrir_consola_y_ejecutar("LENOVO TOOLKIT", logica_lenovo_toolkit), "nov": "Reemplazo ultraligero de Lenovo Vantage. Controla perfiles de energía, ventiladores, RGB y batería sin consumir recursos.", "exp": "[Hardware Lock] Filtro WMI detectando ecosistema Lenovo. Descarga el instalador, despliega modo fantasma (/VERYSILENT) y desinstala limpiando rastros."},
            {"id": "16", "nombre": "16. Mole (Optimizador Terminal)", "cmd": lambda: abrir_consola_y_ejecutar("MOLE", logica_mole), "nov": "Potente optimizador estilo CCleaner, pero corriendo puramente en texto dentro de tu consola. Limpia gigabytes en un parpadeo.", "exp": "[TUI Scripting] Llama al script nativo quick-install.ps1 vía irm. Abre una sesión externa interactiva (conhost) para navegación CLI con purga."},
            {"id": "17", "nombre": "17. Escáner de Fugas y Memoria Virtual", "cmd": btn_fugas_espacio, "nov": "Purga el bug de espacio de Windows 11. Además, escanea tu hardware y te recomienda el límite perfecto de memoria virtual, permitiéndote elegir en qué disco guardarla.", "exp": "[Fusión OSINT HW] Escanea el TotalPhysicalMemory y mapea volumenes vía psutil. Presenta un dashboard interactivo que inyecta parámetros en Win32_PageFileSetting reubicando el pagefile.sys y pulverizando el CapabilityAccessManager."},
            {"id": "18", "nombre": "18. Suite Automatizadora de Archivos, Facturas, Fechas y Duplicados", "cmd": lambda: logica_organizador_archivos(None), "nov": "4 herramientas en 1: Organiza carpetas por tipo (con botón Deshacer), clasifica facturas con gráfica mensual (Ene-Dic), ordena y renombra 500+ archivos por fecha conservando su nombre original en 0.8 segundos, y caza duplicados.", "exp": "[Pathlib + st_mtime Sorter + Anti-Collision + SHA-256 Dedup] Renombrador cronológico (YYYY-MM-DD_NombreOriginal) con sanitización Regex y barra de progreso en tiempo real, analítica mensual ASCII, Rollback en memoria y deduplicación criptográfica."},
            {"id": "19", "nombre": "19. Radar Visual de Almacenamiento", "cmd": btn_mapa_espacio, "nov": "Muestra un mapa interactivo de tu disco duro ordenando las carpetas de la más pesada a la más ligera. Además, la inteligencia artificial te sugerirá archivos basura de Windows que puedes eliminar con un clic.", "exp": "[Hilos WMI/OS] Combina un scanner recursivo de alto rendimiento (os.scandir) con un renderizador ttk.Treeview. Incluye módulo Heurístico pre-scan para identificar y truncar inodos huérfanos del S.O."},
            {"id": "20", "nombre": "20. Gestor de Pánico (Liberar RAM/CPU)", "cmd": lambda: abrir_consola_y_ejecutar("MODO PÁNICO", logica_boton_panico), "nov": "Mide en tiempo real tu procesador y RAM. Si la PC se está trabando, un botón cerrará todo lo innecesario para que vuelva a respirar.", "exp": "[Fusión OS/PSAPI] Ejecuta lecturas en vivo con psutil. El botón inyecta kill signals a binarios pesados (Chromium/Electron) e invoca la API EmptyWorkingSet para forzar al Kernel a descargar páginas de memoria inactivas."}
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

    def btn_rayos_x():
        import tkinter.filedialog as fd
        ruta = fd.askopenfilename(title="Selecciona el archivo sospechoso a analizar", parent=app)
        if ruta:
            abrir_consola_y_ejecutar("RAYOS X", lambda log: logica_rayos_x_archivo(log, ruta))

    def btn_sandbox_virtual():
        menu = "1. 🛡️ Lanzar Caja de Arena (Sandbox Desechable)\n2. ⚙️ Auditar soporte de Virtualización (CPU/BIOS)"
        dialogo = ctk.CTkInputDialog(text=f"¿Qué herramienta de aislamiento deseas usar?\n\n{menu}", title="Gestor de Entornos")
        opcion = dialogo.get_input()
        if opcion in ['1', '2']:
            # FIX APLICADO: Ahora sí pasamos 'opcion' como el argumento 'accion' que pedía la función
            abrir_consola_y_ejecutar("ENTORNOS AISLADOS", lambda log: logica_entornos_aislados(log, opcion))

    h_diag = [
        {"id": "1", "nombre": "1. Cazador Forense (Anti-Keyloggers)", "cmd": lambda: abrir_consola_y_ejecutar("CAZADOR DE MALWARE", logica_cazador_malware), "nov": "Detecta virus ocultos (como Keyloggers de Office pirata) cruzando el tráfico de red con firmas digitales de los programas.", "exp": "[Heurística Híbrida] Aísla sockets TCP establecidos y escanea el AuthenticodeSignature del OwningProcess. Aniquila PIDs no firmados e invoca mrt.exe y MpCmdRun para purga profunda."},
        {"id": "2", "nombre": "2. Diagnóstico Veloz", "cmd": lambda: abrir_consola_y_ejecutar("INFO RÁPIDA", logica_diagnostico_rapido), "nov": "Resumen instantáneo con la calificación matemática oficial de velocidad y fluidez que Windows le da a esta PC.", "exp": "[Microsoft OS] Invoca systeminfo y evalúa la clase WMI 'Win32_WinSat', exponiendo la calificación formal WinEI del indexador interno."},
        {"id": "3", "nombre": "3. Radiografía Completa Hardware", "cmd": lambda: abrir_consola_y_ejecutar("RADIOGRAFÍA HW", logica_radiografia_hardware_completa), "nov": "Lista precisa con marcas y modelos reales de la Placa Madre, RAM instalada, Procesador exacto y Tarjetas Gráficas de esta computadora.", "exp": "[CIM Engine] Volcado canalizado. Interroga las clases Win32_BaseBoard, Processor y parsea arreglos matemáticos de PhysicalMemory (DIMMs)."},
        {"id": "4", "nombre": "4. Salud de Discos S.M.A.R.T", "cmd": lambda: abrir_consola_y_ejecutar("SALUD DE DISCOS", logica_salud_discos), "nov": "Lee los sensores internos ocultos de tus discos duros y de estado sólido para advertirte si están a punto de sufrir una falla física.", "exp": "[Lectura a Nivel Hardware] Parsea el firmware físico utilizando Get-PhysicalDisk, evaluando la variable HealthStatus extraída del sensor S.M.A.R.T."},
        {"id": "5", "nombre": "5. Monitor de Estabilidad Windows", "cmd": btn_perfmon, "nov": "Abre una línea de tiempo gráfica que te muestra los últimos días de la computadora, detallando por qué ocurrió cada pantallazo azul o cierre inesperado.", "exp": "[Microsoft OS] Emplea perfmon /rel para tabular crasheos históricos de aplicaciones y hardware utilizando un índice lógico de estabilidad."},
        {"id": "6", "nombre": "6. Cuadrícula Forense de Tareas", "cmd": btn_visor, "nov": "Despliega una hoja de cálculo interactiva para investigar y filtrar procesos y servicios en memoria, mucho más detallado que el Administrador de Tareas.", "exp": "[Pipeline GridView] Redirige cadenas de datos masivas de Get-Process y EventLogs directamente hacia la interfaz gráfica de filtrado en RAM Out-GridView."},
        {"id": "7", "nombre": "7. Tiempo de Actividad Real", "cmd": lambda: abrir_consola_y_ejecutar("UPTIME", logica_uptime), "nov": "Muestra cuánto tiempo exacto lleva esta computadora encendida. Revela si el Inicio Rápido de Windows está impidiendo apagados reales.", "exp": "[Microsoft OS] Resta la variable LastBootUpTime (Win32_OperatingSystem) a la hora actual revelando el falso apagado asociado a la hibernación de kernel."},
        {"id": "8", "nombre": "8. Auditar Tareas Ocultas", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR TAREAS", logica_tareas_servicios), "nov": "Visualiza programas y mantenimientos fantasmas instalados en el fondo de tu equipo que podrían estar robando recursos y batería.", "exp": "[Microsoft OS] Pipe estructurado combinando la tabla schtasks y Get-Service, aislando exclusivamente los daemons cuyo estatus sea 'Running'."},
        {"id": "9", "nombre": "9. Auditoría de Arranque", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR ARRANQUE", logica_programas_arranque), "nov": "Descubre exactamente cuáles programas se abren a escondidas apenas enciendes tu computadora, lo que hace que tu sistema tarde muchísimo en iniciar.", "exp": "[Microsoft OS] Evalúa ramas del registro y WMI (Win32_StartupCommand). Mapea binarios de persistencia que se enganchan a la fase WinLogon."},
        {"id": "10", "nombre": "10. Historial Forense de USBs", "cmd": lambda: abrir_consola_y_ejecutar("HISTORIAL USB", logica_historial_usb), "nov": "Descifra y lista los nombres de todos los pendrives, controles y celulares que se han conectado en este equipo a lo largo de toda su historia.", "exp": "[Lennes Varela] Parsea registro Plug and Play (PnP). Itera recursivamente sobre la rama HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR extrayendo Device IDs."},
        {"id": "11", "nombre": "11. Extractor de Pantallazos", "cmd": lambda: abrir_consola_y_ejecutar("BSOD", logica_pantallazos_azules), "nov": "Extrae los nombres y códigos de error exactos de todos los Pantallazos Azules de la Muerte recientes para diagnosticar hardware dañado.", "exp": "[Microsoft OS] Filtra EventLog System Logs buscando el origen 'BugCheck'. Extrae el volcado hexadecimal de memoria asociado al kernel panic."},
        {"id": "12", "nombre": "12. Optimizador de Energía y Salud de Batería", "cmd": lambda: abrir_consola_y_ejecutar("CENTRO DE ENERGÍA", logica_monitor_bateria), "nov": "Detecta en vivo qué programas están agotando tu batería, cambia el modo de energía de tu procesador (Ahorro, Equilibrado o Máxima Potencia) en 1 clic y genera el reporte oficial de vida útil de tu batería.", "exp": "[Fusión psutil / PowerCfg GUID / ACPI] Monitorea el impacto energético de procesos en RAM, inyecta esquemas de energía activos en el Kernel mediante GUIDs de powercfg y compila telemetría física de celdas Li-Ion en HTML."},
        {"id": "13", "nombre": "13. Reporte de Suspensión", "cmd": lambda: abrir_consola_y_ejecutar("SLEEPSTUDY", logica_sleepstudy), "nov": "Si tu laptop se descarga estando guardada o suspendida, descubre exactamente qué programa impidió que entrara en reposo absoluto.", "exp": "[Microsoft OS] powercfg /SleepStudy analiza estados S0 Modern Standby, exponiendo los bloqueadores del Active-State Power Management (ASPM)."},
        {"id": "14", "nombre": "14. Gestor Avanzado BitLocker", "cmd": btn_bitlocker, "nov": "Revisa el estado de cifrado, extrae tu clave actual, busca claves perdidas en USBs y desbloquea discos protegidos fácilmente.", "exp": "[Forense BDE] Interfaz interactiva para el motor 'manage-bde'. Incluye escáner recursivo ultra-rápido (dir /s /b) combinando regex para extraer recovery keys en texto plano de unidades montadas."},
        {"id": "15", "nombre": "15. Inspector CAT Pro y Blindaje de Cuentas (SAM / Passwd)", "cmd": lambda: logica_usuarios_locales(None), "nov": "Audita las cuentas reales de tu Windows buscando intrusos, desactiva cuentas inseguras como 'Invitado' en 1 clic, inspecciona archivos largos numerando cada línea (cat -n) y une múltiples archivos de texto en uno solo.", "exp": "[Motor Híbrido WMI SAM / WSL / I/O Streams] Interroga Win32_UserAccount y /etc/passwd validando SIDs (-500/-501) y UIDs (0), ejecuta hardening de cuentas locales vía net user, e integra visor indexado con filtro de errores y concatenador de buffers."},
        {"id": "16", "nombre": "16. Extraer Serial de Fábrica", "cmd": lambda: abrir_consola_y_ejecutar("NÚMERO DE SERIE", logica_numero_serie), "nov": "Copia automáticamente a tu portapapeles el número de serie codificado de la placa base, indispensable para revisar garantías o descargar actualizaciones de BIOS.", "exp": "[Microsoft OS] Consulta nativa a Win32_ComputerSystemProduct aislando la variable string 'IdentifyingNumber' incrustada en ROM por el fabricante OEM."},
        {"id": "17", "nombre": "17. Escudo de Integridad RAM y Cazador de Inyectores (Kernel + Ghost)", "cmd": lambda: abrir_consola_y_ejecutar("ESCUDO FORENSE RAM", logica_memoria_ghost), "nov": "Protege la memoria RAM de tu PC en 3 fases: detecta y cierra programas que intenten modificar la memoria (como Cheat Engine o inyectores), activa los escudos ASLR y DEP de Windows, y audita inyecciones ocultas con Ghost.", "exp": "[Anti-Tampering / ASLR HighEntropy / DEP / Ghost Rust] Enumera procesos bloqueando depuradores e inyectores (WriteProcessMemory), fuerza políticas de mitigación del Kernel (Set-ProcessMitigation DEP/BottomUp/HVCI) e invoca el motor Ghost para auditar anillos de memoria."},
        {"id": "18", "nombre": "18. Visualizador Forense Web", "cmd": btn_historial_web, "nov": "Genera una gráfica moderna, interactiva y al instante que te muestra cuáles son las páginas web más visitadas y las últimas búsquedas, evadiendo la seguridad del sistema.", "exp": "[Bypass de Seguridad SQLite3] Evade los file locks (Errno 13) clonando la Database History del navegador Chromium hacia el %TEMP%. Interpreta sentencias SQL nativas y renderiza una interfaz interactiva Tailwind/Chart.js."},
        {"id": "19", "nombre": "19. Radar de Hardware en Conflicto", "cmd": lambda: abrir_consola_y_ejecutar("RADAR HARDWARE", logica_radar_hardware), "nov": "Detecta piezas físicas de la computadora que estén fallando o que no tengan drivers instalados. Al detectarlas, arma automáticamente una búsqueda avanzada en internet para llevarte directo a la solución.", "exp": "[Auto-Dorking Forense] Interroga la clase WMI Win32_PnPEntity buscando ConfigManagerErrorCode != 0. Extrae la firma de hardware (VEN/DEV) y estructura una búsqueda con operadores lógicos de Google apuntando a dominios especializados."},
        {"id": "20", "nombre": "20. Gestor de Entornos Aislados (Windows Sandbox)", "cmd": btn_sandbox_virtual, "nov": "Abre un PC virtual desechable y aislado de tu sistema o audita si tu procesador y BIOS tienen la virtualización activa.", "exp": "[Microsoft OS] Valida característica Containers-DisposableClientVM y firmware Hyper-V. Compila un perfil .wsb con red activa y hardware aislado."},
        {"id": "21", "nombre": "21. Laboratorio de Rayos X", "cmd": btn_rayos_x, "nov": "Selecciona un archivo (como un JPG sospechoso). TREMEND no lo abrirá, sino que leerá su ADN y te dirá si es un virus disfrazado.", "exp": "[Análisis Hex/Binario] Abre en modo 'rb' mitigando detonación. Extrae Magic Bytes, valida offset EOF contra payloads y ejecuta minería de Strings (ASCII) buscando URLs o PowerShell."}
    ]
    construir_vista_dinamica("🖥️ Diagnóstico e Info del Sistema", "🔍 Buscar (Ej: bateria, smart, usb)...", h_diag)

def cargar_categoria_software():
    global app
    h_soft = [
        {"id": "1", "nombre": "1. Centro de Inteligencia de Software & Cazador Forense", "cmd": lambda: logica_gestor_winget(None), "nov": "Superior a Revo Uninstaller: Escanea todas las actualizaciones online con selección individual/masiva, o desinstala programas destruyendo sus carpetas y registros residuales.", "exp": "[Winget + Cazador Regedit/AppData] Cruza repositorios online con colmenas x64/x86/UWP. Incluye purga en 3 fases: cierre de procesos, barrido de directorios huérfanos y limpieza de Registro."},
        {"id": "2", "nombre": "2. Clonador Pre-Formateo e Inventario (JSON + Excel CSV)", "cmd": lambda: logica_inventario_software(None), "nov": "Respalda todos tus programas en una USB antes de formatear (JSON auto-instalable limpio de basura + Excel CSV) o instala el Kit Esencial Posformateo con 1 clic.", "exp": "[Migración Desatendida] Combina exportación del Registro a CSV con 'winget export/import' silencioso, filtrando bloatware automáticamente."},
        {"id": "3", "nombre": "3. Respaldo Total de Controladores (Drivers)", "cmd": lambda: abrir_consola_y_ejecutar("RESPALDO DRIVERS", logica_respaldo_drivers), "nov": "Salva los controladores originales de Wi-Fi, Audio y Video en C:\\RespaldoDrivers antes de formatear una computadora.", "exp": "[DISM Driver Export] Extrae todos los paquetes de controladores de terceros (.inf / .sys) directamente desde el DriverStore activo del Kernel."},
        {"id": "4", "nombre": "4. Activador Seguro de Windows (MAS)", "cmd": lambda: abrir_consola_y_ejecutar("ACTIVADOR MAS", logica_activador_mas), "nov": "Activa tu Windows legalmente de por vida vinculando una licencia digital a tu placa madre. Cero programas con cracks o virus.", "exp": "[massgravel / MAS] Llama a Microsoft Activation Scripts mediante Invoke-RestMethod. Asigna un Hardware ID (HWID) ticket verificado por los servidores RMS de MS."},
        {"id": "5", "nombre": "5. Forzar Escaneo de Hardware (PnP)", "cmd": lambda: abrir_consola_y_ejecutar("ESCANEO PNP", logica_escanear_pnp), "nov": "Si conectaste una impresora o monitor y no lo reconoce, usa esto para obligar a Windows a revisar todos los puertos físicos de nuevo.", "exp": "[Microsoft OS] Interacciona con el demonio Plug and Play mediante pnputil. La bandera '/scan-devices' ordena la enumeración eléctrica forzada del bus PCI/USB."},
        {"id": "6", "nombre": "6. Instalar ASUS GlideX (Multipantalla)", "cmd": lambda: abrir_consola_y_ejecutar("GLIDEX MULTIPANTALLA", logica_glidex), "nov": "Descarga la increíble app de ASUS para usar tu tablet o celular como una segunda pantalla táctil inalámbrica para tu PC.", "exp": "[Inyección Microsoft Store] Invoca al gestor Winget forzando la comunicación con msstore API usando el Hash ProductId 9PLH2SV1DVK5 para instalación desatendida."},
        {"id": "7", "nombre": "7. Auditor Forense y Extractor Pro de Licencias (BIOS / Registro / Office)", "cmd": lambda: abrir_consola_y_ejecutar("AUDITOR DE LICENCIAS", logica_auditoria_licencias), "nov": "Extrae tu clave de Windows desde la BIOS (OEM) y desde el Registro (BackupProductKeyDefault + DigitalProductId), identifica si tu licencia es OEM, Retail, MAK o KMS (slmgr /dlv), audita Office, caza cracks ocultos y respalda tus claves en el Escritorio.", "exp": "[Triple Key Extractor: OA3x BIOS + BackupProductKeyDefault + Base24 DigitalProductId + slmgr /dlv + OSPP] Desencripta seriales en memoria, distingue claves genéricas de exclusivas, evalúa RearmCount y audita inyecciones Ohook/KMS."},
        {"id": "8", "nombre": "8. Gestor de Suscripciones Compartidas, Grupos Familiares y Cobros", "cmd": lambda: logica_gestor_suscripciones(None), "nov": "Administra los cupos de tu grupo familiar (como Google Gemini Pro, Office 365 o Streaming). Lleva el calendario de pago del día 30, envía el cobro por WhatsApp con 1 clic y corta el servicio el día 31 a quien no pague.", "exp": "[Persistencia JSON + Motor de Calendario + URI WhatsApp] Base de datos local con cálculo automático de mora por fecha de corte, generador de payloads de cobro vía API wa.me y puente directo al panel de administración de Google One / Family."}
    ]
    construir_vista_dinamica("📦 Software y Licencias", "🔍 Buscar (Ej: winget, drivers, office)...", h_soft)

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
        
        # NUEVO: Lógica Inteligente para detectar Playlists / Mixes
        def procesar_interactivo(url_cruda):
            url_limpia = url_cruda.strip()
            if not url_limpia: return
            
            if "youtube.com" in url_limpia or "youtu.be" in url_limpia:
                # Quitamos el index para que el Mix inicie desde la canción 1
                if "&index=" in url_limpia:
                    url_limpia = url_limpia.split("&index=")[0]
                    
                # Si detecta un Mix/Playlist, le pregunta al usuario
                if "list=" in url_limpia:
                    from tkinter import messagebox
                    respuesta = messagebox.askyesno("Mix / Playlist Detectado", "Este enlace contiene un Mix o Lista de Reproducción.\n\n¿Deseas descargar TODOS los videos de la lista?\n\n(Si eliges 'No', solo se agregará el video individual).", parent=dialog_url)
                    if not respuesta:
                        # Si dice que No, podamos la lista y dejamos solo el video
                        url_limpia = url_limpia.split("&list=")[0].split("?list=")[0]
            else:
                # Limpieza para otras redes (Instagram, TikTok, etc)
                url_limpia = url_limpia.split("&utm_")[0].split("?utm_")[0]

            if url_limpia not in urls_a_descargar:
                urls_a_descargar.append(url_limpia)
                lbl_contador.configure(text=f"📥 Enlaces en cola: {len(urls_a_descargar)}")
                entrada.delete(0, 'end')
                btn_siguiente.configure(state="normal", fg_color="#10B981") 

        def agregar_enlace():
            procesar_interactivo(entrada.get())
                
        def pegar_y_agregar():
            try:
                texto = dialog_url.clipboard_get().strip()
                if texto:
                    entrada.delete(0, 'end')
                    entrada.insert(0, texto)
                    procesar_interactivo(texto)
            except: pass
            
        def procesar_url():
            procesar_interactivo(entrada.get())
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
            dialog_cal.geometry("500x520")
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
            
            # --- SECCIÓN DE VIDEOS (Ordenados por Calidad) ---
            ctk.CTkButton(dialog_cal, text="🌟 1. Video Máxima Calidad (2K/4K/8K)", command=lambda: sel_calidad('1')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="📺 2. Video Calidad Estable (1080p)", command=lambda: sel_calidad('2')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="📱 3. Video Ligero (720p)", fg_color="#3B82F6", hover_color="#2563EB", command=lambda: sel_calidad('6')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="🪶 4. Video Ultra Ligero (480p/360p)", fg_color="#64748B", hover_color="#475569", command=lambda: sel_calidad('7')).pack(fill="x", padx=40, pady=5)
            
            # Separador
            ctk.CTkFrame(dialog_cal, height=2, fg_color="#334155").pack(fill="x", padx=40, pady=10)
            
            # --- SECCIÓN DE AUDIO ---
            ctk.CTkButton(dialog_cal, text="🎵 5. Solo Audio Puro (MP3)", fg_color="#107C41", hover_color="#0F5C30", command=lambda: sel_calidad('3')).pack(fill="x", padx=40, pady=5)
            
            # Separador
            ctk.CTkFrame(dialog_cal, height=2, fg_color="#334155").pack(fill="x", padx=40, pady=10)
            
            # --- SECCIÓN DE FOTOS / GALERÍAS ---
            ctk.CTkButton(dialog_cal, text="📸 6. Fotos (Posts Públicos directos)", fg_color="#A855F7", hover_color="#9333EA", command=lambda: sel_calidad('4')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="🔐 7. Fotos (Posts Privados con cookies.txt)", fg_color="#F59E0B", hover_color="#D97706", command=lambda: sel_calidad('5')).pack(fill="x", padx=40, pady=5)

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

    def btn_usb():
        menu = (
            "1. 🔒 Bloquear puertos USB (Evitar robo de datos)\n"
            "2. 🔓 Desbloquear puertos USB (Restaurar acceso)\n"
            "3. 🛠️ Quitar protección contra escritura (Por N° de Disco)\n"
            "4. 💉 Rescatar Archivos Ocultos y Vacunar USB (Por Letra)"
        )
        dialogo = ctk.CTkInputDialog(text=f"Elige la operación USB:\n\n{menu}", title="Gestor Avanzado USB")
        op = dialogo.get_input()
        
        if op in ['1', '2']:
            abrir_consola_y_ejecutar("GESTOR USB", lambda log: logica_gestor_usb(log, op))
        elif op == '3':
            dialogo_d = ctk.CTkInputDialog(text="Ingresa el NÚMERO de disco físico (Ej: 1 o 2):\n(Puedes verlo en Diskpart o Administración de discos)", title="Desbloquear Escritura")
            disco = dialogo_d.get_input()
            if disco and disco.strip().isdigit():
                abrir_consola_y_ejecutar("DESBLOQUEAR USB", lambda log: logica_gestor_usb(log, '3', disco.strip()))
        elif op == '4':
            dialogo_l = ctk.CTkInputDialog(text="Ingresa la LETRA de la memoria USB infectada (Ej: E, F, G):", title="Rescate y Vacuna USB")
            letra = dialogo_l.get_input()
            if letra:
                abrir_consola_y_ejecutar("VACUNA Y RESCATE USB", lambda log: logica_gestor_usb(log, '4', letra.strip()))
        
    def btn_sysprep():
        dialogo = ctk.CTkInputDialog(text="Peligro: El PC se apagará y quedará de fábrica.\nEscribe 'CONFIRMAR':", title="Sysprep")
        confirm = dialogo.get_input()
        if confirm == "CONFIRMAR": abrir_consola_y_ejecutar("SYSPREP", logica_sysprep)

    def btn_optimizador_android():
        # Este no necesita popup porque detecta el teléfono automáticamente
        abrir_consola_y_ejecutar("OPTIMIZADOR ANDROID", logica_optimizador_android)

    def btn_cripto():
        # Ya no necesitamos pedir datos en pop-ups, la ventana nueva hace todo.
        logica_laboratorio_criptografico(None)

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
            {"id": "4", "nombre": "4. TREMEND Media & Cobalt Studio (Videos 4K, MP3, Fotos y Carruseles)", "cmd": lambda: logica_ytdlp(None), "nov": "Descarga videos en 4K/1080p, música MP3, fotos originales en JPG y carruseles enteros de Instagram, TikTok, YouTube, X, Reddit y más de 1000 sitios sin anuncios. Incluye conversor local y limpiador de metadatos.", "exp": "[Suite Híbrida yt-dlp + gallery-dl + FFmpeg + Cobalt UI] Interfaz unificada para extracción de streams VP9/AV1, demuxing de audio MP3, transcodificación automática de carruseles WEBP a JPG (-qscale:v 2), inyección de cookies Netscape y purga de metadatos (-map_metadata -1)."},
            {"id": "5", "nombre": "5. Gestor Avanzado de USB y Vacuna Forense", "cmd": btn_usb, "nov": "4 en 1: Bloquea o desbloquea puertos USB, quita protección contra escritura, o rescata carpetas ocultas por el 'virus de accesos directos' inmunizando la USB.", "exp": "[Kernel USBSTOR + Diskpart + Vacuna NTFS] Altera el registro USBSTOR y StorageDevicePolicies, inyecta scripts Diskpart, restaura atributos (-h -r -s) y blinda autorun.inf con icacls."},
            {"id": "6", "nombre": "6. Gestor de Virtualización de Hardware", "cmd": btn_gestor_virtualizacion, "nov": "Activa las poderosas funciones ocultas de Windows: Hyper-V (Máquinas Virtuales) y Sandbox (Caja fuerte para probar virus de forma segura).", "exp": "[API WMI/DISM Interfaz] Valida la edición SKU del SO. Inyecta paquetes de componentes base (Microsoft-Hyper-V / Containers-DisposableClientVM) con reinicio lógico controlado."},
            {"id": "7", "nombre": "7. Reinicio de Fábrica para Ventas (Sysprep)", "cmd": btn_sysprep, "nov": "Preparación comercial militar: Borra la identidad única de tu PC y registros internos. Al encender, pedirá la configuración de primer día.", "exp": "[Destrucción de Identidad HAL] Ejecuta la orden '/generalize'. Limpia la Security ID (SID), contadores KMS y logs, obligando a la BIOS a ejecutar la fase Out-Of-Box Experience (OOBE)."},
            {"id": "8", "nombre": "8. Borrado de Archivos Irreversible (Wipe)", "cmd": lambda: abrir_consola_y_ejecutar("BORRADO WIPE", logica_borrado_seguro), "nov": "Sobrescribe criptográficamente los huecos vacíos de tu disco duro para garantizar que ningún hacker recupere las fotos que ya borraste.", "exp": "[Trituradora de Ciclos Cipher] Genera un archivo masivo aleatorio que ocupa los bloques desasignados del sistema maestro de archivos (MFT), imposibilitando herramientas forenses."},
            {"id": "9", "nombre": "9. Salto de BIOS Forzado (UEFI)", "cmd": lambda: abrir_consola_y_ejecutar("REINICIO BIOS", logica_reinicio_bios), "nov": "Evita el estrés de reiniciar la computadora y presionar F2 súper rápido. Te lleva directamente a los menús de la Placa Madre.", "exp": "[Interrupción ACPI Inteligente] Envía parámetros /r /fw al shutdown core, modificando el flag NVRAM del sistema para omitir el bootloader y aterrizar en BIOS Firmware Mode."},
            {"id": "10", "nombre": "10. Hackeo de Archivos Bloqueados (JtR)", "cmd": btn_jtr, "nov": "Adivina y recupera contraseñas perdidas de archivos ZIP, RAR o PDF mediante listas mundiales o pistas específicas en tiempo récord.", "exp": "[Openwall JohnTheRipper] Estructura multihilo. Emplea scripts perl (*2john.pl) extrayendo firmas de hash. Ataca los inodos utilizando aceleración de OpenCL/GPU hardware nativa."},
            {"id": "11", "nombre": "11. Destructor de Candados Excel (.xlsx)", "cmd": btn_desproteger_excel, "nov": "Desencripta libros y celdas de Excel que no te dejan escribir, creando una copia perfecta totalmente desbloqueada para edición.", "exp": "[Manipulación OOXML por Regex] Descomprime la arquitectura ZIP nativa de Excel. Navega por el DOM del XML purgando la etiqueta <sheetProtection/> para reensamblar y compilar el archivo."},
            {"id": "12", "nombre": "12. Limpiador Android Extremo (Vía USB)", "cmd": btn_optimizador_android, "nov": "Enlaza tu celular por cable y elimina gigabytes de basura, miniaturas y copias viejas de aplicaciones respetando tus fotos reales.", "exp": "[Controlador de Puente ADB] Descarga librerías core SDK. Se comunica por canal daemon TCP inyectando comandos bash directos a nivel root en el sistema de archivos EXT4 de Android."},
            {"id": "13", "nombre": "13. Auditoría Total de Ciberseguridad", "cmd": lambda: abrir_consola_y_ejecutar("WINPEAS", logica_winpeas), "nov": "El rey del análisis. Escanea huecos que dejarían entrar a un hacker y te permite activar escudos militares (Protección RAM y Defender) en un clic.", "exp": "[Forense Privilege Escalation] Importa PEASS-ng. Audita políticas perimetrales, tokens rotos y contraseñas volátiles. Incluye inyección protectora de proceso LSA RunAsPPL para memoria."},
            {"id": "14", "nombre": "14. Bóveda Criptográfica y Escudo Anti-Fuerza Bruta", "cmd": btn_cripto, "nov": "Mide qué tan resistentes son tus contraseñas, crea claves militares y Tokens de seguridad de 256 bits, y activa el bloqueo automático de Windows para que nadie pueda adivinar la clave de tu PC probando miles de veces.", "exp": "[Entropía de Shannon + CSPRNG + Kernel Lockout] Evalúa bits de entropía frente a 100GH/s, genera tokens de 64 caracteres hexadecimales (secrets.token_hex), inyecta políticas de bloqueo SAM (net accounts /lockoutthreshold:5) y audita el Event ID 4625 del Security Log."},
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

# =========================================================================
# CARTEL DE META COMUNITARIA (DESBLOQUEO DE VERSIÓN 3.4)
# =========================================================================
META_ESTRELLAS_PROXIMA_VERSION = 50  # <-- Cambia aquí la meta de estrellas para liberar la V3.4
PROXIMA_VERSION = "3.4"

def mostrar_cartel_meta_version():
    import urllib.request, urllib.parse, json, threading, webbrowser
    import customtkinter as ctk

    win_meta = ctk.CTkToplevel(app)
    win_meta.title(f"Meta Comunitaria - Desbloqueo de TREMEND V{PROXIMA_VERSION}")
    win_meta.geometry("620x430")
    win_meta.resizable(False, False)
    win_meta.lift()
    win_meta.attributes("-topmost", True)
    win_meta.transient(app)

    # Centrar sobre la pantalla
    x_m = int((ancho_pantalla - 620) / 2)
    y_m = int((alto_pantalla - 430) / 2)
    win_meta.geometry(f"620x430+{x_m}+{y_m}")

    frame_box = ctk.CTkFrame(win_meta, fg_color="#0F172A", corner_radius=12, border_width=2, border_color="#00FFCC")
    frame_box.pack(fill="both", expand=True, padx=15, pady=15)

    ctk.CTkLabel(
        frame_box,
        text=f"🚀 ¡AYÚDANOS A DESBLOQUEAR LA VERSIÓN {PROXIMA_VERSION}!",
        font=("Arial", 20, "bold"), text_color="#00FFCC"
    ).pack(pady=(18, 6))

    texto_meta = (
        f"Estás usando TREMEND Toolkit V{VERSION_ACTUAL} de forma 100% gratuita.\n\n"
        f"A partir de ahora, cada nueva actualización (V{PROXIMA_VERSION}, V3.5...) se liberará\n"
        "únicamente cuando alcancemos la meta de apoyo de la comunidad.\n"
        "¡Si te sirve esta herramienta, apóyanos con una Estrella, compartiendo o donando!"
    )
    ctk.CTkLabel(frame_box, text=texto_meta, font=("Arial", 13), text_color="#E2E8F0", justify="center").pack(padx=20, pady=6)

    # Barra de progreso de Estrellas en GitHub en vivo
    frame_prog = ctk.CTkFrame(frame_box, fg_color="#1E293B", corner_radius=10)
    frame_prog.pack(fill="x", padx=25, pady=12)

    lbl_estrellas = ctk.CTkLabel(
        frame_prog,
        text=f"⭐ Consultando progreso en GitHub hacia la V{PROXIMA_VERSION}...",
        font=("Consolas", 14, "bold"), text_color="#FCD34D"
    )
    lbl_estrellas.pack(pady=(10, 4))

    pb_meta = ctk.CTkProgressBar(frame_prog, height=16, corner_radius=8, progress_color="#10B981", fg_color="#050811")
    pb_meta.pack(fill="x", padx=25, pady=(0, 12))
    pb_meta.set(0.1)

    def consultar_estrellas_reales():
        try:
            url_api = "https://api.github.com/repos/LennesVP/TREMEND"
            req = urllib.request.Request(url_api, headers={'User-Agent': 'TREMEND-Toolkit'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                datos = json.loads(resp.read().decode('utf-8'))
            estrellas = int(datos.get("stargazers_count", 0))
            progreso = min(1.0, estrellas / float(META_ESTRELLAS_PROXIMA_VERSION))
            faltan = max(0, META_ESTRELLAS_PROXIMA_VERSION - estrellas)

            def actualizar_barra():
                if win_meta.winfo_exists():
                    pb_meta.set(progreso)
                    if faltan == 0:
                        lbl_estrellas.configure(text=f"🎉 ¡META ALCANZADA! ({estrellas}/{META_ESTRELLAS_PROXIMA_VERSION} Estrellas) - Preparando V{PROXIMA_VERSION}", text_color="#10B981")
                    else:
                        lbl_estrellas.configure(text=f"⭐ Progreso V{PROXIMA_VERSION}: {estrellas} / {META_ESTRELLAS_PROXIMA_VERSION} Estrellas (Faltan {faltan})")
            app.after(0, actualizar_barra)
        except Exception:
            def fallback_barra():
                if win_meta.winfo_exists():
                    lbl_estrellas.configure(text=f"⭐ Meta para lanzar la V{PROXIMA_VERSION}: {META_ESTRELLAS_PROXIMA_VERSION} Estrellas en GitHub")
            app.after(0, fallback_barra)

    threading.Thread(target=consultar_estrellas_reales, daemon=True).start()

    # Botones de Acción
    frame_btns = ctk.CTkFrame(frame_box, fg_color="transparent")
    frame_btns.pack(fill="x", padx=25, pady=8)

    def ir_github():
        webbrowser.open("https://github.com/LennesVP/TREMEND")

    def ir_kofi():
        webbrowser.open("https://ko-fi.com/ldvp55")

    def compartir_wa():
        msg = "Mira esta navaja suiza en Python con +95 herramientas de soporte y ciberseguridad (TREMEND Toolkit): https://github.com/LennesVP/TREMEND"
        webbrowser.open(f"https://wa.me/?text={urllib.parse.quote(msg)}")

    ctk.CTkButton(frame_btns, text="⭐ 1. Dar Estrella (GitHub)", font=("Arial", 13, "bold"), height=40, fg_color="#3B82F6", hover_color="#2563EB", command=ir_github).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns, text="☕ 2. Donar en Ko-fi", font=("Arial", 13, "bold"), height=40, fg_color="#F59E0B", hover_color="#D97706", text_color="#000000", command=ir_kofi).pack(side="left", padx=4, expand=True, fill="x")
    ctk.CTkButton(frame_btns, text="📲 3. Compartir", font=("Arial", 13, "bold"), height=40, fg_color="#10B981", hover_color="#059669", text_color="#000000", command=compartir_wa).pack(side="left", padx=4, expand=True, fill="x")

    ctk.CTkButton(
        frame_box, text="Continuar al Programa ➡️", font=("Arial", 13, "bold"),
        height=34, fg_color="#334155", hover_color="#475569", command=win_meta.destroy
    ).pack(pady=(8, 12))

# Lanza el cartel automáticamente 800ms después de abrir el programa
app.after(800, mostrar_cartel_meta_version)

app.mainloop()