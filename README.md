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
