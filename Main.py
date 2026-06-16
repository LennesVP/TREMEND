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

# Define la versión de este archivo físico
VERSION_ACTUAL = "2.6"

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
# 1. CONFIGURACIÓN DEL TEMA Y RESPONSIVIDAD UNIVERSAL
# ============================================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

# Motor de Adaptabilidad de Pantalla
ancho_pantalla = app.winfo_screenwidth()
alto_pantalla = app.winfo_screenheight()

# Si es una pantalla inmensa (TV), ocupa el 70%. Si es laptop, ocupa el 85%
factor_escala = 0.7 if ancho_pantalla > 1920 else 0.85 
ancho_app = int(ancho_pantalla * factor_escala)
alto_app = int(alto_pantalla * factor_escala)

app.geometry(f"{ancho_app}x{alto_app}")
# Centramos la ventana automáticamente en la pantalla
x_pos = int((ancho_pantalla - ancho_app) / 2)
y_pos = int((alto_pantalla - alto_app) / 2)
app.geometry(f"+{x_pos}+{y_pos}")

app.title("TREMEND Toolkit V2.6 [ESTABLE Y BLINDADO]")

# ============================================================================
# 2. MOTOR DE TERMINAL NATIVA Y EJECUCIÓN (SEGURO CONTRA CRASHES)
# ============================================================================
def abrir_consola_y_ejecutar(titulo, funcion_python_nativa):
    global app
    win_term = ctk.CTkToplevel(app)
    win_term.title(f"Terminal TREMEND: {titulo}")
    win_term.geometry("950x600")
    
    # Eliminamos .transient(app) para que esta ventana sea 100% independiente.
    # Ahora podrás arrastrarla a un segundo monitor sin que se oculte o se ate a la app principal.
    win_term.focus_force()
    
    # Añadimos wrap="word" para garantizar que ningún texto largo se corte a la derecha
    txt_consola = ctk.CTkTextbox(win_term, width=930, height=580, fg_color="#0A0A0A", text_color="#00FFCC", font=("Consolas", 13), wrap="word")
    txt_consola.pack(padx=10, pady=10, fill="both", expand=True)
    
    txt_consola.insert("end", f"[*] {titulo}\n")
    txt_consola.insert("end", "="*85 + "\n")
    txt_consola.configure(state="disabled")

    # Inyección asíncrona de la UI
    def log(texto):
        def update_ui():
            txt_consola.configure(state="normal")
            txt_consola.insert("end", str(texto) + "\n")
            txt_consola.see("end")
            txt_consola.configure(state="disabled")
        app.after(0, update_ui)

    def correr_proceso():
        try: funcion_python_nativa(log)
        except Exception as e: log(f"\n[!] ERROR CRÍTICO: {e}")
        log("\n" + "="*85 + "\n[+] SECUENCIA FINALIZADA. Puedes cerrar esta ventana.")

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
    run_cmd(log, "ipconfig /release")
    run_cmd(log, "ipconfig /flushdns")
    run_cmd(log, "netsh winsock reset")
    run_cmd(log, "netsh int ip reset")
    run_cmd(log, "ipconfig /renew")

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

# --- CATEGORÍA 2: MANTENIMIENTO ---
def logica_mantenimiento_profundo(log):
    log("\n[*] Iniciando Limpieza de Temporales (Motor Python)...")
    for ruta in [os.environ.get('TEMP'), r"C:\Windows\Temp", r"C:\Windows\Prefetch"]:
        if ruta and os.path.exists(ruta):
            for item in os.listdir(ruta):
                try:
                    p = os.path.join(ruta, item)
                    if os.path.isfile(p): os.unlink(p)
                    elif os.path.isdir(p): shutil.rmtree(p)
                except: pass
    log("[+] Limpieza nativa concluida.")
    run_cmd(log, "DISM /Online /Cleanup-Image /RestoreHealth")
    run_cmd(log, "sfc /scannow")

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
    
    # CORRECCIÓN DE PRIVILEGIOS: Añadimos cabecera User-Agent para evadir el bloqueo de GitHub API
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
                Write-Host "[*] Ejecutando escaneo profundo en anillos de memoria..."
                & $exe | Out-String | Write-Host
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

