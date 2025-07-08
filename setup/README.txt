✨ Características
Descarga Multiformato: Elige entre descargar el vídeo completo en MP4 o extraer únicamente el audio en MP3.

Detección de Playlists: Detecta automáticamente si una URL pertenece a una playlist y te pregunta si quieres descargarla completa.

Selección de Destino: Interfaz gráfica para seleccionar la carpeta exacta donde quieres guardar tus archivos.

Feedback en Tiempo Real: Una barra de progreso y una etiqueta de estado te informan sobre la velocidad y el progreso de la descarga.

Control Total: Opción para cancelar una descarga en curso en cualquier momento.

Interfaz Moderna: Diseño oscuro y minimalista inspirado en la paleta de colores de YouTube para una experiencia de usuario agradable.

Instalador Profesional: Se distribuye con un instalador .exe que crea accesos directos y una entrada de desinstalación.

🚀 Uso (Para Usuarios Finales)
Ve a la sección de "Releases" de este repositorio en GitHub.

Descarga la última versión del instalador (Descargador_Pro_setup.exe).

Ejecuta el instalador y sigue los pasos. Se creará un acceso directo en tu escritorio.

¡Listo! Abre el programa desde el acceso directo y empieza a descargar.

🛠️ Entorno de Desarrollo (Para Programadores)
Si deseas modificar o contribuir al código, sigue estos pasos:

Clona el repositorio:

Bash

git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
Crea un entorno virtual:

Bash

python -m venv venv
Activa el entorno virtual:

En Windows: .\venv\Scripts\activate

En macOS/Linux: source venv/bin/activate

Instala las dependencias:
Crea un archivo requirements.txt con el siguiente contenido:

Plaintext

yt-dlp
Y luego instálalo con:

Bash

pip install -r requirements.txt
Ejecuta la aplicación:

Bash

python tu_script.py
📦 Empaquetado (.exe e Instalador)
Para crear el ejecutable distribuible y el instalador final:

Asegúrate de tener FFmpeg: Descarga ffmpeg.exe y colócalo en la carpeta raíz del proyecto.

Instala PyInstaller: pip install pyinstaller

Genera el .exe: Ejecuta el siguiente comando en la terminal. Esto creará un único archivo .exe en la carpeta dist, con la consola oculta e incluyendo ffmpeg.

Bash

pyinstaller --onefile --windowed --add-binary "ffmpeg.exe;." --hidden-import yt_dlp tu_script.py
Crea el instalador:

Descarga e instala Inno Setup.

Usa el asistente de Inno Setup, seleccionando el .exe creado en el paso anterior como el archivo principal de la aplicación.

Asegúrate de marcar la opción para crear un acceso directo en el escritorio.

Compila el script para generar el setup.exe final.

💻 Tecnologías Utilizadas
Python: Lenguaje principal de la aplicación.

Tkinter: Librería nativa de Python para la construcción de la interfaz gráfica.

yt-dlp: El potente motor que gestiona las descargas de YouTube.

PyInstaller: Herramienta para empaquetar la aplicación en un solo ejecutable.

Inno Setup: Herramienta para crear el instalador de Windows.

📝 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

✍️ Autor
Jaime Gamero Pérez