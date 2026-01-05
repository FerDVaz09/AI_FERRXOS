"""
Script para compilar AI_FERRXOS a .exe con PyInstaller
"""

import subprocess
import sys
from pathlib import Path

def build_exe():
    """Compila la aplicación a ejecutable"""
    
    # Ruta del proyecto
    project_dir = Path(__file__).parent
    src_dir = project_dir / "src"
    main_file = src_dir / "main.py"
    
    # Comando PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=AI_FERRXOS",
        "--onefile",  # Un solo archivo ejecutable
        "--windowed",  # Sin consola
        "--icon=web/favicon.ico" if (project_dir / "web/favicon.ico").exists() else "",
        "--add-data=src/config.json:src",
        "--add-data=src/history.json:src",
        "--collect-all=google",
        "--collect-all=PyQt6",
        str(main_file)
    ]
    
    # Remover strings vacíos
    cmd = [c for c in cmd if c]
    
    print(f"📦 Compilando AI_FERRXOS a .exe...")
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, cwd=str(project_dir), check=True)
        
        exe_path = project_dir / "dist" / "AI_FERRXOS.exe"
        if exe_path.exists():
            print(f"✅ ¡Éxito! Ejecutable creado en: {exe_path}")
            print(f"Tamaño: {exe_path.stat().st_size / (1024*1024):.2f} MB")
        else:
            print("❌ El ejecutable no se creó")
            return False
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error compilando: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
