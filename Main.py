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
VERSION_ACTUAL = "2.0"

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
# 1. CONFIGURACIÓN DEL TEMA
# ============================================================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1150x750")
app.title("TREMEND Toolkit V2 [ESTABLE Y BLINDADO]")

# ============================================================================
# 2. MOTOR DE TERMINAL NATIVA Y EJECUCIÓN (SEGURO CONTRA CRASHES)
# ============================================================================
def abrir_consola_y_ejecutar(titulo, funcion_python_nativa):
    global app
    win_term = ctk.CTkToplevel(app)
    win_term.title(titulo)
    win_term.geometry("950x600")
    
    # CORRECCIÓN: Quitamos el '-topmost' y usamos 'transient' y 'focus_force'
    # Esto mantiene la consola a la vista, pero permite que MAS y GridView salgan al frente
    win_term.transient(app)
    win_term.focus_force()
    
    txt_consola = ctk.CTkTextbox(win_term, width=930, height=580, fg_color="#0A0A0A", text_color="#00FFCC", font=("Consolas", 13))
    txt_consola.pack(padx=10, pady=10)
    txt_consola.insert("end", f"[*] {titulo}\n")
    txt_consola.insert("end", "="*85 + "\n")
    txt_consola.configure(state="disabled")

    # Inyección de seguridad (app.after) para que procesos pesados no congelen la ventana
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

def logica_wifi_forense(log):
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

def logica_dns_cloudflare(log):
    log("\n[*] Inyectando DNS de Cloudflare (1.1.1.1) en todos los adaptadores activos...")
    run_ps_script(log, 'Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | Set-DnsClientServerAddress -ServerAddresses ("1.1.1.1", "1.0.0.1")')
    log("[+] DNS optimizados con éxito para máxima velocidad.")

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

# ============================================================================
# 4. INTERFAZ GRÁFICA Y SISTEMA DE CATEGORÍAS
# ============================================================================
sidebar = ctk.CTkFrame(app, width=240, corner_radius=0)
sidebar.pack(side="left", fill="y")

main_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
main_frame.pack(side="right", fill="both", expand=True)

tools_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
tools_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

preview_frame = ctk.CTkFrame(main_frame, width=350, corner_radius=10, border_width=2, border_color="#444444")
preview_frame.pack(side="right", fill="y", padx=20, pady=20)
preview_frame.pack_propagate(False)

lbl_preview_titulo = ctk.CTkLabel(preview_frame, text="VISTA PREVIA", font=("Arial", 20, "bold"), text_color="#444444")
lbl_preview_titulo.pack(pady=(20, 15))

lbl_novato_texto = ctk.CTkLabel(preview_frame, text="Pasa el cursor sobre una herramienta.", font=("Arial", 12), wraplength=300, justify="left")
lbl_novato_texto.pack(anchor="w", padx=15, pady=5)

lbl_experto_texto = ctk.CTkLabel(preview_frame, text="Esperando selección...", font=("Arial", 12), wraplength=300, justify="left")
lbl_experto_texto.pack(anchor="w", padx=15, pady=5)

def on_enter(event, titulo, txt_novato, txt_experto):
    preview_frame.configure(border_color="#00FFCC")
    lbl_preview_titulo.configure(text=titulo, text_color="#00FFCC")
    lbl_novato_texto.configure(text="🟢 Novato: " + txt_novato)
    lbl_experto_texto.configure(text="🔴 Experto: " + txt_experto)

def on_leave(event):
    preview_frame.configure(border_color="#444444")
    lbl_preview_titulo.configure(text="VISTA PREVIA", text_color="#444444")
    lbl_novato_texto.configure(text="Pasa el cursor sobre una herramienta.")
    lbl_experto_texto.configure(text="Esperando selección...")

def limpiar_panel():
    for widget in tools_frame.winfo_children(): widget.destroy()

def crear_boton_herramienta(texto, comando_python, tit_prev, txt_nov, txt_exp):
    btn = ctk.CTkButton(tools_frame, text=texto, height=45, font=("Arial", 14), fg_color="#1E3A8A", hover_color="#2563EB", command=lambda: abrir_consola_y_ejecutar(tit_prev, comando_python))
    btn.pack(fill="x", pady=5)
    btn.bind("<Enter>", lambda e: on_enter(e, tit_prev, txt_nov, txt_exp))
    btn.bind("<Leave>", on_leave)

