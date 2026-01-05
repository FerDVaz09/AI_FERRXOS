"""
Ventana Principal de AI_FERRXOS
Contiene las pestañas: Live Feed, Configuración e Historial
"""

import json
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from ui.styles import STYLESHEET, get_color
from ui.widgets import (
    CustomButton, ApiKeyInput, ModeSelector, HistoryItem, show_message
)
from core.ai_brain import AIBrain
from core.ghost import enable_ghost_mode
from core.audio import AudioCapture
from core.transcriber import AudioTranscriber

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    # Señales para comunicación entre threads
    test_result_signal = pyqtSignal(bool)
    silence_detected_signal = pyqtSignal()  # Signal para detección de silencio thread-safe
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 AI_FERRXOS - Asistente de Reuniones")
        self.setGeometry(100, 100, 1200, 700)
        
        # Conectar señales
        self.test_result_signal.connect(self._on_test_result)
        self.silence_detected_signal.connect(self._on_silence_detected)
        
        # Cargar config e historial
        self.config_path = Path(__file__).parent.parent / "config.json"
        self.history_path = Path(__file__).parent.parent / "history.json"
        self.config = self._load_config()
        self.history = self._load_history()
        
        # IA
        self.ai_brain = AIBrain()
        
        # Audio
        self.audio_capture = AudioCapture()
        
        # Transcribidor (configurar con API Key)
        api_key = self.config.get("api_key", "")
        if not api_key:
            show_message(None, "Error", "❌ Transcribidor no disponible. Configura tu API Key.", "error")
            self.transcriber = None
        else:
            self.transcriber = AudioTranscriber(api_key=api_key)
        
        # Aplicar estilos
        self.setStyleSheet(STYLESHEET)
        
        # Crear interfaz
        self._create_ui()
        
        # Activar Ghost Mode (invisible en capturas de pantalla)
        try:
            enable_ghost_mode(int(self.winId()))
            print("✅ Ghost Mode activado")
        except Exception as e:
            print(f"⚠️ Ghost Mode no disponible: {e}")
        
        # NO iniciar escucha automática - permitir entrada manual
        print("⏸️ Micrófono desactivado - usa el botón 'Analizar' con texto manual")
    
    def _create_ui(self):
        """Crea la interfaz de usuario"""
        # Widget central con tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab Widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Crear tabs
        self.tab_live = self._create_live_tab()
        self.tab_settings = self._create_settings_tab()
        self.tab_history = self._create_history_tab()
        
        self.tabs.addTab(self.tab_live, "📡 Live Feed")
        self.tabs.addTab(self.tab_settings, "⚙️ Configuración")
        self.tabs.addTab(self.tab_history, "📋 Historial")
    
    def _create_live_tab(self) -> QWidget:
        """Crea la pestaña Live Feed"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Encabezado con título y contador
        header_layout = QHBoxLayout()
        
        # Título
        titulo = QLabel("🎤 Live Feed - Escuchando en Tiempo Real")
        titulo_font = QFont()
        titulo_font.setBold(True)
        titulo_font.setPointSize(14)
        titulo.setFont(titulo_font)
        header_layout.addWidget(titulo, 1)
        
        # Contador de tiempo (derecha)
        self.time_label = QLabel("⏱️ 00:00")
        time_font = QFont()
        time_font.setBold(True)
        time_font.setPointSize(12)
        self.time_label.setFont(time_font)
        self.time_label.setStyleSheet(f"color: {get_color('accent')};")
        header_layout.addWidget(self.time_label, 0)
        
        # Status label
        self.status_label = QLabel("🔴 Detenido")
        status_font = QFont()
        status_font.setBold(True)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet(f"color: {get_color('error')};")
        header_layout.addWidget(self.status_label, 0)
        
        layout.addLayout(header_layout)
        
        # Área de transcripción
        self.live_transcript = QTextEdit()
        self.live_transcript.setPlaceholderText("La transcripción aparecerá aquí en tiempo real...")
        layout.addWidget(self.live_transcript, 2)
        
        # Área de análisis IA
        label_ia = QLabel("🤖 Análisis IA:")
        label_ia.setFont(titulo_font)
        layout.addWidget(label_ia)
        
        self.live_analysis = QTextEdit()
        self.live_analysis.setPlaceholderText("Sugerencias de la IA aparecerán aquí...")
        self.live_analysis.setReadOnly(True)
        layout.addWidget(self.live_analysis, 2)
        
        # Botones de control
        btn_layout = QHBoxLayout()
        
        btn_record = CustomButton("🎤 Grabar", "primary")
        btn_record.clicked.connect(self._on_start_recording)
        btn_layout.addWidget(btn_record)
        
        btn_analyze = CustomButton("🚀 Analizar", "primary")
        btn_analyze.clicked.connect(self._on_manual_analyze)
        btn_layout.addWidget(btn_analyze)
        
        btn_clear = CustomButton("🗑️ Limpiar", "secondary")
        btn_clear.clicked.connect(self._on_clear_transcript)
        btn_layout.addWidget(btn_clear)
        
        layout.addLayout(btn_layout)
        
        # Timer para actualizar contador
        self.recording_timer = QTimer()
        self.recording_timer.timeout.connect(self._update_recording_time)
        self.recording_seconds = 0
        
        return widget
    
    def _create_settings_tab(self) -> QWidget:
        """Crea la pestaña de Configuración"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Título
        titulo = QLabel("⚙️ Centro de Configuración")
        titulo_font = QFont()
        titulo_font.setBold(True)
        titulo_font.setPointSize(14)
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)
        
        # API Key Input
        self.api_key_widget = ApiKeyInput()
        layout.addWidget(self.api_key_widget)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Mode Selector
        self.mode_selector = ModeSelector()
        layout.addWidget(self.mode_selector)
        
        # Separador
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator2)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        
        btn_save = CustomButton("💾 Guardar Configuración")
        btn_save.clicked.connect(self._on_save_config)
        btn_layout.addWidget(btn_save)
        
        btn_test = CustomButton("🧪 Probar Conexión IA", "secondary")
        btn_test.clicked.connect(self._on_test_ai)
        btn_layout.addWidget(btn_test)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        # Cargar config existente
        if self.config.get("api_key"):
            self.api_key_widget.set_api_key(self.config["api_key"])
        if self.config.get("modo"):
            self.mode_selector.set_mode(self.config["modo"])
        
        return widget
    
    def _create_history_tab(self) -> QWidget:
        """Crea la pestaña de Historial"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Título
        titulo = QLabel("📋 Historial de Reuniones")
        titulo_font = QFont()
        titulo_font.setBold(True)
        titulo_font.setPointSize(14)
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)
        
        # Tabla
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels([
            "Fecha", "Título", "Modo", "Acción"
        ])
        self.history_table.horizontalHeader().setStretchLastSection(False)
        layout.addWidget(self.history_table)
        
        # Botón de actualizar
        btn_refresh = CustomButton("🔄 Actualizar")
        btn_refresh.clicked.connect(self._on_refresh_history)
        layout.addWidget(btn_refresh)
        
        # Cargar historial
        self._load_history_table()
        
        return widget
    
    def _load_config(self) -> dict:
        """Carga la configuración desde JSON"""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return self._default_config()
        return self._default_config()
    
    def _default_config(self) -> dict:
        """Retorna config por defecto"""
        return {
            "api_key": "",
            "modo": "negocios",
            "ghost_mode_enabled": False,
            "created_at": datetime.now().isoformat()
        }
    
    def _load_history(self) -> list:
        """Carga el historial desde JSON"""
        if self.history_path.exists():
            try:
                with open(self.history_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_config(self):
        """Guarda la configuración en JSON"""
        self.config["api_key"] = self.api_key_widget.get_api_key()
        self.config["modo"] = self.mode_selector.get_mode()
        self.config["custom_prompt"] = self.mode_selector.get_custom_prompt()
        self.config["updated_at"] = datetime.now().isoformat()
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def _save_history_item(self, titulo: str, resumen: str):
        """Guarda un item en el historial"""
        item = {
            "id": f"uuid-{len(self.history) + 1:03d}",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "titulo": titulo,
            "modo": self.mode_selector.get_mode().upper(),
            "resumen_ia": resumen,
            "transcript_completo": self.live_transcript.toPlainText()
        }
        
        self.history.append(item)
        
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
        
        self._load_history_table()
    
    def _load_history_table(self):
        """Carga el historial en la tabla"""
        self.history_table.setRowCount(len(self.history))
        
        for row, item in enumerate(reversed(self.history)):
            # Fecha
            fecha_item = QTableWidgetItem(item.get("fecha", ""))
            self.history_table.setItem(row, 0, fecha_item)
            
            # Título
            titulo_item = QTableWidgetItem(item.get("titulo", ""))
            self.history_table.setItem(row, 1, titulo_item)
            
            # Modo
            modo_item = QTableWidgetItem(item.get("modo", ""))
            self.history_table.setItem(row, 2, modo_item)
            
            # Botón Copiar
            btn_copy = CustomButton("📋 Copiar")
            btn_copy.clicked.connect(
                lambda checked, resumen=item.get("resumen_ia", ""): self._copy_resumen(resumen)
            )
            self.history_table.setCellWidget(row, 3, btn_copy)
    
    def _copy_resumen(self, resumen: str):
        """Copia un resumen al portapapeles"""
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(resumen)
        show_message(self, "Éxito", "Resumen copiado al portapapeles", "success")
    
    def _on_save_config(self):
        """Handler para guardar configuración"""
        self._save_config()
        
        # Actualizar transcriber con nueva API Key
        api_key = self.api_key_widget.get_api_key()
        self.transcriber.set_api_key(api_key)
        
        show_message(self, "Configuración", "✓ Configuración guardada exitosamente", "success")
    
    def _on_test_ai(self):
        """Handler para probar conexión IA"""
        api_key = self.api_key_widget.get_api_key()
        if not api_key:
            show_message(self, "Error", "⚠️ Ingresa tu API Key primero", "error")
            return
        
        # Configurar IA con la API Key
        self.ai_brain.set_api_key(api_key)
        
        # Prueba en thread separado para no bloquear UI
        import threading
        
        def test_in_thread():
            try:
                result = self.ai_brain.test_connection()
                self.test_result_signal.emit(result)
            except Exception as e:
                print(f"Error en test: {e}")
                self.test_result_signal.emit(False)
        
        thread = threading.Thread(target=test_in_thread, daemon=True)
        thread.start()
    
    def _on_test_result(self, success: bool):
        """Callback para resultado de prueba (slot conectado a señal)"""
        if success:
            show_message(self, "✅ Éxito", "✓ Conexión con Gemini funcionando correctamente", "success")
        else:
            show_message(self, "❌ Error", "No se pudo conectar con Gemini", "error")
    
    def _on_start_recording(self):
        """Handler para iniciar grabación"""
        # Pasar callback de silencio detectado (con signal para thread-safety)
        success = self.audio_capture.start_recording(
            on_silence=lambda: self.silence_detected_signal.emit()
        )
        if success:
            self.status_label.setText("🟢 Escuchando")
            self.status_label.setStyleSheet(f"color: {get_color('success')};")
            self.live_transcript.clear()
            self.live_analysis.clear()
            
            # Iniciar contador
            self.recording_seconds = 0
            self.recording_timer.start(1000)  # Actualizar cada segundo
        else:
            show_message(self, "Error", "❌ No se pudo iniciar micrófono. Usa 'Analizar Texto' en su lugar.", "error")
    
    def _on_stop_and_analyze(self):
        """Handler para finalizar y analizar"""
        # Detener contador de forma thread-safe
        if self.recording_timer.isActive():
            self.recording_timer.stop()
        
        try:
            # Detener grabación
            audio_data = self.audio_capture.stop_recording()
            self.status_label.setText("🔴 Detenido")
            self.status_label.setStyleSheet(f"color: {get_color('danger')};")
            
            if not audio_data or len(audio_data) < 1000:
                print("⚠️ Audio muy corto")
                return
            
            # Validar transcriber disponible
            if not self.transcriber:
                print("❌ Transcribidor no disponible")
                return
            
            # Transcribir audio automáticamente
            print("🎤 Transcribiendo audio...")
            transcript = self.transcriber.transcribe_audio(audio_data, language="es-ES")
            
            if "❌" in transcript or "⚠️" in transcript:
                print(f"⚠️ Error en transcripción: {transcript}")
                return
            
            # Actualizar campo de transcripción
            self.live_transcript.setText(transcript)
            
            # Generar análisis con IA
            print("🤖 Generando análisis con IA...")
            
            analysis = self.ai_brain.analyze(
                transcript,
                mode=self.mode_selector.get_mode(),
                custom_prompt=self.mode_selector.get_custom_prompt()
            )
            
            self.live_analysis.setText(analysis)
            
            # Guardar en historial
            titulo = f"Reunión - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            self._save_history_item(titulo, analysis)
            
            print("✅ Análisis completado")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def _on_manual_analyze(self):
        """Analiza el texto de transcripción manualmente"""
        transcript = self.live_transcript.toPlainText().strip()
        
        if not transcript or len(transcript) < 3:
            print("⚠️ Ingresa texto antes de analizar")
            return
        
        print("🤖 Analizando texto...")
        
        try:
            analysis = self.ai_brain.analyze(
                transcript,
                mode=self.mode_selector.get_mode(),
                custom_prompt=self.mode_selector.get_custom_prompt()
            )
            
            self.live_analysis.setText(analysis)
            
            # Guardar en historial
            titulo = f"Análisis Manual - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            self._save_history_item(titulo, analysis)
            
            print("✅ Análisis completado")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def _on_silence_detected(self):
        """Slot thread-safe - Detiene grabación e intenta transcribir automáticamente"""
        print("🔇 Silencio detectado - deteniendo grabación")
        self._on_stop_and_analyze()
    
    def _update_recording_time(self):
        """Actualiza el contador de tiempo de grabación"""
        self.recording_seconds += 1
        minutes = self.recording_seconds // 60
        seconds = self.recording_seconds % 60
        self.time_label.setText(f"⏱️ {minutes:02d}:{seconds:02d}")
        
        # Actualizar estado
        if self.recording_timer.isActive():
            self.status_label.setText("🟢 Escuchando")
            self.status_label.setStyleSheet(f"color: {get_color('success')};")
    
    def _on_clear_transcript(self):
        """Limpia la transcripción"""
        self.live_transcript.clear()
        self.live_analysis.clear()
    
    def _on_start_meeting(self):
        """Handler para iniciar reunión (deprecated)"""
        self._on_start_recording()
    
    def _on_stop_meeting(self):
        """Handler para finalizar reunión (deprecated)"""
        self._on_stop_and_analyze()
    
    def _on_refresh_history(self):
        """Handler para refrescar historial"""
        self.history = self._load_history()
        self._load_history_table()
        show_message(self, "Historial", "🔄 Historial actualizado", "success")