def logica_ytdlp(log, url, calidad, formato):
    import zipfile
    log(f"\n[*] Iniciando Descargador Multimedia Avanzado (Objetivo: {url})")
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
        
    # 2. CORRECCIÓN MAESTRA: Descarga y Extracción Quirúrgica NAtiva de FFmpeg para Multiplexado
    if (calidad in ['1', '2']) and (not os.path.exists(ffmpeg_path) or not os.path.exists(ffprobe_path)):
        log("[*] Descargando códecs de multiplexado (FFmpeg Essentials)...")
        try:
            zip_path = os.path.join(temp_dir, "ffmpeg.zip")
            urllib.request.urlretrieve("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip", zip_path)
            log("[*] Extrayendo componentes de fusión multimedia de forma limpia...")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    filename = os.path.basename(member)
                    if filename in ["ffmpeg.exe", "ffprobe.exe"]:
                        with open(os.path.join(temp_dir, filename), "wb") as f_out:
                            f_out.write(zip_ref.read(member))
            os.remove(zip_path)
            log("[+] Motores de fusión ensamblados correctamente.")
        except Exception as e:
            log(f"[-] Advertencia al procesar códecs: {e}. Los archivos podrían quedar separados.")

    dl_path = os.path.join(os.environ.get("USERPROFILE"), "Downloads")
    
    # Asignación exacta de comandos según la calidad y formato seleccionados
    if calidad == '3':
        log("[*] Modo seleccionado: Extracción de Audio Puro (MP3)")
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" -x --audio-format mp3 -P "{dl_path}" "{url}"'
    elif calidad == '1':
        log(f"[*] Modo seleccionado: Máxima Calidad Disponible (Fusionando a {formato.upper()})")
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" -f "bestvideo+bestaudio/best" --merge-output-format {formato} -P "{dl_path}" "{url}"'
    elif calidad == '2':
        log(f"[*] Modo seleccionado: Full HD 1080p Estable (Fusionando a {formato.upper()})")
        cmd = f'"{exe_path}" --ffmpeg-location "{temp_dir}" -f "bestvideo[height<=1080]+bestaudio/best" --merge-output-format {formato} -P "{dl_path}" "{url}"'
    else:
        log("[-] Error en la selección de parámetros lógicos."); return

    log("[*] Procesando flujos y uniendo contenedores. Por favor, espera...")
    run_cmd(log, cmd)
    log("[+] Extracción e integración completadas. Archivo unificado en Descargas.")

    # Pregunta de limpieza portátil
    from tkinter import messagebox
    if messagebox.askyesno("Limpieza de Herramienta", "El proceso multimedia ha finalizado con éxito.\n\n¿Deseas ELIMINAR por completo los motores descargados (yt-dlp y FFmpeg) de esta computadora para no dejar rastro?"):
        shutil.rmtree(temp_dir, ignore_errors=True)
        log("[+] Limpieza táctica: Espacio liberado y rastro borrado.")
    else:
        log("[*] Motores conservados para optimizar futuras descargas directas.")

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

def logica_sandbox(log):
    log("\n[*] Activando contenedor virtual Windows Sandbox...")
    run_ps_script(log, 'Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -All -Online -NoRestart')
    log("[+] Sandbox habilitado en el kernel. Requiere REINICIAR el sistema para surtir efecto.")

def logica_sysprep(log):
    log("\n[*] Preparando equipo para clonación/venta (Iniciando Sysprep)...")
    log("[!] El sistema generalizará la imagen y ejecutará el apagado automático.")
    run_cmd(log, r"%windir%\System32\Sysprep\sysprep.exe /generalize /oobe /shutdown")

def logica_borrado_seguro(log):
    log("\n[!] ADVERTENCIA: Esta operación sobrescribe el disco C: con cifrado para evitar recuperaciones forenses.")
    run_cmd(log, "cipher /w:C:\\")

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

# El marco de herramientas ahora ocupa TODO el ancho (Se eliminó la Vista Previa)
tools_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
tools_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

def limpiar_panel():
    for widget in tools_frame.winfo_children(): widget.destroy()

