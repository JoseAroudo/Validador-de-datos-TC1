@echo off
python Main.py
timeout /t 3
set "carpeta=%~dp0Logs"



echo Buscando el archivo más reciente...

for /f "delims=" %%i in ('dir "%carpeta%" /b /a-d /o-d') do (
    set "ultimo=%%i"
    goto abrir
)

:abrir
echo Abriendo: %ultimo%
start "" "%carpeta%\%ultimo%"