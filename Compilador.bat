@echo off
:: Solicitando permisos de Administrador automaticamente
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo [*] Solicitando privilegios de administrador...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

:: Inicio de la Fabrica de Compilacion
color 0B
echo ====================================================
echo   FABRICA DE COMPILACION PRIVADA - TREMEND V2
echo ====================================================
echo.
echo [*] Verificando motor PyInstaller...
pip install pyinstaller
echo.
echo [*] Empaquetando codigo fuente a EXE Portatil (Silencioso)...
pyinstaller --noconfirm --onefile --windowed Main.py
echo.
echo [*] Extrayendo y renombrando el ejecutable maestro...
move /y "dist\Main.exe" "TREMEND.exe"
echo.
echo [*] Destruyendo residuos de compilacion...
rmdir /s /q build
rmdir /s /q dist
del /q Main.spec
echo.
echo ====================================================
echo   [+] EXITO: Tu TREMEND.exe actualizado esta listo.
echo ====================================================
pause