"""
Widgets personalizados para AI_FERRXOS
"""

from PyQt6.QtWidgets import (
    QPushButton, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ui.styles import get_color

class CustomButton(QPushButton):
    """Botón personalizado"""
    def __init__(self, text, variant="primary", parent=None):
        super().__init__(text, parent)
        self.variant = variant
        if variant == "secondary":
            self.setObjectName("secondary")
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class ApiKeyInput(QWidget):
    """Widget para ingresar la API Key de Gemini"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Etiqueta
        label = QLabel("🔑 Google Gemini API Key")
        label_font = QFont()
        label_font.setBold(True)
        label.setFont(label_font)
        layout.addWidget(label)
        
        # Input (contraseña)
        self.input_field = QLineEdit()
        self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_field.setPlaceholderText("Pega tu API Key aquí...")
        layout.addWidget(self.input_field)
        
        # Hint
        hint = QLabel("💡 Tu clave se guarda encriptada localmente")
        hint_font = QFont()
        hint_font.setPointSize(9)
        hint.setFont(hint_font)
        hint.setStyleSheet(f"color: {get_color('text_secondary')};")
        layout.addWidget(hint)

    def get_api_key(self) -> str:
        """Obtiene la API Key"""
        return self.input_field.text().strip()

    def set_api_key(self, key: str):
        """Establece la API Key"""
        self.input_field.setText(key)

class ModeSelector(QWidget):
    """Selector de Modo (Persona) para la IA"""
    mode_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Etiqueta
        label = QLabel("🎯 Selecciona tu Modo (Persona)")
        label_font = QFont()
        label_font.setBold(True)
        label.setFont(label_font)
        layout.addWidget(label)
        
        # ComboBox
        self.combo = QComboBox()
        self.combo.addItems([
            "🎤 Entrevista (Respuestas técnicas)",
            "💼 Negocios (Oportunidades)",
            "🗣️ Presentación (Control de ritmo)",
            "🛠️ Custom (Prompting personalizado)"
        ])
        self.combo.currentTextChanged.connect(self._on_mode_changed)
        layout.addWidget(self.combo)
        
        # Custom prompt (inicialmente oculto)
        self.label_custom = QLabel("✏️ Tu Prompt Personalizado")
        self.label_custom.setFont(label_font)
        self.label_custom.setVisible(False)
        layout.addWidget(self.label_custom)
        
        self.custom_input = QTextEdit()
        self.custom_input.setPlaceholderText("Ej: Actúa como un inversor agresivo que busca disrupción...")
        self.custom_input.setMaximumHeight(150)
        self.custom_input.setVisible(False)
        layout.addWidget(self.custom_input)

    def _on_mode_changed(self, mode_text: str):
        """Muestra/oculta custom prompt según selección"""
        is_custom = "Custom" in mode_text
        self.label_custom.setVisible(is_custom)
        self.custom_input.setVisible(is_custom)
        self.mode_changed.emit(self.get_mode())

    def get_mode(self) -> str:
        """Obtiene el modo seleccionado"""
        text = self.combo.currentText()
        if "Entrevista" in text:
            return "entrevista"
        elif "Negocios" in text:
            return "negocios"
        elif "Presentación" in text:
            return "presentacion"
        else:
            return "custom"

    def get_custom_prompt(self) -> str:
        """Obtiene el prompt personalizado"""
        return self.custom_input.toPlainText().strip()

    def set_mode(self, mode: str):
        """Establece el modo"""
        modo_dict = {
            "entrevista": 0,
            "negocios": 1,
            "presentacion": 2,
            "custom": 3
        }
        index = modo_dict.get(mode, 1)
        self.combo.setCurrentIndex(index)

class HistoryItem(QWidget):
    """Item individual en el historial"""
    def __init__(self, history_data: dict, parent=None):
        super().__init__(parent)
        self.data = history_data
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # Info
        info_layout = QVBoxLayout()
        
        titulo = QLabel(self.data.get("titulo", "Sin título"))
        titulo_font = QFont()
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        info_layout.addWidget(titulo)
        
        fecha = QLabel(f"📅 {self.data.get('fecha', 'Fecha desconocida')} | 🎯 {self.data.get('modo', 'Custom').upper()}")
        fecha_font = QFont()
        fecha_font.setPointSize(9)
        fecha.setFont(fecha_font)
        fecha.setStyleSheet(f"color: {get_color('text_secondary')};")
        info_layout.addWidget(fecha)
        
        layout.addLayout(info_layout, 1)
        
        # Botón Copiar
        btn_copiar = CustomButton("📋 Copiar Resumen")
        btn_copiar.clicked.connect(self._copy_to_clipboard)
        layout.addWidget(btn_copiar)

    def _copy_to_clipboard(self):
        """Copia el resumen al portapapeles"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        resumen = self.data.get("resumen_ia", "Sin resumen")
        clipboard.setText(resumen)
        QMessageBox.information(self, "✅ Éxito", "Resumen copiado al portapapeles")

def show_message(parent, title: str, message: str, msg_type: str = "info"):
    """Muestra mensajes al usuario"""
    if msg_type == "info":
        QMessageBox.information(parent, title, message)
    elif msg_type == "warning":
        QMessageBox.warning(parent, title, message)
    elif msg_type == "error":
        QMessageBox.critical(parent, title, message)
    elif msg_type == "success":
        QMessageBox.information(parent, f"✅ {title}", f"✓ {message}")
