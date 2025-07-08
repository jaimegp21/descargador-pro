; ===================================================================
;  Script de Inno Setup Profesional y Portable para Descargador Pro
; ===================================================================

#define MyAppName "Descargador Pro"
#define MyAppVersion "2.0"
#define MyAppPublisher "Jaime Gamero Pérez"
#define MyAppURL "https://jaimegp21.github.io/JaimeGamero-Portfolio/"
#define MyAppExeName "descargador_audio_y_video.exe"

[Setup]
; --- Identificadores y Nombres ---
AppId={{BC6FA90B-2004-4C31-8A0A-1EE2879FA2FD}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
; Usa el nombre de la app para la carpeta de instalación por consistencia
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}

; --- Arquitectura y Privilegios ---
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
DisableProgramGroupPage=yes

; --- Rutas de Salida y Archivos (Usando Rutas Relativas) ---
; El instalador se creará en una carpeta "Instalador_Final" dentro del proyecto
OutputDir=.\Instalador_Final
OutputBaseFilename=Descargador_Pro_Setup_v{#MyAppVersion}
; El script busca los archivos desde su propia ubicación (la raíz del proyecto)
SetupIconFile=.\src\assets\1-149f569d.ico
LicenseFile=.\setup\Licencia.txt
InfoAfterFile=.\README.txt

; --- Estilo ---
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
; La tarea para crear el icono de escritorio, ahora marcada por defecto
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
; Origen del ejecutable principal desde la carpeta 'dist'
Source: ".\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Icono del escritorio asociado a la tarea anterior
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Opción para ejecutar el programa al finalizar la instalación
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent