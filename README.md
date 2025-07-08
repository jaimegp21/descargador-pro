Descargador Pro
Una aplicación de escritorio moderna y sencilla para descargar vídeos y audio de YouTube, desarrollada con Python y Tkinter. Permite seleccionar el formato (MP4 o MP3), gestionar playlists y elegir la carpeta de destino, todo desde una interfaz intuitiva.



📂 Estructura del Proyecto
El proyecto está organizado de una manera limpia y escalable, separando el código fuente, los recursos y los archivos de distribución.

Descargador-Pro/

```
├── .gitignore              # Archivo para que Git ignore carpetas temporales
├── README.md               # La documentación que estás leyendo
├── requirements.txt        # Las dependencias de Python del proyecto
│
├── src/                    # Carpeta con todo el código fuente
│   ├── descargador_audio_y_video.py         # El script principal de la aplicación
│   ├── assets/             # Recursos visuales
│   │   └── 1-149f569d.ico
│   └── ffmpeg.exe          # El ejecutable de FFmpeg
│
├── setup/                  # Archivos relacionados con el instalador
│   ├── Licencia.txt
│   └── DescargadorPro.iss  # El script de Inno Setup
│
├── dist/                   # (Generada) Aquí aparece el .exe tras compilar
└── build/                  # (Generada) Carpeta temporal de PyInstaller
```

✨ Características
Descarga Multiformato: Elige entre descargar el vídeo completo en MP4 o extraer únicamente el audio en MP3.

Detección de Playlists: Detecta automáticamente si una URL pertenece a una playlist y te pregunta si quieres descargarla completa.

Selección de Destino: Interfaz gráfica para seleccionar la carpeta exacta donde quieres guardar tus archivos.

Feedback en Tiempo Real: Una barra de progreso y una etiqueta de estado te informan sobre la velocidad y el progreso de la descarga.

Control Total: Opción para cancelar una descarga en curso en cualquier momento.

Interfaz Moderna: Diseño oscuro y minimalista para una experiencia de usuario agradable.

Instalador Profesional: Se distribuye con un instalador .exe que crea accesos directos y una entrada de desinstalación.

🚀 Uso (Para Usuarios Finales)
Ve a la sección de "Releases" en la página de GitHub del proyecto.

Descarga la última versión del instalador (ej. Descargador_Pro_Setup_v1.0.exe).

Ejecuta el instalador y sigue los pasos del asistente. Se creará un acceso directo en tu escritorio.

¡Listo! Abre el programa desde el acceso directo y empieza a descargar.

🛠️ Entorno de Desarrollo (Para Programadores)
Si deseas modificar o contribuir al código, sigue estos pasos:

Clona el repositorio:


git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio


Crea y activa un entorno virtual:

# Crear
python -m venv venv
# Activar en Windows
.\venv\Scripts\activate
# Activar en macOS/Linux
source venv/bin/activate


Instala las dependencias:

pip install -r requirements.txt


Ejecuta la aplicación desde el código fuente:

python src/__main__.py


📦 Empaquetado (.exe e Instalador)

Para crear el ejecutable distribuible y el instalador final:

Genera el .exe con PyInstaller:
Asegúrate de estar en la carpeta raíz del proyecto y ejecuta:

pyinstaller --onefile --windowed --icon="src/assets/tu_icono.ico" --add-binary="src/ffmpeg.exe;." --hidden-import yt_dlp src/__main__.py
El ejecutable final aparecerá en la carpeta dist.

Crea el instalador con Inno Setup:

Abre el archivo setup/DescargadorPro.iss con Inno Setup.

Ve a Build > Compile.

El setup.exe final se generará en la carpeta Instalador_Final.



💻 Tecnologías Utilizadas

Python: Lenguaje principal de la aplicación.

Tkinter: Librería nativa de Python para la construcción de la interfaz gráfica.

yt-dlp: El potente motor que gestiona las descargas.

PyInstaller: Herramienta para empaquetar la aplicación en un ejecutable.

Inno Setup: Herramienta para crear el instalador de Windows.


📝 Licencia
Este proyecto está bajo la Licencia MIT.


✍️ Autor
Jaime Gamero Pérez