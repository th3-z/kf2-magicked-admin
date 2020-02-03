<p align="center">
    <img width=125 height=125 src="https://files.th3-z.xyz/standing/kf2-ma-logo.png"/>
</p>

<h1 align="center">Killing Floor 2 Magicked Admin</h1>

[![Downloads](https://img.shields.io/github/downloads/th3-z/kf2-magicked-admin/total.svg)](https://img.shields.io/github/downloads/th3-z/kf2-magicked-admin/total.svg) [![Build Status](https://travis-ci.com/th3-z/kf2-magicked-admin.svg?branch=master)](https://travis-ci.com/th3-z/kf2-magicked-admin) [![Coverage Status](https://coveralls.io/repos/github/th3-z/kf2-magicked-admin/badge.svg?branch=master)](https://coveralls.io/github/th3-z/kf2-magicked-admin?branch=master) [![CodeFactor](https://www.codefactor.io/repository/github/th3-z/kf2-magicked-admin/badge/master)](https://www.codefactor.io/repository/github/th3-z/kf2-magicked-admin/overview/master) [![GitHub license](https://img.shields.io/github/license/th3-z/kf2-magicked-admin)](https://github.com/th3-z/kf2-magicked-admin/blob/master/LICENSE)

Administración con Scripts, estadísticas, y bot para servidor de Killing Floor 2 Ranked. Provee comandos en la partida, Seguimiento de estadísticas por jugador y rankings, tabla de puntuación y estadísticas en vivo, saludador (bienvenida a los jugadores cuando entran a la partida), y funciones de administrador. Ejecución completa a través del Administrador Web, No afecta el estado "Ranked/Custom" del servidor. Se puede ejecutar directamente sobre el servidor o remotamente, y administrar multiples servidores simultáneamente.

Descargas
---------

La versión estable más reciente es la `0.1.5`. Para los usuarios de Windows, los binarios están provistos en la página de lanzamientos (releases). Usuarios de Linux y Max OS deben clonar este repositorio y ejecutar desde la fuente.

[Release 0.1.5](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.1.5)

<details>
<summary>Versiones anteriores</summary>

* [Release 0.1.4](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.1.4)
* [Release 0.1.3](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.1.3)
* [Release 0.1.2](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.1.2)
* [Release 0.0.7](https://github.com/th3-z/kf-magicked-admin/releases/tag/0.0.7) </details>

Características
--------

### Comandos

Cuando escribes comandos através del chat deben ir con el prefijo '!'. Cuando escribes comandos en un script, o los encadenas, el prefijo debe omitirse.

Varios comandos buscarán la coincidencia más cercana en relación a sus parámetros. Por ejemplo '_biotics_' coincidirá con '_kf-biotics-lab_' y '_userO_' coincidirá con '_userOne™/@:®_'.

Todos los comandos tienen ayuda dentro de la partida a la cual puedes acceder con la bandera -h

* Ejemplo: `!commands -h`

Así mismo, todos los comandos tienen además las siguientes banderas.

* `-q` - Suprime la salida.
* `-p` - Esconde la linea con el nombre de usuario.


Secuencias de escape como las siguientes están disponibles para el formato de mensajes.

* `\n` - Salto de linea
    - Ejemplo: `!say linea 0\nlinea 1`
* `\t` - Tab
    - Ejemplo: `!say linea 0\n\tlinea 1 está indentada`

#### Comandos para jugadores

Comandos que pueden ser ejecutados por cualquier jugador.

<details>
<summary>¡Cliquea para ver los comandos para jugadores!</summary>

* `!commands` - Muestra una lista de todos los comandos disponibles para los jugadores
* `!stats <user>` - Muestra estadísticas generales de un usuario
    - Ejemplo: `!stats` Muestra tus estadísticas
    - Ejemplo: `!stats the_z` Muestra las estadísticas de the_z
* `!kills <user>` - Muestra las estadísticas de Kills de un usuario
    - Ejemplo: `!kills` Muestra tus estadísticas de Kills
    - Ejemplo: `!kills the_z` Muestra las estadísticas de the_z
* `!dosh <user>` - Muestra las estadísticas de Dosh de un usuario
    - Ejemplo: `!dosh` Muestra tus estadísticas de Dosh
    - Ejemplo: `!dosh the_z` Muestra las estadísticas de the_z
* `!time <user>` - Muestra las estadísticas de tiempo de un usuario
    - Ejemplo: `!dosh` Muestra tus estadísticas de tiempo
    - Ejemplo: `!dosh the_z` Muestra las estadísticas de the_z
* `!map` - Muestra las estadísticas del mapa actual
* `!record_wave` - Muestra la oleada mas álta alcanza en el mapa actual
* `!top_kills` - Muestra la tabla de posición global de Kills
* `!top_dosh` - Muestra la tabla de posición global de Dosh
* `!top_time` - Muestra la tabla de posición global de Tiempo jugado
* `!top_wave_kills` - Muestra información acerca del jugador que ha matado más ZEDs en la oleada actual. Generalmente se usa con `start_trc`
    - Ejemplo: `!start_trc -- top_wave_kills`
* `!top_wave_dosh` - Muestra información acerca del jugador que obtuvo más dosh en la oleada actual. Generalmente se usa con `!start_trc`
    - Ejemplo: `!start_trc -- top_wave_dosh`
* `!server_kills` - Cantidad total de Kills en el servidor
* `!server_dosh` - Cantidad de Dosh obtenido en el servidor
* `!scoreboard` - Muestra la tabla de posición completa, Útil en servidores con un máximo de jugadores mayor que 6
    - Alias: `!sb` Hace lo mismo
* `!game` - Información de la partida actual
* `!maps [--all]` - Muestra el ciclo de mapas actual
    - Option `-a`: Muestra todos los mapas disponibles
* `!player_count` - Muestra la cantidad actual y máxima de jugadores </details>

#### Comandos de Administrador


Comandos que pueden ser ejecutados por los administradores del servidor o usuarios autorizados con el comando `!op`.
<details>
<summary>¡Cliquea para ver los comandos de administrador!</summary>

* `!op <usuario>` - Le da a un usuario permisos de administrador
    - Ejemplo: `!op the_z`
* `!deop <usuario>` - Quita los permisos de administrador a un usuario
    - Ejemplo: `!deop the_z`
* `!say <mensaje>` - Envia un mensaje por el chat
    - Ejemplo: `!say The quick brown fox jumps over the lazy dog`
    - Ejemplo: `!start_trc -- say El mercader está abierto`
* `!players` - Muestra información detallada de los jugadores que están en el servidor
* `!kick <usuario>` - Expulsa `<user>` de la partida
    - Ejemplo: `!kick the_z`
* `!ban <user>` - Banea a `<user>` del servidor
    - Ejemplo: `!ban the_z`
    - Advertencia: El administrador web tiene un bug que causa que los baneos permanezcan luego de que son borrados, por esa razón no hay comando para desbanear.
* `!length <largo>` - Cambia el largo `<length>` en la siguiente partida
    - Ejemplo: `!length short` (También puede ser medium o long)
* `!difficulty <difficulty>` - Cambia la dificultad a `<difficulty>` en la siguiente partida
    - Ejemplo: `!difficulty hell`
* `!game_mode <game_mode>` - Cambia inmediatamente el modo de juego a `<game_mode>`
    - Ejemplo: `!game_mode endless` Cambia el modo de juego a Sin Fin
* `!load_map <map>` - Cambia inmediatamente el mapa a `<map>`
    - Ejemplo: `!load_map biotics` Cambia el mapa a Biotics Lab
* `!restart` - Reinicia inmediatamente la partida
* `!password [--set] <on|off>`
    - Ejemplo: `!password on` Activa la contraseña del archivo config en el servidor
    - Ejemplo: `!password off` Desactiva la contraseña para el servidor
    - Ejemplo: `!password --set algunaContraseña` Configura una contraseña especifica
* `!start_jc -- <command>` - Comienza un comando que se ejecutará cada vez que alguien entre en la partida
    - Ejemplo: `!start_jc -- say Bienvenido %PLR` - Saluda a un jugador al entrar
    - Claves Disponibles: `%PLR` - Nombre de Usuario, `%KLL` - total de kills, `%DSH` - total de dosh, `%BCK` - "atrás" si el número de sesiones es > (mayor que) 1, `%DRK` - dosh rank, `%KRK` - kill rank, `%TME` - tiempo jugado, `%TRK` - rank de tiempo, `%SES` - sesiones
* `!stop_jc` - Detiene todos los comandos que se ejecutan cuando un jugador entra a la partida
* `!start_wc [-w <wave>] -- <command>` - Comienza un comando que se ejecuta en la oleada `<wave>`
    - `-w` Oleada en la cual ejecutar el comando, puede ser omitido para ejecutar el comando en todas las oleadas
    - `-w` Puede ser un valor negativo para contar desde la oleada del jefe hacia atras
    - Ejemplo: `!start_wc -1 -- say Bienvenidos a la oleada del Jefe`
* `!stop_wc` - Detiene todos los comandos que se ejecutan en oleadas
* `!start_tc [-r, -t <seconds>] -- <command>` - Comienza un comando que se ejecuta cada `<seconds>` segundos
    - Opción `-r`: Añádela para que el comando se ejecute repetidas veces
    - Opción `-t`: Requerida, el número de segundos a esperar para ejecutar el comando
    - Ejemplo: `!start_tc -rt 600 -- say Únete a nuestro grupo de Steam!\n
http://steam.group/`
* `!stop_tc` - Detiene todos los comandos que se ejecutan con tiempo
* `!start_trc [-w <wave>] -- <command>` - Gatilla comandos que se ejecutan cuando abre el mercader
    - `-w` Olada en la cual ejecutar el comando, puede omitirse para que se ejecute en todas las oleadas
    - `-w` Puede ser un valor negativo para contar desde la oleada del jefe hacia atras
    - Ejemplo: `!start_trc -- top_wave_dosh` - Muestra quien obtuvo la mayor cantidad de Dosh cuando abre el mercader
* `!stop_trc` - Detiene todos los comandos que se ejecutan cuando abre el mercader
* `!silent` - Activa / Desactiva la supresión del chat, los comandos seguirán teniendo efecto, pero la respuesta no será visible para los jugadores
* `!run <script_name>` - Ejecuta un script de la carpeta `conf/scripts`, más información en la sección de scripts
    - Ejemplo: `!run example`
* `!marquee <marquee_name>` - Ejecuta un marquee de la carpeta `conf/marquee`, _experimental_
    - Ejemplo: `!marquee example`
* `!update_motd <type>` - Actualiza la tabla de posición de la pantalla de bienvenida, El tipo puede ser uno de estos: kills, dosh, o time
    - Ejemplo: `!start_tc 300 -- update_motd kills`
* `!reload_motd` - Recarga el archivo `*.motd` desde `conf`
* `!enforce_dosh <amount>` - Expulsa a todos los jugadores que tengan más dosh que el especificado en `amount`
    - Ejemplo: `!start_tc 600 -- enforce_dosh 60000` </details>

### MOTD leaderboard

Crea un archivo `conf/server_name.motd` que contenga pares de `%PLR` y `%SCR`. `%PLR` será reemplazado con el nombre del jugador y `%SCR` será reemplazado con su puntuación actual. Ahora puedes usar `!update_motd <type>` para mostrar la tabla en un pantalla de bienvenida, `<type>` debe ser kills, dosh, o time dependiendo de cual sistema de medida quieras usar.

`%SRV_D` y `%SRV_K` será reemplazado por el total de dosh y kills respectivamente, en el servidor.

### Scripts

Escribir un archivo `server_name.init` en la carpeta `conf/scripts` con una serie de comandos, se ejecutarán en secuencia cuando el bot se inicie en `server_name`.

Scripts adicionales pueden ser escritos en la carpeta `conf/scripts` y ejecutados con el comando `!run`. Ya hay un ejemplo dentro de la carpeta el cual puede ser ejecutado con `!run example`.

* Se pueden añadir comentarios en el script con el prefijo `;` antes de escribir en una linea.

### Parches del Administrador Web (Webadmin Patches)

Para que modos de juego distintos a supervivencia funcionen completamente, los parches deben ser aplicados a la carpeta `KFGame/Web/ServerAdmin` del servidor.
Por esta razón, se provee un script en la carpeta `admin-patches` que parcheará automáticamente tu servidor.

Actualmente no existe un CLI (Interfáz de linea de comandos) o Windows build para éste componente. Puedes ejecutarlo con `python3 admin-patches/admin-patches.py`. Un cuadro de diálogo aparecerá pidiéndote que búsques tu servidor. 


Opciones de Configuración
---------------------

La configuración básica se hace en la primera ejecución. Sin embargo, esto no cubre todas las opciones que KF2-MA puede ofrecer. Por favor revisa el archivo `conf/magicked_admin.conf`, para más opciones de configuración ya que algunas características están desactivadas por defecto.

Cada servidor administrado por KF2-MA tiene una sección que luce algo como `[server_one]`, seguido de varias opciones (`x = y`). Copia y edita la "default server section" si quieres administrar múltiples servidores. `[server_one]` es el nombre del servidor, esto puede cambiarse a lo que tu quieras.

### Opciones

Las opciones pueden configurarse en el archivo `conf/magicked_admin.conf`.

* `address`
    - Dirección web del Servidor (Panel Web). Requiere esquema y protocolo, ej: `https://0.0.0.0:8080`
* `username`
    - Nombre de usuario para logearse en el Administrador Web, éste nombre aparecera en el chat cuando el bot tenga algo que decir. Se recomienda crear una cuenta aparte para el bot.
* `password`
    - Contraseña del Administrador Web que le pertenece al nombre de usuario anterior.
* `game_password`
    - Contraseña del servidor por defecto para activar / desactivar con el comando `!password <on|off>`.
* `motd_scoreboard`
    - Valor Booleano, Activa o desactiva la característica del MOTD. Desactivado por defecto.
* `scoreboard_type`
    - Valores posibles: `kills`, o `dosh`. Cambia el tipo de puntuacíon que se muestra en el MOTD.

Ejecución con Docker
---------------------------

Ejecutar con Docket es fácil. Solo escribe éste comando:
```
    docker run -it -p 1880:1880 --name kf2-magicked-admin -v '<host config folder location>':'/magicked_admin/conf' th3z/kf2-magicked-admin
```
Tendrás que cambiar `<host config folder location>` a donde sea que quieras guardar la carpeta de configuración. `/mnt/user/appdata/kf2-magicked-admin` es la elección más popular en sistemas que ejecutan Unraid.

Luego de que finalice este comando, el contenedor se cerrará y los logs te pedirán que hagas tu archivo de configuración. Ve a la carpeta `conf` y configura lo necesario, luego ejecuta el contenedor nuevamente y estarás ¡listo para partir!


Ejecutando desde fuentes Python
---------------------------

Antes de contribuir con código necesitarás instalar los requerimientos de Python.

### Requerimientos
Éstos ejemplos funcionan en Debian 10 y Ubuntu Xenial, podrían ser distintos para otros sistemas operativos. Instala los siguientes paquetes.

* Python 3.7 - `apt install python3`
* Pip - `apt install python3-pip`
* Python 3 dependencies - `pip3 install -r requirements.txt`
    - Podrias tener problemas con que cx_freeze  no se instale si no tienes zlib-dev, pero cx_freeze solo se necesita para la compilación del projecto.

### Ejecución
`git clone git@github.com:th3-z/kf2-magicked-admin.git`

`cd kf2-magicked-admin`

`pip3 install -r requirements.txt`

`python3 -O magicked_admin/magicked_admin.py`

La bandera `-O` ejecuta el programa en modo "release", quítala para ejecutar el programa en modo "debug". El modo "Debug" habilitará salidas mas detallas por consola.

Building
--------

Puedes construir (build) un release binario para distribución con `make` luego de instalar ambos requerimientos "run" y "build".

### Requerimientos
Éstos ejemplos funcionan en Debian 10 y Ubuntu Xenial, podrían ser distintos para otros sistemas operativos. Instala los siguientes paquetes.

* Python 3.7 - `apt install python3`
* Pip - `apt install python3-pip`
* Pip dependencies - `pip3 install -r requirements.txt`
* Make - `apt install make`
* zlib-dev - `apt install zlib1g-dev`

### Usuario de Windows
Puedes construir el programa sin `make` ejecutando `setup.py`

* `python3 setup.py build`

