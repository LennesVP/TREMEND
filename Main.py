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
        
import pyttsx3

def notificar_voz(mensaje):
    """Reproduce el mensaje por los altavoces."""
    try:
        motor = pyttsx3.init()
        # El número 150 es la velocidad. Puedes subirlo o bajarlo luego si quieres.
        motor.setProperty('rate', 150) 
        motor.say(mensaje)
        motor.runAndWait()
    except Exception as e:
        print(f"No se pudo reproducir la voz: {e}")

# Define la versión de este archivo físico
VERSION_ACTUAL = "3.1"

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

app.title("TREMEND Toolkit V3.1 [ESTABLE Y BLINDADO]")

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

def logica_geolocalizar_ip(log):
    log("[*] Triangulando coordenadas mediante API REST (Motor ip-api)...")
    try:
        req = urllib.request.Request("http://ip-api.com/json/", headers={'User-Agent': 'Mozilla/5.0'})
        datos = json.loads(urllib.request.urlopen(req, timeout=5).read().decode('utf8'))
        if datos.get("status") == "success":
            log(f"\n IP: {datos.get('query')}\n Ciudad: {datos.get('city')}\n Región: {datos.get('regionName')}\n País: {datos.get('country')}\n ISP: {datos.get('isp')}\n Lat/Lon: {datos.get('lat')}, {datos.get('lon')}")
        else: log("[-] Error de la API al buscar la IP.")
    except Exception as e: log(f"[-] Error de conexión: {e}")

def logica_wifi_forense(log, accion):
    if accion == '1':
        log("\n[*] Extrayendo perfiles y contraseñas Wi-Fi (Motor Nativo)...")
        try:
            out = subprocess.run('netsh wlan show profiles', shell=True, capture_output=True, text=True, encoding='cp850').stdout
            perfiles = [line.split(":")[1].strip() for line in out.splitlines() if ("Perfil" in line or "Profile" in line) and ":" in line]
            if not perfiles: log("[-] No se encontraron redes guardadas."); return
            for p in perfiles:
                detalles = subprocess.run(f'netsh wlan show profile name="{p}" key=clear', shell=True, capture_output=True, text=True, encoding='cp850').stdout
                clave = "SIN CLAVE / RED ABIERTA"
                for line in detalles.splitlines():
                    if ("Contenido de la clave" in line or "Key Content" in line) and ":" in line:
                        clave = line.split(":")[1].strip()
                log(f" -> RED: {p.ljust(20)} | CLAVE: {clave}")
        except Exception as e: log(f"[-] Error: {e}")
    
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
    dns_map = {
        '1': ("1.1.1.1, 1.0.0.1", "Cloudflare (Máxima Rapidez y Privacidad)"),
        '2': ("8.8.8.8, 8.8.4.4", "Google (Alta Estabilidad y Resolución)"),
        '3': ("9.9.9.9, 149.112.112.112", "Quad9 (Bloqueo Nativo de Malware)"),
        '4': ("94.140.14.14, 94.140.15.15", "AdGuard (Bloqueo de Anuncios / Ads)"),
        '5': ("208.67.222.222, 208.67.220.220", "OpenDNS (Seguridad y Filtro Parental)")
    }
    
    if opcion in dns_map:
        ips, nombre = dns_map[opcion]
        log(f"[*] Inyectando Servidores: {nombre}")
        run_ps_script(log, f'Get-NetAdapter | Where-Object {{$_.Status -eq "Up"}} | Set-DnsClientServerAddress -ServerAddresses {ips}')
        log(f"[+] Servidores DNS cambiados a {ips} exitosamente.")
    elif opcion == '6':
        log("[*] Restaurando DNS Automático (DHCP por defecto)...")
        run_ps_script(log, 'Get-NetAdapter | Where-Object {{$_.Status -eq "Up"}} | Set-DnsClientServerAddress -ResetServerAddresses')
        log("[+] DNS restaurados a la configuración de fábrica de tu proveedor de internet.")
    
    run_cmd(log, "ipconfig /flushdns")

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

def logica_qr_wifi(log, ssid, pwd):
    log(f"\n[*] Generando Código QR para la red: {ssid}")
    try:
        formato = f"WIFI:T:WPA;S:{urllib.parse.quote(ssid)};P:{urllib.parse.quote(pwd)};;" if pwd else f"WIFI:T:nopass;S:{urllib.parse.quote(ssid)};P:;;"
        url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={formato}"
        ruta_qr = os.path.join(os.environ.get('TEMP'), f"WiFi_QR_{ssid.replace(' ', '_')}.png")
        urllib.request.urlretrieve(url, ruta_qr)
        log("[+] Código QR generado con éxito. Abriendo imagen...")
        os.startfile(ruta_qr)
    except Exception as e: log(f"[-] Error al generar QR: {e}")

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

def logica_bloquear_web(log, dominio):
    log(f"\n[*] Inyectando regla de bloqueo (loopback) para: {dominio}")
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    dominio_limpio = dominio.replace("http://", "").replace("https://", "").replace("www.", "").strip("/")
    try:
        with open(hosts_path, "a") as f: f.write(f"\n0.0.0.0 {dominio_limpio}\n0.0.0.0 www.{dominio_limpio}")
        run_cmd(log, "ipconfig /flushdns")
        log("[+] Dominio bloqueado exitosamente en el archivo Hosts.")
    except Exception as e: log(f"[-] Error de permisos: {e}")

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

def logica_escaner_puertos_python(log, ip):
    import socket
    log(f"\n[*] Iniciando Escáner de Puertos Avanzado (Motor Python Socket) en IP: {ip}")
    puertos_comunes = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP"}
    abiertos = 0
    for puerto, servicio in puertos_comunes.items():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # Timeout ultrarrápido
        resultado = s.connect_ex((ip, puerto))
        if resultado == 0:
            log(f"[+] PUERTO ABIERTO: {puerto} ({servicio}) -> ¡Posible vector de ataque/servicio activo!")
            abiertos += 1
        s.close()
    if abiertos == 0: log("[-] La máquina parece estar blindada o apagada. No hay puertos comunes expuestos.")
    log("\n[+] Escaneo finalizado.")

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
def logica_fuga_espacio_w11(log):
    import os, subprocess, platform
    from tkinter import messagebox

    log("\n[*] Iniciando Escáner de Fuga de Almacenamiento (Bug de Windows 11)...")

    # 1. Verificación de Arquitectura
    if platform.system() != "Windows" or int(platform.version().split('.')[2]) < 22000:
        log("[-] Tu sistema no es Windows 11. Este bug masivo es exclusivo de esa versión.")
        return

    # 2. Escáner de la Carpeta Problemática
    ruta_cam = r"C:\ProgramData\Microsoft\Windows\CapabilityAccessManager"
    tamano_mb = 0
    log("[*] Calculando el peso físico de la base de datos 'CapabilityAccessManager'...")
    
    if os.path.exists(ruta_cam):
        try:
            for root, dirs, files in os.walk(ruta_cam):
                for f in files:
                    tamano_mb += os.path.getsize(os.path.join(root, f))
            tamano_mb = tamano_mb / (1024 * 1024)
        except Exception as e:
            log(f"[-] Error al leer la carpeta: {e}")

    log(f"    -> Tamaño actual detectado: {tamano_mb:.2f} MB")

    if tamano_mb > 500:
        log("    [!] ALERTA ROJA: Se detectó un consumo anómalo y excesivo de almacenamiento.")
    else:
        log("    [+] El tamaño es normal. Tu disco no está sufriendo la fuga de espacio.")

    # 3. Escáner de Parches de Seguridad
    log("\n[*] Interrogando a Windows Update por el parche de seguridad oficial...")
    # Buscamos específicamente el parche KB5095093 que soluciona este fallo
    script_ps = "Get-HotFix -Id KB5095093 -ErrorAction SilentlyContinue"
    resultado = subprocess.run(["powershell", "-NoProfile", "-Command", script_ps], capture_output=True, text=True)

    if "KB5095093" in resultado.stdout:
        log("[+] ¡Blindaje Confirmado! El parche oficial KB5095093 ya está instalado en este equipo.")
    else:
        log("[-] ADVERTENCIA: El parche KB5095093 NO está instalado. El equipo es vulnerable al fallo.")

    # 4. Reparación Automatizada (Bypass del Modo Seguro)
    if tamano_mb > 500 or "KB5095093" not in resultado.stdout:
        if messagebox.askyesno("Reparación Automática", f"Se detectó vulnerabilidad o un consumo alto ({tamano_mb:.2f} MB).\n\n¿Deseas que TREMEND detenga el servicio y purgue la base de datos corrupta automáticamente (Sin usar Modo Seguro)?"):
            
            log("\n[*] Iniciando protocolo de purga automatizada...")
            
            # Detenemos el servicio camsvc a la fuerza
            log("    -> Apagando el servicio 'camsvc' (Administrador de funcionalidad de acceso)...")
            subprocess.run("net stop camsvc", shell=True, capture_output=True)
            subprocess.run('taskkill /F /FI "SERVICES eq camsvc"', shell=True, capture_output=True)
            
            # Reutilizamos la magia de tu Destructor para adueñarnos de la carpeta rebelde
            log("    -> Rompiendo candados del sistema (Takeown/Icacls)...")
            subprocess.run(f'takeown.exe /f "{ruta_cam}" /a /r /d y 2>nul', shell=True, capture_output=True)
            subprocess.run(f'icacls.exe "{ruta_cam}" /grant *S-1-5-32-544:F /t /c /q', shell=True, capture_output=True)
            
            log("    -> Destruyendo los archivos basura...")
            import shutil
            try:
                # En lugar de renombrar a .old y dejar la basura ahí, la aniquilamos
                shutil.rmtree(ruta_cam, ignore_errors=True)
                log("    [+] Archivos corruptos pulverizados con éxito.")
            except Exception as e:
                log(f"    [-] Algunos archivos están muy bloqueados: {e}")
                
            log("    -> Reactivando servicios de Windows...")
            subprocess.run("net start camsvc", shell=True, capture_output=True)
            
            log("\n[+] REPARACIÓN EXITOSA. Has recuperado todo el espacio robado.")
            log("[!] Recomendación: Ve a Windows Update e instala las actualizaciones pendientes para evitar que el fallo regrese.")
        else:
            log("\n[*] Operación cancelada por el usuario.")

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