# === VISTAS DE LAS CATEGORÍAS ===
def cargar_categoria_redes():
    global app
    limpiar_panel()
    ctk.CTkLabel(tools_frame, text="🌐 Redes e Internet", font=("Arial", 24, "bold")).pack(pady=(0, 20), anchor="w")
    
    # --- CUADROS DE DIÁLOGO ---
    def btn_ping():
        dest = simpledialog.askstring("Ping", "Ingresa IP o Dominio a escanear:", parent=app)
        if dest:
            puerto = simpledialog.askstring("TCP", "Puerto TCP (Opcional, vacío para normal):", parent=app)
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
        ip = simpledialog.askstring("Escáner", "Ingresa la IP de la máquina a auditar (ej. 192.168.1.1):", parent=app)
        if ip: abrir_consola_y_ejecutar("ESCANER NMAP", lambda log: logica_escaner_puertos_python(log, ip))
        
    def btn_nas():
        ruta = simpledialog.askstring("Servidor NAS", "Ruta de la carpeta (ej. C:\\Trabajo):", parent=app)
        if ruta:
            nombre = simpledialog.askstring("Servidor NAS", "Nombre para el recurso en red:", parent=app)
            if nombre: abrir_consola_y_ejecutar("NAS", lambda log: logica_crear_nas(log, ruta, nombre))

    def btn_latencia():
        dest = simpledialog.askstring("Latencia", "Ingresa dominio para medir (ej. google.com):", parent=app)
        if dest: abrir_consola_y_ejecutar("LATENCIA", lambda log: logica_auditoria_latencia(log, dest))

    # --- RENDEREIZADO DE BOTONES ---
    crear_boton_herramienta("1. Info Básica de Red e IP", logica_info_red, "INFO DE RED", "Muestra IP local y pública.", "[Autor: Python / MS] Usa Sockets nativos y consulta API externa para ignorar NAT.")
    crear_boton_herramienta("2. Reparación Total de Red", logica_reparacion_red, "REPARAR RED", "Arregla internet cuando falla.", "[Autor: Microsoft OS] Ejecuta FlushDNS, Winsock Reset e IP Renew.")
    
    b3 = ctk.CTkButton(tools_frame, text="3. Prueba de Conectividad (Ping / TCP)", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_ping); b3.pack(fill="x", pady=5)
    b3.bind("<Enter>", lambda e: on_enter(e, "PING Y TCP", "Verifica si un servidor responde.", "[Autor: Microsoft OS] Ejecuta Test-NetConnection evadiendo bloqueos ICMP.")); b3.bind("<Leave>", on_leave)

    crear_boton_herramienta("4. Monitor Conexiones TCP", logica_conexiones_tcp, "MONITOR TCP", "Mira quién usa red.", "[Autor: Microsoft OS] Get-NetTCPConnection filtrado por Estado Establecido.")
    
    b5 = ctk.CTkButton(tools_frame, text="5. Identificar Proceso por Puerto", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_puerto_proceso); b5.pack(fill="x", pady=5)
    b5.bind("<Enter>", lambda e: on_enter(e, "RASTREO PUERTO", "Qué bloquea un puerto.", "[Autor: Microsoft OS] Cruza Get-NetTCPConnection con PID en Get-Process.")); b5.bind("<Leave>", on_leave)

    crear_boton_herramienta("6. Extractor Forense Wi-Fi", logica_wifi_forense, "WI-FI FORENSE", "Contraseñas guardadas.", "[Autor: Microsoft OS] Subprocess de netsh wlan parseando llave en texto claro.")
    
    b7 = ctk.CTkButton(tools_frame, text="7. Código QR para Wi-Fi", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_qr_wifi); b7.pack(fill="x", pady=5)
    b7.bind("<Enter>", lambda e: on_enter(e, "QR WI-FI", "Crea código QR de conexión.", "[Autor: goqr.me API] Ensambla URI WPA y descarga archivo codificado PNG.")); b7.bind("<Leave>", on_leave)

    crear_boton_herramienta("8. Geolocalizar IP", logica_geolocalizar_ip, "GEOLOCALIZACIÓN", "Ciudad de tu conexión.", "[Autor: ip-api.com] Petición REST extrayendo Latitud y ASN.")
    crear_boton_herramienta("9. Diagnóstico Wi-Fi (WlanReport)", logica_reporte_wifi, "REPORTE WI-FI", "Reporte de caídas de red.", "[Autor: Microsoft OS] Motor ETW compilando eventos en HTML oculto.")
    
    b10 = ctk.CTkButton(tools_frame, text="10. Resolución DNS", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_dns_res); b10.pack(fill="x", pady=5)
    b10.bind("<Enter>", lambda e: on_enter(e, "RESOLVER DNS", "Descubre la IP de una web.", "[Autor: Microsoft OS] Interroga servidores raíz mediante Resolve-DnsName.")); b10.bind("<Leave>", on_leave)
    
    b11 = ctk.CTkButton(tools_frame, text="11. Bloqueador de Webs (Hosts)", height=45, fg_color="#1E3A8A", hover_color="#880000", command=btn_bloquear_web); b11.pack(fill="x", pady=5)
    b11.bind("<Enter>", lambda e: on_enter(e, "BLOQUEO WEB", "Bloquea páginas con loopback.", "[Autor: OS Base] Sinkhole inyectado directamente en drivers/etc/hosts.")); b11.bind("<Leave>", on_leave)

    b12 = ctk.CTkButton(tools_frame, text="12. Abrir Puertos Firewall", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_abrir_puerto); b12.pack(fill="x", pady=5)
    b12.bind("<Enter>", lambda e: on_enter(e, "FIREWALL REGLA", "Abre paso en Firewall.", "[Autor: Microsoft OS] Inyección de directivas Inbound vía netsh.")); b12.bind("<Leave>", on_leave)

    crear_boton_herramienta("13. Purgar Historial Wi-Fi", logica_purgar_wifi_historial, "PURGAR WI-FI", "Borra todas las redes memorizadas.", "[Autor: Microsoft OS] Ejecuta profile name=* i=* en netsh.")
    crear_boton_herramienta("14. Reset Firewall a Fábrica", logica_reset_firewall, "RESET FIREWALL", "Limpia bloqueos de terceros.", "[Autor: Microsoft OS] Advfirewall reset destruyendo GPOs externas.")
    crear_boton_herramienta("15. Purgar Caché ARP", logica_limpiar_arp, "PURGAR ARP", "Fuerza re-descubrimiento de la red.", "[Autor: Protocolo ARP] Eliminación de enrutamiento estático local.")
    crear_boton_herramienta("16. Optimizar DNS (Cloudflare)", logica_dns_cloudflare, "DNS CLOUDFLARE", "Acelera internet con DNS globales.", "[Autor: Cloudflare Inc] Set-DnsClientServerAddress inyectando 1.1.1.1.")
    
    # --- LAS NUEVAS INYECCIONES ---
    crear_boton_herramienta("17. Gestionar Sesiones SMB", logica_sesiones_smb, "SESIONES SMB", "Mira quién está en tu red corporativa.", "[Autor: Microsoft OS] Enumera sesiones SMB activas extrayendo ClientUserName.")
    crear_boton_herramienta("18. Radar Wi-Fi en Tiempo Real", logica_radar_wifi, "RADAR WI-FI", "Busca puntos ciegos en la señal Wi-Fi.", "[Autor: Microsoft OS] Loop BSSID leyendo espectro de radiofrecuencia local.")
    
    b19 = ctk.CTkButton(tools_frame, text="19. Auditoría de Latencia (Microcortes)", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_latencia); b19.pack(fill="x", pady=5)
    b19.bind("<Enter>", lambda e: on_enter(e, "LATENCIA", "Busca caídas de internet con reloj.", "[Autor: Python] Loop ICMP acoplado a datetime nativo evaluando Timeout.")); b19.bind("<Leave>", on_leave)

    b20 = ctk.CTkButton(tools_frame, text="20. Motor Avanzado de Escaneo (Puertos)", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_escaner); b20.pack(fill="x", pady=5)
    b20.bind("<Enter>", lambda e: on_enter(e, "ESCÁNER PUERTOS", "Escanea vulnerabilidades en una IP.", "[Autor: Lennes Varela] Algoritmo Python Sockets para escaneo asíncrono.")); b20.bind("<Leave>", on_leave)

    b21 = ctk.CTkButton(tools_frame, text="21. Crear Servidor NAS Compartido", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_nas); b21.pack(fill="x", pady=5)
    b21.bind("<Enter>", lambda e: on_enter(e, "SERVIDOR NAS", "Comparte una carpeta en la red LAN.", "[Autor: Microsoft OS] Implementa New-SmbShare y altera el Firewall.")); b21.bind("<Leave>", on_leave)

    crear_boton_herramienta("22. Auditar Caché DNS (DisplayDNS)", logica_auditar_cache_dns, "AUDITAR DNS", "Mira a qué webs se conectó tu PC.", "[Autor: Microsoft OS] Vuelca el buffer del cliente DNS local a la consola.")

