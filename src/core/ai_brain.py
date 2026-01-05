"""
Módulo de IA usando Google Gemini
Procesamiento de análisis de reuniones
"""

from typing import Optional

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class AIBrain:
    """Gestor de IA con Gemini"""
    
    # Prompts predefinidos por modo
    SYSTEM_PROMPTS = {
        "entrevista": """Eres un entrevistador técnico experto. 
Tu rol es:
- Analizar las respuestas del candidato
- Identificar fortalezas técnicas
- Detectar áreas de mejora
- Sugerir preguntas de seguimiento
Sé conciso (máx 150 palabras por análisis).""",
        
        "negocios": """Eres un asesor comercial experimentado.
Tu rol es:
- Detectar oportunidades de venta
- Identificar objeciones
- Sugerir cierres
- Analizar el perfil del cliente
Sé accionable (máx 150 palabras por análisis).""",
        
        "presentacion": """Eres un coach de presentaciones.
Tu rol es:
- Evaluar el ritmo y claridad
- Sugerir puntos clave
- Detectar áreas de mejora
- Proporcionar transiciones fluidas
Sé constructivo (máx 150 palabras por análisis).""",
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """Inicializa el cliente de Gemini"""
        self.api_key = api_key
        
        if GENAI_AVAILABLE and api_key:
            try:
                genai.configure(api_key=api_key)
                print("✅ IA (Gemini) inicializada")
            except Exception as e:
                print(f"Error configurando Gemini: {e}")
    
    def set_api_key(self, api_key: str):
        """Configura una nueva API Key"""
        self.api_key = api_key
        if GENAI_AVAILABLE:
            try:
                genai.configure(api_key=api_key)
                return True
            except Exception as e:
                print(f"Error configurando API Key: {e}")
                return False
        return False
    
    def analyze(self, text: str, mode: str = "negocios", custom_prompt: str = "") -> str:
        """Analiza un texto usando IA"""
        if not self.api_key:
            return "❌ IA no configurada. Configura tu API Key primero."
        
        # Seleccionar prompt
        if mode == "custom" and custom_prompt:
            system_prompt = custom_prompt
        else:
            system_prompt = self.SYSTEM_PROMPTS.get(mode, self.SYSTEM_PROMPTS["negocios"])
        
        # Crear mensaje
        full_prompt = f"""{system_prompt}

TRANSCRIPCIÓN A ANALIZAR:
{text}

ANÁLISIS:"""
        
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(full_prompt)
            return response.text if response else "Sin respuesta"
        except Exception as e:
            return f"❌ Error en análisis IA: {str(e)}"
    
    def test_connection(self) -> bool:
        """Prueba la conexión con Gemini"""
        if not self.api_key:
            return False
        
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content("Responde con 'OK'")
            return response and len(response.text) > 0
        except Exception as e:
            print(f"Error en test_connection: {e}")
            return False
