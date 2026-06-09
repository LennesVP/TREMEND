
```bat
@echo off
title Sincronizador GitHub - TREMEND
color 0A

:: Asegurar que la consola se ubique en la carpeta correcta
pushd "%CD%"
CD /D "%~dp0"

echo ====================================================
echo      NUBE AUTOMATICA GITHUB - TREMEND TOOLKIT
echo ====================================================
echo.

:: Detectar si hay cambios antes de hacer nada
git status -s
echo.

:: Pedir el mensaje de la actualizacion
set /p mensaje="Escribe que cambiaste (o presiona Enter para usar la fecha automatica): "

:: Si no escribes nada, le pone la fecha y hora del sistema
if "%mensaje%"=="" set mensaje=Actualizacion de codigo: %date% %time%

echo.
echo [*] Empaquetando archivos modificados...
git add .

echo [*] Creando punto de restauracion (Commit)...
git commit -m "%mensaje%"

echo [*] Sincronizando previamente con la nube (Pull)...
git pull --rebase origin main

echo [*] Inyectando codigo en los servidores de GitHub (Push)...
git push

echo.
echo ====================================================
echo   [+] EXITO: Tu codigo esta seguro en la nube.
echo ====================================================
pause