def cargar_categoria_mantenimiento():
    limpiar_panel()
    ctk.CTkLabel(tools_frame, text="🧹 Mantenimiento y Optimización", font=("Arial", 24, "bold")).pack(pady=(0, 20), anchor="w")
    
    def btn_debloat():
        app_name = simpledialog.askstring("Debloat", "App a eliminar (ej. xbox, zune, bing):", parent=app)
        if app_name: abrir_consola_y_ejecutar("DEBLOAT", lambda log: logica_debloat(log, app_name))

    def btn_chkdsk():
        letra = simpledialog.askstring("CHKDSK", "Letra de unidad a reparar (ej. C):", parent=app)
        if letra: abrir_consola_y_ejecutar("CHKDSK", lambda log: logica_chkdsk(log, letra))

    t_mant_n = "Realiza una limpieza automática y profunda. Elimina gigas de basura oculta en carpetas temporales, lanza el liberador de espacio y verifica que ningún archivo vital de Windows esté dañado, reparándolo automáticamente si es necesario."
    t_mant_e = "[Autor: Microsoft OS / Python] Ejecuta una limpieza recursiva mediante 'shutil.rmtree' en variables TEMP y Prefetch. Posteriormente invoca los motores DISM (/RestoreHealth) y SFC (/scannow) para validar y descargar componentes corruptos de la imagen del sistema base."
    crear_boton_herramienta("1. Mantenimiento Profundo y SFC/DISM", logica_mantenimiento_profundo, "MANTENIMIENTO", t_mant_n, t_mant_e)

    t_titus_n = "La mejor herramienta del mundo para acelerar computadoras lentas. Abre un panel avanzado que te permite desactivar funciones inútiles de Windows con un solo clic, instalando programas esenciales y mejorando el rendimiento en juegos."
    t_titus_e = "[Autor: Chris Titus Tech] Invoca el script remoto de optimización a través de 'irm christitus.com/win | iex'. Despliega una interfaz gráfica en PowerShell (WPF) que aplica tweaks de registro (MicroWin), deshabilita servicios innecesarios y optimiza procesos de red."
    crear_boton_herramienta("2. Optimización Avanzada (Chris Titus)", logica_titus, "OPTIMIZACIÓN TITUS", t_titus_n, t_titus_e)
    
    t_deb_n = "Elimina de raíz esos programas basura que vienen preinstalados en Windows (como Xbox, Zune, o publicidad) que no se pueden desinstalar normalmente desde el panel de control. Acelera el arranque y limpia el menú de inicio."
    t_deb_e = "[Autor: Microsoft OS] Emplea el cmdlet 'Get-AppxPackage' filtrando mediante comodines el string ingresado, canalizando el output hacia 'Remove-AppxPackage -AllUsers'. Purga paquetes provisionados UWP (Universal Windows Platform) del registro base."
    b3 = ctk.CTkButton(tools_frame, text="3. Debloat del Sistema (Apps Nativas)", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_debloat); b3.pack(fill="x", pady=5)
    b3.bind("<Enter>", lambda e: on_enter(e, "DEBLOAT", t_deb_n, t_deb_e)); b3.bind("<Leave>", on_leave)

    t_sp_n = "Soluciona de inmediato el problema clásico cuando mandas a imprimir un documento y la impresora se queda atascada sin hacer nada. Destruye los trabajos trabados y reinicia la comunicación con la impresora."
    t_sp_e = "[Autor: Microsoft OS] Detiene el servicio Spooler. Purga recursivamente los archivos de caché .SHD y .SPL del directorio System32\\Spool\\Printers, liberando el buffer bloqueado, y restablece el servicio para forzar la reenumeración de colas."
    crear_boton_herramienta("4. Restablecer Cola Impresión", logica_spooler, "REPARAR IMPRESIÓN", t_sp_n, t_sp_e)

    t_wx_n = "Libera una cantidad masiva de disco duro (a veces más de 10 GB) eliminando copias de seguridad de actualizaciones viejas de Windows. Advertencia: tras usarlo, no podrás desinstalar actualizaciones pasadas."
    t_wx_e = "[Autor: Microsoft OS] Ejecuta 'DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase'. Consolida todos los componentes del sistema (WinSxS) reemplazando la línea base, lo que impide el rollback a versiones previas pero minimiza el footprint drásticamente."
    crear_boton_herramienta("5. Limpieza Extrema WinSxS", logica_winsxs, "LIMPIEZA WINSXS", t_wx_n, t_wx_e)

    t_up_n = "Arregla el problema crítico cuando Windows Update se queda trabado en 'Descargando 0%' y no avanza. Borra el catálogo corrupto de descargas para que el sistema empiece a bajar las actualizaciones desde cero."
    t_up_e = "[Autor: Microsoft OS] Detiene los servicios criptográficos (wuauserv, cryptSvc, bits). Renombra los directorios SoftwareDistribution y catroot2 a '.old'. Al reiniciar los demonios, el motor de actualización regenera bases de datos limpias."
    crear_boton_herramienta("6. Reparar Windows Update", logica_reparar_update, "REPARAR UPDATE", t_up_n, t_up_e)

    t_vss_n = "Borra copias de seguridad de Windows muy antiguas (Puntos de Restauración) que consumen espacio oculto en tu disco duro sin que te des cuenta. Es completamente seguro si tu PC funciona bien actualmente."
    t_vss_e = "[Autor: Microsoft OS] Invoca el gestor nativo de instantáneas de volumen (VSS) mediante 'vssadmin delete shadows /all /quiet'. Purga registros inactivos y shadow copies asignadas por el sistema operativo, recuperando gigabytes de espacio."
    crear_boton_herramienta("7. Purgar Puntos Restauración", logica_shadowcopies, "BORRAR VSS", t_vss_n, t_vss_e)

    t_wmi_n = "Arregla errores graves en la computadora cuando los programas no pueden leer la información de tu PC (por ejemplo, cuando no te muestra cuánta batería tienes o no se abre la información del sistema)."
    t_wmi_e = "[Autor: Microsoft OS] Diagnóstico y reparación del Instrumental de Administración de Windows (WMI). Detiene winmgmt, ejecuta la bandera '/resetrepository' para reconstruir los archivos CIM averiados y relanza el servicio principal."
    crear_boton_herramienta("8. Reparar Repositorio WMI", logica_wmi, "REPARAR WMI", t_wmi_n, t_wmi_e)

    t_tel_n = "Evita que Windows envíe información privada sobre cómo usas tu computadora a los servidores de Microsoft. Mejora el rendimiento de tu internet y cuida tu privacidad al máximo apagando estos reportes."
    t_tel_e = "[Autor: Lennes Varela / GPO Base] Fuerza la detención del servicio de rastreo DiagTrack. Modifica la directiva de grupo (Registry) DataCollection, estableciendo la llave DWORD AllowTelemetry en 0, cortando el tráfico saliente de recolección de Microsoft."
    crear_boton_herramienta("9. Bloquear Telemetría Microsoft", logica_telemetria, "BLOQUEO TELEMETRÍA", t_tel_n, t_tel_e)

    t_ntp_n = "Soluciona el temido error 'La conexión no es privada' en las páginas web, que suele ocurrir cuando la hora de tu computadora está atrasada. Obliga a tu PC a sincronizar la hora exacta con los servidores mundiales."
    t_ntp_e = "[Autor: Microsoft OS] Reinicia el servicio Time Broker (w32time). Modifica el peerlist forzando la sincronización SNTP contra el servidor maestro 'time.windows.com', seguido de un '/resync /force' para reajustar el reloj RTC físico de la motherboard."
    crear_boton_herramienta("10. Reparar Hora (NTP)", logica_hora, "REPARAR HORA", t_ntp_n, t_ntp_e)

    t_nav_n = "Acelera tus navegadores borrando archivos basura temporales que vuelven lenta la navegación. Es totalmente seguro: no borrará tus contraseñas guardadas, ni tu historial, ni tus marcadores, solo los archivos caché pesados."
    t_nav_e = "[Autor: Python shutil] Mapea dinámicamente las variables de entorno %LOCALAPPDATA% del sistema. Itera de forma recursiva destruyendo los directorios 'Cache_Data' de motores Chromium (Chrome, Edge, Brave) evadiendo bloqueos de acceso."
    crear_boton_herramienta("11. Limpiar Navegadores (Caché)", logica_limpiar_navegadores, "PURGAR NAVEGADORES", t_nav_n, t_nav_e)

    t_chk_n = "Repara sectores dañados físicamente en tu disco duro. Si la computadora está extremadamente lenta o lanza errores al intentar copiar un archivo, esta función bloqueará las zonas dañadas del disco para salvar el sistema."
    t_chk_e = "[Autor: Microsoft OS] Interfaz para la utilidad CheckDisk. Programa una ejecución estructurada de 'chkdsk /f /r /x' en el volumen indicado. Fuerza el desmontaje de inodos y mapea sectores defectuosos trasladando la data recuperable a sectores sanos."
    b12 = ctk.CTkButton(tools_frame, text="12. Reparación Disco (CHKDSK)", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_chkdsk); b12.pack(fill="x", pady=5)
    b12.bind("<Enter>", lambda e: on_enter(e, "CHKDSK", t_chk_n, t_chk_e)); b12.bind("<Leave>", on_leave)

    t_ico_n = "Soluciona ese fallo visual fastidioso donde los iconos de tus programas en el escritorio aparecen como hojas en blanco o se ven borrosos. Resetea los gráficos del sistema y todo vuelve a la normalidad en un segundo."
    t_ico_e = "[Autor: Microsoft OS] Interrupción táctica del Shell de Windows. Destruye la interfaz de usuario (explorer.exe), localiza y purga el archivo base de datos de iconos 'IconCache.db' en el directorio oculto, y relanza el Shell forzando un renderizado nuevo."
    crear_boton_herramienta("13. Reconstruir Caché de Iconos", logica_iconos, "REPARAR ICONOS", t_ico_n, t_ico_e)

