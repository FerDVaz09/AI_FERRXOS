"""
AI_FERRXOS - Asistente de Escritorio para Reuniones
Entrada principal de la aplicación
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