def logica_bateria(log):
    ruta = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "ReporteBateria.html")
    run_cmd(log, f"powercfg /batteryreport /output {ruta} & start {ruta}")

def logica_sleepstudy(log):
    ruta = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "SleepStudy.html")
    run_cmd(log, f"powercfg /SleepStudy /output {ruta} & start {ruta}")

def logica_bitlocker(log):
    log("\n[*] Verificando estado AES (BitLocker)...")
    run_cmd(log, "manage-bde -status")

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
    import urllib.request, json, os, platform, subprocess, shutil, zipfile, tarfile
    from tkinter import messagebox

    log("\n[*] Iniciando Radar de Tráfico de Red (Motor Sniffnet)...")
    temp_dir = os.path.join(os.environ.get('TEMP') if os.name == 'nt' else '/tmp', "Tremend_Sniffnet")
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)

    sistema = platform.system().lower()
    arquitectura = platform.machine().lower()
    
    log(f"[*] Plataforma detectada: {sistema.upper()} ({arquitectura})")

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
                log("[+] Motor Sniffnet preexistente detectado en el sistema.")
                break

    archivo_destino = ""
    
    # 3. Descarga y Despliegue (Solo si no está preinstalado)
    if not sniffnet_preexistente:
        log("    -> Contactando API de GitHub para ubicar la última versión...")
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
            
        log("[*] Desplegando motor...")
        try:
            if archivo_destino.endswith('.zip'):
                with zipfile.ZipFile(archivo_destino, 'r') as zip_ref: zip_ref.extractall(temp_dir)
            elif archivo_destino.endswith('.tar.gz'):
                with tarfile.open(archivo_destino, 'r:gz') as tar_ref: tar_ref.extractall(temp_dir)
            
            # --- FIX MAESTRO: INSTALACIÓN GHOST (SILENCIOSA) ---
            elif archivo_destino.endswith('.msi'):
                log("    -> Ejecutando Instalación Silenciosa Temporal (Modo Ghost)...")
                subprocess.run(f'msiexec.exe /i "{archivo_destino}" /qn /norestart', shell=True)
                for r in rutas_comunes:
                    if os.path.exists(r): 
                        exe_path = r
                        break
                        
            # Búsqueda general si fue ZIP o tar.gz
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
    log("[*] Lanzando Sniffnet...")
    log("[!] Cierra la ventana externa de Sniffnet cuando termines el diagnóstico.")
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
    # Si nosotros hicimos la instalación silenciosa, ejecutamos la desinstalación silenciosa
    if sistema == 'windows' and archivo_destino.endswith('.msi') and not sniffnet_preexistente:
        log("[*] Borrando huellas: Desinstalando motor silenciosamente...")
        subprocess.run(f'msiexec.exe /x "{archivo_destino}" /qn /norestart', shell=True)

    if messagebox.askyesno("Limpieza de Base", "¿Deseas ELIMINAR el instalador base de Sniffnet para no dejar rastro en el equipo?"):
        try: shutil.rmtree(temp_dir, ignore_errors=True); log("[+] Archivos base eliminados.")
        except: pass

    if sistema == 'windows' and os.path.exists(r"C:\Windows\System32\Npcap"):
        if messagebox.askyesno("Limpieza de Driver", "Sniffnet ya cerró.\n\n¿Deseas DESINSTALAR el driver 'Npcap' para borrar absolutamente todo rastro de tu intervención en el sistema?"):
            uninstaller = r"C:\Program Files\Npcap\uninstall.exe"
            if os.path.exists(uninstaller):
                log("[*] Lanzando desinstalador de Npcap...")
                script_un = f"Start-Process -FilePath '{uninstaller}' -Verb RunAs -Wait"
                subprocess.run(["powershell", "-NoProfile", "-Command", script_un], startupinfo=startupinfo)
                log("[+] Driver Npcap purgado del sistema.")
            else: log("[-] Desinstalador de Npcap no encontrado.")

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