def cargar_categoria_diagnostico():
    limpiar_panel()
    ctk.CTkLabel(tools_frame, text="🖥️ Diagnóstico e Info del Sistema", font=("Arial", 24, "bold")).pack(pady=(0, 20), anchor="w")
    
    def btn_perfmon():
        op = simpledialog.askstring("Monitor", "1. Monitor | 2. Reporte", parent=app)
        if op in ['1', '2', '01', '02']: abrir_consola_y_ejecutar("PERFMON", lambda log: logica_perfmon(log, op))

    def btn_visor():
        op = simpledialog.askstring("Visor", "1. Procesos | 2. Servicios | 3. Errores", parent=app)
        if op in ['1', '2', '3']: abrir_consola_y_ejecutar("VISOR GRÁFICO", lambda log: logica_visor_grafico(log, op))

    t_rap_n = "Muestra un resumen inmediato de tu computadora y verifica si el sistema operativo le ha dado una buena calificación de rendimiento general a tus componentes físicos."
    t_rap_e = "[Autor: Microsoft OS] Invoca systeminfo extraído mediante CLI y complementa la salida evaluando la clase WMI 'Win32_WinSat', exponiendo la calificación formal de la Evaluación de la Experiencia de Windows (WinEI)."
    crear_boton_herramienta("1. Diagnóstico Rápido (HW)", logica_diagnostico_rapido, "INFO RÁPIDA", t_rap_n, t_rap_e)

    t_hw_n = "Genera el informe más completo y detallado posible sobre las piezas de tu computadora. Te dice la marca de tu placa madre, modelo de procesador, y exactamente cuánta memoria RAM y ranuras tienes conectadas."
    t_hw_e = "[Autor: Lennes Varela / CIM] Ejecuta un volcado CIM masivo canalizado. Interroga Win32_BaseBoard, Processor y VideoController. Parsea el array PhysicalMemory para iterar la capacidad, velocidad y part number de cada módulo DIMM instalado en placa."
    crear_boton_herramienta("2. Radiografía Completa HW", logica_radiografia_hardware_completa, "RADIOGRAFÍA HW", t_hw_n, t_hw_e)

    t_hdd_n = "Lee los sensores internos ocultos de tus discos duros o unidades de estado sólido (SSD) para avisarte a tiempo si están sanos o si están a punto de dañarse y debes hacer una copia de seguridad urgente."
    t_hdd_e = "[Autor: Microsoft OS] Parsea el firmware físico a través del cmdlet 'Get-PhysicalDisk'. Evalúa la variable HealthStatus y OperationalStatus extraída de los microcontroladores S.M.A.R.T. determinando la vida útil restante de los inodos."
    crear_boton_herramienta("3. Salud Física Discos (S.M.A.R.T)", logica_salud_discos, "SALUD DE DISCOS", t_hdd_n, t_hdd_e)
    
    t_pfm_n = "Abre un historial visual interactivo con gráficas que te dice exactamente qué día, a qué hora y por qué falló un programa, o por qué la computadora se reinició inesperadamente la semana pasada."
    t_pfm_e = "[Autor: Microsoft OS] Ejecuta 'perfmon /rel' para abrir el Monitor de Confiabilidad de Windows, el cual tabula crasheos de aplicaciones, fallos de hardware y problemas de Windows Update utilizando una escala de índice de estabilidad de 1 a 10."
    b4 = ctk.CTkButton(tools_frame, text="4. Monitor de Confiabilidad", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_perfmon); b4.pack(fill="x", pady=5)
    b4.bind("<Enter>", lambda e: on_enter(e, "PERFMON", t_pfm_n, t_pfm_e)); b4.bind("<Leave>", on_leave)

    t_vis_n = "Muestra una tabla avanzada (tipo Excel) para ver exactamente qué procesos, servicios o errores recientes están corriendo en tu PC. Puedes filtrar la tabla para buscar algo específico rápidamente."
    t_vis_e = "[Autor: Microsoft OS] Redirige el pipeline de salida de Get-Process, Get-Service o Get-EventLog hacia la interfaz interactiva 'Out-GridView'. Permite ordenamiento de memoria y filtrado en tiempo real sin saturar la consola CLI estándar."
    b5 = ctk.CTkButton(tools_frame, text="5. Visor Gráfico (GridView)", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_visor); b5.pack(fill="x", pady=5)
    b5.bind("<Enter>", lambda e: on_enter(e, "VISOR GRIDVIEW", t_vis_n, t_vis_e)); b5.bind("<Leave>", on_leave)

    t_upt_n = "Calcula con precisión cronométrica cuántos días, horas y minutos lleva encendida tu computadora sin apagarse realmente. Muy útil para descubrir si la opción de 'Inicio Rápido' te está engañando."
    t_upt_e = "[Autor: Microsoft OS] Resta el valor LastBootUpTime (extraído asincrónicamente de Win32_OperatingSystem) contra el timestamp del sistema actual. Revela el falso apagado de Windows asociado a la hibernación del kernel S4."
    crear_boton_herramienta("6. Tiempo de Actividad (Uptime)", logica_uptime, "UPTIME", t_upt_n, t_upt_e)

    t_aud_n = "Te muestra qué programas o mantenimientos están ejecutándose silenciosamente en el fondo de tu PC como tareas programadas sin que te des cuenta. Ideal para auditar lentitud inexplicable."
    t_aud_e = "[Autor: Microsoft OS] Extrae la tabla de ejecución de 'schtasks' en formato tabular y realiza un pipe estructurado en Get-Service aislando exclusivamente los daemons cuyo System Status equivale a 'Running'."
    crear_boton_herramienta("7. Auditar Tareas y Servicios", logica_tareas_servicios, "AUDITAR TAREAS", t_aud_n, t_aud_e)

    t_arr_n = "Descubre exactamente qué programas están configurados para abrirse apenas enciendes tu computadora. Si tu PC tarda 3 minutos en mostrar el escritorio, el culpable se encuentra en esta lista."
    t_arr_e = "[Autor: Microsoft OS] Evalúa las ramas de registro HKLM/HKCU asociadas al Run, RunOnce y Startup a través del wrapper WMI 'Win32_StartupCommand'. Mapea el binario ejecutable y su ruta para análisis de persistencia."
    crear_boton_herramienta("8. Auditar Arranque de Windows", logica_programas_arranque, "AUDITAR ARRANQUE", t_arr_n, t_arr_e)

    t_usb_n = "Muestra una lista forense de todos los pendrives, celulares y discos externos que se han conectado en esta PC en el pasado, revelando el nombre de los dispositivos aunque ya no estén conectados."
    t_usb_e = "[Autor: Lennes Varela] Extrae y parsea el registro de dispositivos Plug and Play (PnP) persistentes. Itera sobre las llaves HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR para revelar el FriendlyName del hardware de almacenamiento acoplado."
    crear_boton_herramienta("9. Historial Forense de USBs", logica_historial_usb, "HISTORIAL USB", t_usb_n, t_usb_e)

    t_bsod_n = "Si tu computadora se reinicia sola y muestra la pantalla azul de la muerte, esta herramienta extrae de la memoria el código de error exacto para que sepas qué pieza física está dañada."
    t_bsod_e = "[Autor: Microsoft OS] Interroga el visor de eventos del sistema (EventLog). Filtra por System Logs cuyo originador sea la firma 'BugCheck'. Extrae el volcado en crudo asociado a pánicos del kernel por interrupciones de hardware o fallos de paginación."
    crear_boton_herramienta("10. Auditoría de BSOD (Pantallazos)", logica_pantallazos_azules, "BSOD", t_bsod_n, t_bsod_e)

    t_bat_n = "Calcula la salud real de la batería de tu laptop. Genera un reporte web muy profesional que te muestra de cuántos miliamperios era tu batería en la fábrica, y cuánta vida útil física le queda actualmente."
    t_bat_e = "[Autor: Microsoft OS] Inyecta comandos ACPI en el controlador de energía. Genera un archivo HTML utilizando 'powercfg /batteryreport' el cual interpola el Full Charge Capacity vs el Design Capacity arrojando el Wear Level estructural."
    crear_boton_herramienta("11. Reporte Físico de Batería", logica_bateria, "REPORTE BATERÍA", t_bat_n, t_bat_e)

    t_slp_n = "Si tu laptop sufre del molesto problema de descargarse por completo estando guardada en la mochila o 'suspendida', aquí verás qué programa está manteniendo encendido el procesador en la sombra."
    t_slp_e = "[Autor: Microsoft OS] Analiza los estados S0 Modern Standby generando un volcado 'powercfg /SleepStudy'. Expone el Active-State Power Management (ASPM) y localiza fugas de energía causadas por adaptadores de red o controladores SoC."
    crear_boton_herramienta("12. Reporte de Suspensión (S0)", logica_sleepstudy, "SLEEPSTUDY", t_slp_n, t_slp_e)

    t_bit_n = "Revisa rápidamente si el disco duro de tu computadora está encriptado con contraseña militar. Si lo está y olvidas la clave o conectas el disco en otra PC, perderás toda tu información para siempre."
    t_bit_e = "[Autor: Microsoft OS] Verifica el estado del algoritmo AES en los volúmenes montados llamando a la consola de administración 'manage-bde -status'. Revela el porcentaje de encripción y el método de desbloqueo TPM asociado al chip físico."
    crear_boton_herramienta("13. Estado de Cifrado BitLocker", logica_bitlocker, "BITLOCKER", t_bit_n, t_bit_e)

    t_usr_n = "Lista todas las cuentas de usuario registradas en la computadora y te indica en qué fecha y hora exacta se conectaron por última vez al sistema operativo."
    t_usr_e = "[Autor: Microsoft OS] Extrae la base de datos de cuentas locales (SAM - Security Accounts Manager) ejecutando Get-LocalUser. Retorna los estados Booleanos (Enabled) y el timestamp del LastLogon de las sesiones locales."
    crear_boton_herramienta("14. Auditoría de Usuarios Locales", logica_usuarios_locales, "USUARIOS LOCALES", t_usr_n, t_usr_e)

    t_ser_n = "Copia al portapapeles automáticamente el número de serie de fábrica y el modelo exacto de tu computadora. Es indispensable para buscar drivers en internet o pedir soporte de garantía al fabricante."
    t_ser_e = "[Autor: Microsoft OS] Consulta el WMI class Win32_ComputerSystemProduct. Extrae el atributo 'IdentifyingNumber', un identificador hexadecimal embebido en la BIOS por el Vendor OEM, y transfiere el hash resultante directamente al portapapeles."
    crear_boton_herramienta("15. Extraer Número de Serie (PC)", logica_numero_serie, "NÚMERO DE SERIE", t_ser_n, t_ser_e)

    t_gh_n = "La mejor defensa contra hackers. Algunos virus no se guardan en el disco duro, sino que se inyectan directamente en la memoria RAM de tu computadora volviéndose invisibles. Esta herramienta escanea tu memoria buscando infecciones silenciosas."
    t_gh_e = "[Autor: pandaadir05 - GitHub] Inyecta el motor forense 'Ghost' compilado en lenguaje Rust. Escanea mapeos de memoria de procesos localizando banderas RWX anómalas e hilos huérfanos. Detecta vectores de ataque como Process Hollowing y Code Cave injections en Ring 3."
    crear_boton_herramienta("16. Escáner Forense RAM (Ghost)", logica_memoria_ghost, "GHOST RAM", t_gh_n, t_gh_e)

def cargar_categoria_software():
    limpiar_panel()
    ctk.CTkLabel(tools_frame, text="📦 Software y Licencias", font=("Arial", 24, "bold")).pack(pady=(0, 20), anchor="w")
    
    txt_winget_nov = "Tener programas desactualizados es un riesgo de seguridad. Esta herramienta analiza todos los programas de tu computadora y los actualiza a su última versión oficial automáticamente, sin que tengas que descargar molestos instaladores manualmente."
    txt_winget_exp = "[Autor: Microsoft Corp] Invoca el gestor de paquetes nativo de Windows (Winget) mediante la terminal. Ejecuta un 'upgrade --all' con banderas silenciosas (--silent) aceptando términos de forma desatendida para parchear vulnerabilidades en segundo plano."
    crear_boton_herramienta("1. Actualizar Apps (Winget)", logica_gestor_winget, "WINGET UPGRADE", txt_winget_nov, txt_winget_exp)

    txt_clave_nov = "Si necesitas formatear tu PC pero perdiste la caja donde venía tu clave de Windows, esta herramienta escanea el chip de tu placa base y extrae la licencia original de fábrica para que nunca la pierdas."
    txt_clave_exp = "[Autor: Nativo Windows] Realiza una consulta directa a la tabla ACPI (MSDM) y lee la rama del registro 'SoftwareProtectionPlatform' extrayendo el valor 'BackupProductKeyDefault'. Identifica licencias OEM embebidas en el firmware UEFI."
    crear_boton_herramienta("2. Clave Original Windows", logica_clave_windows, "CLAVE WINDOWS", txt_clave_nov, txt_clave_exp)

    txt_csv_nov = "Ideal para empresas. Crea un documento Excel instantáneo en tu escritorio que contiene una lista perfecta y ordenada de absolutamente todos los programas que están instalados en tu computadora y sus respectivas versiones."
    txt_csv_exp = "[Autor: Nativo Python] Itera recursivamente las ramas 'Uninstall' del registro (HKLM y Wow6432Node) usando la librería 'winreg' de Python. Parsea los valores 'DisplayName' y exporta un array estructurado a formato CSV."
    crear_boton_herramienta("3. Inventario Software CSV", logica_inventario_software, "INVENTARIO CSV", txt_csv_nov, txt_csv_exp)

    txt_drivers_nov = "¿Vas a formatear un PC viejo y no tienes los discos de instalación? Esta opción clona los controladores de tu red, video y sonido actuales y los guarda en la carpeta C:\\RespaldoDrivers para que los restaures luego."
    txt_drivers_exp = "[Autor: Nativo Windows] Emplea la herramienta de mantenimiento de imágenes de despliegue (DISM). Ejecuta el comando '/export-driver' para volcar todos los archivos .inf, .sys y catálogos de terceros instalados actualmente en el host."
    crear_boton_herramienta("4. Respaldar Controladores", logica_respaldo_drivers, "CLONAR DRIVERS", txt_drivers_nov, txt_drivers_exp)

    txt_office_nov = "Descubre si tu instalación de Microsoft Word o Excel es original o si fue activada con programas piratas defectuosos. Ideal para auditar la legalidad del software en computadoras de oficina."
    txt_office_exp = "[Autor: Nativo Windows] Localiza el script de administración OSPP.VBS en los archivos de programa de Office 16. Lo invoca mediante cscript.exe pasando la bandera '/dstatus' para parsear los tickets KMS, MAK o Retail inyectados."
    crear_boton_herramienta("5. Auditar MS Office", logica_auditar_office, "AUDITAR OFFICE", txt_office_nov, txt_office_exp)

    txt_mas_nov = "Si Windows te pide activación, esta herramienta segura lo soluciona. Vincula una licencia digital permanente a tu placa madre, activando el sistema para siempre sin necesidad de descargar troyanos ni programas piratas."
    txt_mas_exp = "[Autor: massgravel / MAS] Llama a la herramienta open-source Microsoft Activation Scripts a través de Invoke-RestMethod. Inyecta tickets genuinos HWID en el servicio de protección de software sin modificar ni corromper archivos del sistema."
    crear_boton_herramienta("6. Activador de Windows (MAS)", logica_activador_mas, "ACTIVADOR MAS", txt_mas_nov, txt_mas_exp)

    txt_pnp_nov = "Si conectaste una impresora, una tarjeta gráfica o un mando y la computadora no lo reconoce, esta herramienta fuerza a Windows a escanear todos los puertos para encontrar piezas nuevas y prepararlas."
    txt_pnp_exp = "[Autor: Nativo Windows] Interacciona directamente con el administrador Plug and Play (PnP) mediante la utilidad pnputil. Ejecuta un '/scan-devices' para forzar una enumeración completa de hardware en el bus del sistema y solicitar drivers."
    crear_boton_herramienta("7. Escanear Hardware (PnP)", logica_escanear_pnp, "ESCANEO PNP", txt_pnp_nov, txt_pnp_exp)