# --- MOTOR MAESTRO DE VISTAS (Fábrica de Tarjetas) ---
def construir_vista_dinamica(titulo_categoria, placeholder, lista_herramientas):
    limpiar_panel()
    
    # Encabezado
    header_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))
    ctk.CTkLabel(header_frame, text=titulo_categoria, font=("Arial", 24, "bold")).pack(side="left")
    
    # ... (código anterior: barra de búsqueda) ...
    search_var = ctk.StringVar()
    barra = ctk.CTkEntry(header_frame, textvariable=search_var, placeholder_text=placeholder, width=350, font=("Arial", 14), corner_radius=15, border_color="#38BDF8")
    barra.pack(side="right", padx=10)

    # --- EL FIX DE PAGINACIÓN ---
    estado = {"pagina": 0, "filtradas": lista_herramientas}
    ITEMS_POR_PAGINA = 3 # Reducido a 4 para que respiren las descripciones

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
        
        for item in lote:
            color_borde = item.get("color_borde", "#38BDF8")
            if "Wipe" in item["nombre"] or "Destructor" in item["nombre"] or "Sysprep" in item["nombre"]:
                color_borde = "#EF4444" # Rojo para herramientas peligrosas
            
            tarjeta = ctk.CTkFrame(lista_frame, fg_color="#1E293B", corner_radius=10, border_width=1, border_color=color_borde)
            tarjeta.pack(fill="x", pady=8, padx=10)
            
            # Encabezado de la Tarjeta (Título y Experto)
            th = ctk.CTkFrame(tarjeta, fg_color="transparent")
            th.pack(fill="x", padx=20, pady=(12, 5))
            ctk.CTkLabel(th, text=item["nombre"], font=("Arial", 16, "bold"), text_color="#FFFFFF").pack(side="left")
            if "exp" in item:
                ctk.CTkLabel(th, text=f"  |  {item['exp']}", font=("Arial", 12, "italic"), text_color="#94A3B8").pack(side="left", padx=10)
            
            # Descripción (Novato)
            if "nov" in item:
                ctk.CTkLabel(tarjeta, text=item["nov"], font=("Arial", 14), justify="left", wraplength=850).pack(padx=20, pady=(0, 10), anchor="w")
            
            # Botón de Ejecución
            txt_btn = item.get("txt_btn", "⚡ Ejecutar Herramienta")
            color_btn = "#10B981" if txt_btn == "⚡ Ejecutar Herramienta" else "#3B82F6"
            if color_borde == "#EF4444": color_btn = "#EF4444"
            ctk.CTkButton(tarjeta, text=txt_btn, font=("Arial", 14, "bold"), height=35, fg_color=color_btn, hover_color="#059669", command=item["cmd"]).pack(padx=20, pady=(0, 15), anchor="e")
            
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
        dest = simpledialog.askstring("Ping", "Ingresa IP o Dominio a escanear:", parent=app)
        if dest:
            puerto = simpledialog.askstring("TCP", "Puerto TCP (Opcional):", parent=app)
            abrir_consola_y_ejecutar("PING Y TCP", lambda log: logica_ping_tcp(log, dest, puerto))
    def btn_puerto_proceso():
        puerto = simpledialog.askstring("Rastreo", "Puerto local a investigar (ej. 8080):", parent=app)
        if puerto: abrir_consola_y_ejecutar("PUERTO", lambda log: logica_puerto_proceso(log, puerto))
    def btn_qr_wifi():
        ssid = simpledialog.askstring("QR", "Nombre de la red Wi-Fi (SSID):", parent=app)
        if ssid:
            pwd = simpledialog.askstring("Clave", "Contraseña (vacío si es libre):", parent=app)
            abrir_consola_y_ejecutar("QR WI-FI", lambda log: logica_qr_wifi(log, ssid, pwd))
    def btn_dns_res():
        dom = simpledialog.askstring("DNS", "Dominio a resolver (ej. facebook.com):", parent=app)
        if dom: abrir_consola_y_ejecutar("DNS", lambda log: logica_resolucion_dns(log, dom))
    def btn_bloquear_web():
        dom = simpledialog.askstring("Bloqueo Web", "Dominio a bloquear (ej. tiktok.com):", parent=app)
        if dom: abrir_consola_y_ejecutar("BLOQUEO", lambda log: logica_bloquear_web(log, dom))
    def btn_abrir_puerto():
        puerto = simpledialog.askstring("Firewall", "Puerto a ABRIR en Firewall:", parent=app)
        if puerto:
            proto = simpledialog.askstring("Protocolo", "Protocolo (TCP o UDP):", parent=app)
            if proto: abrir_consola_y_ejecutar("FIREWALL", lambda log: logica_abrir_puerto(log, puerto, proto.upper()))
    def btn_escaner():
        ip = simpledialog.askstring("Escáner", "Ingresa la IP de la máquina (ej. 192.168.1.1):", parent=app)
        if ip: abrir_consola_y_ejecutar("ESCANER NMAP", lambda log: logica_escaner_puertos_python(log, ip))
    def btn_nas():
        ruta = simpledialog.askstring("Servidor NAS", "Ruta de la carpeta (ej. C:\\Trabajo):", parent=app)
        if ruta:
            nombre = simpledialog.askstring("Servidor NAS", "Nombre para el recurso en red:", parent=app)
            if nombre: abrir_consola_y_ejecutar("NAS", lambda log: logica_crear_nas(log, ruta, nombre))
    def btn_latencia():
        dest = simpledialog.askstring("Latencia", "Ingresa dominio para medir (ej. google.com):", parent=app)
        if dest: abrir_consola_y_ejecutar("LATENCIA", lambda log: logica_auditoria_latencia(log, dest))
    def btn_wifi():
        op = simpledialog.askstring("Forense Wi-Fi", "1. Ver Claves en Pantalla\n2. Exportar Backup\n3. Importar Backup", parent=app)
        if op in ['1', '2', '3']: abrir_consola_y_ejecutar("WI-FI FORENSE", lambda log: logica_wifi_forense(log, op))
    def btn_dns_opt():
        menu = "1. Cloudflare\n2. Google\n3. Quad9\n4. AdGuard\n5. OpenDNS\n6. Restaurar Fábrica"
        op = simpledialog.askstring("Optimizador DNS", f"Elige el proveedor:\n\n{menu}", parent=app)
        if op in ['1','2','3','4','5','6']: abrir_consola_y_ejecutar("OPTIMIZAR DNS", lambda log: logica_optimizar_dns(log, op))

    h_redes = [
        {"id": "1", "nombre": "1. Info Básica de Red e IP", "cmd": lambda: abrir_consola_y_ejecutar("INFO DE RED", logica_info_red), "nov": "Muestra IP local y pública al instante. Útil para configuraciones y diagnósticos rápidos.", "exp": "[Sockets nativos / API REST] Resuelve hostname e invoca a api.ipify.org para evadir NAT y exponer IP WAN."},
        {"id": "2", "nombre": "2. Reparación Total de Red", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR RED", logica_reparacion_red), "nov": "Soluciona problemas de conexión a internet limpiando configuraciones atascadas y solicitando una nueva dirección IP al router.", "exp": "[Microsoft OS] Secuencia progresiva: ipconfig /flushdns, reset de la pila TCP/IP (Winsock) y renovación DHCP."},
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
        {"id": "22", "nombre": "22. Auditar Caché DNS (DisplayDNS)", "cmd": lambda: abrir_consola_y_ejecutar("AUDITAR DNS", logica_auditar_cache_dns), "nov": "Revela una lista oculta de las páginas web a las que esta PC se ha conectado, incluso si borraron el historial del navegador.", "exp": "[Microsoft OS] Volcado directo del búfer interno del resolver DNS de Windows, exponiendo registros A/CNAME."}
    ]
    construir_vista_dinamica("🌐 Redes e Internet", "🔍 Buscar (Ej: dns, 16, wifi)...", h_redes)

def cargar_categoria_mantenimiento():
    global app
    def btn_debloat():
        app_name = simpledialog.askstring("Debloat", "App a eliminar (ej. xbox, zune):", parent=app)
        if app_name: abrir_consola_y_ejecutar("DEBLOAT", lambda log: logica_debloat(log, app_name))
    def btn_chkdsk():
        letra = simpledialog.askstring("CHKDSK", "Letra de unidad a reparar (ej. C):", parent=app)
        if letra: abrir_consola_y_ejecutar("CHKDSK", lambda log: logica_chkdsk(log, letra))

    h_mant = [
        {"id": "1", "nombre": "1. Mantenimiento Profundo y SFC/DISM", "cmd": lambda: abrir_consola_y_ejecutar("MANTENIMIENTO", logica_mantenimiento_profundo), "nov": "Realiza una limpieza automática profunda. Elimina gigas de basura oculta y repara archivos vitales dañados de Windows.", "exp": "[Python/OS] shutil.rmtree en TEMP/Prefetch. Luego invoca motores DISM /RestoreHealth y SFC /scannow para validar imagen."},
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
        {"id": "13", "nombre": "13. Reconstruir Caché de Iconos", "cmd": lambda: abrir_consola_y_ejecutar("REPARAR ICONOS", logica_iconos), "nov": "Soluciona el fallo visual donde los iconos de tus programas aparecen como hojas en blanco o se ven borrosos en el escritorio.", "exp": "[Microsoft OS] Destruye el explorer.exe, purga el archivo IconCache.db en AppData y relanza el Shell forzando un render."}
    ]
    construir_vista_dinamica("🧹 Mantenimiento y Optimización", "🔍 Buscar (Ej: chkdsk, debloat)...", h_mant)

def cargar_categoria_diagnostico():
    global app
    def btn_perfmon():
        op = simpledialog.askstring("Monitor", "1. Monitor | 2. Reporte", parent=app)
        if op in ['1', '2', '01', '02']: abrir_consola_y_ejecutar("PERFMON", lambda log: logica_perfmon(log, op))
    def btn_visor():
        op = simpledialog.askstring("Visor", "1. Procesos | 2. Servicios | 3. Errores", parent=app)
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
        {"id": "7", "nombre": "7. Escanear Hardware (PnP)", "cmd": lambda: abrir_consola_y_ejecutar("ESCANEO PNP", logica_escanear_pnp), "nov": "Si conectaste una impresora o tarjeta gráfica y no la reconoce, fuerza a Windows a escanear todos los puertos buscando hardware.", "exp": "[Microsoft OS] Interacciona con el administrador Plug and Play mediante pnputil. '/scan-devices' fuerza enumeración de bus y petición de drivers."}
    ]
    construir_vista_dinamica("📦 Software y Licencias", "🔍 Buscar (Ej: winget, office)...", h_soft)