def logica_ytdlp(log, lista_urls, calidad, formato):
    import zipfile, urllib.request, os, shutil, subprocess
    log(f"\n[*] Iniciando Descargador Multimedia Avanzado (Lote de {len(lista_urls)} enlaces)")
    temp_dir = r"C:\Tremend_Media"
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)
    
    exe_path = os.path.join(temp_dir, "yt-dlp.exe")
    ffmpeg_path = os.path.join(temp_dir, "ffmpeg.exe")
    ffprobe_path = os.path.join(temp_dir, "ffprobe.exe")
    
    # 1. Asegurar Motor Base de Descarga
    if not os.path.exists(exe_path):
        log("[*] Descargando motor de extracción portátil (yt-dlp)...")
        try: urllib.request.urlretrieve("https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe", exe_path)
        except Exception as e: log(f"[-] Error de red en yt-dlp: {e}"); return
        
    # 2. Descarga y Extracción de FFmpeg (PARCHE DE VELOCIDAD)
    if (calidad in ['1', '2']) and (not os.path.exists(ffmpeg_path) or not os.path.exists(ffprobe_path)):
        log("[*] Descargando códecs de multiplexado (FFmpeg)...")
        log("    -> [!] Son unos 100MB. Descargando silenciosamente a máxima velocidad, por favor espera...")
        try:
            zip_path = os.path.join(temp_dir, "ffmpeg.zip")
            # Cambiamos gyan.dev por el CDN de GitHub (BtbN Builds) que es muchísimo más rápido
            url_ffmpeg = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            
            req = urllib.request.Request(url_ffmpeg, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120) as response, open(zip_path, 'wb') as out_file:
                out_file.write(response.read())
                
            log("[*] Extrayendo componentes de fusión multimedia...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    filename = os.path.basename(member)
                    if filename in ["ffmpeg.exe", "ffprobe.exe"]:
                        with open(os.path.join(temp_dir, filename), "wb") as f_out: f_out.write(zip_ref.read(member))
            os.remove(zip_path)
            log("[+] Códecs instalados con éxito.")
        except Exception as e: log(f"[-] Advertencia al procesar códecs: {e}")

    dl_path = os.path.join(os.environ.get("USERPROFILE"), "Downloads")
    
    # Convertimos la lista de URLs en un formato que la consola entienda
    urls_param = ' '.join([f'"{u}"' for u in lista_urls])
    
    # 1. PARÁMETROS BASE (Bloqueo de playlists y nombres seguros)
    params_base = '--no-playlist --windows-filenames -o "%(title).80s [%(id)s].%(ext)s" --embed-metadata --embed-thumbnail'
    
    # 2. LÓGICA DINÁMICA DE FORMATOS
    if calidad == '3':
        log("[*] Modo seleccionado: Extracción de Audio Puro (MP3)")
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -x --audio-format mp3 -P "{dl_path}" {urls_param}'
    elif calidad == '1':
        log(f"[*] Modo seleccionado: Máxima Calidad Disponible (Fusionando a {formato.upper()})")
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -S "vcodec:vp9" --remux-video {formato} -f "bestvideo+bestaudio/best" --merge-output-format {formato} -P "{dl_path}" {urls_param}'
    elif calidad == '2':
        log(f"[*] Modo seleccionado: Full HD 1080p Estable (Fusionando a {formato.upper()})")
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" {params_base} -S "vcodec:vp9" --remux-video {formato} -f "bestvideo[height<=1080]+bestaudio/best" --merge-output-format {formato} -P "{dl_path}" {urls_param}'
    else: return

    log("[*] Procesando flujos y uniendo contenedores. Por favor, espera...")
    
    # Ejecución
    run_cmd(log, cmd)
    
    log("[+] Extracción e integración completadas. Archivos unificados en Descargas.")

    # AVISO DE VOZ AL TERMINAR
    try:
        notificar_voz("La descarga del contenido ha finalizado.")
    except: pass

    # Pregunta de limpieza portátil
    from tkinter import messagebox
    if messagebox.askyesno("Limpieza de Herramienta", "El proceso multimedia ha finalizado.\n\n¿Deseas ELIMINAR por completo los motores descargados de esta computadora para no dejar rastro?"):
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        log("[+] Limpieza táctica: Espacio liberado.")
    else:
        log("[*] Motores conservados.")

def logica_bloquear_usb(log, bloquear):
    valor = 4 if bloquear else 3
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\USBSTOR", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, valor)
        log(f"[+] Puertos USB {'BLOQUEADOS' if bloquear else 'DESBLOQUEADOS'} a nivel de registro.")
    except Exception as e: log(f"[-] Error de privilegios: {e}")

def logica_diskpart_usb(log, disco):
    log(f"\n[*] Removiendo protección contra escritura en el Disco Físico N° {disco}...")
    script_path = os.path.join(os.environ.get("TEMP"), "dp_unlock.txt")
    try:
        with open(script_path, "w") as f:
            f.write(f"select disk {disco}\nattributes disk clear readonly\nexit")
        run_cmd(log, f'diskpart /s "{script_path}"')
        log("[+] Atributos de solo lectura eliminados. La unidad ya se puede formatear.")
    except Exception as e: log(f"[-] Error: {e}")

    notificar_voz("El Proceso De Desbloqueo USB ha terminado.")

def logica_sysprep(log):
    log("\n[*] Preparando equipo para clonación/venta (Iniciando Sysprep)...")
    log("[!] El sistema generalizará la imagen y ejecutará el apagado automático.")
    run_cmd(log, r"%windir%\System32\Sysprep\sysprep.exe /generalize /oobe /shutdown")

def logica_borrado_seguro(log):
    log("\n[!] ADVERTENCIA: Esta operación sobrescribe el disco C: con cifrado para evitar recuperaciones forenses.")
    run_cmd(log, "cipher /w:C:\\")

    notificar_voz("El Borrado Seguro ha terminado.")

def logica_pass_fuerte(log):
    clave = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%^&*") for i in range(16))
    log(f"\n[+] CLAVE SEGURA GENERADA: {clave}")
    run_cmd(log, f"echo {clave} | clip")

def logica_modo_dios(log):
    ruta = os.path.join(os.environ.get("USERPROFILE"), "Desktop", "ModoDios_Tremend.{ED7BA470-8E54-465E-825C-99712043E01C}")
    try: os.makedirs(ruta); log("[+] Modo Dios creado en tu Escritorio.")
    except: log("[-] Ya existe.")

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

# Variables globales para el efecto "Libro"
datos_enciclopedia = []
datos_tienda = []
indice_tienda = 0
indice_enciclopedia = 0

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
# 4. INTERFAZ GRÁFICA Y SISTEMA DE CATEGORÍAS
# ============================================================================
sidebar = ctk.CTkFrame(app, width=240, corner_radius=0)
sidebar.pack(side="left", fill="y")

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

# --- MOTOR LÓGICO DEL HUD (100% NATIVO, SIN LAG) ---
from ctypes import wintypes

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

def arrancar_motor_hud():
    # Función para leer los latidos del procesador desde el Kernel
    def get_system_times():
        idleTime, kernelTime, userTime = FILETIME(), FILETIME(), FILETIME()
        ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idleTime), ctypes.byref(kernelTime), ctypes.byref(userTime))
        idle = (idleTime.dwHighDateTime << 32) | idleTime.dwLowDateTime
        sys_time = ((kernelTime.dwHighDateTime << 32) | kernelTime.dwLowDateTime) + ((userTime.dwHighDateTime << 32) | userTime.dwLowDateTime)
        return idle, sys_time

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
                ram_total = stat.ullTotalPhys / (1024**3)
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

