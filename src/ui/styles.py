"""
Estilos y temas para la interfaz gráfica
Tema: Bloomberg Terminal (Dark Mode Financiero)
"""

# Paleta de colores
COLORS = {
    "background": "#0F172A",      # Azul oscuro profundo
    "surface": "#1A2940",          # Azul oscuro secundario
    "accent": "#00D9FF",           # Cian brillante
    "success": "#10B981",          # Verde
    "warning": "#F59E0B",          # Naranja
    "error": "#EF4444",            # Rojo
    "text_primary": "#F0F9FF",     # Blanco azulado
    "text_secondary": "#94A3B8",   # Gris
    "border": "#334155",           # Gris oscuro
}

# Estilos CSS para PyQt6
STYLESHEET = f"""
/* VENTANA PRINCIPAL */
QMainWindow {{
    background-color: {COLORS['background']};
    color: {COLORS['text_primary']};
}}

/* TABS */
QTabWidget {{
    background-color: {COLORS['background']};
    color: {COLORS['text_primary']};
}}

QTabBar::tab {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_secondary']};
    padding: 8px 20px;
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['accent']};
    color: {COLORS['background']};
    font-weight: bold;
}}

/* LABELS */
QLabel {{
    color: {COLORS['text_primary']};
}}

/* INPUTS DE TEXTO */
QLineEdit, QTextEdit {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 8px;
    selection-background-color: {COLORS['accent']};
}}

QLineEdit:focus, QTextEdit:focus {{
    border: 2px solid {COLORS['accent']};
}}

/* COMBO BOX (DROPDOWN) */
QComboBox {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 6px;
}}

QComboBox::drop-down {{
    border: none;
    background-color: transparent;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_primary']};
    selection-background-color: {COLORS['accent']};
}}

/* BOTONES */
QPushButton {{
    background-color: {COLORS['accent']};
    color: {COLORS['background']};
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 12px;
}}

QPushButton:hover {{
    background-color: #00B8CC;
}}

QPushButton:pressed {{
    background-color: #0099AA;
}}

QPushButton:disabled {{
    background-color: {COLORS['border']};
    color: {COLORS['text_secondary']};
}}

/* BOTONES SECUNDARIOS */
QPushButton#secondary {{
    background-color: {COLORS['surface']};
    color: {COLORS['accent']};
    border: 1px solid {COLORS['accent']};
}}

QPushButton#secondary:hover {{
    background-color: {COLORS['border']};
}}

/* TABLA (HISTORY) */
QTableWidget {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_primary']};
    gridline-color: {COLORS['border']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
}}

QTableWidget::item {{
    padding: 6px;
    border-bottom: 1px solid {COLORS['border']};
}}

QTableWidget::item:selected {{
    background-color: {COLORS['accent']};
    color: {COLORS['background']};
}}

QHeaderView::section {{
    background-color: {COLORS['background']};
    color: {COLORS['accent']};
    padding: 8px;
    border: none;
    border-bottom: 2px solid {COLORS['accent']};
    font-weight: bold;
}}

/* SCROLLBARS */
QScrollBar:vertical {{
    background-color: {COLORS['surface']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['accent']};
}}

QScrollBar:horizontal {{
    background-color: {COLORS['surface']};
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS['accent']};
}}

/* SEPARADORES */
QFrame[frameShape="4"] {{
    color: {COLORS['border']};
}}

/* CUADROS DE DIÁLOGO */
QDialog {{
    background-color: {COLORS['background']};
    color: {COLORS['text_primary']};
}}
"""

def get_stylesheet():
    """Retorna el stylesheet completo"""
    return STYLESHEET

def get_color(color_name: str) -> str:
    """Obtiene un color de la paleta"""
    return COLORS.get(color_name, COLORS["text_primary"])
