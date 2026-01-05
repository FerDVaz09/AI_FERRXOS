"""
Módulo de Ghost Mode - Invisibilidad en compartir pantalla
Usa Windows API para excluir la ventana de capturas
"""

import sys
from ctypes import windll, c_long

# Constante de Windows API
WDA_EXCLUDEFROMCAPTURE = 0x00000011

def enable_ghost_mode(hwnd: int) -> bool:
    """
    Activa Ghost Mode para una ventana
    La ventana no aparecerá en screenshots/compartir pantalla
    
    Args:
        hwnd: Handle de la ventana (int)
    
    Returns:
        bool: True si tuvo éxito
    """
    if sys.platform != "win32":
        print("⚠️ Ghost Mode solo funciona en Windows")
        return False
    
    try:
        # Obtener función SetWindowDisplayAffinity
        user32 = windll.user32
        result = user32.SetWindowDisplayAffinity(c_long(hwnd), WDA_EXCLUDEFROMCAPTURE)
        
        if result:
            print("✅ Ghost Mode activado - Ventana invisible en compartir pantalla")
            return True
        else:
            print("❌ Error activando Ghost Mode")
            return False
    except Exception as e:
        print(f"❌ Error en Ghost Mode: {e}")
        return False

def disable_ghost_mode(hwnd: int) -> bool:
    """
    Desactiva Ghost Mode
    
    Args:
        hwnd: Handle de la ventana (int)
    
    Returns:
        bool: True si tuvo éxito
    """
    if sys.platform != "win32":
        return False
    
    try:
        user32 = windll.user32
        result = user32.SetWindowDisplayAffinity(c_long(hwnd), 0)
        
        if result:
            print("✅ Ghost Mode desactivado")
            return True
        else:
            print("❌ Error desactivando Ghost Mode")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