arrancar_motor_hud()

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
    def btn_puerto_proceso():
        dialogo = ctk.CTkInputDialog(text="Puerto local a investigar (ej. 8080):", title="Rastreo")
        puerto = dialogo.get_input()
        if puerto: abrir_consola_y_ejecutar("PUERTO", lambda log: logica_puerto_proceso(log, puerto))
        
    def btn_qr_wifi():
        dialogo_ssid = ctk.CTkInputDialog(text="Nombre de la red Wi-Fi (SSID):", title="QR")
        ssid = dialogo_ssid.get_input()
        if ssid:
            dialogo_pwd = ctk.CTkInputDialog(text="Contraseña (vacío si es libre):", title="Clave")
            pwd = dialogo_pwd.get_input()
            abrir_consola_y_ejecutar("QR WI-FI", lambda log: logica_qr_wifi(log, ssid, pwd))
            
    def btn_dns_res():
        dialogo = ctk.CTkInputDialog(text="Dominio a resolver (ej. facebook.com):", title="DNS")
        dom = dialogo.get_input()
        if dom: abrir_consola_y_ejecutar("DNS", lambda log: logica_resolucion_dns(log, dom))
        
    def btn_bloquear_web():
        dialogo = ctk.CTkInputDialog(text="Dominio a bloquear (ej. tiktok.com):", title="Bloqueo Web")
        dom = dialogo.get_input()
        if dom: abrir_consola_y_ejecutar("BLOQUEO", lambda log: logica_bloquear_web(log, dom))
        
    def btn_abrir_puerto():
        dialogo_puerto = ctk.CTkInputDialog(text="Puerto a ABRIR en Firewall:", title="Firewall")
        puerto = dialogo_puerto.get_input()
        if puerto:
            dialogo_proto = ctk.CTkInputDialog(text="Protocolo (TCP o UDP):", title="Protocolo")
            proto = dialogo_proto.get_input()
            if proto: abrir_consola_y_ejecutar("FIREWALL", lambda log: logica_abrir_puerto(log, puerto, proto.upper()))
            
    def btn_escaner():
        dialogo = ctk.CTkInputDialog(text="Ingresa la IP de la máquina (ej. 192.168.0.0):", title="Escáner")
        ip = dialogo.get_input()
        if ip: abrir_consola_y_ejecutar("ESCANER NMAP", lambda log: logica_escaner_puertos_python(log, ip))
        
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
        dialogo = ctk.CTkInputDialog(text="1. Ver Claves en Pantalla\n2. Exportar Backup\n3. Importar Backup", title="Forense Wi-Fi")
        op = dialogo.get_input()
        if op in ['1', '2', '3']: abrir_consola_y_ejecutar("WI-FI FORENSE", lambda log: logica_wifi_forense(log, op))
        
    def btn_dns_opt():
        menu = "1. Cloudflare\n2. Google\n3. Quad9\n4. AdGuard\n5. OpenDNS\n6. Restaurar Fábrica"
        dialogo = ctk.CTkInputDialog(text=f"Elige el proveedor:\n\n{menu}", title="Optimizador DNS")
        op = dialogo.get_input()
        if op in ['1','2','3','4','5','6']: abrir_consola_y_ejecutar("OPTIMIZAR DNS", lambda log: logica_optimizar_dns(log, op))

    h_redes = [
        {"id": "1", "nombre": "1. Info Básica de Red e IP", "cmd": lambda: abrir_consola_y_ejecutar("INFO DE RED", logica_info_red), "nov": "Muestra IP local y pública al instante. Útil para configuraciones y diagnósticos rápidos.", "exp": "[Sockets nativos / API REST] Resuelve hostname e invoca a api.ipify.org para evadir NAT y exponer IP WAN."},
        {"id": "2", "nombre": "2. Reparador de Red Autónomo (Auto-Fix)", "cmd": lambda: abrir_consola_y_ejecutar("REPARADOR DE RED", logica_reparacion_red), "nov": "Soluciona el error 'Conectado sin internet'. Limpia el DNS, renueva la IP y fuerza el protocolo automático.", "exp": "[Autónomo] Ejecuta un reseteo de Winsock e inyecta parámetros netsh dinámicamente escaneando los adaptadores activos vía PowerShell para forzar el DHCP."},
        {"id": "3", "nombre": "3. Prueba de Conectividad (Ping / TCP)", "cmd": btn_ping, "nov": "Verifica si una web está en línea y responde correctamente, con la opción adicional de escanear puertos específicos.", "exp": "[Microsoft OS] Llama a Test-NetConnection para trazar latencia ICMP o auditar el estado de puertos TCP."},
        {"id": "4", "nombre": "4. Monitor Conexiones TCP", "cmd": lambda: abrir_consola_y_ejecutar("MONITOR TCP", logica_conexiones_tcp), "nov": "Escanea y muestra en tiempo real qué programas de tu computadora están conectados a internet consumiendo ancho de banda.", "exp": "[Microsoft OS] Filtra la tabla de enrutamiento (Get-NetTCPConnection) y cruza el PID para revelar el ejecutable."},
        {"id": "5", "nombre": "5. Identificar Proceso por Puerto", "cmd": btn_puerto_proceso, "nov": "Si un programa falla porque 'el puerto está en uso', descubre exactamente qué aplicación lo está bloqueando en la sombra.", "exp": "[Microsoft OS] Interroga puertos locales activos y extrae el OwningProcess mapeando la ruta física del binario."},
        {"id": "6", "nombre": "6. Forense y Migración Wi-Fi", "cmd": btn_wifi, "nov": "Recupera todas las contraseñas Wi-Fi guardadas, expórtalas a una USB para no perderlas al formatear, o impórtalas a una PC nueva.", "exp": "[Microsoft OS] Herramienta modular. Parsea XML nativo de 'netsh wlan export/add profile' para migraciones Zero-Touch."},
        {"id": "7", "nombre": "7. Código QR para Wi-Fi", "cmd": btn_qr_wifi, "nov": "Genera un código QR de tu red para que invitados se conecten escaneándolo rápidamente con su celular sin dictar claves.", "exp": "[API goqr.me] Ensambla URI WIFI:T:WPA y descarga el binario PNG generado por la API REST para visualización."},
        {"id": "8", "nombre": "8. Geolocalizar IP", "cmd": lambda: abrir_consola_y_ejecutar("GEOLOCALIZACIÓN", logica_geolocalizar_ip), "nov": "Rastrea cualquier dirección IP para descubrir de qué país, ciudad, coordenadas y proveedor de internet proviene la conexión.", "exp": "[API ip-api.com] Triangulación mediante peticiones GET al endpoint JSON de IP-API, extrayendo metadatos ASN."},
        {"id": "9", "nombre": "9. Diagnóstico Wi-Fi (WlanReport)", "cmd": lambda: abrir_consola_y_ejecutar("REPORTE WI-FI", logica_reporte_wifi), "nov": "Genera un reporte web muy profesional sobre la salud de tu tarjeta Wi-Fi, mostrando un historial de caídas y desconexiones.", "exp": "[Microsoft OS] Invoca el motor nativo ETW (Event Tracing for Windows) compilando un HTML con transiciones de red."},
        {"id": "10", "nombre": "10. Resolución DNS", "cmd": btn_dns_res, "nov": "Convierte el nombre de cualquier página web (ej. google.com) en su dirección IP numérica real de servidores (Resolución Inversa).", "exp": "[Microsoft OS] Utiliza Resolve-DnsName interrumpiendo la caché local para interrogar servidores raíz sobre registros."},
        {"id": "11", "nombre": "11. Bloqueador de Webs (Hosts)", "cmd": btn_bloquear_web, "nov": "Bloquea el acceso a páginas web específicas (como redes sociales o sitios peligrosos) modificando el sistema de forma nativa.", "exp": "[OS Base] Inyecta un Sinkhole DNS en la ruta nativa drivers/etc/hosts, redirigiendo peticiones a la interfaz loopback."},
        {"id": "12", "nombre": "12. Abrir Puertos Firewall", "cmd": btn_abrir_puerto, "nov": "Crea reglas rápidas para permitir que juegos o programas compartidos se comuniquen libremente sin que el antivirus los bloquee.", "exp": "[Microsoft OS] Inserta reglas directas Inbound en Defender Firewall mediante netsh, habilitando el puerto."},
        {"id": "13", "nombre": "13. Purgar Historial Wi-Fi", "cmd": lambda: abrir_consola_y_ejecutar("PURGAR WI-FI", logica_purgar_wifi_historial), "nov": "Elimina por completo todas las redes memorizadas en tu PC para resolver problemas de conexión por claves viejas.", "exp": "[Microsoft OS] Emplea un wildcard en la interfaz CLI de WLAN (profile name=* i=*) para truncar la base de perfiles."},
        {"id": "14", "nombre": "14. Reset Firewall a Fábrica", "cmd": lambda: abrir_consola_y_ejecutar("RESET FIREWALL", logica_reset_firewall), "nov": "Restaura las defensas y bloqueos de Windows a su estado original. Útil si bloqueaste tu propio internet por error.", "exp": "[Microsoft OS] Reset absoluto de Advanced Firewall, reconstruyendo las tablas y eliminando GPOs de terceros."},
        {"id": "15", "nombre": "15. Purgar Caché ARP", "cmd": lambda: abrir_consola_y_ejecutar("PURGAR ARP", logica_limpiar_arp), "nov": "Obliga a tu computadora a volver a identificar los equipos físicos de tu red. Útil si cambiaste de router recientemente.", "exp": "[Protocolo ARP] Ejecuta arp -d * para vaciar la tabla estática de traducción de IPs a direcciones físicas MAC."},
        {"id": "16", "nombre": "16. Optimizador Avanzado de DNS", "cmd": btn_dns_opt, "nov": "Acelera tu navegación (Cloudflare), bloquea anuncios de todo el sistema (AdGuard) o protégete de virus web (Quad9).", "exp": "[Inyección PS] Inyecta mediante Set-DnsClientServerAddress arreglos de IPs públicas en todas las interfaces activas."},
        {"id": "17", "nombre": "17. Gestionar Sesiones SMB", "cmd": lambda: abrir_consola_y_ejecutar("SESIONES SMB", logica_sesiones_smb), "nov": "Detecta al instante si alguien más en tu misma red LAN está accediendo a tus carpetas compartidas sin tu permiso.", "exp": "[Microsoft OS] Audita el servicio Server Message Block (SMB) usando Get-SmbSession, revelando clientes conectados."},
        {"id": "18", "nombre": "18. Radar Wi-Fi en Tiempo Real", "cmd": lambda: abrir_consola_y_ejecutar("RADAR WI-FI", logica_radar_wifi), "nov": "Escanea a tu alrededor para ver todas las redes Wi-Fi (incluso las ocultas) y encontrar canales menos saturados.", "exp": "[Microsoft OS] Despliega un loop temporal sobre mode=bssid para realizar barridos de radiofrecuencia e intensidad."},
        {"id": "19", "nombre": "19. Auditoría de Latencia (Microcortes)", "cmd": btn_latencia, "nov": "Envía paquetes de forma continua para detectar pequeñas caídas ocultas de internet que causan lag en tus juegos o llamadas.", "exp": "[Python/ICMP] Combina un loop de Pings discretos con el módulo datetime logueando ms para cazar timeouts."},
        {"id": "20", "nombre": "20. Motor Avanzado de Escaneo (Puertos)", "cmd": btn_escaner, "nov": "Analiza tu propia computadora o una IP externa para encontrar vulnerabilidades y puertas traseras abiertas por virus.", "exp": "[Python Sockets] Algoritmo asíncrono para testear puertos TCP estándar. Identifica servicios con timeouts ultracortos."},
        {"id": "21", "nombre": "21. Crear Servidor NAS Compartido", "cmd": btn_nas, "nov": "Transforma cualquier carpeta de tu PC en un servidor rápido para que celulares o TVs de tu casa puedan acceder a su contenido.", "exp": "[Microsoft OS] Automatiza New-SmbShare concediendo permisos a Everyone y adaptando dinámicamente el Firewall."},
        {"id": "22", "nombre": "22. Auditar Caché DNS (DisplayDNS)", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR DNS", logica_auditar_cache_dns), "nov": "Revela una lista oculta de las páginas web a las que esta PC se ha conectado, incluso si borraron el historial del navegador.", "exp": "[Microsoft OS] Volcado directo del búfer interno del resolver DNS de Windows, exponiendo registros A/CNAME."},
        {"id": "23","nombre": "23. Radar de Tráfico de Red (Sniffnet)","cmd": lambda: abrir_consola_y_ejecutar("SNIFFNET", logica_sniffnet),"nov": "Abre una interfaz gráfica moderna para ver en tiempo real qué programas están consumiendo tu internet.","exp": "[Multiplataforma] Instala dependencias Pcap al vuelo, ejecuta binario nativo interceptando sockets y aplica purga forense."},
        {"id": "24", "nombre": "24. Escáner Forense (Nmap)", "cmd": btn_nmap_win, "nov": "Mapea los puertos abiertos, detecta los sistemas operativos y busca vulnerabilidades en cualquier equipo conectado a la red.", "exp": "[Forense Nmap] Descarga la build portátil de Win32, compila el comando según la agresividad y vuelca los resultados de mapeo en tiempo real."},
        {"id": "25", "nombre": "25. Reparar Visibilidad LAN (Carpetas)", "cmd": lambda: abrir_consola_y_ejecutar("VISIBILIDAD RED", logica_visibilidad_lan), "nov": "Soluciona el problema de no poder ver a otras computadoras en la red para compartir archivos o impresoras.", "exp": "[Microsoft OS] Automatiza el arranque de servicios fdPHost y FDResPub. Habilita reglas Inbound/Outbound del Firewall para Network Discovery."}
    ]
    construir_vista_dinamica("🌐 Redes e Internet", "🔍 Buscar (Ej: dns, 16, wifi)...", h_redes)

def cargar_categoria_mantenimiento():
    global app
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

    h_mant = [
        {"id": "1","nombre": "1. Mantenimiento Extremo (Discos y USBs)","cmd": btn_mantenimiento_extremo,"nov": "Detecta todos tus discos y memorias USB conectadas. Vacía papeleras ocultas, borra cachés basura, rastros y repara el sistema.","exp": "[Interfaz CTk + WMI] Escanea Win32_LogicalDisk. Ejecuta rmdir recursivo en metadatos, limpia TEMP y lanza DISM/SFC sobre la raíz del sistema."},
        {"id": "2", "nombre": "2. Optimización Avanzada (Chris Titus)", "cmd": lambda: abrir_consola_y_ejecutar("OPTIMIZACIÓN TITUS", logica_titus), "nov": "La mejor herramienta para acelerar PCs lentas. Desactiva funciones inútiles, instala programas base y mejora el rendimiento.", "exp": "[Chris Titus Tech] irm christitus.com/win | iex. Despliega panel WPF para aplicar tweaks de registro y purga de servicios."},
        {"id": "3", "nombre": "3. Debloat del Sistema (Apps Nativas)", "cmd": btn_debloat, "nov": "Elimina de raíz programas basura preinstalados (como Xbox o Bing) que no se pueden desinstalar desde el panel de control.", "exp": "[Microsoft OS] Get-AppxPackage canalizado hacia Remove-AppxPackage -AllUsers. Purga paquetes provisionados UWP."},
        {"id": "4", "nombre": "4. Restablecer Cola Impresión", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR IMPRESIÓN", logica_spooler), "nov": "Soluciona de inmediato los atascos cuando envías un documento y la impresora se queda trabada sin hacer nada.", "exp": "[Microsoft OS] Detiene Spooler. Purga recursivamente caché .SHD y .SPL del directorio System32, liberando el buffer."},
        {"id": "5", "nombre": "5. Limpieza Extrema WinSxS", "cmd": lambda: abrir_consola_y_ejecutar("LIMPIEZA WINSXS", logica_winsxs), "nov": "Libera masivamente espacio de disco duro borrando copias de seguridad de actualizaciones viejas de Windows.", "exp": "[Microsoft OS] DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase. Minimiza el footprint consolidando el SO."},
        {"id": "6", "nombre": "6. Reparar Windows Update", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR UPDATE", logica_reparar_update), "nov": "Arregla el problema crítico cuando las actualizaciones de Windows se quedan trabadas en 'Descargando 0%'.", "exp": "[Microsoft OS] Detiene criptográficos (wuauserv, bits), renombra SoftwareDistribution a .old y regenera bases de datos."},
        {"id": "7", "nombre": "7. Purgar Puntos Restauración", "cmd": lambda: abrir_consola_y_ejecutar("BORRAR VSS", logica_shadowcopies), "nov": "Borra copias de seguridad de Windows muy antiguas que consumen espacio oculto en tu disco duro (Completamente seguro).", "exp": "[Microsoft OS] vssadmin delete shadows /all /quiet. Purga registros inactivos y shadow copies asignadas recuperando GBs."},
        {"id": "8", "nombre": "8. Reparar Repositorio WMI", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR WMI", logica_wmi), "nov": "Arregla errores graves cuando los programas no pueden leer la información de tu PC (como el nivel de batería).", "exp": "[Microsoft OS] Detiene winmgmt, ejecuta la bandera '/resetrepository' para reconstruir archivos CIM averiados y relanza."},
        {"id": "9", "nombre": "9. Bloquear Telemetría Microsoft", "cmd": lambda: abrir_consola_y_ejecutar("BLOQUEO TELEMETRÍA", logica_telemetria), "nov": "Evita que Windows envíe reportes de uso a los servidores de Microsoft. Mejora el rendimiento del internet y cuida tu privacidad.", "exp": "[Lennes Varela] Fuerza detención de DiagTrack y altera llave DWORD AllowTelemetry en el Registro cortando el tráfico saliente."},
        {"id": "10", "nombre": "10. Reparar Hora (NTP)", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR HORA", logica_hora), "nov": "Soluciona el error 'La conexión no es privada' obligando a tu PC a sincronizar la hora exacta con servidores mundiales.", "exp": "[Microsoft OS] Reinicia Time Broker. Modifica peerlist forzando sincronización SNTP contra time.windows.com con resync."},
        {"id": "11", "nombre": "11. Limpiar Navegadores (Caché)", "cmd": lambda: abrir_consola_y_ejecutar("PURGAR NAVEGADORES", logica_limpiar_navegadores), "nov": "Acelera navegadores borrando archivos temporales pesados. (No borra tus contraseñas, ni historial, ni marcadores).", "exp": "[Python shutil] Destruye de forma recursiva los directorios 'Cache_Data' de motores Chromium en el LOCALAPPDATA."},
        {"id": "12", "nombre": "12. Reparación Disco (CHKDSK)", "cmd": btn_chkdsk, "nov": "Repara sectores dañados físicamente en tu disco duro si la computadora está extremadamente lenta o lanza errores al copiar.", "exp": "[Microsoft OS] Programa chkdsk /f /r /x para desmontaje de inodos y traslado de data recuperable a sectores sanos."},
        {"id": "13", "nombre": "13. Reconstruir Caché de Iconos", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR ICONOS", logica_iconos), "nov": "Soluciona el fallo visual donde los iconos de tus programas aparecen como hojas en blanco o se ven borrosos en el escritorio.", "exp": "[Microsoft OS] Destruye el explorer.exe, purga el archivo IconCache.db en AppData y relanza el Shell forzando un render."},
        {"id": "14","nombre": "14. G-Helper (Optimizador ASUS)","cmd": lambda: abrir_consola_y_ejecutar("G-HELPER", logica_ghelper),"nov": "Reemplazo ultraligero de Armoury Crate exclusivo para laptops ASUS. Controla ventiladores, batería y hardware.","exp": "[Hardware Lock] Escanea el firmware WMI. Si detecta placa ASUS, descarga el binario y lo ejecuta en RAM; si no, bloquea la ejecución para evitar crasheos."},
        {"id": "15","nombre": "15. Lenovo Legion Toolkit (Optimizador)","cmd": lambda: abrir_consola_y_ejecutar("LENOVO TOOLKIT", logica_lenovo_toolkit),"nov": "Reemplazo ultraligero de Lenovo Vantage. Controla perfiles de energía, ventiladores, RGB y batería sin consumir recursos en segundo plano.","exp": "[Hardware Lock] Escanea el firmware WMI detectando placas Lenovo. Descarga el ejecutable nativo desde GitHub y lo lanza con elevación UAC."},
        {"id": "16","nombre": "16. Mole (Optimizador Terminal)","cmd": lambda: abrir_consola_y_ejecutar("MOLE", logica_mole),"nov": "Potente optimizador estilo CCleaner directo en terminal. Limpia cachés, temporales y libera gigabytes de espacio.","exp": "[Experimental] Llama al script nativo quick-install.ps1 vía irm. Abre una sesión externa interactiva (conhost) para navegación por teclado."},
        {"id": "17", "nombre": "17. Reparar Fuga de Espacio (Bug W11)", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR FUGA ESPACIO W11", logica_fuga_espacio_w11), "nov": "Soluciona un error grave de Windows 11 donde un archivo oculto crece descontroladamente robando hasta 500 GB de tu disco duro.", "exp": "[Autónomo] Escanea la base CapabilityAccessManager y el parche KB5095093. Automatiza la detención de camsvc y purga los inodos sin requerir Modo Seguro."}
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

    h_diag = [
        {"id": "1", "nombre": "1. Diagnóstico Rápido (HW)", "cmd": lambda: abrir_consola_y_ejecutar("INFO RÁPIDA", logica_diagnostico_rapido), "nov": "Muestra un resumen inmediato de tu PC y verifica la calificación de rendimiento general que le ha dado Windows.", "exp": "[Microsoft OS] Invoca systeminfo y evalúa la clase WMI 'Win32_WinSat', exponiendo la calificación formal WinEI."},
        {"id": "2", "nombre": "2. Radiografía Completa HW", "cmd": lambda: abrir_consola_y_ejecutar("RADIOGRAFÍA HW", logica_radiografia_hardware_completa), "nov": "Informe extremo de las piezas físicas: marca de placa madre, modelo de CPU, RAM exacta y ranuras usadas.", "exp": "[CIM Engine] Volcado canalizado. Interroga Win32_BaseBoard, Processor y parsea PhysicalMemory (DIMMs)."},
        {"id": "3", "nombre": "3. Salud Física Discos (S.M.A.R.T)", "cmd": lambda: abrir_consola_y_ejecutar("SALUD DE DISCOS", logica_salud_discos), "nov": "Lee los sensores internos de tus discos o SSD para avisarte si están sanos o si están a punto de dañarse físicamente.", "exp": "[Microsoft OS] Parsea el firmware físico (Get-PhysicalDisk), evaluando HealthStatus extraído de S.M.A.R.T."},
        {"id": "4", "nombre": "4. Monitor de Confiabilidad", "cmd": btn_perfmon, "nov": "Abre gráficas que te indican a qué hora falló un programa o por qué la computadora se reinició la semana pasada.", "exp": "[Microsoft OS] perfmon /rel tabula crasheos de aplicaciones y hardware utilizando un índice de estabilidad de 1 a 10."},
        {"id": "5", "nombre": "5. Visor Gráfico (GridView)", "cmd": btn_visor, "nov": "Abre una tabla avanzada interactiva para buscar y filtrar procesos, servicios o errores recientes que corren en tu PC.", "exp": "[Microsoft OS] Redirige pipeline de Get-Process/Service hacia Out-GridView para ordenamiento y filtrado RAM."},
        {"id": "6", "nombre": "6. Tiempo de Actividad (Uptime)", "cmd": lambda: abrir_consola_y_ejecutar("UPTIME", logica_uptime), "nov": "Calcula con precisión cuántos días y horas lleva encendida tu computadora sin apagarse realmente (Inicio Rápido).", "exp": "[Microsoft OS] Resta LastBootUpTime (Win32_OperatingSystem) revelando el falso apagado asociado a hibernación S4."},
        {"id": "7", "nombre": "7. Auditar Tareas y Servicios", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR TAREAS", logica_tareas_servicios), "nov": "Te muestra qué programas o mantenimientos están ejecutándose escondidos en el fondo de tu PC causando lentitud.", "exp": "[Microsoft OS] Pipe estructurado de la tabla schtasks y Get-Service aislando exclusivamente los daemons en 'Running'."},
        {"id": "8", "nombre": "8. Auditar Arranque de Windows", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR ARRANQUE", logica_programas_arranque), "nov": "Descubre exactamente qué programas están configurados para abrirse apenas enciendes tu computadora ralentizando el inicio.", "exp": "[Microsoft OS] Evalúa ramas HKLM/HKCU asociadas a Startup via Win32_StartupCommand. Mapea binarios de persistencia."},
        {"id": "9", "nombre": "9. Historial Forense de USBs", "cmd": lambda: abrir_consola_y_ejecutar("HISTORIAL USB", logica_historial_usb), "nov": "Muestra una lista forense de todos los pendrives o celulares que se han conectado en esta PC en toda su historia.", "exp": "[Lennes Varela] Parsea registro Plug and Play (PnP). Itera sobre HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR."},
        {"id": "10", "nombre": "10. Auditoría de BSOD (Pantallazos)", "cmd": lambda: abrir_consola_y_ejecutar("BSOD", logica_pantallazos_azules), "nov": "Si tu PC mostró la pantalla azul de la muerte, extrae el código de error exacto para saber qué pieza está dañada.", "exp": "[Microsoft OS] Filtra EventLog System Logs por origen 'BugCheck'. Extrae el volcado crudo asociado a pánicos del kernel."},
        {"id": "11", "nombre": "11. Reporte Físico de Batería", "cmd": lambda: abrir_consola_y_ejecutar("REPORTE BATERÍA", logica_bateria), "nov": "Genera un reporte web que muestra de cuántos miliamperios era tu batería de fábrica, y cuánta vida útil real le queda.", "exp": "[Microsoft OS] Invoca powercfg /batteryreport que interpola Full Charge Capacity vs Design Capacity (Wear Level)."},
        {"id": "12", "nombre": "12. Reporte de Suspensión (S0)", "cmd": lambda: abrir_consola_y_ejecutar("SLEEPSTUDY", logica_sleepstudy), "nov": "Si tu laptop se descarga estando guardada o 'suspendida', descubre qué programa mantuvo encendido el procesador.", "exp": "[Microsoft OS] powercfg /SleepStudy analiza S0 Modern Standby exponiendo el Active-State Power Management (ASPM)."},
        {"id": "13", "nombre": "13. Estado de Cifrado BitLocker", "cmd": lambda: abrir_consola_y_ejecutar("BITLOCKER", logica_bitlocker), "nov": "Avisa si tu disco está encriptado con clave. Si conectas un disco encriptado en otra PC, perderás tu información.", "exp": "[Microsoft OS] Verifica estado del algoritmo AES en volúmenes montados vía manage-bde. Revela método de desbloqueo TPM."},
        {"id": "14", "nombre": "14. Auditoría de Usuarios Locales", "cmd": lambda: abrir_consola_y_ejecutar("USUARIOS LOCALES", logica_usuarios_locales), "nov": "Lista todas las cuentas registradas en la máquina e indica en qué fecha y hora exacta se conectaron por última vez.", "exp": "[Microsoft OS] Extrae base de datos local (SAM) ejecutando Get-LocalUser para retornar el timestamp del LastLogon."},
        {"id": "15", "nombre": "15. Extraer Número de Serie (PC)", "cmd": lambda: abrir_consola_y_ejecutar("NÚMERO DE SERIE", logica_numero_serie), "nov": "Copia al portapapeles el número de serie de fábrica de la computadora. Indispensable para soporte de garantía.", "exp": "[Microsoft OS] Consulta Win32_ComputerSystemProduct extrayendo el hash 'IdentifyingNumber' embebido por el Vendor OEM."},
        {"id": "16", "nombre": "16. Escáner Forense RAM (Ghost)", "cmd": lambda: abrir_consola_y_ejecutar("GHOST RAM", logica_memoria_ghost), "nov": "Escanea la memoria RAM buscando virus invisibles (Fileless) que no se guardan en el disco duro para evadir al antivirus.", "exp": "[pandaadir05] Inyecta motor Ghost en Rust. Analiza procesos localizando banderas RWX anómalas (Process Hollowing) en Ring 3."}
    ]
    construir_vista_dinamica("🖥️ Diagnóstico e Info del Sistema", "🔍 Buscar (Ej: bateria, smart, usb)...", h_diag)

def cargar_categoria_software():
    global app
    h_soft = [
        {"id": "1", "nombre": "1. Actualizar Apps (Winget)", "cmd": lambda: abrir_consola_y_ejecutar("WINGET UPGRADE", logica_gestor_winget), "nov": "Analiza los programas de tu computadora y los actualiza a su última versión oficial automáticamente, sin buscar instaladores.", "exp": "[Microsoft Corp] Invoca el gestor Winget. Ejecuta 'upgrade --all' con banderas silenciosas (--silent) aceptando EULAs en background."},
        {"id": "2", "nombre": "2. Clave Original Windows", "cmd": lambda: abrir_consola_y_ejecutar("CLAVE WINDOWS", logica_clave_windows), "nov": "Si vas a formatear y perdiste tu licencia, esta herramienta escanea el chip de la placa base y extrae la clave de fábrica.", "exp": "[Microsoft OS] Lee tabla ACPI (MSDM) y la rama del registro SoftwareProtectionPlatform extrayendo el 'BackupProductKeyDefault'."},
        {"id": "3", "nombre": "3. Inventario Software CSV", "cmd": lambda: abrir_consola_y_ejecutar("INVENTARIO CSV", logica_inventario_software), "nov": "Crea un documento Excel (CSV) en tu escritorio con una lista perfecta de todos los programas instalados y sus versiones.", "exp": "[Python winreg] Itera recursivamente ramas 'Uninstall' (HKLM y Wow6432Node) parseando DisplayName hacia un formato delimitado."},
        {"id": "4", "nombre": "4. Respaldar Controladores", "cmd": lambda: abrir_consola_y_ejecutar("CLONAR DRIVERS", logica_respaldo_drivers), "nov": "Ideal antes de formatear un PC viejo. Clona los controladores de red, video y sonido actuales y los guarda en C:\\RespaldoDrivers.", "exp": "[Microsoft OS] Emplea la utilidad de imágenes DISM con comando '/export-driver' para volcar archivos .inf, .sys y catálogos."},
        {"id": "5", "nombre": "5. Auditar MS Office", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR OFFICE", logica_auditar_office), "nov": "Descubre si el paquete de Word o Excel instalado es original o si fue activado ilegalmente con activadores KMS inseguros.", "exp": "[Microsoft OS] Localiza script OSPP.VBS en Office 16 y lo invoca vía cscript /dstatus para parsear tickets Retail/MAK/KMS instalados."},
        {"id": "6", "nombre": "6. Activador de Windows (MAS)", "cmd": lambda: abrir_consola_y_ejecutar("ACTIVADOR MAS", logica_activador_mas), "nov": "Activa Windows legalmente de por vida vinculando una licencia digital a tu placa madre. Sin descargar troyanos o cracks.", "exp": "[massgravel / MAS] Llama a Microsoft Activation Scripts vía Invoke-RestMethod. Inyecta tickets HWID genuinos sin alterar binarios del SO."},
        {"id": "7", "nombre": "7. Escanear Hardware (PnP)", "cmd": lambda: abrir_consola_y_ejecutar("ESCANEO PNP", logica_escanear_pnp), "nov": "Si conectaste una impresora o tarjeta gráfica y no la reconoce, fuerza a Windows a escanear todos los puertos buscando hardware.", "exp": "[Microsoft OS] Interacciona con el administrador Plug and Play mediante pnputil. '/scan-devices' fuerza enumeración de bus y petición de drivers."},
        {"id": "8", "nombre": "8. Instalar GlideX (Extensión de Pantalla)", "cmd": lambda: abrir_consola_y_ejecutar("GLIDEX MULTIPANTALLA", logica_glidex), "nov": "Instala la app oficial de ASUS para duplicar o extender la pantalla de tu PC a una tablet o celular (Funciona en cualquier PC).", "exp": "[Microsoft Store] Invoca al gestor Winget para descargar e instalar el paquete UWP nativo de forma desatendida mediante su ProductId."}
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
        dialog_url.title("YouTube-DL - Paso 1: Cola de Descargas")
        dialog_url.geometry("550x260")
        dialog_url.attributes("-topmost", True)
        dialog_url.transient(app)
        
        ctk.CTkLabel(dialog_url, text="Ingresa el enlace (URL) y dale a 'Pegar y Agregar':", font=("Arial", 14)).pack(pady=(20, 5))
        entrada = ctk.CTkEntry(dialog_url, width=450)
        entrada.pack(pady=5)
        
        lbl_contador = ctk.CTkLabel(dialog_url, text="📥 Enlaces en cola: 0", font=("Arial", 13, "bold"), text_color="#38BDF8")
        lbl_contador.pack(pady=5)
        
        btn_frame_int = ctk.CTkFrame(dialog_url, fg_color="transparent")
        btn_frame_int.pack(pady=10)
        
        def limpiar_url_magico(url_cruda):
            url_limpia = url_cruda.strip()
            if not url_limpia: return None
            # Limpiador suave: Quita listas de reproducción de YouTube, pero respeta los IDs de otros sitios
            if "youtube.com" in url_limpia or "youtu.be" in url_limpia:
                return url_limpia.split("&list=")[0].split("&index=")[0]
            else:
                # Quitamos rastreadores de marketing (utm_) pero dejamos los identificadores vitales (?viewkey, ?id, etc)
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
            dialog_cal.title("YouTube-DL - Paso 2")
            dialog_cal.geometry("450x250")
            dialog_cal.attributes("-topmost", True)
            dialog_cal.transient(app)
            ctk.CTkLabel(dialog_cal, text=f"Elige la calidad para los {len(lista_urls)} enlaces:", font=("Arial", 14, "bold")).pack(pady=(20, 15))
            def sel_calidad(cal):
                dialog_cal.destroy()
                if cal == '3': abrir_consola_y_ejecutar("DESCARGADOR MEDIOS", lambda log: logica_ytdlp(log, lista_urls, '3', 'mp3'))
                else: abrir_ventana_formato(lista_urls, cal)
            ctk.CTkButton(dialog_cal, text="🌟 1. Máxima Calidad Posible (2K/4K/8K)", command=lambda: sel_calidad('1')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="📺 2. Calidad Full HD (1080p)", command=lambda: sel_calidad('2')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="🎵 3. Solo Audio (MP3)", fg_color="#107C41", hover_color="#0F5C30", command=lambda: sel_calidad('3')).pack(fill="x", padx=40, pady=15)

        def abrir_ventana_formato(lista_urls, calidad):
            dialog_fmt = ctk.CTkToplevel(app)
            dialog_fmt.title("YouTube-DL - Paso 3")
            dialog_fmt.geometry("450x250")
            dialog_fmt.attributes("-topmost", True)
            dialog_fmt.transient(app)
            ctk.CTkLabel(dialog_fmt, text="Elige el formato de video:", font=("Arial", 14, "bold")).pack(pady=(20, 15))
            def sel_formato(fmt):
                dialog_fmt.destroy(); abrir_consola_y_ejecutar("DESCARGADOR LOTE", lambda log: logica_ytdlp(log, lista_urls, calidad, fmt))
            ctk.CTkButton(dialog_fmt, text="🎬 MP4 (Universal / Estándar)", command=lambda: sel_formato('mp4')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_fmt, text="🎞️ MKV (Alta Calidad / PC)", command=lambda: sel_formato('mkv')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_fmt, text="🍏 MOV (Apple / Mac)", fg_color="#444444", hover_color="#222222", command=lambda: sel_formato('mov')).pack(fill="x", padx=40, pady=15)

    def btn_diskpart():
        dialogo = ctk.CTkInputDialog(text="Ingresa el NÚMERO del disco bloqueado (ej. 1, 2):", title="Desbloqueo USB")
        disco = dialogo.get_input()
        if disco: abrir_consola_y_ejecutar("DISKPART", lambda log: logica_diskpart_usb(log, disco))
        
    def btn_sysprep():
        dialogo = ctk.CTkInputDialog(text="Peligro: El PC se apagará y quedará de fábrica.\nEscribe 'CONFIRMAR':", title="Sysprep")
        confirm = dialogo.get_input()
        if confirm == "CONFIRMAR": abrir_consola_y_ejecutar("SYSPREP", logica_sysprep)

    def btn_optimizador_android():
        # Este no necesita popup porque detecta el teléfono automáticamente
        abrir_consola_y_ejecutar("OPTIMIZADOR ANDROID", logica_optimizador_android)

    h_sop = [
        {"id": "1", "nombre": "1. Destructor de Carpetas Rebeldes", "cmd": btn_destructor, "nov": "Un destructor forzado. Elimina permanentemente cualquier carpeta bloqueada, virus persistente o archivo que Windows no te deje borrar.", "exp": "[Microsoft OS] takeown /f /a + icacls inyectando SID Admin *S-1-5-32-544:F + shutil.rmtree para vaciar inodos."},
        {"id": "2", "nombre": "2. Cambiar o Quitar Contraseña Windows", "cmd": btn_cambiar_clave, "nov": "Te permite cambiar la clave de acceso de cualquier usuario por una nueva o eliminarla para que la PC inicie directamente sin pedir contraseña.", "exp": "[Microsoft OS] Manipulación de SAM inyectando net.exe user bajo UAC, bypassando requerimiento de hash original."},
        {"id": "3", "nombre": "3. Extracción de Credenciales (LaZagne)", "cmd": lambda: abrir_consola_y_ejecutar("LAZAGNE", logica_lazagne), "nov": "Escaneo forense para recuperar todas las contraseñas guardadas en navegadores. Genera un documento de texto en tu escritorio.", "exp": "[AlessandroZ] Exclusión Defender temporal. Dumpea LSA secrets y bases SQLite vía payload descargado de GitHub."},
        {"id": "4", "nombre": "4. Descargador Multimedia (yt-dlp)", "cmd": btn_ytdlp, "nov": "Descarga videos o música (MP3/MP4) a máxima calidad de YouTube, Facebook o Twitter, sin instalar programas con publicidad.", "exp": "[yt-dlp] Motor CLI + FFmpeg embebidos en memoria temporal para merge de flujos de video y audio libres de DRM."},
        {"id": "5", "nombre": "5. Bloquear Puertos USB", "cmd": lambda: abrir_consola_y_ejecutar("BLOQUEO USB", lambda log: logica_bloquear_usb(log, True)), "nov": "Impide la lectura de memorias USB para evitar robo de información. Podrás seguir conectando tu teclado o cargando el celular.", "exp": "[Lennes Varela] Modifica HKLM SYSTEM USBSTOR 'Start' a DWORD 4. Deniega el montaje del driver masivo."},
        {"id": "6", "nombre": "6. Desbloquear Puertos USB", "cmd": lambda: abrir_consola_y_ejecutar("DESBLOQUEO USB", lambda log: logica_bloquear_usb(log, False)), "nov": "Habilita nuevamente la lectura de discos externos y memorias USB en la computadora.", "exp": "[Lennes Varela] Reestablece la llave DWORD Start a valor 3 en USBSTOR, rehabilitando el montaje PnP."},
        {"id": "7", "nombre": "7. Quitar Protección contra Escritura (USB)", "cmd": btn_diskpart, "nov": "Desbloquea memorias USB que no te dejan guardar archivos ni formatear porque dicen estar 'Protegidas contra escritura'.", "exp": "[Microsoft OS] Inyecta script temporal 'attributes disk clear readonly' hacia el motor lógico diskpart /s."},
        {"id": "8", "nombre": "8. Gestor de Virtualización NATIVA (Hyper-V & Sandbox)","cmd": btn_gestor_virtualizacion,"nov": "Escanea el sistema y activa entornos virtuales. Incluye manuales de uso auto-destructibles.","exp": "Utiliza llamadas WMI/DISM para validar la arquitectura del OS y habilitar los flags de Microsoft-Hyper-V y Containers-DisposableClientVM."},
        {"id": "9", "nombre": "9. Preparar PC para Venta (Sysprep)", "cmd": btn_sysprep, "nov": "Ideal para vendedores. Borra los identificadores únicos y drivers de tu placa. Al prender, la PC pedirá la configuración inicial de idioma.", "exp": "[Microsoft OS] Sysprep /generalize purga el SID del host y logs; /oobe fuerza la experiencia out-of-box."},
        {"id": "10", "nombre": "10. Borrado Forense Militar (Wipe)", "cmd": lambda: abrir_consola_y_ejecutar("BORRADO WIPE", logica_borrado_seguro), "nov": "Sobrescribe con ceros todo el espacio vacío del disco para garantizar que ninguna foto o documento que borraste pueda ser recuperado por hackers.", "exp": "[Microsoft OS] cipher /w:C:\\ barre los clusters libres de la MFT sobrescribiéndolos con múltiples pasadas."},
        {"id": "11", "nombre": "11. Reiniciar directo a la BIOS (UEFI)", "cmd": lambda: abrir_consola_y_ejecutar("REINICIO BIOS", logica_reinicio_bios), "nov": "Un salvavidas: Reinicia la PC y te lleva directamente a la pantalla de la BIOS/UEFI sin que tengas que machacar F2 o SUPR repetidas veces.", "exp": "[Microsoft OS] Llamada ACPI ejecutando shutdown.exe /r /fw delegando la interrupción POST al firmware UEFI."},
        {"id": "12", "nombre": "12. Rompe-Claves de Archivos (John The Ripper)","cmd": btn_jtr,"nov": "Descifra y recupera contraseñas olvidadas de archivos .ZIP, .RAR y .PDF bloqueados mediante fuerza bruta.","exp": "[Openwall] Descarga motor JtR Jumbo a %TEMP%. Inyecta *2john tools para aislar el hash cifrado y ejecuta un wordlist attack mediante algoritmos MD5/SHA en la CPU."},
        {"id": "13", "nombre": "13. Desbloqueador de Excel (.xlsx)", "cmd": btn_desproteger_excel, "nov": "Elimina al instante la contraseña de celdas y hojas bloqueadas de cualquier archivo de Excel moderno, creando una copia limpia para que puedas editarla libremente.", "exp": "[Automatización XML] Desempaqueta la estructura OOXML en memoria temporal, utiliza expresiones regulares (Regex) para purgar la etiqueta <sheetProtection> en los archivos sheet.xml y reempaqueta el documento."},
        {"id": "14", "nombre": "14. Limpiador Android Extremo (Vía USB)", "cmd": btn_optimizador_android, "nov": "Libera gigabytes de espacio oculto en celulares (WhatsApp, Telegram, Facebook) conectándolo por USB. No borra tus cuentas, fotos ni chats, solo la basura acumulada.", "exp": "[Motor ADB] Descarga el bridge ADB oficial a la RAM. Conecta por shell inyectando comandos Linux 'rm -rf' en cachés globales, msgstore-* antiguos y thumbnails."},
        {"id": "15", "nombre": "15. Auditoría de Seguridad (WinPEAS)", "cmd": lambda: abrir_consola_y_ejecutar("WINPEAS", logica_winpeas), "nov": "Escanea la computadora buscando vulnerabilidades, contraseñas mal protegidas y errores de configuración que permitirían a un virus escalar privilegios.", "exp": "[PEASS-ng] Descarga winPEASany.exe desde GitHub. Ejecuta un análisis de enumeración profunda (Privesc) y vuelca los resultados en un archivo de texto en el Escritorio."}
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

def cargar_categoria_tienda():
    import urllib.request, json, time, webbrowser
    global app, datos_tienda, indice_tienda
    
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
        
        # --- FIX: Inyección de Funciones Nativas (No más duplicados manuales) ---
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