def cargar_categoria_soporte():
    global app 
    def btn_destructor():
        ruta = simpledialog.askstring("Destructor", "Ruta EXACTA de la carpeta a destruir:", parent=app)
        if ruta: abrir_consola_y_ejecutar("DESTRUCTOR", lambda log: logica_destructor(log, ruta))
    def btn_cambiar_clave():
        usr = simpledialog.askstring("Usuario", "Nombre del usuario local a modificar:", parent=app)
        if usr:
            pwd = simpledialog.askstring("Clave", "Nueva clave (deja vacío para eliminarla):", parent=app)
            if pwd is not None: abrir_consola_y_ejecutar("GESTOR CLAVES", lambda log: logica_cambiar_clave(log, usr, pwd))
    def btn_ytdlp():
        dialog_url = ctk.CTkToplevel(app)
        dialog_url.title("YouTube-DL - Paso 1")
        dialog_url.geometry("550x200")
        dialog_url.attributes("-topmost", True)
        dialog_url.transient(app)
        ctk.CTkLabel(dialog_url, text="Ingresa el enlace (URL) del video o canción:", font=("Arial", 14)).pack(pady=(20, 5))
        entrada = ctk.CTkEntry(dialog_url, width=450); entrada.pack(pady=10)
        btn_frame_int = ctk.CTkFrame(dialog_url, fg_color="transparent"); btn_frame_int.pack(pady=10)
        def pegar_texto():
            try: entrada.delete(0, 'end'); entrada.insert(0, dialog_url.clipboard_get())
            except: pass
        def procesar_url():
            url = entrada.get()
            if not url: return
            dialog_url.destroy(); abrir_ventana_calidad(url)
        ctk.CTkButton(btn_frame_int, text="📋 Pegar Enlace", width=120, fg_color="#444444", hover_color="#666666", command=pegar_texto).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame_int, text="Siguiente", width=120, command=procesar_url).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame_int, text="Cancelar", width=120, fg_color="#880000", hover_color="#AA0000", command=dialog_url.destroy).pack(side="left", padx=5)

        def abrir_ventana_calidad(url):
            dialog_cal = ctk.CTkToplevel(app)
            dialog_cal.title("YouTube-DL - Paso 2")
            dialog_cal.geometry("450x250")
            dialog_cal.attributes("-topmost", True)
            dialog_cal.transient(app)
            ctk.CTkLabel(dialog_cal, text="Elige la calidad de descarga:", font=("Arial", 14, "bold")).pack(pady=(20, 15))
            def sel_calidad(cal):
                dialog_cal.destroy()
                if cal == '3': abrir_consola_y_ejecutar("DESCARGADOR MEDIOS", lambda log: logica_ytdlp(log, url, '3', 'mp3'))
                else: abrir_ventana_formato(url, cal)
            ctk.CTkButton(dialog_cal, text="🌟 1. Máxima Calidad Posible (2K/4K/8K)", command=lambda: sel_calidad('1')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="📺 2. Calidad Full HD (1080p)", command=lambda: sel_calidad('2')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="🎵 3. Solo Audio (MP3)", fg_color="#107C41", hover_color="#0F5C30", command=lambda: sel_calidad('3')).pack(fill="x", padx=40, pady=15)

        def abrir_ventana_formato(url, calidad):
            dialog_fmt = ctk.CTkToplevel(app)
            dialog_fmt.title("YouTube-DL - Paso 3")
            dialog_fmt.geometry("450x250")
            dialog_fmt.attributes("-topmost", True)
            dialog_fmt.transient(app)
            ctk.CTkLabel(dialog_fmt, text="Elige el formato de video:", font=("Arial", 14, "bold")).pack(pady=(20, 15))
            def sel_formato(fmt):
                dialog_fmt.destroy(); abrir_consola_y_ejecutar("DESCARGADOR MEDIOS", lambda log: logica_ytdlp(log, url, calidad, fmt))
            ctk.CTkButton(dialog_fmt, text="🎬 MP4 (Universal / Estándar)", command=lambda: sel_formato('mp4')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_fmt, text="🎞️ MKV (Alta Calidad / PC)", command=lambda: sel_formato('mkv')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_fmt, text="🍏 MOV (Apple / Mac)", fg_color="#444444", hover_color="#222222", command=lambda: sel_formato('mov')).pack(fill="x", padx=40, pady=15)

    def btn_diskpart():
        disco = simpledialog.askstring("Desbloqueo USB", "Ingresa el NÚMERO del disco bloqueado (ej. 1, 2):", parent=app)
        if disco: abrir_consola_y_ejecutar("DISKPART", lambda log: logica_diskpart_usb(log, disco))
    def btn_sysprep():
        confirm = simpledialog.askstring("Sysprep", "Peligro: El PC se apagará y quedará de fábrica.\nEscribe 'CONFIRMAR':", parent=app)
        if confirm == "CONFIRMAR": abrir_consola_y_ejecutar("SYSPREP", logica_sysprep)

    h_sop = [
        {"id": "1", "nombre": "1. Destructor de Carpetas Rebeldes", "cmd": btn_destructor, "nov": "Un destructor forzado. Elimina permanentemente cualquier carpeta bloqueada, virus persistente o archivo que Windows no te deje borrar.", "exp": "[Microsoft OS] takeown /f /a + icacls inyectando SID Admin *S-1-5-32-544:F + shutil.rmtree para vaciar inodos."},
        {"id": "2", "nombre": "2. Cambiar o Quitar Contraseña Windows", "cmd": btn_cambiar_clave, "nov": "Te permite cambiar la clave de acceso de cualquier usuario por una nueva o eliminarla para que la PC inicie directamente sin pedir contraseña.", "exp": "[Microsoft OS] Manipulación de SAM inyectando net.exe user bajo UAC, bypassando requerimiento de hash original."},
        {"id": "3", "nombre": "3. Extracción de Credenciales (LaZagne)", "cmd": lambda: abrir_consola_y_ejecutar("LAZAGNE", logica_lazagne), "nov": "Escaneo forense para recuperar todas las contraseñas guardadas en navegadores. Genera un documento de texto en tu escritorio.", "exp": "[AlessandroZ] Exclusión Defender temporal. Dumpea LSA secrets y bases SQLite vía payload descargado de GitHub."},
        {"id": "4", "nombre": "4. Descargador Multimedia (yt-dlp)", "cmd": btn_ytdlp, "nov": "Descarga videos o música (MP3/MP4) a máxima calidad de YouTube, Facebook o Twitter, sin instalar programas con publicidad.", "exp": "[yt-dlp] Motor CLI + FFmpeg embebidos en memoria temporal para merge de flujos de video y audio libres de DRM."},
        {"id": "5", "nombre": "5. Bloquear Puertos USB", "cmd": lambda: abrir_consola_y_ejecutar("BLOQUEO USB", lambda log: logica_bloquear_usb(log, True)), "nov": "Impide la lectura de memorias USB para evitar robo de información. Podrás seguir conectando tu teclado o cargando el celular.", "exp": "[Lennes Varela] Modifica HKLM SYSTEM USBSTOR 'Start' a DWORD 4. Deniega el montaje del driver masivo."},
        {"id": "6", "nombre": "6. Desbloquear Puertos USB", "cmd": lambda: abrir_consola_y_ejecutar("DESBLOQUEO USB", lambda log: logica_bloquear_usb(log, False)), "nov": "Habilita nuevamente la lectura de discos externos y memorias USB en la computadora.", "exp": "[Lennes Varela] Reestablece la llave DWORD Start a valor 3 en USBSTOR, rehabilitando el montaje PnP."},
        {"id": "7", "nombre": "7. Quitar Protección contra Escritura (USB)", "cmd": btn_diskpart, "nov": "Desbloquea memorias USB que no te dejan guardar archivos ni formatear porque dicen estar 'Protegidas contra escritura'.", "exp": "[Microsoft OS] Inyecta script temporal 'attributes disk clear readonly' hacia el motor lógico diskpart /s."},
        {"id": "8", "nombre": "8. Activar Windows Sandbox", "cmd": lambda: abrir_consola_y_ejecutar("SANDBOX", logica_sandbox), "nov": "Crea una PC desechable aislada dentro de tu máquina. Ideal para abrir archivos sospechosos de virus sin poner en riesgo tu sistema real.", "exp": "[Microsoft OS] Enable-WindowsOptionalFeature Containers-DisposableClientVM. Inicializa entorno aislado vía hipervisor."},
        {"id": "9", "nombre": "9. Preparar PC para Venta (Sysprep)", "cmd": btn_sysprep, "nov": "Ideal para vendedores. Borra los identificadores únicos y drivers de tu placa. Al prender, la PC pedirá la configuración inicial de idioma.", "exp": "[Microsoft OS] Sysprep /generalize purga el SID del host y logs; /oobe fuerza la experiencia out-of-box."},
        {"id": "10", "nombre": "10. Borrado Forense Militar (Wipe)", "cmd": lambda: abrir_consola_y_ejecutar("BORRADO WIPE", logica_borrado_seguro), "nov": "Sobrescribe con ceros todo el espacio vacío del disco para garantizar que ninguna foto o documento que borraste pueda ser recuperado por hackers.", "exp": "[Microsoft OS] cipher /w:C:\\ barre los clusters libres de la MFT sobrescribiéndolos con múltiples pasadas."},
        {"id": "11", "nombre": "11. Reiniciar directo a la BIOS (UEFI)", "cmd": lambda: abrir_consola_y_ejecutar("REINICIO BIOS", logica_reinicio_bios), "nov": "Un salvavidas: Reinicia la PC y te lleva directamente a la pantalla de la BIOS/UEFI sin que tengas que machacar F2 o SUPR repetidas veces.", "exp": "[Microsoft OS] Llamada ACPI ejecutando shutdown.exe /r /fw delegando la interrupción POST al firmware UEFI."}
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
    
    # --- ENCABEZADO CON SISTEMA DE FILTRADO ---
    header_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))
    
    ctk.CTkLabel(header_frame, text="📚 Enciclopedia de Apps", font=("Arial", 24, "bold")).pack(side="left")
    
    # Descargar el índice JSON si aún no lo hemos descargado en esta sesión
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

    # --- LÓGICA DE FILTRADO DINÁMICO ---
    # Extraemos todas las categorías únicas automáticamente del JSON
    categorias_unicas = set()
    for item in datos_enciclopedia:
        categorias_unicas.add(item.get('categoria', 'Sin Categoría'))
        
    lista_filtros = ["Mostrar Todas"] + sorted(list(categorias_unicas))
    datos_filtrados = datos_enciclopedia.copy()
    indice_actual = 0
    var_filtro = ctk.StringVar(value="Mostrar Todas")

    # --- DISEÑO DE LA PÁGINA (El Libro) ---
    tarjeta_frame = ctk.CTkFrame(tools_frame, fg_color="#1E293B", corner_radius=15)
    tarjeta_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    lbl_titulo = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 22, "bold"), text_color="#38BDF8", wraplength=550)
    lbl_titulo.pack(pady=(30, 5), padx=30, anchor="w")
    
    lbl_autor = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 14, "italic"), text_color="#94A3B8")
    lbl_autor.pack(pady=(0, 5), padx=30, anchor="w")
    
    lbl_cat = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 12, "bold"), text_color="#A78BFA")
    lbl_cat.pack(pady=(0, 20), padx=30, anchor="w")
    
    lbl_desc = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 15), justify="left", wraplength=550)
    lbl_desc.pack(pady=10, padx=30, anchor="w")
    
    lbl_adv = ctk.CTkLabel(tarjeta_frame, text="", font=("Arial", 14, "bold"), text_color="#EF4444", justify="left", wraplength=550)
    lbl_adv.pack(pady=20, padx=30, anchor="w")
    
    btn_frame = ctk.CTkFrame(tarjeta_frame, fg_color="transparent")
    btn_frame.pack(pady=30)

    # --- CONTROLES DEL CARRUSEL ---
    nav_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    nav_frame.pack(fill="x", pady=20)
    
    btn_prev = ctk.CTkButton(nav_frame, text="⬅️ Anterior", width=120, fg_color="#334155", hover_color="#475569")
    btn_prev.pack(side="left", padx=30)
    
    lbl_contador = ctk.CTkLabel(nav_frame, text="", font=("Arial", 14, "bold"))
    lbl_contador.pack(side="left", expand=True)
    
    btn_next = ctk.CTkButton(nav_frame, text="Siguiente ➡️", width=120, fg_color="#334155", hover_color="#475569")
    btn_next.pack(side="right", padx=30)

    # --- FUNCIÓN: RENDERIZAR PÁGINA ---
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
        
        for widget in btn_frame.winfo_children(): widget.destroy()
            
        if item.get('es_enlace', False):
            def abrir_repo(url=item.get('enlace', '')): webbrowser.open(url)
            ctk.CTkButton(btn_frame, text="🌐 Abrir Repositorio Oficial", font=("Arial", 16, "bold"), height=50, fg_color="#3B82F6", hover_color="#2563EB", text_color="#FFFFFF", command=abrir_repo).pack()
        else:
            def accionar_instalacion():
                def comando_puente(log): logica_instalar_herramienta(log, item.get('carpeta',''), item.get('archivos',[]), item.get('comando_instalacion',''))
                app_consola = ctk.CTkToplevel(app)
                app_consola.title(f"Instalando: {item.get('titulo', '')}")
                app_consola.geometry("600x400")
                app_consola.configure(bg="#0F172A")
                app_consola.attributes("-topmost", True)
                txt_log = ctk.CTkTextbox(app_consola, width=580, height=380, fg_color="#000000", text_color="#00FF00", font=("Consolas", 12))
                txt_log.pack(padx=10, pady=10)
                def log_a_consola(texto): txt_log.insert("end", texto + "\n"); txt_log.see("end")
                threading.Thread(target=comando_puente, args=(log_a_consola,), daemon=True).start()
                
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

    # --- FUNCIÓN PARA EJECUTAR EL FILTRO ---
    def aplicar_filtro(seleccion):
        nonlocal datos_filtrados, indice_actual
        if seleccion == "Mostrar Todas":
            datos_filtrados = datos_enciclopedia.copy()
        else:
            datos_filtrados = [item for item in datos_enciclopedia if item.get('categoria', 'Sin Categoría') == seleccion]
        
        indice_actual = 0  # Volver a la página 1 del nuevo filtro
        mostrar_pagina(indice_actual)

    # --- EL BOTÓN DESPLEGABLE (ComboBox) ---
    combo_filtro = ctk.CTkOptionMenu(header_frame, values=lista_filtros, variable=var_filtro, command=aplicar_filtro, fg_color="#3B82F6", button_color="#2563EB", button_hover_color="#1D4ED8", font=("Arial", 14, "bold"))
    combo_filtro.pack(side="right")
    ctk.CTkLabel(header_frame, text="🔍 Filtrar: ", font=("Arial", 14, "bold"), text_color="#94A3B8").pack(side="right", padx=10)

    # Iniciar la lectura del libro
    mostrar_pagina(0)

