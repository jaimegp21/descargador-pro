import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import sys
import os
from pathlib import Path

try:
    import winsound 
except ImportError:
    winsound = None

# --- Paleta de Colores ---
COLOR_BG = "#424242"
COLOR_FIELD_BG = "#555555"
COLOR_FG = "#FFFFFF"
COLOR_BUTTON_SECONDARY = "#616161"
COLOR_RED_PRIMARY = "#FF0000"
COLOR_GREEN_SUCCESS = "#28a745"
COLOR_AMBER_WARN = "#FFC107"

class VideoDownloaderApp:
    # El constructor. Se ejecuta una vez al arrancar para preparar la aplicación.
    def __init__(self, root):
        self.root = root
        self.setup_main_window()
        self.download_thread = None
        self.is_cancelled = False
        self.is_processing = False
        self.is_cancelling = False # El nuevo estado para la animación de cancelar
        self.animation_dots = 0
        self.create_widgets()
        self.reset_ui()

    # Ajusta las propiedades básicas de la ventana principal.
    def setup_main_window(self):
        self.root.title("Descargador Pro")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)

    # Dibuja todos los componentes visuales en la pantalla.
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg=COLOR_BG)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        tk.Label(main_frame, text="URL del Vídeo o Playlist:", bg=COLOR_BG, fg=COLOR_FG, font=("Helvetica", 12)).pack(anchor="w")
        self.url_entry = tk.Entry(main_frame, width=70, font=("Helvetica", 10), bg=COLOR_FIELD_BG, fg=COLOR_FG, insertbackground=COLOR_FG, relief="flat")
        self.url_entry.pack(fill="x", pady=(5, 15))
        tk.Label(main_frame, text="Carpeta de Destino:", bg=COLOR_BG, fg=COLOR_FG, font=("Helvetica", 12)).pack(anchor="w")
        dest_frame = tk.Frame(main_frame, bg=COLOR_BG)
        dest_frame.pack(fill="x", pady=5)
        self.destination_label = tk.Label(dest_frame, text="", bg=COLOR_BG, fg="#AAAAAA", font=("Helvetica", 9))
        self.destination_label.pack(side="left", fill="x", expand=True, anchor="w")
        self.select_btn = tk.Button(dest_frame, text="Seleccionar...", bg=COLOR_BUTTON_SECONDARY, fg=COLOR_FG, command=self.select_folder, relief="flat", activebackground="#666666")
        self.select_btn.pack(side="right")
        tk.Label(main_frame, text="Formato de Descarga:", bg=COLOR_BG, fg=COLOR_FG, font=("Helvetica", 12)).pack(anchor="w", pady=(15, 0))
        style = ttk.Style()
        style.configure("TRadiobutton", background=COLOR_BG, foreground=COLOR_FG, font=("Helvetica", 10))
        style.map("TRadiobutton", background=[('active', COLOR_BG)])
        format_frame = tk.Frame(main_frame, bg=COLOR_BG)
        format_frame.pack(anchor="w", pady=5)
        self.download_format = tk.StringVar(value="video")
        video_rb = ttk.Radiobutton(format_frame, text="Vídeo (MP4)", variable=self.download_format, value="video")
        video_rb.pack(side="left", padx=5)
        audio_rb = ttk.Radiobutton(format_frame, text="Solo Audio (MP3)", variable=self.download_format, value="audio")
        audio_rb.pack(side="left", padx=20)
        self.download_btn = tk.Button(main_frame, text="Descargar", font=("Helvetica", 12, "bold"), bg=COLOR_RED_PRIMARY, fg=COLOR_FG, command=self.start_download, relief="flat", activebackground="#E60000")
        self.cancel_btn = tk.Button(main_frame, text="Cancelar Descarga", font=("Helvetica", 12), bg=COLOR_BUTTON_SECONDARY, fg=COLOR_FG, command=self.cancel_download, relief="flat", activebackground="#666666")
        self.status_label = tk.Label(main_frame, text="", bg=COLOR_BG, fg=COLOR_FG, font=("Helvetica", 10))
        self.status_label.pack(pady=(10, 5))
        style.configure("red.Horizontal.TProgressbar", foreground=COLOR_RED_PRIMARY, background=COLOR_RED_PRIMARY, troughcolor=COLOR_FIELD_BG)
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=100, mode="determinate", style="red.Horizontal.TProgressbar")
        tk.Label(main_frame, text="Historial de Sesión:", bg=COLOR_BG, fg=COLOR_FG, font=("Helvetica", 12)).pack(anchor="w", pady=(15, 0))
        history_frame = tk.Frame(main_frame)
        history_frame.pack(fill="both", expand=True, pady=5)
        self.history_text = tk.Text(history_frame, height=5, bg=COLOR_FIELD_BG, fg="#AAAAAA", relief="flat", font=("Consolas", 9), wrap="word")
        self.history_text.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(history_frame, command=self.history_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_text.config(yscrollcommand=scrollbar.set, state="disabled")
        tk.Label(main_frame, text="Creado por Jaime Gamero Pérez © 2025", bg=COLOR_BG, fg="#AAAAAA", font=("Helvetica", 8)).pack(side="bottom", anchor="se", padx=5)
        self.history_text.tag_configure("success", foreground=COLOR_GREEN_SUCCESS)
        self.history_text.tag_configure("error", foreground=COLOR_RED_PRIMARY)
        self.history_text.tag_configure("cancelled", foreground=COLOR_AMBER_WARN)

    # Lo que ocurre cuando el usuario pulsa "Descargar".
    def start_download(self):
        url = self.url_entry.get()
        destination = self.destination_label.cget("text")
        download_format = self.download_format.get()
        if not url: return messagebox.showerror("Error", "Introduce una URL.")
        if not os.path.isdir(destination): return messagebox.showerror("Error", "La carpeta de destino no es válida.")
        
        download_playlist = False
        if 'list=' in url:
            download_playlist = messagebox.askyesno("Playlist Detectada", "¿Quieres descargar la playlist completa?")
        
        self.is_cancelled = False
        self.is_processing = False
        self.is_cancelling = False
        
        self.set_ui_state_downloading()
        
        self.download_thread = threading.Thread(target=self.execute_yt_dlp, args=(url, destination, download_playlist, download_format))
        self.download_thread.start()

    # El motor de la aplicación: prepara y ejecuta la descarga con yt-dlp.
    def execute_yt_dlp(self, url, destination, download_playlist, download_format):
        opciones = {
            'outtmpl': os.path.join(destination, '%(title)s.%(ext)s'),
            'ffmpeg_location': self.get_ffmpeg_path(),
            'noplaylist': not download_playlist,
            'progress_hooks': [self.progress_hook],
            'no_mtime': True,
            'add_metadata': False,
            'postprocessor_args': ['-map_metadata', '-1'] if download_format == 'audio' else None,
        }
        if download_format == 'audio':
            opciones['format'] = 'bestaudio/best'
            opciones['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '256',}]
        else:
            opciones['format'] = 'bestvideo+bestaudio/best'
            opciones['merge_output_format'] = 'mp4'
        
        try:
            ydl = yt_dlp.YoutubeDL(opciones)
            result_info = ydl.extract_info(url, download=True)
            
            self.is_processing = False

            if not self.is_cancelled:
                entries = result_info.get('entries', [result_info])
                for video_info in entries:
                    final_filepath = video_info.get('requested_downloads')[0].get('filepath')
                    if final_filepath and os.path.exists(final_filepath):
                        os.utime(final_filepath, None)
                        filename = os.path.basename(final_filepath)
                        self.add_to_history("completada", filename)
                    else:
                        filename = video_info.get('title', 'archivo desconocido')
                        self.add_to_history("error_file_not_found", filename)
                
                self.status_label.config(text="✅ ¡Proceso finalizado!", fg=COLOR_GREEN_SUCCESS)
                if winsound: winsound.Beep(1000, 300)
                self.set_ui_state_finished()

        except Exception as e:
            self.is_processing = False
            self.is_cancelling = False # Detenemos la animación de cancelar
            if self.is_cancelled:
                self.status_label.config(text="Descarga cancelada.", fg=COLOR_AMBER_WARN)
                self.add_to_history("cancelada", "Operación cancelada")
            else:
                self.status_label.config(text=f"❌ Error en la descarga", fg=COLOR_RED_PRIMARY)
                self.add_to_history("error", str(e))
            self.set_ui_state_finished()

    # Añade una nueva línea con color al historial de la sesión.
    def add_to_history(self, status, filename):
        if status == "completada":
            log_message = f"✅ Completada: {filename}"
            tag = "success"
        elif status == "cancelada":
            log_message = f"🟡 Cancelada: {filename}"
            tag = "cancelled"
        elif status == "error_file_not_found":
             log_message = f"❌ Error: El archivo '{filename}' no se guardó. Revisa los permisos."
             tag = "error"
        else: 
            log_message = f"❌ Error: {filename}"
            tag = "error"
        
        self.history_text.config(state="normal")
        self.history_text.insert("1.0", log_message + "\n", tag)
        self.history_text.config(state="disabled")

    # Un "informante" que nos da actualizaciones en tiempo real para la barra de progreso.
    def progress_hook(self, d):
        if self.is_cancelled: raise Exception("Download cancelled.")
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                percentage = (d['downloaded_bytes'] / total_bytes) * 100
                self.progress_bar.config(value=percentage)
                speed = d.get('speed')
                if speed:
                    speed_mbps = speed / 1024 / 1024
                    self.status_label.config(text=f"Descargando... {percentage:.1f}% ({speed_mbps:.2f} MB/s)", fg=COLOR_FG)
        elif d['status'] == 'finished':
            if not self.is_processing:
                self.is_processing = True
                self.animation_dots = 0
                self.animate_processing_text()

    # Restaura la interfaz a su estado inicial para una nueva descarga.
    def reset_ui(self):
        self.url_entry.config(state="normal")
        self.url_entry.delete(0, "end")
        self.select_btn.config(state="normal")
        
        try:
            default_path = str(Path.home() / "Downloads")
            if not os.path.exists(default_path): os.makedirs(default_path)
            self.destination_label.config(text=default_path)
        except Exception:
            self.destination_label.config(text="No se pudo encontrar la carpeta Descargas")
        
        if not self.is_processing and not self.is_cancelling:
            self.status_label.config(text="")
        
        self.cancel_btn.pack_forget()
        self.download_btn.pack(pady=20, fill="x")
        
        for child in self.root.winfo_children()[0].winfo_children():
            if isinstance(child, tk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Radiobutton):
                        widget.config(state="normal")

    #  El resto son funciones auxiliares para la UI y la gestión de archivos 

    def select_folder(self):
        path = filedialog.askdirectory()
        if path: self.destination_label.config(text=path)
        
    def animate_processing_text(self):
        if not self.is_processing: return
        dots = "." * self.animation_dots
        self.status_label.config(text=f"Procesando{dots}", fg="#AAAAAA")
        self.animation_dots = (self.animation_dots + 1) % 4
        self.root.after(500, self.animate_processing_text)
    
    # Animación de "Cancelando..."
    def animate_cancelling_text(self):
        if not self.is_cancelling: return
        dots = "." * self.animation_dots
        self.status_label.config(text=f"Cancelando{dots}", fg=COLOR_AMBER_WARN)
        self.animation_dots = (self.animation_dots + 1) % 4
        self.root.after(500, self.animate_cancelling_text)

    # Ahora, al cancelar, también se inicia la animación.
    def cancel_download(self): 
        self.is_cancelled = True
        if not self.is_cancelling:
            self.is_cancelling = True
            self.animation_dots = 0
            self.animate_cancelling_text()
    
    def set_ui_state_downloading(self):
        self.url_entry.config(state="disabled")
        self.select_btn.config(state="disabled")
        self.download_btn.pack_forget()
        self.cancel_btn.pack(pady=20, fill="x")
        self.progress_bar.pack(fill="x", pady=5)
        self.status_label.config(text="")
        for child in self.root.winfo_children()[0].winfo_children():
            if isinstance(child, tk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Radiobutton):
                        widget.config(state="disabled")

    def set_ui_state_finished(self):
        self.cancel_btn.pack_forget()
        self.progress_bar.pack_forget()
        self.root.after(3000, self.reset_ui) 
        
    def get_ffmpeg_path(self):
        if getattr(sys, 'frozen', False): return os.path.join(sys._MEIPASS, "ffmpeg.exe")
        return "ffmpeg.exe"

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()