def cargar_categoria_soporte():
    global app 
    limpiar_panel()
    ctk.CTkLabel(tools_frame, text="🛠️ Soporte Técnico y Utilidades", font=("Arial", 24, "bold")).pack(pady=(0, 20), anchor="w")
    
    # --- CUADROS DE DIÁLOGO NATIVOS ---
    def btn_destructor():
        ruta = simpledialog.askstring("Destructor", "Ruta EXACTA de la carpeta a destruir:", parent=app)
        if ruta: abrir_consola_y_ejecutar("DESTRUCTOR", lambda log: logica_destructor(log, ruta))
    
    def btn_cambiar_clave():
        usr = simpledialog.askstring("Usuario", "Nombre del usuario local a modificar:", parent=app)
        if usr:
            pwd = simpledialog.askstring("Clave", "Nueva clave (deja vacío para eliminarla):", parent=app)
            if pwd is not None: abrir_consola_y_ejecutar("GESTOR CLAVES", lambda log: logica_cambiar_clave(log, usr, pwd))
            
    def btn_ytdlp():
        # VENTANA 1: Pegar URL
        dialog_url = ctk.CTkToplevel(app)
        dialog_url.title("YouTube-DL - Paso 1: Enlace")
        dialog_url.geometry("550x200")
        dialog_url.attributes("-topmost", True)
        dialog_url.transient(app)
        
        ctk.CTkLabel(dialog_url, text="Ingresa el enlace (URL) del video o canción:", font=("Arial", 14)).pack(pady=(20, 5))
        entrada = ctk.CTkEntry(dialog_url, width=450)
        entrada.pack(pady=10)
        
        btn_frame = ctk.CTkFrame(dialog_url, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        def pegar_texto():
            try:
                entrada.delete(0, 'end')
                entrada.insert(0, dialog_url.clipboard_get())
            except: pass
            
        def procesar_url():
            url = entrada.get()
            if not url: return
            dialog_url.destroy()
            abrir_ventana_calidad(url) # Pasa al paso 2

        ctk.CTkButton(btn_frame, text="📋 Pegar Enlace", width=120, fg_color="#444444", hover_color="#666666", command=pegar_texto).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Siguiente", width=120, command=procesar_url).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancelar", width=120, fg_color="#880000", hover_color="#AA0000", command=dialog_url.destroy).pack(side="left", padx=5)

        def abrir_ventana_calidad(url):
            # VENTANA 2: Elegir Calidad
            dialog_cal = ctk.CTkToplevel(app)
            dialog_cal.title("YouTube-DL - Paso 2: Calidad")
            dialog_cal.geometry("450x250")
            dialog_cal.attributes("-topmost", True)
            dialog_cal.transient(app)
            
            ctk.CTkLabel(dialog_cal, text="Elige la calidad de descarga:", font=("Arial", 14, "bold")).pack(pady=(20, 15))
            
            def sel_calidad(cal):
                dialog_cal.destroy()
                if cal == '3':
                    # Si es MP3, descarga de una vez sin preguntar formato de video
                    abrir_consola_y_ejecutar("DESCARGADOR MEDIOS", lambda log: logica_ytdlp(log, url, '3', 'mp3'))
                else:
                    abrir_ventana_formato(url, cal) # Pasa al paso 3
                    
            ctk.CTkButton(dialog_cal, text="🌟 1. Máxima Calidad Posible (2K/4K/8K)", command=lambda: sel_calidad('1')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="📺 2. Calidad Full HD (1080p Estable)", command=lambda: sel_calidad('2')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_cal, text="🎵 3. Solo Audio (Música MP3)", fg_color="#107C41", hover_color="#0F5C30", command=lambda: sel_calidad('3')).pack(fill="x", padx=40, pady=15)

        def abrir_ventana_formato(url, calidad):
            # VENTANA 3: Elegir Formato de Video
            dialog_fmt = ctk.CTkToplevel(app)
            dialog_fmt.title("YouTube-DL - Paso 3: Formato")
            dialog_fmt.geometry("450x250")
            dialog_fmt.attributes("-topmost", True)
            dialog_fmt.transient(app)
            
            ctk.CTkLabel(dialog_fmt, text="Elige el formato de video:", font=("Arial", 14, "bold")).pack(pady=(20, 15))
            
            def sel_formato(fmt):
                dialog_fmt.destroy()
                abrir_consola_y_ejecutar("DESCARGADOR MEDIOS", lambda log: logica_ytdlp(log, url, calidad, fmt))
                
            ctk.CTkButton(dialog_fmt, text="🎬 MP4 (Universal / Estándar)", command=lambda: sel_formato('mp4')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_fmt, text="🎞️ MKV (Alta Calidad / PC)", command=lambda: sel_formato('mkv')).pack(fill="x", padx=40, pady=5)
            ctk.CTkButton(dialog_fmt, text="🍏 MOV (Formato Apple / Mac)", fg_color="#444444", hover_color="#222222", command=lambda: sel_formato('mov')).pack(fill="x", padx=40, pady=15)

    def btn_diskpart():
        disco = simpledialog.askstring("Desbloqueo USB", "Ingresa el NÚMERO del disco bloqueado (ej. 1, 2):", parent=app)
        if disco: abrir_consola_y_ejecutar("DISKPART", lambda log: logica_diskpart_usb(log, disco))
        
    def btn_sysprep():
        confirm = simpledialog.askstring("Sysprep", "Peligro: El PC se apagará y quedará de fábrica.\nEscribe 'CONFIRMAR' para proceder:", parent=app)
        if confirm == "CONFIRMAR": abrir_consola_y_ejecutar("SYSPREP", logica_sysprep)

    # --- TEXTOS LARGOS Y RENDEREIZADO DE BOTONES ---
    t_dest_n = "Hay ocasiones en las que intentas eliminar una carpeta y Windows te lo impide mostrando un error de 'Acceso denegado' o 'El archivo está en uso'. Esto ocurre por protecciones internas. Esta herramienta actúa como un destructor forzado: se salta las reglas del sistema y elimina permanentemente cualquier carpeta bloqueada, virus persistente o archivo rebelde. Solo debes pegar la ruta exacta y el programa la pulverizará sin dejar rastro. Úsala con precaución."
    t_dest_e = "[Autor: Microsoft OS] Ejecuta una toma de posesión forzada mediante los binarios nativos del sistema. Utiliza 'takeown.exe /f /a /r /d y' para reasignar el Owner al grupo de Administradores. Luego, emplea 'icacls.exe' inyectando el SID universal '*S-1-5-32-544:F' para otorgar permisos Full Control sobre el árbol de directorios ignorando las listas ACL previas. Finalmente, invoca la librería 'shutil.rmtree' para vaciar los inodos y eliminar el directorio recursivamente desde la raíz del disco."
    b1 = ctk.CTkButton(tools_frame, text="1. Destructor de Carpetas Rebeldes", height=45, fg_color="#1E3A8A", hover_color="#880000", command=btn_destructor); b1.pack(fill="x", pady=5)
    b1.bind("<Enter>", lambda e: on_enter(e, "DESTRUCTOR", t_dest_n, t_dest_e)); b1.bind("<Leave>", on_leave)

    t_pwd_n = "Olvidar la contraseña para entrar a la computadora es un problema grave, pero esta herramienta te salva la vida. Te permite cambiar la clave de acceso de cualquier usuario registrado en la máquina por una nueva, o si lo prefieres, eliminarla por completo para que la PC inicie directamente al escritorio sin pedir contraseña. No necesitas saber cuál era la clave anterior para que el sistema realice el cambio."
    t_pwd_e = "[Autor: Microsoft OS] Herramienta de manipulación de la base de datos SAM (Security Account Manager) del sistema local. Realiza una llamada directa al binario 'net.exe user' inyectando el alias del usuario y el string criptográfico en el input. Al operar bajo el contexto de UAC Admin, el kernel bypassa el requerimiento de la contraseña actual, reescribiendo el hash NTLM asociado al SID en milisegundos."
    b2 = ctk.CTkButton(tools_frame, text="2. Cambiar o Quitar Contraseña de Windows", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_cambiar_clave); b2.pack(fill="x", pady=5)
    b2.bind("<Enter>", lambda e: on_enter(e, "GESTOR CLAVES", t_pwd_n, t_pwd_e)); b2.bind("<Leave>", on_leave)

    t_laz_n = "Si olvidaste las contraseñas de tus redes sociales o correos, esta herramienta hace magia. Realiza un escaneo profundo en los archivos ocultos de tus navegadores y en las bases de datos de tu computadora para recuperar todas tus contraseñas guardadas históricamente. Al finalizar, genera un documento de texto en tu escritorio con la lista completa de usuarios y claves para que puedas respaldarlas. Tu antivirus podría alertarte temporalmente, pero es completamente seguro."
    t_laz_e = "[Autor: AlessandroZ - GitHub] Despliega el motor forense open-source LaZagne. Inyecta una exclusión temporal en Defender vía PowerShell (Add-MpPreference) evitando el bloqueo heurístico. Descarga el payload desde la API de GitHub, lo aloja aislado y lanza el módulo 'all' para dumpear secretos del registro, LSA secrets, DPAPI, y credenciales de navegadores en formato SQLite/JSON, canalizando el output hacia un archivo txt local."
    crear_boton_herramienta("3. Extracción de Credenciales (LaZagne)", logica_lazagne, "LAZAGNE", t_laz_n, t_laz_e)

    t_yt_n = "La herramienta definitiva para descargar videos o música de internet sin publicidad y sin instalar programas extraños. Soporta cientos de páginas web como YouTube, Facebook, o Twitter. Solo necesitas pegar el enlace del video que deseas y elegir si quieres guardarlo en MP4/MKV o extraer únicamente el audio (MP3). El programa descargará el archivo con la máxima calidad posible y lo guardará directamente en tu carpeta de Descargas de forma muy limpia."
    t_yt_e = "[Autor: yt-dlp contributors] Interfaz gráfica interactiva que envuelve el potente motor de línea de comandos yt-dlp. Descarga el binario ejecutable en memoria temporal y solicita al usuario el formato de multiplexado final (mp4, mkv, mov o mp3). Canaliza el flujo de red directamente al directorio '%USERPROFILE%\\Downloads', evadiendo restricciones de ancho de banda y protecciones DRM básicas. Se autodestruye tras uso."
    b4 = ctk.CTkButton(tools_frame, text="4. Descargador Multimedia (yt-dlp)", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_ytdlp); b4.pack(fill="x", pady=5)
    b4.bind("<Enter>", lambda e: on_enter(e, "YT-DLP", t_yt_n, t_yt_e)); b4.bind("<Leave>", on_leave)

    t_usb_n = "Protege tu computadora contra el robo de información y los virus de pendrives. Al activar el bloqueo, los puertos USB seguirán dando energía (podrás cargar celulares o conectar tu teclado sin problemas), pero la computadora rechazará la lectura de cualquier memoria USB. Nadie podrá sacar ni meter archivos. Es ideal para oficinas, cibercafés o si prestas tu equipo. Puedes desbloquearlo en cualquier momento desde esta misma interfaz con un solo clic."
    t_usb_e = "[Autor: Lennes Varela] Modifica el comportamiento del demonio de almacenamiento de Windows a nivel de Registro. Utiliza la librería 'winreg' de Python para acceder a HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR y altera el valor DWORD de la llave 'Start'. Un valor de 4 instruye al kernel a no cargar el driver de clase de almacenamiento masivo USB, denegando el montaje de volúmenes extraíbles sin afectar los periféricos."
    crear_boton_herramienta("5. Bloquear Puertos USB", lambda log: logica_bloquear_usb(log, True), "BLOQUEO USB", t_usb_n, t_usb_e)
    crear_boton_herramienta("6. Desbloquear Puertos USB", lambda log: logica_bloquear_usb(log, False), "DESBLOQUEO USB", "Habilita nuevamente la lectura de discos externos y memorias USB revertiendo el bloqueo de seguridad previamente aplicado al registro del sistema.", "[Autor: Lennes Varela] Reestablece la llave DWORD Start a valor 3 en USBSTOR.")

    t_disk_n = "A veces las memorias USB o los discos duros se bloquean y no te dejan guardar archivos ni formatearlos porque dicen estar 'Protegidos contra escritura'. Esta función utiliza herramientas profundas del sistema para eliminar esa bandera de seguridad, desbloqueando el disco físico a la fuerza para que vuelva a funcionar normalmente. Solo necesitas saber el número de disco asignado por el sistema para aplicar la reparación."
    t_disk_e = "[Autor: Microsoft OS] Herramienta de inyección de comandos hacia el motor de particionado 'diskpart'. Crea un script de texto temporal en AppData que contiene las directivas 'select disk X' y 'attributes disk clear readonly'. Luego lanza el ejecutable pasando el archivo por argumento silencioso (/s). Elimina la bandera de solo lectura incrustada a nivel de volumen lógico y firmware del dispositivo."
    b7 = ctk.CTkButton(tools_frame, text="7. Quitar Protección contra Escritura (USB)", height=45, fg_color="#1E3A8A", hover_color="#2563EB", command=btn_diskpart); b7.pack(fill="x", pady=5)
    b7.bind("<Enter>", lambda e: on_enter(e, "DISKPART", t_disk_n, t_disk_e)); b7.bind("<Leave>", on_leave)

    t_sb_n = "Crea una computadora virtual completamente desechable y segura dentro de tu propia máquina. Si sospechas que un archivo, programa o enlace que descargaste tiene virus, puedes abrirlo dentro de este Sandbox. Todo lo que ocurra ahí dentro está aislado; si realmente es un virus, no afectará tu PC real. Al cerrar la ventana del Sandbox, todo el contenido malicioso se eliminará de forma permanente como si nunca hubiera existido."
    t_sb_e = "[Autor: Microsoft OS] Ejecuta una llamada de elevación al paquete Feature Management de Windows. Invoca el comando PowerShell 'Enable-WindowsOptionalFeature -FeatureName Containers-DisposableClientVM' para instalar la característica base del Sandbox. Inicializa un entorno de escritorio en contenedor atado al kernel anfitrión pero aislado hipervisoriamente en memoria y disco."
    crear_boton_herramienta("8. Activar Windows Sandbox", logica_sandbox, "SANDBOX", t_sb_n, t_sb_e)

    t_sys_n = "La opción nuclear para vendedores y técnicos. Si vas a vender tu computadora o clonar el disco duro para otra PC, debes usar esta herramienta. Elimina todos los identificadores únicos de Windows, borra los drivers específicos de tu placa y apaga la máquina. La próxima vez que alguien la encienda, iniciará como si estuviera recién comprada en la tienda, pidiendo la configuración inicial de idioma y usuario."
    t_sys_e = "[Autor: Microsoft OS] Utiliza la herramienta de preparación del sistema (Sysprep) alojada en System32. Ejecuta las banderas '/generalize /oobe /shutdown'. La bandera generalize purga el SID (Security Identifier) del host, limpia registros de eventos y elimina hardware instalado, preparando la imagen para ser desplegada en arquitecturas dispares. OOBE fuerza la experiencia de primer inicio."
    b9 = ctk.CTkButton(tools_frame, text="9. Preparar PC para Venta (Sysprep)", height=45, fg_color="#1E3A8A", hover_color="#880000", command=btn_sysprep); b9.pack(fill="x", pady=5)
    b9.bind("<Enter>", lambda e: on_enter(e, "SYSPREP", t_sys_n, t_sys_e)); b9.bind("<Leave>", on_leave)

    t_wipe_n = "Cuando borras un archivo de la papelera, realmente no desaparece; queda invisible y puede ser recuperado por hackers o programas especiales. Esta herramienta realiza un borrado militar forense: sobrescribe con ceros todo el espacio vacío de tu disco duro para garantizar que cualquier foto, documento o contraseña que hayas eliminado en el pasado quede destruida e irrecuperable para siempre. Es un proceso muy demorado pero indispensable para tu privacidad."
    t_wipe_e = "[Autor: Microsoft OS] Invoca el algoritmo nativo de cifrado y sobreescritura de sistema de archivos mediante 'cipher.exe /w:C:\\'. Barre los clústeres marcados como libres o no asignados en la MFT del volumen C:, sobrescribiéndolos con múltiples pasadas (ceros, unos y números aleatorios logrando mitigación contra Data Recovery y file carving avanzado en análisis forense)."
    crear_boton_herramienta("10. Borrado Forense Militar (Wipe)", logica_borrado_seguro, "BORRADO WIPE", t_wipe_n, t_wipe_e)