def cargar_categoria_tienda():
    import urllib.request, json, time, webbrowser
    global app, datos_tienda, indice_tienda
    
    limpiar_panel()
    ctk.CTkLabel(tools_frame, text="🛒 Venta de Licencias Oficiales", font=("Arial", 24, "bold")).pack(pady=(0, 20), anchor="w")
    
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

    # --- DISEÑO DEL CARRUSEL COMERCIAL ---
    tarjeta_frame = ctk.CTkFrame(tools_frame, fg_color="#1E293B", corner_radius=15, border_width=2, border_color="#F59E0B")
    tarjeta_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
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

    # --- NUEVO TEXTO DE ADVERTENCIA DE PRECIOS ---
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

    # --- FUNCIÓN: RENDERIZAR PRODUCTO ---
    def mostrar_producto(idx):
        item = datos_tienda[idx]
        lbl_titulo.configure(text=item.get('producto', ''))
        lbl_precio_tremend.configure(text=f"Precio TREMEND: {item.get('precio_tremend', '')}")
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

    # --- CONTROLES DEL CARRUSEL ---
    def cambiar_pagina(direccion):
        global indice_tienda
        indice_tienda += direccion
        if indice_tienda < 0: indice_tienda = len(datos_tienda) - 1
        elif indice_tienda >= len(datos_tienda): indice_tienda = 0
        mostrar_producto(indice_tienda)
        lbl_contador.configure(text=f"Producto {indice_tienda + 1} de {len(datos_tienda)}")

    nav_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
    nav_frame.pack(fill="x", pady=20)
    
    ctk.CTkButton(nav_frame, text="⬅️ Anterior", width=120, fg_color="#334155", hover_color="#475569", command=lambda: cambiar_pagina(-1)).pack(side="left", padx=30)
    lbl_contador = ctk.CTkLabel(nav_frame, text="", font=("Arial", 14, "bold"))
    lbl_contador.pack(side="left", expand=True)
    ctk.CTkButton(nav_frame, text="Siguiente ➡️", width=120, fg_color="#334155", hover_color="#475569", command=lambda: cambiar_pagina(1)).pack(side="right", padx=30)
    
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

