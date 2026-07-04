@echo off
title TREMEND Toolkit - Despliegue en la Nube
color 0B

echo ========================================================
echo   SISTEMA DE DESPLIEGUE AUTOMATICO - TREMEND V3.0
echo ========================================================
echo.

:: 1. Muestra el estado actual de los archivos (opcional, para que veas que sube)
git status
echo.

:: 2. Te pide que escribas el mensaje de la actualizacion
set /p mensaje="Escribe el mensaje de los cambios (Ej: Lanzamiento V3.0): "

echo.
echo [*] Empaquetando nuevos archivos...
git add .

echo [*] Creando punto de restauracion (Commit)...
git commit -m "%mensaje%"

echo [*] Inyectando codigo en los servidores de GitHub...
git push origin main

echo.
echo ========================================================
echo  [+] SUBIDA A LA NUBE FINALIZADA CON EXITO.
echo ========================================================
pause