# ============================================================================
# 6. MENÚ LATERAL Y ARRANQUE
# ============================================================================
ctk.CTkLabel(sidebar, text="TREMEND", font=("Arial", 32, "bold"), text_color="#00FFCC").pack(pady=30, padx=20)
ctk.CTkLabel(sidebar, text="CATEGORÍAS", font=("Arial", 12, "bold"), text_color="#888888").pack(pady=(0, 10))

ctk.CTkButton(sidebar, text="🌐 Redes e Internet", fg_color="transparent", border_width=1, command=cargar_categoria_redes).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(sidebar, text="🧹 Mantenimiento", fg_color="transparent", border_width=1, command=cargar_categoria_mantenimiento).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(sidebar, text="🖥️ Diagnóstico", fg_color="transparent", border_width=1, command=cargar_categoria_diagnostico).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(sidebar, text="📦 Software/Licencias", fg_color="transparent", border_width=1, command=cargar_categoria_software).pack(pady=5, padx=20, fill="x")
ctk.CTkButton(sidebar, text="🛠️ Soporte Técnico", fg_color="transparent", border_width=1, command=cargar_categoria_soporte).pack(pady=5, padx=20, fill="x")

cargar_categoria_redes()

def verificar_actualizaciones():
    # Importamos todo aquí adentro para evitar problemas
    import urllib.request
    import time
    from tkinter import messagebox
    import webbrowser

    try:
        # 1. Enlace con reloj incluido para romper la memoria caché de GitHub
        url = f"https://raw.githubusercontent.com/LennesVP/TREMEND/main/version.txt?t={time.time()}"
        
        # 2. EL DISFRAZ MAESTRO: Nos hacemos pasar por un navegador de Windows
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cache-Control': 'no-cache'
        }
        
        # 3. Lanzamos la petición a la nube
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            version_nube = response.read().decode('utf-8').strip()
        
        # 4. Comparamos las versiones
        if version_nube != VERSION_ACTUAL:
            respuesta = messagebox.askyesno(
                "¡Actualización Crítica Disponible!", 
                f"¡Hay un nuevo parche disponible para TREMEND!\n\nTu versión local: {VERSION_ACTUAL}\nVersión en la nube: {version_nube}\n\n¿Deseas descargarla ahora?"
            )
            if respuesta:
                webbrowser.open("https://github.com/LennesVP/TREMEND")
        else:
            # 5. MODO DEBUG: Si logra conectarse pero las versiones son iguales, te avisará
            messagebox.showinfo("Prueba Exitosa", f"Conexión perfecta con GitHub.\nAmbas versiones son la {version_nube}")

    except Exception as e:
        # 6. CHIVATO DE ERROR: Si algo falla (internet, firewall), nos dirá exactamente por qué
        messagebox.showerror("Error de Diagnóstico", f"Fallo al leer la nube:\n{e}")

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

app.mainloop()