def cargar_categoria_android():
    import urllib.request, json, time, webbrowser
    global app
    limpiar_panel()
    
    # Título temático
    ctk.CTkLabel(tools_frame, text="🤖 Aplicaciones y APKs para Android", font=("Arial", 24, "bold")).pack(pady=(0, 20), anchor="w")

    # Descarga e inyección del catálogo JSON
    url_android = f"https://raw.githubusercontent.com/LennesVP/Encyclopedia-of-Tools/main/android.json?t={time.time()}"
    try:
        req = urllib.request.Request(url_android, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
        respuesta = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        datos_android = json.loads(respuesta)
    except Exception as e:
        ctk.CTkLabel(tools_frame, text=f"Error al conectar con la Nube:\n{e}", text_color="#FF4444").pack(pady=20)
        return

    if not datos_android:
        ctk.CTkLabel(tools_frame, text="El catálogo de Android está vacío.", text_color="#AAAAAA").pack(pady=20)
        return

    # --- RENDERIZADO DE TARJETAS DESLIZABLES ---
    for item in datos_android:
        tarjeta = ctk.CTkFrame(tools_frame, fg_color="#1E293B", corner_radius=10, border_width=1, border_color="#3DDC84")
        tarjeta.pack(fill="x", pady=10, padx=10)

        header_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        ctk.CTkLabel(header_frame, text=item.get('nombre', ''), font=("Arial", 18, "bold"), text_color="#3DDC84").pack(side="left")
        
        badge_text = "🔓 Código Abierto (Open Source)" if item.get('es_open_source', False) else "🔒 Código Cerrado"
        badge_color = "#10B981" if item.get('es_open_source', False) else "#EF4444"
        ctk.CTkLabel(header_frame, text=f"  |  Autor: {item.get('autor', '')}  |  {badge_text}", font=("Arial", 12, "italic"), text_color=badge_color).pack(side="left", padx=10)

        ctk.CTkLabel(tarjeta, text=item.get('descripcion', ''), font=("Arial", 14), justify="left", wraplength=700).pack(padx=20, pady=5, anchor="w")
        
        ctk.CTkLabel(tarjeta, text="Características y Funciones:", font=("Arial", 12, "bold"), text_color="#94A3B8").pack(padx=20, pady=(10, 0), anchor="w")
        ctk.CTkLabel(tarjeta, text=item.get('ventajas', ''), font=("Arial", 13), justify="left", wraplength=700).pack(padx=20, pady=(5, 15), anchor="w")

        def abrir_repo(url=item.get('enlace', '')):
            webbrowser.open(url)
        
        ctk.CTkButton(tarjeta, text="🌐 Ver Repositorio y Release Oficial", font=("Arial", 14, "bold"), height=40, fg_color="#3DDC84", hover_color="#2EB86A", text_color="#000000", command=abrir_repo).pack(padx=20, pady=(0, 15), anchor="e")
        
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

ctk.CTkButton(sidebar, text="🐧 Linux", font=("Arial", 14, "bold"), fg_color="transparent", border_width=1, command=lambda: cargar_placeholder("Linux")).pack(pady=2, padx=10, fill="x")
ctk.CTkButton(sidebar, text="🍏 Mac", font=("Arial", 14, "bold"), fg_color="transparent", border_width=1, command=lambda: cargar_placeholder("Mac")).pack(pady=2, padx=10, fill="x")
ctk.CTkButton(sidebar, text="🤖 Android", font=("Arial", 14, "bold"), fg_color="transparent", border_width=1, command=cargar_categoria_android).pack(pady=2, padx=10, fill="x")
ctk.CTkButton(sidebar, text="📱 iOS", font=("Arial", 14, "bold"), fg_color="transparent", border_width=1, command=lambda: cargar_placeholder("iOS")).pack(pady=2, padx=10, fill="x")

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